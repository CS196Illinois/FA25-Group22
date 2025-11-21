"""
FastAPI Backend Server for Stock Prediction
============================================
This server exposes the ML model trained in predictor.ipynb as REST API endpoints.
It handles:
- Stock predictions (BUY/SELL/HOLD decisions)
- Recent stock data retrieval
- Model feature calculations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
import requests
import joblib
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Stock Predictor API",
    description="Machine Learning API for stock market predictions",
    version="1.0.0"
)

# ============================================================================
# CORS Configuration - Allows frontend to communicate with backend
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default dev server
        "http://localhost:3000",  # Alternative React dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ============================================================================
# Load ML Model - Load the trained RandomForest model on startup
# ============================================================================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "trained_stock_model.pkl")
try:
    model = joblib.load(MODEL_PATH)
    print(f"✓ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = None

# ============================================================================
# Configuration - Get API key from environment variable for security
# ============================================================================
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "vFDjkUVRfPnedLrbRjm75BZ9CJHz3dfv")

# ============================================================================
# Pydantic Models - Define data structures for API requests/responses
# ============================================================================

class PredictionResponse(BaseModel):
    """Response format for prediction endpoint"""
    ticker: str
    decision: str  # BUY, SELL, or HOLD
    confidence: float  # Probability (0-1)
    timestamp: str
    current_price: float
    features: Dict[str, float]  # Technical indicators used for prediction
    probabilities: Dict[str, float]  # Probability for each class

class StockDataResponse(BaseModel):
    """Response format for stock data endpoint"""
    ticker: str
    data: List[Dict]  # List of OHLCV bars
    count: int

class HealthResponse(BaseModel):
    """Response format for health check endpoint"""
    status: str
    model_loaded: bool
    api_key_configured: bool

# ============================================================================
# Helper Functions - Core logic from predictor.ipynb
# ============================================================================

def pull_polygon_data(ticker: str, start: str, end: str, api_key: str) -> pd.DataFrame:
    """
    Fetch minute-level stock data from Polygon.io API

    Args:
        ticker: Stock symbol (e.g., 'AAPL')
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format
        api_key: Polygon.io API key

    Returns:
        DataFrame with columns: timestamp, open, high, low, close, volume
    """
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{start}/{end}?apiKey={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()

        # Check if we got valid data back
        if 'results' not in data or len(data['results']) < 2:
            raise ValueError(f"Insufficient data returned from Polygon API. Response: {data}")

        # Convert JSON to DataFrame and format timestamps
        df = pd.DataFrame(data['results'])
        df['timestamp'] = pd.to_datetime(df['t'], unit='ms')

        # Rename columns to standard OHLCV format
        df = df.rename(columns={
            'o': 'open',
            'h': 'high',
            'l': 'low',
            'c': 'close',
            'v': 'volume'
        })

        # Select only the columns we need
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        return df

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch data from Polygon API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing stock data: {str(e)}")


def calculate_features_for_prediction(df: pd.DataFrame) -> tuple:
    """
    Calculate technical indicators from recent price data
    This replicates the feature engineering from predictor.ipynb

    Args:
        df: DataFrame with OHLCV data (must have at least 2 rows)

    Returns:
        Tuple of (feature_dict, last_bar) containing:
        - feature_dict: Dictionary with all 6 features for model input
        - last_bar: Most recent price bar for context
    """
    # Get last two bars (we need 2 for momentum calculation)
    last_two = df.iloc[-2:]

    # Feature 1: Momentum (1-minute price change percentage)
    momentum_1min = (last_two['close'].iloc[1] - last_two['close'].iloc[0]) / last_two['close'].iloc[0]

    # Feature 2: Volatility (squared momentum - proxy for price volatility)
    volatility_1min = momentum_1min ** 2

    # Feature 3: Price direction (1 if close > open, 0 otherwise)
    price_direction = int(last_two['close'].iloc[1] > last_two['open'].iloc[1])

    # Feature 4: VWAP deviation (how far current price is from volume-weighted average)
    # VWAP = cumulative (price * volume) / cumulative volume
    vwap = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    vwap_dev = (last_two['close'].iloc[1] - vwap.iloc[-1]) / vwap.iloc[-1]

    # Feature 5 & 6: Time features (hour and minute of day)
    hour = last_two['timestamp'].iloc[1].hour
    minute = last_two['timestamp'].iloc[1].minute

    # Combine all features into dictionary matching model's expected format
    features = {
        'momentum_1min': momentum_1min,
        'volatility_1min': volatility_1min,
        'price_direction': price_direction,
        'vwap_dev': vwap_dev,
        'hour': hour,
        'minute': minute
    }

    return features, last_two.iloc[1]


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running
    Returns status of model and API key configuration
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "api_key_configured": POLYGON_API_KEY != ""
    }


@app.get("/api/predict/{ticker}", response_model=PredictionResponse)
async def predict_stock(ticker: str, prob_threshold: float = 0.55):
    """
    Get BUY/SELL/HOLD prediction for a stock ticker

    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')
        prob_threshold: Confidence threshold for BUY/SELL signals (default: 0.55)
                       Higher = more conservative (more HOLD signals)

    Returns:
        Prediction with decision, confidence, and technical details

    Example:
        GET /api/predict/AAPL
        GET /api/predict/AAPL?prob_threshold=0.6  (more conservative)
    """
    # Validate model is loaded
    if model is None:
        raise HTTPException(status_code=503, detail="ML model not loaded")

    # Validate ticker format
    ticker = ticker.upper().strip()
    if not ticker.isalpha() or len(ticker) > 5:
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")

    try:
        # Step 1: Fetch recent stock data (last 24 hours to ensure we have market hours data)
        today = datetime.now().date()
        start_date = today - timedelta(days=1)

        df = pull_polygon_data(ticker, str(start_date), str(today), POLYGON_API_KEY)

        # Step 2: Calculate features from the data
        features, last_bar = calculate_features_for_prediction(df)

        # Step 3: Prepare features for model prediction (must match training order)
        feature_row = pd.DataFrame([{
            'momentum_1min': features['momentum_1min'],
            'volatility_1min': features['volatility_1min'],
            'price_direction': features['price_direction'],
            'vwap_dev': features['vwap_dev'],
            'hour': features['hour'],
            'minute': features['minute']
        }])

        # Step 4: Get model prediction probabilities
        # pred_proba returns [P(down), P(up)] - probability for each class
        pred_proba = model.predict_proba(feature_row)[0]

        # Step 5: Apply threshold logic to make BUY/SELL/HOLD decision
        if pred_proba[1] > prob_threshold:
            # High confidence price will go UP -> BUY
            decision = "BUY"
            confidence = pred_proba[1]
        elif pred_proba[0] > prob_threshold:
            # High confidence price will go DOWN -> SELL
            decision = "SELL"
            confidence = pred_proba[0]
        else:
            # Low confidence in either direction -> HOLD
            decision = "HOLD"
            confidence = max(pred_proba)

        # Step 6: Format and return response
        return {
            "ticker": ticker,
            "decision": decision,
            "confidence": float(confidence),
            "timestamp": str(last_bar['timestamp']),
            "current_price": float(last_bar['close']),
            "features": {k: float(v) for k, v in features.items()},
            "probabilities": {
                "down": float(pred_proba[0]),
                "up": float(pred_proba[1])
            }
        }

    except HTTPException:
        # Re-raise HTTP exceptions (already formatted)
        raise
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/api/data/{ticker}", response_model=StockDataResponse)
async def get_stock_data(ticker: str, days: int = 1):
    """
    Get recent stock price data for a ticker

    Args:
        ticker: Stock symbol
        days: Number of days of historical data to retrieve (default: 1)

    Returns:
        OHLCV data for the requested period

    Example:
        GET /api/data/AAPL
        GET /api/data/AAPL?days=5  (5 days of data)
    """
    # Validate ticker
    ticker = ticker.upper().strip()
    if not ticker.isalpha() or len(ticker) > 5:
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")

    # Validate days parameter
    if days < 1 or days > 30:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 30")

    try:
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        # Fetch data from Polygon
        df = pull_polygon_data(ticker, str(start_date), str(end_date), POLYGON_API_KEY)

        # Convert DataFrame to list of dictionaries for JSON response
        data = df.to_dict('records')

        # Convert timestamps to strings for JSON serialization
        for record in data:
            record['timestamp'] = str(record['timestamp'])

        return {
            "ticker": ticker,
            "data": data,
            "count": len(data)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data retrieval error: {str(e)}")


# ============================================================================
# Server Startup
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Run the server on port 8000
    # Access at: http://localhost:8000
    # API docs at: http://localhost:8000/docs (automatic Swagger UI)
    uvicorn.run(
        "api:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,
        reload=True  # Auto-reload on code changes (for development)
    )

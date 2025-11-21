# Full Stack Integration Guide

This guide explains how to run the complete stock prediction application with both frontend and backend connected.

## Architecture Overview

```
┌─────────────────┐         HTTP Requests        ┌─────────────────┐
│                 │  ────────────────────────>    │                 │
│  React Frontend │                               │  FastAPI Backend│
│  (Port 5173)    │  <────────────────────────    │  (Port 8000)    │
│                 │         JSON Responses        │                 │
└─────────────────┘                               └─────────────────┘
        │                                                   │
        │                                                   │
        │ Displays predictions                             │ Loads ML model
        │ and stock data                                   │ Fetches from Polygon API
        │                                                   │
        v                                                   v
   User Interface                               RandomForest Model (.pkl)
```

## What's Been Integrated

### Backend (`Project/backend/`)
- **FastAPI server** (`api.py`) that wraps the ML model
- **Endpoints:**
  - `GET /` - Health check
  - `GET /api/predict/{ticker}` - Get BUY/SELL/HOLD prediction
  - `GET /api/data/{ticker}` - Get historical OHLCV data
- **CORS enabled** to allow frontend communication
- **Environment variables** for API key management
- **Error handling** for invalid tickers and API failures

### Frontend (`Project/ui_figma_stock_predictor/`)
- **API client** (`src/services/api.ts`) with TypeScript types
- **Search functionality** - Enter stock tickers in the header
- **Real-time predictions** - Displays BUY/SELL/HOLD with confidence
- **Technical indicators** - Shows all 6 features used by the model
- **Loading states** - Visual feedback while fetching data
- **Error handling** - User-friendly error messages

### Data Flow

1. User enters ticker (e.g., "AAPL") in search bar
2. Frontend calls `api.getPrediction("AAPL")`
3. Backend fetches recent data from Polygon.io
4. Backend calculates features (momentum, volatility, VWAP, etc.)
5. ML model predicts probability of price going up/down
6. Backend applies threshold logic to decide BUY/SELL/HOLD
7. Frontend displays decision, confidence, price, and indicators

## Setup Instructions

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **Polygon.io API Key** (free tier works)

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd Project/backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (API key already set in .env)
# If needed, edit backend/.env to update your API key
```

### Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd Project/ui_figma_stock_predictor

# Install dependencies
npm install

# Environment is already configured in .env
# It points to http://localhost:8000 (backend URL)
```

### Step 3: Verify Model File

Make sure the trained model exists:
```bash
# From Project/ directory
ls trained_stock_model.pkl
```

If missing, run the `predictor.ipynb` notebook to train and save the model.

## Running the Application

You need to run **both** backend and frontend simultaneously in separate terminals:

### Terminal 1: Start Backend

```bash
# From Project/backend/
python api.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ Model loaded successfully
```

**Test the backend:**
- Visit http://localhost:8000/docs for interactive API documentation
- Visit http://localhost:8000 to check health status

### Terminal 2: Start Frontend

```bash
# From Project/ui_figma_stock_predictor/
npm run dev
```

You should see:
```
VITE v5.0.8  ready in XXX ms

➜  Local:   http://localhost:5173/
```

**Open the app:**
- Visit http://localhost:5173 in your browser

## Using the Application

1. **View Default Prediction**
   - Opens with Apple (AAPL) prediction loaded

2. **Search for Stock**
   - Enter ticker in search bar (e.g., MSFT, GOOGL, TSLA)
   - Press Enter or click search icon
   - Wait for prediction to load

3. **Read the Prediction**
   - **Decision:** BUY (green), SELL (red), or HOLD (yellow)
   - **Confidence:** How certain the model is (0-100%)
   - **Probabilities:** Separate up/down probabilities
   - **Technical Indicators:** All 6 features used by the model

4. **Refresh Data**
   - Click "Refresh Prediction" button to get latest data

## Understanding the Features

The model uses 6 technical indicators:

| Feature | Description | How It's Used |
|---------|-------------|---------------|
| **Momentum (1min)** | % price change in last minute | Captures short-term trend |
| **Volatility** | Squared momentum | Measures price stability |
| **Price Direction** | Close vs Open | Bullish (↑) or Bearish (↓) |
| **VWAP Deviation** | Distance from volume-weighted avg | Over/undervalued signal |
| **Hour** | Time of day (0-23) | Market session effects |
| **Minute** | Minute within hour (0-59) | Intraday patterns |

## Decision Logic

```python
if P(up) > 0.55:      # Model is confident price will rise
    → BUY

elif P(down) > 0.55:  # Model is confident price will fall
    → SELL

else:                 # Model is uncertain
    → HOLD
```

You can adjust the threshold (default 0.55) in the API call for more/less conservative signals.

## Troubleshooting

### Backend Issues

**Error: "Model not loaded"**
- Make sure `trained_stock_model.pkl` exists in `Project/`
- Run the predictor notebook to train the model

**Error: "Failed to fetch data from Polygon API"**
- Check your API key in `backend/.env`
- Verify you have API quota remaining (500 calls/day on free tier)
- Check if the ticker symbol is valid

**Error: "Port 8000 already in use"**
```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Error: "API Error: Failed to fetch"**
- Make sure backend is running on port 8000
- Check CORS is enabled in backend (it should be)
- Verify `VITE_API_URL` in frontend/.env is correct

**Error: "Module not found"**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**TypeScript errors**
```bash
# Rebuild TypeScript
npm run build
```

### Common Issues

**Old predictions showing**
- Click "Refresh Prediction" button
- Market may be closed (data only updates during trading hours)

**Slow API responses**
- Polygon API can be slow during market hours
- Model prediction itself is fast (<100ms)
- Most delay is from data fetching

## API Documentation

Once backend is running, visit these URLs:

- **Swagger UI:** http://localhost:8000/docs
  - Interactive API documentation
  - Test endpoints directly in browser

- **ReDoc:** http://localhost:8000/redoc
  - Clean, organized API reference

## Next Steps

### Potential Enhancements

1. **Real-time Updates**
   - Add WebSocket connection for live predictions
   - Auto-refresh every minute during market hours

2. **Chart Visualization**
   - Replace `ChartPlaceholder` with real price chart
   - Use Chart.js or Recharts library
   - Display historical predictions

3. **Model Improvements**
   - Add more features (volume, RSI, MACD)
   - Try different ML algorithms
   - Ensemble multiple models

4. **Database Layer**
   - Store predictions in PostgreSQL/MongoDB
   - Track model performance over time
   - Show accuracy metrics

5. **User Features**
   - Save favorite tickers
   - Set price alerts
   - View prediction history

6. **Deployment**
   - Deploy backend to Heroku/AWS/Railway
   - Deploy frontend to Vercel/Netlify
   - Use production environment variables

## File Structure

```
FA25-Group22/
├── Project/
│   ├── backend/                    # NEW: FastAPI backend
│   │   ├── api.py                 # Main API server
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── .env                   # API keys (not in git)
│   │   ├── .env.example          # Template for .env
│   │   └── README.md             # Backend documentation
│   │
│   ├── ui_figma_stock_predictor/  # React frontend
│   │   ├── src/
│   │   │   ├── services/         # NEW: API client
│   │   │   │   └── api.ts        # Backend communication
│   │   │   ├── pages/
│   │   │   │   └── HomePage.tsx  # UPDATED: Shows real data
│   │   │   ├── components/
│   │   │   │   └── Layout.tsx    # UPDATED: Search functionality
│   │   │   └── App.tsx           # UPDATED: State management
│   │   ├── .env                  # API URL (not in git)
│   │   ├── .env.example         # Template
│   │   └── package.json
│   │
│   ├── trained_stock_model.pkl   # ML model (used by backend)
│   ├── predictor.ipynb           # Model training notebook
│   └── CLAUDE.md                 # Project documentation
│
├── INTEGRATION_GUIDE.md          # This file
└── .gitignore                    # Already configured for .env
```

## Security Notes

- ✓ API keys stored in `.env` files (not committed to git)
- ✓ `.gitignore` already configured to exclude `.env`
- ✓ CORS restricted to localhost (update for production)
- ✓ Input validation on both frontend and backend
- ⚠ For production: Use proper secrets management (AWS Secrets Manager, etc.)

## Support

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review `backend/README.md` for backend-specific help
3. Check API docs at http://localhost:8000/docs
4. Verify both servers are running in separate terminals
5. Check browser console for frontend errors
6. Check backend terminal for API errors

## Summary

You now have a fully integrated full-stack application:

- ✅ FastAPI backend serving ML predictions
- ✅ React frontend consuming the API
- ✅ Real-time stock predictions with BUY/SELL/HOLD signals
- ✅ Interactive search and data visualization
- ✅ Environment-based configuration
- ✅ Comprehensive error handling
- ✅ Type-safe TypeScript integration
- ✅ Professional API documentation

The frontend and backend communicate seamlessly to provide real-time stock market predictions powered by your RandomForest machine learning model!

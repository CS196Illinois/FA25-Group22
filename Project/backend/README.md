# Stock Prediction Backend API

FastAPI server that exposes the ML model as REST endpoints.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   # Copy the example env file
   cp .env.example .env

   # Edit .env and add your Polygon.io API key
   ```

3. **Run the server:**
   ```bash
   python api.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Health Check
- **GET** `/`
- Returns server status and model info

### Get Prediction
- **GET** `/api/predict/{ticker}`
- **Parameters:**
  - `ticker` (path): Stock symbol (e.g., AAPL, MSFT)
  - `prob_threshold` (query, optional): Confidence threshold (default: 0.55)
- **Returns:** BUY/SELL/HOLD decision with confidence and features

**Example:**
```bash
curl http://localhost:8000/api/predict/AAPL
```

### Get Stock Data
- **GET** `/api/data/{ticker}`
- **Parameters:**
  - `ticker` (path): Stock symbol
  - `days` (query, optional): Days of history (default: 1, max: 30)
- **Returns:** OHLCV price data

**Example:**
```bash
curl http://localhost:8000/api/data/AAPL?days=5
```

## Interactive API Docs

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Model Info

The API uses the trained RandomForest model from `trained_stock_model.pkl`.

**Features used:**
1. `momentum_1min` - 1-minute price momentum
2. `volatility_1min` - Squared momentum
3. `price_direction` - Binary (close > open)
4. `vwap_dev` - Deviation from VWAP
5. `hour` - Hour of day
6. `minute` - Minute of hour

**Decision Logic:**
- **BUY:** P(up) > threshold (default 0.55)
- **SELL:** P(down) > threshold
- **HOLD:** Neither condition met (uncertain)

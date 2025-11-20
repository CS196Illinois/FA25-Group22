# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a stock market prediction application combining machine learning models with a React-based UI. The project uses minute-level stock data from Polygon.io API to predict short-term price movements and generate trading signals (BUY/SELL/HOLD).

The codebase is split into two main components:
- **ML Backend**: Jupyter notebooks for model training, feature analysis, and prediction
- **UI Frontend**: React + TypeScript + TailwindCSS application

## Development Commands

### Frontend (ui_figma_stock_predictor/)

Navigate to the UI directory before running these commands:
```bash
cd ui_figma_stock_predictor
```

- **Install dependencies**: `npm install`
- **Start dev server**: `npm run dev`
- **Build for production**: `npm run build`
- **Preview production build**: `npm run preview`
- **Lint code**: `npm run lint`

The frontend uses Vite as the build tool and development server.

### Backend (Jupyter Notebooks)

The ML models are developed in Jupyter notebooks. Key notebooks:
- `predictor.ipynb` - Main prediction model with BUY/SELL/HOLD signals
- `feature_analysis.ipynb` - Feature correlation analysis
- `Model Building DEMO.ipynb` - Volatility prediction demo
- `Momentum_Predictor (1).ipynb` - Additional predictor implementation

To run notebooks, ensure you have pandas, scikit-learn, requests, and joblib installed.

## Architecture

### Machine Learning Pipeline

The prediction system follows this workflow:

1. **Data Acquisition**: Pull minute-level OHLCV data from Polygon.io API
2. **Feature Engineering**: Calculate technical indicators:
   - `momentum_1min`: 1-minute price momentum (pct_change)
   - `volatility_1min`: Squared momentum
   - `price_direction`: Binary indicator (close > open)
   - `vwap_dev`: Deviation from Volume-Weighted Average Price
   - `hour`, `minute`: Time-based features
3. **Model Training**: RandomForestClassifier (100 estimators) predicts next-minute direction
4. **Decision Logic**: Probability threshold-based BUY/SELL/HOLD signals (default threshold: 0.55)

The trained model is saved as `trained_stock_model.pkl` using joblib.

### Frontend Architecture

Located in `ui_figma_stock_predictor/`:

```
src/
├── App.tsx              # Main app with routing
├── main.tsx             # Entry point
├── components/          # Reusable UI components
│   ├── Layout.tsx       # App layout wrapper
│   ├── StatCard.tsx     # Statistics display card
│   └── ChartPlaceholder.tsx
└── pages/
    └── HomePage.tsx     # Main landing page
```

The UI is built with:
- React 18 + TypeScript
- React Router for navigation
- TailwindCSS for styling
- Vite for bundling and dev server

## Key Implementation Details

### Chronological Train/Test Split

The model uses an 80/20 chronological split (NOT random) to prevent look-ahead bias:
```python
split_index = int(len(X)*0.8)
X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
```

### Polygon.io API Integration

The `pull_polygon_data()` function queries:
```
https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{start}/{end}?apiKey={api_key}
```

API key is currently hardcoded in notebooks. Consider environment variables for production.

### VWAP Calculation

VWAP (Volume-Weighted Average Price) is computed cumulatively:
```python
df['vwap'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
```

This provides context for price deviation from volume-weighted average.

### Decision Threshold Logic

The `get_recent_minute_decision()` function uses probability thresholds:
- BUY: if P(up) > 0.55
- SELL: if P(down) > 0.55
- HOLD: otherwise (uncertain predictions)

Adjust `prob_threshold` parameter to tune signal sensitivity.

## File Locations

- **Trained model**: `trained_stock_model.pkl` (root directory)
- **Sample data**: `MSFT_1m.csv` (Microsoft minute-level data)
- **Frontend build output**: `ui_figma_stock_predictor/dist/` (after build)

## Adding New Features to UI

1. Create component in `src/components/` or page in `src/pages/`
2. Add route in `src/App.tsx` if creating a new page
3. Use TailwindCSS classes for styling to match existing design
4. Follow TypeScript strict typing conventions

## Model Retraining

To retrain the model with new data:
1. Update date ranges in notebook cells
2. Run data pull and feature calculation cells
3. Re-run model training cell
4. Save new model with `joblib.dump(model, "trained_stock_model.pkl")`

The model currently achieves ~52-53% accuracy on test data, slightly better than random.

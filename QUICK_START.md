# Quick Start Guide

Get the stock prediction app running in 3 steps!

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Windows (for `.bat` scripts) or Mac/Linux (use manual commands)

## Windows Users (Easiest)

### Step 1: Start Backend

1. Open a terminal (Command Prompt or PowerShell)
2. Navigate to project root: `cd FA25-Group22`
3. Run: `start-backend.bat`
4. Wait for "✓ Model loaded successfully"

### Step 2: Start Frontend

1. Open a **NEW** terminal (keep backend running)
2. Navigate to project root: `cd FA25-Group22`
3. Run: `start-frontend.bat`
4. Wait for "Local: http://localhost:5173/"

### Step 3: Use the App

1. Open browser to http://localhost:5173
2. Search for any stock ticker (AAPL, MSFT, GOOGL, etc.)
3. See BUY/SELL/HOLD predictions in real-time!

## Mac/Linux Users

### Terminal 1 - Backend

```bash
cd FA25-Group22/Project/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python api.py
```

### Terminal 2 - Frontend

```bash
cd FA25-Group22/Project/ui_figma_stock_predictor

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Terminal 3 - Open Browser

```bash
# macOS
open http://localhost:5173

# Linux
xdg-open http://localhost:5173
```

## Troubleshooting

**"Model not found" error:**
- Run the `predictor.ipynb` notebook first to train the model
- Make sure `trained_stock_model.pkl` exists in `Project/` directory

**Backend won't start:**
- Make sure port 8000 is available
- Check Python version: `python --version` (need 3.8+)

**Frontend won't start:**
- Make sure port 5173 is available
- Check Node version: `node --version` (need 16+)
- Try deleting `node_modules` and running `npm install` again

**Can't connect to backend:**
- Make sure backend is running (check Terminal 1)
- Verify http://localhost:8000 shows health check
- Check `Project/ui_figma_stock_predictor/.env` has correct API URL

## What You'll See

1. **Search Bar** - Enter stock tickers (top right)
2. **Prediction** - Large BUY/SELL/HOLD display with color coding
3. **Confidence** - How certain the model is
4. **Stats Cards** - Probability up/down, current price
5. **Technical Indicators** - All 6 features the model uses
6. **Refresh Button** - Get latest prediction

## Next Steps

- Read `INTEGRATION_GUIDE.md` for detailed documentation
- Check `Project/backend/README.md` for API details
- Visit http://localhost:8000/docs for interactive API docs
- Experiment with different tickers and thresholds

## Stock Tickers to Try

- **AAPL** - Apple
- **MSFT** - Microsoft
- **GOOGL** - Google
- **TSLA** - Tesla
- **AMZN** - Amazon
- **NVDA** - Nvidia
- **META** - Meta/Facebook
- **NFLX** - Netflix

Happy trading! 📈

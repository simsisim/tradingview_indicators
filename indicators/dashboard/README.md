# TradingView Dashboard Generator

Generate a TradingView Pine Script dashboard from a CSV watchlist file.

## Quick Start

1. **Edit your watchlist**: Update `watchlist.csv` with your stocks
2. **Generate dashboard**: Run `python3 gen_dashboard.py`
3. **Load in TradingView**: Copy `dashboard.pine` into TradingView

## Files

- `watchlist.csv` - Your stock watchlist (edit this file)
- `gen_dashboard.py` - Generator script
- `dashboard.pine` - Generated Pine Script (don't edit manually)
- `gen_monitor.py` - Old generator (deprecated)

## CSV Format

Your `watchlist.csv` must have these columns:

```csv
Ticker,Trigger,Stop,Notes
AAPL,150.50,145.00,Tech / Strong earnings
TSLA,250.00,240.00,EV / High growth
```

**Column Descriptions:**
- **Ticker**: Stock symbol (e.g., AAPL, GETTEX:RHM)
- **Trigger**: Entry/trigger price level
- **Stop**: Stop loss price
- **Notes**: Industry or notes about the stock

## Usage

### Basic (use defaults)
```bash
python3 gen_dashboard.py
```
Reads: `watchlist.csv` → Generates: `dashboard.pine`

### Custom input file
```bash
python3 gen_dashboard.py my_stocks.csv
```

### Custom input and output
```bash
python3 gen_dashboard.py my_stocks.csv custom_output.pine
```

## Dashboard Features

The generated dashboard includes:

### Core Features
- **20 Symbol Slots**: Automatically populated from CSV
- **Real-time Price Data**: Live price updates
- **Performance Metrics**: Daily change %, Change from open
- **Previous Day Levels**: PDH (Previous Day High), PDL (Previous Day Low)

### Technical Indicators
- **EMA 10**: 10-period Exponential Moving Average
- **EMA 20**: 20-period Exponential Moving Average
- **SMA 50**: 50-period Simple Moving Average
- **Distances**: Percentage distance to each metric

### Trading Signals
- **SlingShot**: Breakout pattern detection
- **Price/Volume Breakout**: Combined price and volume breakouts
- **Risk:Reward Ratio**: Automatic R:R calculations

### Candle Patterns
- **Kicker**: Strong reversal pattern
- **Oops**: Failed breakout pattern
- **OEL/OEH**: Open equals Low/High patterns
- **Inside/Engulf**: Inside bars and engulfing patterns
- **3Bar Break**: 3-bar breakout patterns

### Column Visibility
Toggle individual column groups:
- Basic Info (Name, Price, Chg %, Performance)
- Pre-MP (Pre-Market) - *disabled by default*
- Post-MP (Post-Market) - *disabled by default*
- Price Levels (PDL, PDH)
- Metrics (EMA/SMA values)
- Distances to Metrics
- Trading (Trigger, Stop, R:R)
- SlingShot Signals
- Price/Volume Breakout
- Candle Combos
- Industry Notes

## Default Settings

The dashboard comes with these defaults:
- **Metrics**: EMA 10, EMA 20, SMA 50
- **Pre-MP/Post-MP**: Hidden by default

## Workflow

### 1. Update Watchlist
Edit `watchlist.csv` with your current stock picks:
```csv
Ticker,Trigger,Stop,Notes
NVDA,500.00,480.00,AI / Semiconductors
MSFT,380.00,370.00,Tech / Cloud
```

### 2. Generate Dashboard
```bash
python3 gen_dashboard.py
```

Output:
```
============================================================
TradingView Dashboard Generator
============================================================
Reading watchlist CSV: watchlist.csv
Found 24 symbols in watchlist
Generating symbol inputs...
Generating table rows...
Assembling Pine Script...

✅ Dashboard generated successfully: dashboard.pine

============================================================
SUMMARY
============================================================
Symbols processed: 24
Output file: dashboard.pine
...
```

### 3. Load in TradingView
1. Open TradingView
2. Go to Pine Editor
3. Click "Open" → "Import script"
4. Select `dashboard.pine`
5. Click "Add to chart"

## Troubleshooting

### Script won't run
```bash
# Install pandas if needed
pip install pandas
```

### CSV not found
Make sure `watchlist.csv` is in the same directory as `gen_dashboard.py`

### Generated file looks wrong
- Check CSV format (must have: Ticker, Trigger, Stop, Notes)
- Ensure no special characters in Notes that could break Pine Script
- Single quotes in Notes are automatically escaped

### Symbols not showing in TradingView
- Verify ticker symbols are correct (e.g., use NASDAQ:AAPL for AAPL)
- Check that `show_1`, `show_2`, etc. are set to `true` for active symbols
- Confirm symbols are not delisted or invalid

## Advanced Usage

### Multiple Watchlists
Generate different dashboards for different strategies:

```bash
# Growth stocks
python3 gen_dashboard.py growth_stocks.csv growth_dashboard.pine

# Value stocks
python3 gen_dashboard.py value_stocks.csv value_dashboard.pine

# Day trading
python3 gen_dashboard.py daytrading.csv daytrading_dashboard.pine
```

### Automation
Add to cron for daily updates:
```bash
# Generate dashboard every day at 8 AM
0 8 * * * cd /path/to/dashboard+alert && python3 gen_dashboard.py
```

## Version History

- **v2.1**: Removed alert system (memory limit issues), optimized for performance
- **v2.0**: Separated Pre-MP/Post-MP, separated metrics/distances, updated defaults
- **v1.0**: Original gen_monitor.py (deprecated)

## Support

For issues or questions:
1. Check CSV format is correct
2. Verify pandas is installed: `pip install pandas`
3. Run with verbose errors: `python3 gen_dashboard.py 2>&1 | tee error.log`

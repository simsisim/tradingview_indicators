# TradingView Publication Description

## Title
s-PV Gap Screener - Price & Volume Breakouts + Gap Detection

## Short Description
Multi-signal screener combining trend-filtered price/volume breakouts with dual-threshold gap detection. 19 output columns for comprehensive technical filtering.

## Full Description

---

### 📊 Overview

**s-PV Gap Screener** is a comprehensive technical screener designed for TradingView's Pine Screener that combines two powerful signal types:

1. **Price & Volume Breakouts** - Detects when price and volume simultaneously break out, filtered by trend (200 SMA)
2. **Gap Detection** - Identifies significant overnight price gaps with dual customizable thresholds

**Inspiration:** This screener is inspired by the excellent [Price and Volume Breakout Buy Strategy by TradeDots](https://www.tradingview.com/script/jc2hs2qK-Price-and-Volume-Breakout-Buy-Strategy-TradeDots/), expanding on that concept to add gap detection, short setups, and multi-signal confirmation.

---

### ✨ Key Features

**Price & Volume Breakout Detection:**
- ✅ Trend-filtered breakouts (SMA confirmation - avoid counter-trend signals)
- ✅ Both long AND short breakout detection
- ✅ Customizable lookback periods (10-500 bars)
- ✅ Strength calculation (% above/below breakout level)
- ✅ Volume confirmation (must exceed highest volume in period)

**Gap Detection:**
- ✅ Dual threshold system (default 5% and 10%)
- ✅ Independent tracking for moderate and major gaps
- ✅ Direction filtering (gap up, gap down, or both)
- ✅ Historical gap scanning (up to 500 bars)

**Composite Signals:**
- ✅ Combined Score (0-80 weighted system)
- ✅ "Any Signal" flag for quick filtering
- ✅ 19 total output columns

---

### 🎯 How It Works

#### Price & Volume Breakout Logic

**Long Breakout Triggers When:**
1. Close > Highest High in lookback period
2. Volume > Highest Volume in lookback period
3. Close > SMA (trend filter - ensures uptrend)

**Short Breakout Triggers When:**
1. Close < Lowest Low in lookback period
2. Volume > Highest Volume in lookback period
3. Close < SMA (trend filter - ensures downtrend)

The trend filter is crucial - it prevents false breakouts by ensuring the move aligns with the dominant trend direction. This is inspired by TradeDots' approach but adds the short side capability.

#### Gap Detection Logic

Calculates overnight gap: `(Open - Previous Close) / Previous Close * 100`

Tracks the most recent gap for each threshold independently, allowing you to monitor both moderate gaps (5%) and major gaps (10%) separately.

---

### 📈 Screener Output Columns (19 Total)

**Price & Volume Breakout (7 columns):**
- PV Breakout Flag (0/1)
- PV Days Ago
- PV Breakout Date (YYYYMMDD format)
- PV Strength %
- PV Type (1=long, -1=short, 0=none)
- Volume Ratio (current/average)
- Price vs SMA % (distance from trend line)

**Gap Threshold 1 (5 columns):**
- Gap1 Flag, Days Ago, Date, Size %, Direction

**Gap Threshold 2 (5 columns):**
- Gap2 Flag, Days Ago, Date, Size %, Direction

**Composite (2 columns):**
- Any Signal (quick filter)
- Combined Score (weighted 0-80)

---

### ⚙️ Input Parameters

**Fully Customizable:**
- Price/Volume breakout periods (default 60 bars)
- Trend filter SMA length (default 200)
- Gap thresholds (default 5% and 10%)
- Historical lookback (default 100 bars)
- Direction filters (long only, short only, or both)

---

### 💡 Example Usage Scenarios

**1. Fresh Momentum Breakouts:**
```
PV Breakout Flag = 1
PV Days Ago <= 5
Volume Ratio >= 1.5
```

**2. Major Gaps Awaiting Confirmation:**
```
Gap2 Flag = 1
Gap2 Days Ago <= 20
PV Breakout Flag = 0
Price vs SMA % > 0
```

**3. High Conviction Multi-Signal:**
```
PV Breakout Flag = 1
Gap1 Flag = 1
Combined Score >= 60
Volume Ratio >= 2.0
```

**4. Long Setups in Strong Trends:**
```
PV Type = 1
Price vs SMA % >= 5
PV Strength % >= 3
```

---

### 🎓 How to Use

**Step 1:** Add indicator to a **DAILY chart**

**Step 2:** Configure settings (or use defaults)

**Step 3:** Open Pine Screener: https://www.tradingview.com/pine-screener/

**Step 4:** Add "s-PV Gap Screener" to your screener columns

**Step 5:** Apply filters and sort by Combined Score

**Detailed documentation:** See published script comments or README

---

### 📅 Date Format

Dates display as **YYYYMMDD** (e.g., 20260212 = February 12, 2026)
- Sortable chronologically
- ISO 8601 standard
- Easy to filter by date ranges

---

### ⚠️ Important Notes

**DAILY TIMEFRAME ONLY:** This screener is designed for daily bars. Other timeframes may produce unexpected results.

**500-Bar Limit:** Pine Screener loads last 500 bars (~2 years on daily). This is a TradingView platform limitation.

**Combined Score Weights:**
- PV Breakout: +30 points
- Gap Threshold 1: +20 points
- Gap Threshold 2: +30 points
- Maximum: 80 points

---

### 🔄 Differences from TradeDots Strategy

This screener **expands** on the TradeDots concept:

✅ **Added:** Gap detection (dual thresholds)
✅ **Added:** Short breakout detection
✅ **Added:** Combined scoring system
✅ **Added:** Multiple output columns for detailed filtering
✅ **Modified:** Designed specifically for Pine Screener (not a strategy)
✅ **Kept:** Core PV breakout logic with trend filter

**Credit:** Original PV breakout concept from [TradeDots' Price and Volume Breakout Buy Strategy](https://www.tradingview.com/script/jc2hs2qK-Price-and-Volume-Breakout-Buy-Strategy-TradeDots/)

---

### 🎯 Best For

- Swing traders looking for momentum setups
- Traders who combine multiple technical signals
- Screening large watchlists for breakout opportunities
- Finding gap plays with volume confirmation
- Multi-timeframe position traders

---

### 📊 Tips for Best Results

1. **Start Broad:** Filter by `Any Signal = 1`, sort by Combined Score
2. **Volume Confirmation:** Add `Volume Ratio >= 1.5` for stronger signals
3. **Trend Alignment:** Filter by `Price vs SMA % > 0` for longs (or `< 0` for shorts)
4. **Fresh Signals:** Use `PV Days Ago <= 10` for recent breakouts
5. **Save Presets:** Create filter combinations for different strategies

---

### 🔧 Customization

All parameters are configurable via inputs:
- Adjust periods to match your trading timeframe
- Modify gap thresholds for your volatility preference
- Enable/disable specific signal types
- Change trend filter SMA length (50, 100, 200, etc.)

---

### 📚 Additional Resources

**Full Documentation:** See README.md in published script or at:
https://github.com/[your-repo]/indicators/pine-screeners/PVscreener/

**Pine Screener Guide:** https://www.tradingview.com/pine-screener/

**Original Inspiration:** [TradeDots PV Breakout Strategy](https://www.tradingview.com/script/jc2hs2qK-Price-and-Volume-Breakout-Buy-Strategy-TradeDots/)

---

### ⚖️ Disclaimer

This indicator is for informational and educational purposes only. It does not constitute financial advice. Always do your own research and use proper risk management. Past performance does not guarantee future results.

---

### 🙏 Credits

- **Inspired by:** TradeDots' Price and Volume Breakout Buy Strategy
- **Original concept:** Price + Volume confirmation with trend filter
- **Enhancements:** Gap detection, short setups, multi-signal scoring

---

**Version:** 2.0
**Type:** Screener Indicator
**Timeframe:** Daily (1D)
**Outputs:** 19 columns
**License:** Mozilla Public License 2.0

---

### 📝 Release Notes

**v2.0 (February 2026)**
- Optimized for Pine Screener usage
- 19 output columns for comprehensive filtering
- Dual gap threshold system
- Combined scoring mechanism
- Full input customization

**v1.0**
- Initial release with PV breakout detection
- Gap detection added
- Trend filtering implemented

---

### 🏷️ Tags

`screener` `breakout` `volume` `gap` `momentum` `trend` `technical-analysis` `multi-signal` `price-action` `volatility`

---

**If you find this screener useful, please give it a boost! 🚀**

**Questions or suggestions? Leave a comment below!**

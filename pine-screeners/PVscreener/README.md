# s-PV Gap Screener - Complete Guide

**Pine Script for TradingView Pine Screener**
**File:** `s-PVGapEarnings.pine`

---

## 🎯 Overview

This screener combines two powerful technical analysis tools:

1. **Price & Volume Breakouts** - Detect when price and volume simultaneously break out with trend confirmation
2. **Gap Detection** - Find stocks with significant price gaps (dual customizable thresholds)

**Key Features:**
- ✅ Trend-filtered breakouts (200 SMA confirmation)
- ✅ Dual gap thresholds (default 5% and 10%)
- ✅ Historical tracking up to 500 bars (~2 years)
- ✅ 19 screener output columns
- ✅ Weighted combined scoring (0-80)
- ✅ Fully configurable settings

---

## 📋 Quick Start

### Step 1: Add Indicator to Chart
1. Open TradingView and load a **DAILY chart** (important!)
2. Open Pine Editor (bottom of screen)
3. Create new indicator and paste the code from `s-PVGapEarnings.pine`
4. Click "Add to Chart"
5. Configure settings (see Input Parameters below)

### Step 2: Add to Pine Screener
1. Navigate to: https://www.tradingview.com/pine-screener/
2. Click "Add indicator" or "+"
3. Find "s-PV Gap Screener" in your indicators
4. Click to add it - all columns will appear in the screener

### Step 3: Apply Filters
Use the screener interface to filter stocks:
- Click column headers to sort
- Use filter inputs to narrow results
- Save filter presets for different strategies

---

## ⚙️ Input Parameters

### Price & Volume Breakout Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| **Enable PV Breakout Scanning** | ✓ | - | Turn PV breakout detection on/off |
| **Price Breakout Period** | 60 | 10-500 | Bars to compare for highest/lowest price |
| **Volume Breakout Period** | 60 | 10-500 | Bars to compare for highest volume |
| **Trend Filter SMA** | 200 | 20-500 | SMA for trend confirmation (long above, short below) |
| **Search Last N Days** | 100 | 1-500 | How far back to scan for breakouts |
| **Breakout Direction** | Both | Long/Short/Both | Filter for long or short breakouts |

**What is Trend Filter SMA?**
- Uses a Simple Moving Average (default 200-day) to confirm trend direction
- **Long breakouts** only trigger if price is **above** the SMA (bullish trend)
- **Short breakouts** only trigger if price is **below** the SMA (bearish trend)
- Prevents false breakouts by ensuring alignment with the dominant trend

**Recommended Settings:**
- **Conservative:** 30-day periods, 50 SMA, 50-day lookback
- **Standard:** 60-day periods, 200 SMA, 100-day lookback (default)
- **Aggressive:** 120-day periods, 200 SMA, 200-day lookback

### Gap Detection Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| **Enable Gap Scanning** | ✓ | - | Turn gap detection on/off |
| **Gap Threshold 1 (%)** | 5.0 | 0.1-30.0 | First gap threshold percentage |
| **Gap Threshold 2 (%)** | 10.0 | 0.1-30.0 | Second gap threshold percentage |
| **Gap Direction** | Both | Up/Down/Both | Filter for gap-up or gap-down only |
| **Search Last N Days** | 100 | 1-500 | How far back to scan for gaps |

**Common Threshold Combinations:**
- **Small gaps:** 3% / 7%
- **Standard gaps:** 5% / 10% (default)
- **Large gaps:** 10% / 15%
- **Extreme gaps:** 15% / 20%

---

## 📊 Screener Columns (19 Outputs)

### Price & Volume Breakout Columns (7)

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **PV Breakout Flag** | Flag | 0 or 1 | 1 = Breakout found, 0 = No breakout |
| **PV Days Ago** | Integer | 0-500 | Days since breakout occurred |
| **PV Breakout Date** | Date | YYYYMMDD | Date of breakout (e.g., 20260212 = Feb 12, 2026) |
| **PV Strength %** | Percentage | 0-100+ | Strength of breakout (% above/below breakout level) |
| **PV Type** | Direction | 1, -1, 0 | 1 = Long, -1 = Short, 0 = None |
| **Volume Ratio** | Ratio | 0+ | Current volume / average volume |
| **Price vs SMA %** | Percentage | -100 to +100 | Distance from trend SMA (+ = above, - = below) |

**How PV Breakout Works:**
- **Long breakout** = Close > Highest High **AND** Volume > Highest Volume **AND** Close > SMA
- **Short breakout** = Close < Lowest Low **AND** Volume > Highest Volume **AND** Close < SMA
- Scans historical bars to find most recent occurrence

### Gap Detection Columns - Threshold 1 (5)

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **Gap1 Flag** | Flag | 0 or 1 | 1 = Gap >= Threshold 1 found |
| **Gap1 Days Ago** | Integer | 1-500 | Days since gap occurred |
| **Gap1 Date** | Date | YYYYMMDD | Date of gap |
| **Gap1 Size %** | Percentage | -30 to +30 | Actual gap size (+ = gap up, - = gap down) |
| **Gap1 Direction** | Direction | 1, -1 | 1 = Gap up, -1 = Gap down |

### Gap Detection Columns - Threshold 2 (5)

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **Gap2 Flag** | Flag | 0 or 1 | 1 = Gap >= Threshold 2 found |
| **Gap2 Days Ago** | Integer | 1-500 | Days since gap occurred |
| **Gap2 Date** | Date | YYYYMMDD | Date of gap |
| **Gap2 Size %** | Percentage | -30 to +30 | Actual gap size |
| **Gap2 Direction** | Direction | 1, -1 | 1 = Gap up, -1 = Gap down |

### Composite Columns (2)

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **Any Signal** | Flag | 0 or 1 | 1 = At least one signal (PV, Gap1, or Gap2) detected |
| **Combined Score** | Score | 0-80 | Weighted score of all signals |

**Combined Score Breakdown:**
- PV Breakout: +30 points
- Gap Threshold 1: +20 points
- Gap Threshold 2: +30 points
- **Maximum:** 80 points

---

## 🎯 Example Filter Strategies

### Strategy 1: Fresh Breakouts (Last 5 Days)
**Goal:** Find recent price & volume breakouts

**Filters:**
```
PV Breakout Flag = 1
PV Days Ago <= 5
Volume Ratio >= 1.5
```

**Why it works:** Recent breakouts with volume confirmation have higher continuation probability

---

### Strategy 2: Major Gaps Awaiting Confirmation
**Goal:** Find big gap-ups that haven't broken out yet

**Filters:**
```
Gap2 Flag = 1
Gap2 Direction = 1  (gap up)
Gap2 Days Ago <= 20
PV Breakout Flag = 0  (no breakout yet)
Price vs SMA % > 0  (above trend)
```

**Why it works:** Large gaps often lead to consolidation before next leg

---

### Strategy 3: Gap & Breakout Combo (High Conviction)
**Goal:** Find stocks with multiple confirmations

**Filters:**
```
Gap1 Flag = 1
PV Breakout Flag = 1
Gap1 Days Ago <= 7
PV Days Ago <= 7
Combined Score >= 50
```

**Why it works:** Multiple signals increase probability of sustained move

---

### Strategy 4: Long Setups in Strong Trends
**Goal:** Find bullish breakouts in uptrends

**Filters:**
```
PV Breakout Flag = 1
PV Type = 1  (long)
Price vs SMA % >= 5
PV Strength % >= 3
```

**Why it works:** Breakouts aligned with trend have better success rates

---

### Strategy 5: High Conviction Multi-Signal
**Goal:** Find stocks with maximum technical confirmation

**Filters:**
```
Combined Score >= 60
PV Breakout Flag = 1
Gap2 Flag = 1
Volume Ratio >= 2.0
```

**Sort by:** Combined Score (descending)

**Why it works:** Multiple confirmations reduce false signals

---

## 📅 Reading Date Format

Dates are displayed in **YYYYMMDD** format:

```
Screener shows:  20260212
Actually means:  2026 / 02 / 12
                 Year  Mon  Day
                 February 12, 2026
```

**How to read:**
1. First 4 digits = Year (2026)
2. Next 2 digits = Month (02 = February)
3. Last 2 digits = Day (12)

**Why this format?**
- ✅ Chronologically sortable (20260212 > 20260131)
- ✅ Internationally recognized (ISO 8601 standard)
- ✅ Easy to filter by date ranges

---

## 🚀 Quick Filter Reference

### 🎯 MOMENTUM PLAYS

**Fresh Breakouts:**
```
PV Breakout Flag = 1
PV Days Ago <= 5
Volume Ratio >= 1.5
```

**Strong Uptrend Breakouts:**
```
PV Breakout Flag = 1
PV Type = 1
Price vs SMA % >= 5
PV Strength % >= 3
```

**High Volume Confirmation:**
```
PV Breakout Flag = 1
Volume Ratio >= 2.0
PV Days Ago <= 10
```

### 📊 GAP PLAYS

**Fresh Gap-Ups (Last Week):**
```
Gap1 Flag = 1
Gap1 Direction = 1
Gap1 Days Ago <= 5
Gap1 Size % >= 5
```

**Major Gaps Not Yet Broken Out:**
```
Gap2 Flag = 1
Gap2 Days Ago <= 20
PV Breakout Flag = 0
Price vs SMA % > 0
```

**Gap & Breakout Combo:**
```
Gap1 Flag = 1
PV Breakout Flag = 1
Gap1 Days Ago <= 7
PV Days Ago <= 7
Combined Score >= 50
```

### 🎯 HIGH CONVICTION SETUPS

**Triple Confirmation:**
```
PV Breakout Flag = 1
Gap1 Flag = 1
Volume Ratio >= 2.0
Combined Score >= 60
```

**Extreme Moves:**
```
Gap2 Flag = 1
Gap2 Size % >= 15
PV Breakout Flag = 1
Combined Score >= 70
```

### 📉 SHORT SETUPS

**Short Breakdowns:**
```
PV Breakout Flag = 1
PV Type = -1
Price vs SMA % <= -5
Volume Ratio >= 1.5
```

**Gap-Down Breakdowns:**
```
Gap1 Direction = -1
Gap1 Days Ago <= 10
Price vs SMA % < 0
Volume Ratio >= 1.5
```

---

## ⚠️ Important Limitations

### 1. 500-Bar Historical Data Limit
- Pine Screener only loads the **last 500 bars** (~2 years on daily charts)
- Events older than 500 bars **will not be detected**
- This is a TradingView platform limitation

**Impact:**
- ✅ Works perfectly for swing/momentum trading (recent events)
- ⚠️ May miss very old breakouts or gaps
- ✅ Sufficient for most short-to-medium term strategies

### 2. Same Settings for All Symbols
- Input parameters apply to **all stocks** in the screener
- Cannot have different thresholds per symbol
- Must remove/re-add indicator to change settings

**Workaround:**
- Use screener filters to fine-tune results
- Create multiple versions with different default settings
- Save filter presets for different strategies

### 3. Numeric Output Only
- Pine Screener only displays numbers, not text
- Dates shown as numbers (YYYYMMDD)
- Cannot show company names or formatted strings

---

## 🔧 Troubleshooting

### Issue: "No data" or all values are 0
**Solution:**
- Ensure chart is on **DAILY** timeframe
- Check that lookback periods aren't longer than available data
- Verify symbol has sufficient price history

### Issue: Dates look wrong (e.g., 19700101)
**Solution:**
- This is January 1, 1970 (Unix epoch) - means no event found
- Filter to exclude these: `PV Breakout Date > 20000101`

### Issue: Too many/too few results
**Solution:**
- Adjust lookback periods (larger = more results)
- Adjust thresholds (smaller = more results)
- Use `Combined Score` to filter for high-quality setups

---

## 💡 Best Practices

### Daily Workflow

**After market close (10 minutes):**
1. Run "Fresh Breakouts" filter (PV Days Ago <= 1)
2. Run "Fresh Gaps" filter (Gap1 Days Ago <= 1)
3. Check Combined Score >= 60 for high conviction setups
4. Add promising stocks to watchlist

**Weekly review (30 minutes):**
1. Run broader scan (PV Days Ago <= 7)
2. Review all Combined Score >= 50 stocks
3. Adjust filter thresholds based on results
4. Check for patterns in successful setups

### Filter Strategy

**Start broad, narrow down:**
```
1. Any Signal = 1  (see everything)
2. Add: Combined Score >= 40  (medium quality)
3. Add: Volume Ratio >= 1.5  (volume confirmation)
4. Review results, adjust thresholds
```

### Save Filter Presets

Create saved searches for different strategies:
- "Fresh Breakouts"
- "Major Gaps"
- "High Conviction Setups"
- "Long Only Setups"
- "Short Only Setups"

---

## 📈 Technical Details

### Price & Volume Breakout Logic

**Long Breakout Conditions:**
1. Close > Highest High in prior period
2. Volume > Highest Volume in prior period
3. Close > SMA (trend filter)

**Short Breakout Conditions:**
1. Close < Lowest Low in prior period
2. Volume > Highest Volume in prior period
3. Close < SMA (trend filter)

**Strength Calculation:**
- **Long:** `(Close - Highest High) / Highest High * 100`
- **Short:** `(Lowest Low - Close) / Lowest Low * 100`

### Gap Detection Logic

**Gap Percentage Calculation:**
```
gap_pct = (Open - Previous Close) / Previous Close * 100
```

**Example:**
- Previous close = $100
- Current open = $107
- Gap = 7.0% (gap up)

**Dual Threshold System:**
- Tracks most recent gap for each threshold independently
- Threshold 1 (default 5%): Moderate gaps
- Threshold 2 (default 10%): Major gaps

---

## 📚 Example Use Cases

### Swing Trading (1-4 weeks)
```
PV Breakout Flag = 1
PV Days Ago <= 20
Volume Ratio >= 1.3
Price vs SMA % >= 3
```

### Position Trading (1-6 months)
```
PV Strength % >= 5
Price vs SMA % >= 10
Gap2 Flag = 1
Combined Score >= 50
```

### Day Trading Setup (Next Day)
```
PV Days Ago <= 1
OR
Gap2 Days Ago <= 1
Volume Ratio >= 2.0
```

---

## 🎓 Getting Started Checklist

- [ ] Copy Pine Script code to TradingView
- [ ] Add to DAILY chart
- [ ] Configure input settings (start with defaults)
- [ ] Open Pine Screener
- [ ] Add indicator to screener
- [ ] Verify columns appear correctly
- [ ] Test sorting by `Combined Score`
- [ ] Create first filter: `Any Signal = 1`
- [ ] Review top 20 results
- [ ] Save filter preset
- [ ] Refine thresholds based on results

---

## 📊 What Makes This Screener Unique

**Compared to basic screeners:**
- ✅ Combines PV breakouts + gap detection
- ✅ Historical tracking (not just today's data)
- ✅ Trend-filtered for higher accuracy
- ✅ Customizable thresholds
- ✅ Multi-factor confirmation via Combined Score
- ✅ Dual gap thresholds for flexibility

**Best Practice:** Use this screener for technical signals, then cross-check with fundamental analysis and manual chart review.

---

**Version:** 2.0 (Earnings feature removed)
**Last Updated:** February 2026
**Compatible with:** TradingView Pine Script v5, Pine Screener
**Recommended Timeframe:** Daily (1D)

**Happy Trading! 📊**

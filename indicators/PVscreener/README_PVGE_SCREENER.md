# PV Gap Earnings Screener - Complete Guide

**Pine Script for TradingView Pine Screener**
**File:** `PVGapEarnings_Screener.pine`

---

## 🎯 Overview

This screener combines three powerful technical analysis tools:
1. **Price & Volume Breakouts** - Detect when price and volume simultaneously break out
2. **Gap Detection** - Find stocks with significant price gaps (customizable thresholds)
3. **Earnings Tracking** - Monitor days since last earnings report

---

## 📋 Quick Start

### Step 1: Add Indicator to Chart
1. Open TradingView and load a **DAILY chart** (important!)
2. Open Pine Editor (bottom of screen)
3. Create new indicator and paste the code from `PVGapEarnings_Screener.pine`
4. Click "Add to Chart"
5. Configure settings (see Input Parameters below)

### Step 2: Add to Pine Screener
1. Navigate to: https://www.tradingview.com/pine-screener/
2. Click "Add indicator" or "+"
3. Find "PV Gap Earnings Screener" in your indicators
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

### Earnings Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| **Enable Earnings Tracking** | ✓ | - | Turn earnings tracking on/off |
| **Max Days to Track** | 120 | 30-500 | Stop tracking earnings older than this |

**Note:** Only PAST earnings available (future earnings not supported in Pine Script)

---

## 📊 Screener Columns (Output Values)

### Price & Volume Breakout Columns

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **PV Breakout Flag** | Flag | 0 or 1 | 1 = Breakout found, 0 = No breakout |
| **PV Days Ago** | Integer | 0-500 | Days since breakout occurred |
| **PV Breakout Date** | Date | YYYYMMDD | Date of breakout (e.g., 20,260,127.00 = Jan 27, 2026) |
| **PV Strength %** | Percentage | 0-100+ | Strength of breakout (% above/below breakout level) |
| **PV Type** | Direction | 1, -1, 0 | 1 = Long breakout, -1 = Short breakout, 0 = None |
| **Volume Ratio** | Ratio | 0+ | Current volume / average volume |
| **Price vs SMA %** | Percentage | -100 to +100 | Distance from trend SMA (+ = above, - = below) |

### Gap Detection Columns (Threshold 1)

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **Gap1 Flag** | Flag | 0 or 1 | 1 = Gap >= Threshold 1 found |
| **Gap1 Days Ago** | Integer | 1-500 | Days since gap occurred |
| **Gap1 Date** | Date | YYYYMMDD | Date of gap |
| **Gap1 Size %** | Percentage | -30 to +30 | Actual gap size (+ = gap up, - = gap down) |
| **Gap1 Direction** | Direction | 1, -1 | 1 = Gap up, -1 = Gap down |

### Gap Detection Columns (Threshold 2)

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **Gap2 Flag** | Flag | 0 or 1 | 1 = Gap >= Threshold 2 found |
| **Gap2 Days Ago** | Integer | 1-500 | Days since gap occurred |
| **Gap2 Date** | Date | YYYYMMDD | Date of gap |
| **Gap2 Size %** | Percentage | -30 to +30 | Actual gap size |
| **Gap2 Direction** | Direction | 1, -1 | 1 = Gap up, -1 = Gap down |

### Earnings Columns

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **Days Since Earnings** | Integer | 0-120 | Days since last earnings report |
| **Last Earnings Date** | Date | YYYYMMDD | Date of last earnings report |
| **Earnings 90-Day Flag** | Flag | 0 or 1 | 1 = Between 80-95 days (approaching next earnings) |

### Composite Columns

| Column Name | Type | Values | Description |
|-------------|------|--------|-------------|
| **Any Signal** | Flag | 0 or 1 | 1 = At least one signal (PV, Gap1, or Gap2) detected |
| **Combined Score** | Score | 0-100 | Weighted score of all signals (higher = more signals) |

**Combined Score Breakdown:**
- PV Breakout: +30 points
- Gap Threshold 1: +20 points
- Gap Threshold 2: +30 points
- Recent earnings (≤5 days): +10 points
- Approaching earnings cycle: +10 points
- **Maximum:** 100 points

---

## 🎯 Example Filter Strategies

### Strategy 1: Fresh Breakouts After Earnings
**Goal:** Find stocks that broke out 1-2 weeks after earnings

**Filters:**
```
PV Breakout Flag = 1
PV Days Ago <= 10
Days Since Earnings >= 7
Days Since Earnings <= 21
```

**Why it works:** Post-earnings consolidation often leads to continuation moves

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

### Strategy 3: Pre-Earnings Setup
**Goal:** Find stocks in strong uptrends approaching earnings

**Filters:**
```
Earnings 90-Day Flag = 1
PV Breakout Flag = 1
PV Type = 1  (long breakout)
PV Days Ago >= 20  (not too recent)
Gap2 Flag = 0  (no major volatility)
```

**Why it works:** Strong stocks into earnings often continue momentum

---

### Strategy 4: Post-Gap Breakout Confirmation
**Goal:** Find stocks that gapped AND broke out (high conviction)

**Filters:**
```
Gap1 Flag = 1
PV Breakout Flag = 1
Gap1 Days Ago <= 5
PV Days Ago <= 5
Combined Score >= 50
```

**Why it works:** Multiple signals increase probability of sustained move

---

### Strategy 5: Earnings Fade Setup
**Goal:** Find stocks with declining volume after earnings

**Filters:**
```
Days Since Earnings >= 1
Days Since Earnings <= 7
Volume Ratio < 0.5  (volume drying up)
Price vs SMA % < 0  (below trend)
PV Breakout Flag = 0
```

**Why it works:** Post-earnings exhaustion can lead to reversals

---

### Strategy 6: High Conviction Multi-Signal
**Goal:** Find stocks with multiple technical triggers

**Filters:**
```
Combined Score >= 60
PV Breakout Flag = 1
Any Signal = 1
Volume Ratio >= 1.5
```

**Sort by:** Combined Score (descending)

**Why it works:** Multiple confirmations reduce false signals

---

## 📅 Reading Date Format

Dates are displayed in **YYYYMMDD** format with automatic thousand separators:

```
Screener shows:  20,260,127.00
                 ↓   ↓   ↓
Actually means:  2026 / 01 / 27
                 Year  Mon  Day
```

**How to read:**
1. Ignore the commas: 20,260,127 → 20260127
2. Ignore the decimals: 20260127.00 → 20260127
3. Split into groups: 2026 / 01 / 27
4. Read as: January 27, 2026

**Why this format?**
- ✅ Chronologically sortable (2026 sorts after 2025)
- ✅ Internationally recognized (ISO 8601 standard)
- ✅ Easy to filter by year/month/day ranges
- ⚠️ Only limitation: Pine Screener can only display numbers, not formatted text

---

## ⚠️ Important Limitations

### 1. 500-Bar Historical Data Limit
- Pine Screener only loads the **last 500 bars** (~2 years on daily charts)
- Events older than 500 bars **will not be detected**
- This is a TradingView platform limitation, not a code issue

**Impact:**
- ✅ Works perfectly for swing/momentum trading (recent events)
- ⚠️ May miss very old breakouts or gaps
- ✅ Sufficient for most short-to-medium term strategies

### 2. Future Earnings Not Available
- `request.earnings()` only provides **past** earnings dates
- **Cannot** show scheduled/upcoming earnings
- Data updates **after** earnings are reported (usually next day)

**Workaround:**
- Use TradingView's Stock Screener for future earnings filters
- Check: https://www.tradingview.com/markets/stocks-usa/earnings/
- Manually note upcoming earnings for watchlist stocks

### 3. Same Settings for All Symbols
- Input parameters apply to **all stocks** in the screener
- Cannot have different thresholds per symbol
- Must remove/re-add indicator to change settings

**Workaround:**
- Use screener filters to fine-tune results
- Create multiple versions with different default settings
- Save filter presets for different strategies

### 4. Numeric Output Only
- Pine Screener only displays numbers, not text
- Dates shown as numbers (YYYYMMDD)
- Cannot show company names, tickers, or formatted strings

---

## 🔧 Troubleshooting

### Issue: "No data" or all values are 0
**Solution:**
- Ensure chart is on **DAILY** timeframe
- Check that lookback periods aren't longer than available data
- Verify symbol has sufficient price history

### Issue: Earnings columns show N/A
**Solution:**
- Not all symbols have earnings data (e.g., ETFs, indices)
- Disable earnings tracking for non-stock instruments
- Check that `Enable Earnings Tracking` is on

### Issue: Dates look wrong (e.g., 19,700,101.00)
**Solution:**
- This is January 1, 1970 (Unix epoch) - means no event found
- Filter to exclude these: `PV Breakout Date > 20000101`

### Issue: Too many/too few results
**Solution:**
- Adjust lookback periods (larger = more results)
- Adjust thresholds (smaller = more results)
- Use `Combined Score` to filter for high-quality setups

---

## 📈 Performance Optimization

### For Large Watchlists (500+ stocks):
1. Enable only needed features (disable if not using)
2. Reduce lookback periods to 50-100 bars
3. Use stricter thresholds to reduce false positives
4. Filter by `Combined Score >= 50` for high-conviction only

### For Swing Trading (1-4 weeks):
1. Set lookbacks to 50-100 days
2. Use 5%/10% gap thresholds
3. Filter for `PV Days Ago <= 20`
4. Focus on recent signals

### For Position Trading (1-6 months):
1. Set lookbacks to 200-500 days (max)
2. Use 10%/15% gap thresholds (major events)
3. Include earnings cycle flag
4. Look for multiple confirmations

---

## 💡 Tips & Best Practices

### 1. Start with Defaults
Use default settings (60/60/200, 5%/10%) for first scan, then adjust based on results.

### 2. Combine with Other Screeners
1. Run Pine Screener for technical signals
2. Export/note ticker symbols
3. Cross-check with fundamental screeners
4. Check earnings calendar manually

### 3. Save Filter Presets
Create saved searches for different strategies:
- "Fresh Breakouts"
- "Post-Earnings Plays"
- "Major Gaps"
- "High Conviction Setups"

### 4. Use Combined Score for Ranking
Sort by `Combined Score` descending to see highest-probability setups first.

### 5. Avoid Earnings Volatility
If you trade breakouts but avoid earnings:
```
Filter: Days Since Earnings <= 7 OR Days Since Earnings >= 90
```
This avoids the pre-earnings runup period.

### 6. Volume Confirmation
Always check `Volume Ratio >= 1.5` for stronger confirmation.

### 7. Regular Monitoring
Run screener daily after market close to catch fresh signals.

---

## 🔄 Updating Settings

### To Change Input Parameters:
1. Open Pine Screener
2. Find "PV Gap Earnings Screener" column
3. Click settings icon (gear)
4. Adjust inputs
5. Apply changes (affects all symbols)

### To Use Different Settings Simultaneously:
1. Create copies of the Pine Script with different default values
2. Rename each version (e.g., "PVGE Conservative", "PVGE Aggressive")
3. Add both to screener
4. Compare columns side-by-side

---

## 📚 Additional Resources

**TradingView Links:**
- Pine Screener: https://www.tradingview.com/pine-screener/
- Earnings Calendar: https://www.tradingview.com/markets/stocks-usa/earnings/
- Stock Screener (for future earnings): https://www.tradingview.com/screener/

**Related Documentation:**
- `PINE_SCREENER_LIMITATION.md` - Understanding 500-bar limit
- `PINE_SCREENER_DATE_FORMATTING_RESEARCH.md` - Why YYYYMMDD format
- `io_PVscreener_v2` - Original PV breakout logic
- `price_volume_breakout.txt` - Source strategy

---

## 🎓 Learning Path

**Beginner:**
1. Use default settings
2. Filter by `Any Signal = 1`
3. Sort by `Combined Score`
4. Review top 10 results

**Intermediate:**
1. Customize thresholds for your timeframe
2. Create specific filter combinations
3. Track results over time
4. Refine based on performance

**Advanced:**
1. Create multiple versions with different settings
2. Combine with fundamental filters
3. Develop custom scoring systems
4. Integrate with other indicators

---

## 📊 Example Screener Layout

**Recommended Column Order:**

1. Symbol (default)
2. **Combined Score** ← Sort by this
3. **Any Signal** ← Quick filter
4. **PV Breakout Flag**
5. **PV Days Ago**
6. **PV Type**
7. **Gap2 Flag**
8. **Gap2 Size %**
9. **Days Since Earnings**
10. **Volume Ratio**

Hide less-used columns to reduce clutter.

---

## ✅ Checklist: First-Time Setup

- [ ] Copy Pine Script code to TradingView
- [ ] Add to DAILY chart
- [ ] Configure input settings
- [ ] Open Pine Screener
- [ ] Add indicator to screener
- [ ] Verify columns appear correctly
- [ ] Test sorting by `Combined Score`
- [ ] Create first filter: `Any Signal = 1`
- [ ] Review results
- [ ] Save filter preset
- [ ] Refine thresholds based on results

---

**Version:** 1.0
**Last Updated:** February 2026
**Compatible with:** TradingView Pine Script v5, Pine Screener
**Recommended Timeframe:** Daily (1D)

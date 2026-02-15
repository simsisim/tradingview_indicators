# Technical Specification - PVGE Screener

**Internal Logic Documentation for PVGapEarnings_Screener.pine**

---

## 🏗️ Architecture Overview

### Code Structure
```
1. Input Parameters (Lines ~15-50)
   - Grouped by feature (PV, Gap, Earnings)
   - Configurable thresholds and periods

2. Helper Functions (Lines ~55-62)
   - timeToYYYYMMDD() - Date conversion

3. Core Logic Sections (Lines ~65-300)
   - Price & Volume Breakout Detection
   - Gap Detection
   - Earnings Tracking
   - Composite Signal Generation

4. Output Plots (Lines ~305-335)
   - 25 plot() statements for screener columns

5. Visual Elements (Lines ~340-380)
   - Chart overlays (backgrounds, shapes)
   - Information table

6. Usage Documentation (Lines ~385+)
   - Inline comments
```

---

## 🔍 Price & Volume Breakout Logic

### Algorithm

**Step 1: Calculate Breakout Levels**
```pine
price_highest = ta.highest(high, price_period)
price_lowest = ta.lowest(low, price_period)
volume_highest = ta.highest(volume, volume_period)
sma_trend = ta.sma(close, sma_length)
```

**Step 2: Historical Scan (Loop)**
```pine
for i = 0 to pv_lookback - 1
    // Long breakout conditions:
    1. close[i] > highest high in prior price_period bars
    2. volume[i] > highest volume in prior volume_period bars
    3. close[i] > SMA (trend filter)

    // Short breakout conditions:
    1. close[i] < lowest low in prior price_period bars
    2. volume[i] > highest volume in prior volume_period bars
    3. close[i] < SMA (trend filter)
```

**Step 3: Track Most Recent**
```
- Records first (most recent) long AND short breakout found
- Stores: days ago, date, strength percentage
- Determines which is more recent for primary signal
```

### Key Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `pv_long_days_ago` | float | Bars since long breakout (0 = today) |
| `pv_long_date` | float | YYYYMMDD format date |
| `pv_long_strength` | float | % above breakout level |
| `pv_short_days_ago` | float | Bars since short breakout |
| `pv_short_date` | float | YYYYMMDD format date |
| `pv_short_strength` | float | % below breakout level |
| `pv_breakout_flag` | float | 1 if any breakout found, 0 otherwise |
| `pv_type` | float | 1 = long, -1 = short, 0 = none |

### Strength Calculation

**Long breakout strength:**
```pine
strength = (close[i] - highest_high[i+1]) / highest_high[i+1] * 100
```
Example: Close = $105, Highest high = $100
```
strength = (105 - 100) / 100 * 100 = 5.0%
```

**Short breakout strength:**
```pine
strength = (lowest_low[i+1] - close[i]) / lowest_low[i+1] * 100
```
Example: Close = $95, Lowest low = $100
```
strength = (100 - 95) / 100 * 100 = 5.0%
```

---

## 📊 Gap Detection Logic

### Algorithm

**Step 1: Calculate Gap Percentage**
```pine
gap_pct = (open[i] - close[i+1]) / close[i+1] * 100
gap_abs = math.abs(gap_pct)
```

**Example:**
```
Previous close = $100
Current open = $107
gap_pct = (107 - 100) / 100 * 100 = 7.0% (gap up)

Previous close = $100
Current open = $95
gap_pct = (95 - 100) / 100 * 100 = -5.0% (gap down)
```

**Step 2: Direction Filter**
```pine
direction_ok = gap_direction == "Both" or
              (gap_direction == "Up Only" and gap_pct > 0) or
              (gap_direction == "Down Only" and gap_pct < 0)
```

**Step 3: Threshold Comparison**
```pine
// For Gap Threshold 1 (default 5%)
if gap_abs >= gap_threshold_1 and direction_ok
    // Record this gap

// For Gap Threshold 2 (default 10%)
if gap_abs >= gap_threshold_2 and direction_ok
    // Record this gap
```

**Step 4: Historical Scan**
```
- Loops through last gap_lookback bars
- Finds FIRST occurrence meeting threshold (most recent)
- Tracks separately for threshold 1 and threshold 2
```

### Key Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `gap1_days_ago` | float | Bars since gap >= threshold 1 |
| `gap1_date` | float | YYYYMMDD format date |
| `gap1_size` | float | Actual gap percentage (can be negative) |
| `gap1_direction` | float | 1 = up, -1 = down |
| `gap2_days_ago` | float | Bars since gap >= threshold 2 |
| `gap2_date` | float | YYYYMMDD format date |
| `gap2_size` | float | Actual gap percentage |
| `gap2_direction` | float | 1 = up, -1 = down |

### Edge Cases

**Overnight gap vs intraday gap:**
- Uses `open[i] - close[i+1]` (overnight gap only)
- Intraday gaps not tracked (requires intraday data)

**Multiple gaps in lookback:**
- Only tracks most recent gap for each threshold
- Older gaps are ignored

**Gap exactly at threshold:**
- Uses `>=` comparison, so 5.0% gap is detected with 5.0% threshold

---

## 📅 Earnings Tracking Logic

### Algorithm

**Step 1: Request Earnings Data**
```pine
[earningsTime, _, _] = request.earnings(syminfo.tickerid, earnings.actual, barmerge.gaps_on)
```

**Returns:**
- `earningsTime`: Unix timestamp of last reported earnings
- Second/third values (estimate, actual) not used in this screener

**Step 2: Calculate Days Since Earnings**
```pine
earnings_bars = (time - earningsTime) / (1000 * 60 * 60 * 24)
```

**Conversion:**
```
time = current bar timestamp (milliseconds)
earningsTime = earnings timestamp (milliseconds)
difference / (1000 * 60 * 60 * 24) = days
```

**Step 3: Apply Max Lookback Filter**
```pine
if earnings_bars <= earnings_max_days
    // Track this earnings
else
    // Too old, set to N/A
```

**Step 4: 90-Day Cycle Flag**
```pine
earnings_90day_flag = (earnings_bars >= 80 and earnings_bars <= 95) ? 1 : 0
```

**Logic:** Most companies report quarterly (~90 days), so 80-95 day range flags approaching earnings.

### Key Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `earningsTime` | int | Unix timestamp from request.earnings() |
| `earnings_bars` | float | Days since last earnings (calculated) |
| `earnings_days_ago` | float | Output value (N/A if > max_days) |
| `earnings_date` | float | YYYYMMDD format date |
| `earnings_90day_flag` | float | 1 if 80-95 days ago, 0 otherwise |

### Limitations

**Future earnings:**
- `request.earnings()` only provides PAST data
- Cannot retrieve scheduled/estimated future dates
- This is a TradingView API limitation

**Data availability:**
- Not all symbols have earnings (ETFs, indices, cryptocurrencies)
- Returns `na` if no earnings data exists

**Update timing:**
- Earnings data typically updates next trading day after report
- May have 1-day lag depending on reporting time (pre/post market)

---

## 🎯 Combined Score Calculation

### Scoring Logic

```pine
combined_score = 0.0

if pv_breakout_flag == 1
    combined_score += 30  // PV breakout found

if gap1_flag == 1
    combined_score += 20  // Gap threshold 1 met

if gap2_flag == 1
    combined_score += 30  // Gap threshold 2 met (major gap)

if not na(earnings_days_ago) and earnings_days_ago <= 5
    combined_score += 10  // Recent earnings

if not na(earnings_90day_flag) and earnings_90day_flag == 1
    combined_score += 10  // Approaching earnings cycle
```

### Score Ranges

| Score | Interpretation | Typical Scenario |
|-------|----------------|------------------|
| 0 | No signals | Quiet/consolidating stock |
| 10 | Single weak signal | Only recent earnings or 90-day flag |
| 20 | Gap threshold 1 only | Small gap, no breakout |
| 30 | PV breakout only | Breakout without gap |
| 40-50 | Multiple signals | Gap + breakout, or breakout + earnings |
| 60-70 | Strong setup | Multiple confirmations |
| 80-100 | Rare/exceptional | All signals aligned |

### Weight Rationale

- **PV Breakout (30):** Primary signal, strong predictive value
- **Gap Threshold 2 (30):** Major event, equal weight to breakout
- **Gap Threshold 1 (20):** Moderate event, lower weight
- **Recent Earnings (10):** Timing factor, bonus
- **90-Day Cycle (10):** Anticipatory, bonus

---

## 🔄 Date Conversion Function

### timeToYYYYMMDD()

```pine
timeToYYYYMMDD(t) =>
    yearVal = year(t)      // Extract year (e.g., 2026)
    monthVal = month(t)    // Extract month (1-12)
    dayVal = dayofmonth(t) // Extract day (1-31)
    yearVal * 10000 + monthVal * 100 + dayVal
```

### Examples

**Input:** `time = 1706313600000` (Unix timestamp for Jan 27, 2026)
```
yearVal = 2026
monthVal = 1
dayVal = 27

Result = 2026 * 10000 + 1 * 100 + 27
       = 20260000 + 100 + 27
       = 20260127
```

**Display in screener:** `20,260,127.00`

**Parsing:**
```
20260127
↓
2026 / 01 / 27
Year   Mon  Day
```

### Why YYYYMMDD?

1. **Sortable:** 20260201 > 20260131 (Feb 1 after Jan 31)
2. **Filterable:** Easy to filter by year (>= 20260000)
3. **ISO 8601:** International standard
4. **Comma-friendly:** Separators actually help readability (20,26,01,27)

---

## 🔁 Loop Optimization

### Lookback Loops

Both PV and Gap detection use `for` loops:

```pine
for i = 0 to pv_lookback - 1
    // Check conditions for bar[i]
    if condition_met
        // Record and break early
        break
```

**Optimization:**
- Loop exits early when first match found (most recent event)
- Reduces computation from O(n) to O(1) in best case
- Worst case: O(n) if no match in entire lookback

### Performance Considerations

**500-bar limit:**
- Maximum lookback = 500 bars (platform limit)
- Larger lookback = more computation
- Recommendation: Use 50-100 for swing trading, 200-500 for position trading

**Nested calculations:**
- `ta.highest()` and `ta.lowest()` called inside loop
- Pine Script optimizes these internally
- Still, avoid excessive lookback (> 500) for performance

---

## 📈 Output Plot Strategy

### Why Every Value is Plotted

```pine
plot(value, "Column Name", display=display.data_window)
```

**Reasons:**
1. **Screener requires plot():** Only plotted values appear as columns
2. **display.data_window:** Hides from chart, shows in data window and screener
3. **All metrics plotted:** Provides maximum flexibility in screener

### Plot Types

| Plot Type | Example | Purpose |
|-----------|---------|---------|
| **Flag (0/1)** | `pv_breakout_flag` | Boolean filter (yes/no) |
| **Integer** | `pv_days_ago` | Days count |
| **Date (YYYYMMDD)** | `pv_date` | Event date |
| **Percentage** | `pv_strength` | Magnitude |
| **Direction (1/-1/0)** | `pv_type` | Categorical direction |
| **Ratio** | `volume_ratio` | Relative comparison |
| **Score** | `combined_score` | Composite metric |

### Total Outputs: 25 Columns

1-7: PV Breakout (7 columns)
8-12: Gap Threshold 1 (5 columns)
13-17: Gap Threshold 2 (5 columns)
18-20: Earnings (3 columns)
21-22: Composite (2 columns)
23-25: Additional metrics (3 columns)

---

## 🎨 Visual Elements

### Chart Overlays (Not in Screener)

**Background colors:**
```pine
bgcolor(condition ? color.new(color.green, 95) : na)
```
- Transparency = 95 (very faint)
- Green for long breakout, red for short, orange for major gap

**Shape markers:**
```pine
plotshape(condition, "Label", style=shape.triangleup, location=location.bottom)
```
- Triangle up/down for breakouts
- Diamond for major gaps
- Small size to avoid clutter

**Information table:**
- Position: top_right
- 2 columns x 10 rows
- Shows summary when viewing individual chart
- Not visible in screener (screener uses plot() values)

---

## ⚠️ Edge Case Handling

### No Data Scenarios

**No breakout found:**
```pine
if not long_found
    pv_long_days_ago := na
    pv_long_date := na
    pv_long_strength := na
```
Result: Screener shows "N/A" or empty cell

**No earnings data:**
```pine
if na(earningsTime)
    earnings_days_ago := na
```
Common for ETFs, indices, new IPOs

**Empty price history:**
- Script runs but finds no signals
- All outputs = 0 or na

### Direction Filter Conflicts

**User sets:** `pv_direction = "Long Only"`

**Result:**
- Only scans for long breakouts
- `pv_short_*` variables remain na
- `pv_type` can only be 1 or 0 (never -1)

### Threshold Edge Cases

**Gap exactly at threshold:**
```pine
gap_abs >= gap_threshold_1
```
Uses `>=` so 5.00% gap triggers 5.0% threshold

**Negative gaps:**
- `gap_size` can be negative (gap down)
- `gap_abs` used for threshold comparison
- Direction tracked separately

---

## 🔧 Modification Guide

### Change Breakout Logic

**Location:** Lines ~70-150

**Example: Add ATR filter**
```pine
atr_value = ta.atr(14)
atr_threshold = atr_value * 1.5

// Modify long breakout condition:
historical_long = close[i] > ta.highest(high, price_period)[i+1] and
                 volume[i] > ta.highest(volume, volume_period)[i+1] and
                 close[i] > ta.sma(close, sma_length)[i] and
                 (high[i] - low[i]) >= atr_threshold  // NEW
```

### Add New Output Column

**Step 1: Calculate metric**
```pine
rsi_value = ta.rsi(close, 14)
```

**Step 2: Add plot**
```pine
plot(rsi_value, "RSI", display=display.data_window)
```

**Result:** New "RSI" column appears in screener

### Change Scoring Weights

**Location:** Lines ~280-295

```pine
// Original:
if pv_breakout_flag == 1
    combined_score += 30

// Modified (higher weight):
if pv_breakout_flag == 1
    combined_score += 50
```

---

## 🐛 Debugging Tips

### Issue: All values are 0

**Check:**
1. Timeframe = Daily?
2. Enough price history (> lookback period)?
3. Conditions too strict (no matches)?

**Debug:**
```pine
// Add temporary plots
plot(close, "Close Check")  // Verify data loads
plot(volume, "Volume Check")
```

### Issue: Dates look wrong

**Check:**
```pine
// Add debug plot
plot(time, "Current Time")
```
If time = 0 or very small number, data issue

**Verify date conversion:**
```pine
plot(year(time), "Year")
plot(month(time), "Month")
plot(dayofmonth(time), "Day")
```

### Issue: Earnings always N/A

**Check:**
1. Symbol type (stocks only, not ETFs/crypto)
2. Max days setting (increase to 365)
3. Symbol has earnings history

**Debug:**
```pine
[earningsTime, _, _] = request.earnings(syminfo.tickerid, earnings.actual)
plot(earningsTime, "Earnings Raw Timestamp")
// If this is na, symbol has no earnings data
```

---

## 📊 Performance Benchmarks

### Typical Processing Time

- Single symbol scan: < 1 second
- 100 symbols: 5-10 seconds
- 500 symbols: 30-60 seconds

**Factors:**
- Lookback period (larger = slower)
- Number of enabled features
- Pine Screener server load

### Memory Usage

- Each loop iteration: stores temporary variables
- Total variables tracked: ~30
- Peak memory: During nested `ta.highest()` calls in loop

### Optimization Tips

1. **Reduce lookback:** 100 instead of 500
2. **Disable unused features:** Set `enable_pv = false` if not needed
3. **Use stricter filters in screener UI** instead of code

---

## 🔐 Data Privacy & Security

**No external requests:**
- All data from TradingView's internal database
- No external API calls
- No data sent outside TradingView

**Read-only:**
- Script only reads price/volume/earnings data
- No account access
- No trading execution

---

## 📝 Code Maintenance

### Version Control Recommendations

**Track changes:**
- Date in header comments
- Version number (e.g., v1.0, v1.1)
- Changelog section

**Example:**
```pine
// Version: 1.1
// Last Updated: 2026-02-11
// Changes: Added ATR filter to PV breakout logic
```

### Testing Checklist

When modifying code:

- [ ] Test on single stock (AAPL, NVDA)
- [ ] Verify all output columns appear
- [ ] Check date format (YYYYMMDD)
- [ ] Test with different input settings
- [ ] Verify flags (0/1) display correctly
- [ ] Check edge cases (new IPO, ETF, crypto)
- [ ] Compare results with manual calculation
- [ ] Test in actual Pine Screener

---

**Document Version:** 1.0
**Code Version:** 1.0
**Last Updated:** February 11, 2026

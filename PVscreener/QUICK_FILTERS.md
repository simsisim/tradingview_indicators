# Quick Filter Reference - PVGE Screener

**Quick copy-paste filters for common trading scenarios**

---

## 🚀 MOMENTUM PLAYS

### Fresh Breakouts (Last 5 Days)
```
PV Breakout Flag = 1
PV Days Ago <= 5
Volume Ratio >= 1.5
```

### Strong Uptrend Breakouts
```
PV Breakout Flag = 1
PV Type = 1
Price vs SMA % >= 5
PV Strength % >= 3
```

### High Volume Confirmation
```
PV Breakout Flag = 1
Volume Ratio >= 2.0
PV Days Ago <= 10
```

---

## 📊 GAP PLAYS

### Fresh Gap-Ups (Last Week)
```
Gap1 Flag = 1
Gap1 Direction = 1
Gap1 Days Ago <= 5
Gap1 Size % >= 5
```

### Major Gaps Not Yet Broken Out
```
Gap2 Flag = 1
Gap2 Days Ago <= 20
PV Breakout Flag = 0
Price vs SMA % > 0
```

### Gap & Breakout Combo (High Conviction)
```
Gap1 Flag = 1
PV Breakout Flag = 1
Gap1 Days Ago <= 7
PV Days Ago <= 7
Combined Score >= 50
```

---

## 💰 EARNINGS-BASED

### Post-Earnings Breakouts
```
PV Breakout Flag = 1
Days Since Earnings >= 1
Days Since Earnings <= 14
PV Type = 1
```

### Pre-Earnings Runners (Approaching Cycle)
```
Earnings 90-Day Flag = 1
Price vs SMA % >= 3
Volume Ratio >= 1.2
PV Breakout Flag = 1
```

### Avoid Earnings Volatility
```
PV Breakout Flag = 1
Days Since Earnings >= 14
Days Since Earnings <= 75
(or)
Days Since Earnings >= 0
Days Since Earnings <= 7
```

### Post-Earnings Fade Setup
```
Days Since Earnings >= 1
Days Since Earnings <= 10
Volume Ratio < 0.7
Price vs SMA % < -2
```

---

## 🎯 HIGH CONVICTION SETUPS

### Triple Confirmation
```
PV Breakout Flag = 1
Gap1 Flag = 1
Volume Ratio >= 2.0
Combined Score >= 60
```

### Multi-Signal with Earnings
```
Combined Score >= 50
Days Since Earnings >= 7
Days Since Earnings <= 21
Any Signal = 1
```

### Extreme Moves
```
Gap2 Flag = 1
Gap2 Size % >= 15
PV Breakout Flag = 1
Combined Score >= 70
```

---

## 📉 SHORT SETUPS

### Short Breakdowns
```
PV Breakout Flag = 1
PV Type = -1
Price vs SMA % <= -5
Days Since Earnings >= 14
```

### Gap-Down Breakdowns
```
Gap1 Direction = -1
Gap1 Days Ago <= 10
Price vs SMA % < 0
Volume Ratio >= 1.5
```

### Failed Breakouts (Reversal)
```
PV Breakout Flag = 1
PV Days Ago >= 10
PV Days Ago <= 30
Price vs SMA % < 0
Volume Ratio < 0.6
```

---

## 🔍 SCREENING WORKFLOW

### Step 1: Broad Filter
```
Any Signal = 1
```
**Sort by:** Combined Score (descending)
**Review:** Top 50 results

### Step 2: Refine for Timeframe
**Swing Trade (1-4 weeks):**
```
PV Days Ago <= 20
Volume Ratio >= 1.3
```

**Position Trade (1-6 months):**
```
PV Strength % >= 5
Price vs SMA % >= 10
Gap2 Flag = 1
```

### Step 3: Earnings Filter
**Avoid earnings risk:**
```
Days Since Earnings <= 10
OR
Days Since Earnings >= 85
```

**Earnings catalyst:**
```
Days Since Earnings <= 5
OR
Earnings 90-Day Flag = 1
```

---

## 📅 DATE RANGE EXAMPLES

### Recent Events Only (Last 2 Weeks)
```
PV Days Ago <= 10
Gap1 Days Ago <= 10
```

### Medium-Term (2-6 Weeks)
```
PV Days Ago >= 10
PV Days Ago <= 42
```

### Longer-Term Setups (1-3 Months)
```
PV Days Ago >= 20
PV Days Ago <= 90
PV Strength % >= 10
```

---

## 🎚️ VOLATILITY FILTERS

### Low Volatility (Steady Grind)
```
Gap1 Size % < 3
PV Breakout Flag = 1
Volume Ratio >= 1.0
Volume Ratio <= 2.0
```

### High Volatility (Explosive Moves)
```
Gap2 Flag = 1
Volume Ratio >= 3.0
PV Strength % >= 10
```

### Moderate Volatility (Goldilocks)
```
Gap1 Flag = 1
Gap1 Size % >= 5
Gap1 Size % <= 10
Volume Ratio >= 1.5
Volume Ratio <= 3.0
```

---

## 🏆 TOP PICKS DAILY SCAN

**Run this every day after close:**

```
Combined Score >= 40
PV Days Ago <= 5
Volume Ratio >= 1.5
```

**Sort by:** Combined Score (descending)
**Review:** Top 10-20 stocks
**Action:** Add to watchlist, check charts manually

---

## 💡 CUSTOM SCORING FILTERS

### Aggressive (High Score Threshold)
```
Combined Score >= 70
Any Signal = 1
```

### Moderate (Balanced)
```
Combined Score >= 50
PV Breakout Flag = 1
```

### Conservative (Multi-Confirmation)
```
PV Breakout Flag = 1
Gap1 Flag = 1
Days Since Earnings >= 7
Volume Ratio >= 2.0
```

---

## 🔄 WEEKLY VS DAILY SCANS

### Daily Scan (Fresh Signals)
```
PV Days Ago <= 1
OR
Gap1 Days Ago <= 1
```
**Purpose:** Catch new setups same-day

### Weekly Scan (Broader View)
```
PV Days Ago <= 7
Gap1 Days Ago <= 7
Combined Score >= 40
```
**Purpose:** Review all signals from past week

---

## ⚡ QUICK EXCLUDE FILTERS

### Exclude Weak Volume
```
Volume Ratio >= 1.0
```

### Exclude Against Trend
```
Price vs SMA % >= -5
(for longs)

Price vs SMA % <= 5
(for shorts)
```

### Exclude Stale Signals
```
PV Days Ago <= 30
Gap1 Days Ago <= 30
```

### Exclude Recent Earnings
```
Days Since Earnings >= 7
OR
Days Since Earnings <= 0
```

---

## 🎯 SECTOR ROTATION STRATEGY

### Leading Stocks in Sector
1. Apply sector filter in main screener
2. Then apply:
```
Combined Score >= 50
PV Breakout Flag = 1
Volume Ratio >= 1.5
```
**Sort by:** Combined Score
**Result:** Top 3-5 stocks per sector

---

## 📊 COMPARISON FILTERS

### Gap vs Breakout: Which Came First?

**Gap first, breakout later:**
```
Gap1 Days Ago > PV Days Ago
PV Breakout Flag = 1
Gap1 Flag = 1
```

**Breakout first, gap later:**
```
PV Days Ago > Gap1 Days Ago
PV Breakout Flag = 1
Gap1 Flag = 1
```

---

## 🚨 ALERT-WORTHY SETUPS

**Save these as presets and check daily:**

### "New Breakout Today"
```
PV Days Ago <= 1
PV Breakout Flag = 1
Volume Ratio >= 2.0
```

### "Major Gap Today"
```
Gap2 Days Ago <= 1
Gap2 Flag = 1
```

### "Post-Earnings Move"
```
Days Since Earnings <= 3
PV Breakout Flag = 1
```

### "High Conviction Setup"
```
Combined Score >= 70
PV Days Ago <= 5
```

---

## 🎓 LEARNING FILTERS

**Beginner - Start Here:**
```
Any Signal = 1
Combined Score >= 40
```
*Sort by Combined Score, review top 20*

**Intermediate:**
```
PV Breakout Flag = 1
Volume Ratio >= 1.5
Days Since Earnings >= 7
```
*Understand each component*

**Advanced:**
```
(Gap1 Flag = 1 AND Gap1 Days Ago <= 10)
AND
(PV Breakout Flag = 1 AND PV Days Ago <= 5)
AND
(Days Since Earnings >= 7 AND Days Since Earnings <= 21)
AND
Combined Score >= 60
```
*Complex multi-factor confirmation*

---

## 📋 COPY-PASTE TEMPLATES

### Template 1: Conservative Long
```
PV Breakout Flag = 1
PV Type = 1
PV Days Ago <= 10
Price vs SMA % >= 3
Volume Ratio >= 1.5
Days Since Earnings >= 14
Gap2 Flag = 0
```

### Template 2: Aggressive Momentum
```
Combined Score >= 60
PV Days Ago <= 5
Gap1 Flag = 1
Volume Ratio >= 2.0
```

### Template 3: Value Gap Play
```
Gap2 Flag = 1
Gap2 Days Ago >= 5
Gap2 Days Ago <= 20
PV Breakout Flag = 0
Price vs SMA % > 0
Volume Ratio < 1.0
```

### Template 4: Earnings Catalyst
```
Days Since Earnings <= 7
PV Breakout Flag = 1
Gap1 Flag = 1
Combined Score >= 50
```

---

## 🔧 TROUBLESHOOTING FILTERS

### "Too Many Results" (>100 stocks)
**Add:**
```
Combined Score >= 50
Volume Ratio >= 2.0
PV Days Ago <= 10
```

### "Too Few Results" (<10 stocks)
**Try:**
```
Any Signal = 1
Combined Score >= 30
PV Days Ago <= 30
```

### "All Results Look Old"
**Reduce lookback:**
```
PV Days Ago <= 20
Gap1 Days Ago <= 20
```

### "Results Not Relevant"
**Check timeframe alignment:**
- Daily charts = daily breakouts
- Verify input settings match strategy
- Adjust thresholds (60→30 for shorter-term)

---

**Pro Tip:** Save 3-5 favorite filter combinations as presets in Pine Screener for quick daily scans.

**Remember:** Start broad (`Any Signal = 1`), then narrow with additional filters based on your strategy.

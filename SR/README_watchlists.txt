RATIO WATCHLIST FILES - QUICK START GUIDE
==========================================

COMPREHENSIVE WATCHLISTS
------------------------
1. ratio_watchlist_organized.txt (94 lines)
   - All 50 ratios with section headers
   - Organized by 10 categories
   - Use for manual reference

2. ratio_watchlist_clean.txt (50 lines)
   - All 50 ratios without comments
   - Ready for TradingView import
   - Complete master watchlist

3. ratio_reference_guide.txt
   - Detailed descriptions of all 50 ratios
   - Use cases and screener tips
   - Comprehensive documentation

FOCUSED WATCHLISTS (by Category)
---------------------------------
4. ratio_watchlist_value_growth.txt (5 ratios)
   Categories: Value vs Growth across all cap sizes
   - IWD/IWF, SPYV/SPYG (Large Cap)
   - MDYV/MDYG (Mid Cap)
   - IJS/IJT, IWN/IWO (Small Cap)
   Use: Factor rotation analysis

5. ratio_watchlist_risk_indicators.txt (8 ratios)
   Categories: Risk-on/off + Inter-asset
   - XLP/XLY, SPY/QQQ, DJU/DJT (Risk indicators)
   - SPY/TLT, SPY/GLD, BTC/GLD, QQQ/SPY (Cross-asset)
   Use: Risk management and asset allocation

6. ratio_watchlist_sector_rotation.txt (11 ratios)
   Categories: All S&P sectors vs SPY
   - XLB/SPY through XLE/SPY (11 sectors)
   - Plus SPY/DJUSSC (Semiconductors)
   Use: Sector leadership identification

QUICK START
===========

Option 1: Import Complete Watchlist
------------------------------------
1. Open ratio_watchlist_clean.txt
2. Copy all 50 ratios
3. In TradingView: Create watchlist "Market Ratios (All)"
4. Import → Paste ratios
5. Run Pine Screener with performance_display_v1

Option 2: Import Focused Watchlists (Recommended)
--------------------------------------------------
Create separate TradingView watchlists:

A. "Value-Growth Ratios"
   - Import: ratio_watchlist_value_growth.txt (5 ratios)
   - Best for: Factor rotation strategies
   
B. "Risk Indicators"
   - Import: ratio_watchlist_risk_indicators.txt (8 ratios)
   - Best for: Risk management dashboards
   
C. "Sector Rotation"
   - Import: ratio_watchlist_sector_rotation.txt (11 ratios)
   - Best for: Sector leadership analysis

SCREENER SETTINGS RECOMMENDATIONS
==================================

For ratio analysis, configure Performance Display v1 as:

Returns:
- Enable: 1M, 3M, 6M, YTD, 1Y
- Focus on shorter periods (1M, 3M) for tactical signals
- Use longer periods (6M, 1Y) for strategic trends

RS Ratings:
- Benchmark: SPY (for most ratios)
- Benchmark: TLT (for bond ratios)
- Benchmark: DJP (for commodity ratios)
- Enable: RS 1M, RS 3M, RS 6M, RS 1Y

Sorting:
- By 1M Return %: Find recent momentum shifts
- By RS 1Y: Find sustained strength/weakness
- By YTD Return %: Year-to-date leaders

INTERPRETATION GUIDE
====================

RISING RATIO = Numerator outperforming Denominator
FALLING RATIO = Denominator outperforming Numerator

Examples:

IWD/IWF rising → Value outperforming Growth
XLP/XLY rising → Defensive positioning (risk-off)
SPY/TLT rising → Stocks outperforming Bonds (risk-on)
TLT/SHY rising → Yield curve steepening
GLD/SLV rising → Gold stronger than Silver

RATIO CATEGORIES BREAKDOWN
===========================

VALUE vs GROWTH (5 ratios)
- Track factor performance across cap sizes
- Rising = Value leadership
- Falling = Growth leadership

RISK-ON/OFF (3 ratios)  
- XLP/XLY: Classic defensive vs cyclical
- SPY/QQQ: Broad vs tech-heavy
- DJU/DJT: Utilities vs transportation

SECTOR ROTATION (11 ratios)
- Each sector / SPY
- Rising = Sector outperforming market
- Falling = Sector underperforming market

GOVERNMENT BONDS (7 ratios)
- Treasuries vs GOVT benchmark
- Track duration performance

CORPORATE BONDS (2 ratios)
- LQD, HYG vs VBINX
- Credit performance tracking

COMMODITIES (8 ratios)
- Individual commodities vs DJP index
- Identify hot commodity sectors

ALTERNATIVE ASSETS (3 ratios)
- BTC, DXY, SPY vs VBINX
- Alternative asset performance

YIELD CURVE (3 ratios)
- TLT/SHY, IEF/BIL, TLH/IEI
- Curve shape and steepness

COMMODITY SPREADS (3 ratios)
- GLD/SLV, USO/DBA, DBB/GLD
- Within-commodity relationships

INTER-ASSET (5 ratios)
- SPY/TLT, SPY/GLD, BTC/GLD, etc.
- Major cross-asset signals

TOTAL SYMBOLS: 50 RATIOS

FILES LOCATION
==============
/home/imagda/_invest2024/tradingview/myIndicators/github/SR/

For questions or issues, refer to:
- ratio_reference_guide.txt (comprehensive documentation)
- ratiosAssets_v1.pine (asset-benchmark mapping logic)
- SR_v1.pine (value-growth ratio logic)

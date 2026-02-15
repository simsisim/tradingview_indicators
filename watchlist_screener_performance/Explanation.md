Based on your Pine Script code (
performance_vs_VBINX_display.pine
), here is the breakdown of the three different metrics you are seeing:

1. Return (Return %)
What it is: The simple percentage price change of the stock itself.

Formula: (Current Price - Old Price) / Old Price
Meaning: "how much money this stock made (or lost)."
Example: If a stock goes from $100 to $110, the Return is +10%.
2. Relative Return (Rel Return %)
What it is: The percentage change of the ratio between your stock and the benchmark (default VBINX). It measures outperformance.

Formula: It calculates the ratio (Stock Price / Benchmark Price) and then measures the percentage change of that ratio.
Meaning: "How much did this stock beat (or lag) the market?"
Example: If your stock went up 10%, but the benchmark went up 6%, your Rel Return will be roughly +4%.
Example: If your stock went up 10%, but the benchmark also went up 10%, your Rel Return is 0% (you simply matched the market).
3. RS (RS Rating)
What it is: A normalized score from 1 to 99 that ranks the current strength relative to its recent range.

Formula: It takes the RS Ratio (Stock / Benchmark) and normalizes it based on the highest and lowest points of that ratio over the specific time period.
Meaning: It tells you if the trend is near its peak or bottom for that specific timeframe.
~99: The stock is performing at its absolute best compared to the benchmark for this period.
~1: The stock is performing at its absolute worst compared to the benchmark for this period.
~50: The relative performance is in the middle of its recent range.
In Summary
Metric	Answers the question...	Value Type
Return	Did the price go up or down?	Percentage (%)
Rel Return	Did it beat the market?	Percentage (%)
RS	Is the relative strength currently high or low compared to its recent history?	Score (1-99)
Good
Bad


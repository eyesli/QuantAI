


from utils.ProgressBar import progress, ProgressStatus, TaskName


##### Fundamental Agent #####
def fundamentals(financial_metrics):
    """Analyzes fundamental data and generates trading signals for multiple tickers."""

    # Get the financial metrics

    if not financial_metrics:
        progress.update(TaskName.FUNDAMENTALS, ProgressStatus.ERROR, "没有 financial_metrics 数据 ")

    # Pull the most recent financial metrics
    metrics = financial_metrics[0]

    # Initialize signals list for different fundamental aspects
    signals = []
    reasoning = {}

    # 1. Profitability Analysis
    return_on_equity = metrics.return_on_equity
    net_margin = metrics.net_margin
    operating_margin = metrics.operating_margin

    thresholds = [
        (return_on_equity, 0.15),  # Strong ROE above 15%
        (net_margin, 0.20),  # Healthy profit margins
        (operating_margin, 0.15),  # Strong operating efficiency
    ]
    profitability_score = sum(metric is not None and metric > threshold for metric, threshold in thresholds)

    signals.append("bullish" if profitability_score >= 2 else "bearish" if profitability_score == 0 else "neutral")
    reasoning["profitability_signal"] = {
        "signal": signals[0],
        "details": (f"ROE: {return_on_equity:.2%}" if return_on_equity else "ROE: N/A") + ", " + (
            f"Net Margin: {net_margin:.2%}" if net_margin else "Net Margin: N/A") + ", " + (
                       f"Op Margin: {operating_margin:.2%}" if operating_margin else "Op Margin: N/A"),
    }

    progress.update(TaskName.FUNDAMENTALS, "working", "Analyzing growth")
    # 2. Growth Analysis
    revenue_growth = metrics.revenue_growth
    earnings_growth = metrics.earnings_growth
    book_value_growth = metrics.book_value_growth

    thresholds = [
        (revenue_growth, 0.10),  # 10% revenue growth
        (earnings_growth, 0.10),  # 10% earnings growth
        (book_value_growth, 0.10),  # 10% book value growth
    ]
    growth_score = sum(metric is not None and metric > threshold for metric, threshold in thresholds)

    signals.append("bullish" if growth_score >= 2 else "bearish" if growth_score == 0 else "neutral")
    reasoning["growth_signal"] = {
        "signal": signals[1],
        "details": (f"Revenue Growth: {revenue_growth:.2%}" if revenue_growth else "Revenue Growth: N/A") + ", " + (
            f"Earnings Growth: {earnings_growth:.2%}" if earnings_growth else "Earnings Growth: N/A"),
    }

    progress.update(TaskName.FUNDAMENTALS, ProgressStatus.WORKING, " Financial Health ")

    # 3. Financial Health
    current_ratio = metrics.current_ratio
    debt_to_equity = metrics.debt_to_equity
    free_cash_flow_per_share = metrics.free_cash_flow_per_share
    earnings_per_share = metrics.earnings_per_share

    health_score = 0
    if current_ratio and current_ratio > 1.5:  # Strong liquidity
        health_score += 1
    if debt_to_equity and debt_to_equity < 0.5:  # Conservative debt levels
        health_score += 1
    if free_cash_flow_per_share and earnings_per_share and free_cash_flow_per_share > earnings_per_share * 0.8:  # Strong FCF conversion
        health_score += 1

    signals.append("bullish" if health_score >= 2 else "bearish" if health_score == 0 else "neutral")
    reasoning["financial_health_signal"] = {
        "signal": signals[2],
        "details": (f"Current Ratio: {current_ratio:.2f}" if current_ratio else "Current Ratio: N/A") + ", " + (
            f"D/E: {debt_to_equity:.2f}" if debt_to_equity else "D/E: N/A"),
    }

    progress.update(TaskName.FUNDAMENTALS, ProgressStatus.WORKING, "Analyzing valuation ratios")

    # 4. Price to X ratios
    pe_ratio = metrics.price_to_earnings_ratio
    pb_ratio = metrics.price_to_book_ratio
    ps_ratio = metrics.price_to_sales_ratio

    thresholds = [
        (pe_ratio, 25),  # Reasonable P/E ratio
        (pb_ratio, 3),  # Reasonable P/B ratio
        (ps_ratio, 5),  # Reasonable P/S ratio
    ]
    price_ratio_score = sum(metric is not None and metric > threshold for metric, threshold in thresholds)

    signals.append("bearish" if price_ratio_score >= 2 else "bullish" if price_ratio_score == 0 else "neutral")
    reasoning["price_ratios_signal"] = {
        "signal": signals[3],
        "details": (f"P/E: {pe_ratio:.2f}" if pe_ratio else "P/E: N/A") + ", " + (
            f"P/B: {pb_ratio:.2f}" if pb_ratio else "P/B: N/A") + ", " + (
                       f"P/S: {ps_ratio:.2f}" if ps_ratio else "P/S: N/A"),
    }

    progress.update(TaskName.FUNDAMENTALS, ProgressStatus.WORKING, "Calculating final signal")

    # Determine overall signal
    bullish_signals = signals.count("bullish")
    bearish_signals = signals.count("bearish")

    if bullish_signals > bearish_signals:
        overall_signal = "bullish"
    elif bearish_signals > bullish_signals:
        overall_signal = "bearish"
    else:
        overall_signal = "neutral"

    # Calculate confidence level
    total_signals = len(signals)
    confidence = round(max(bullish_signals, bearish_signals) / total_signals, 2) * 100

    fundamental_analysis= {
        "signal": overall_signal,
        "confidence": confidence,
        "reasoning": reasoning,
    }
    progress.update(TaskName.FUNDAMENTALS, ProgressStatus.DONE, "基本面分析完成")
    return fundamental_analysis



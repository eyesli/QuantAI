
from tools.api import get_financial_metrics, get_market_cap, search_line_items,call_deepseek
import json
from utils.constants import TEMPLATE

"""
    您是一个比尔·阿克曼（Bill Ackman）风格的 AI 投资代理人，依据他的原则进行投资决策：

    1. 寻找具有持久竞争优势（护城河）的高质量企业。
    2. 优先考虑持续的自由现金流和增长潜力。
    3. 主张严格的财务纪律（合理的杠杆，高效的资本配置）。
    4. 重视估值：以内在价值和安全边际为目标。
    5. 在集中投资的长期投资组合中以高度信念进行投资。
    6. 如果管理层或运营改进可以释放价值，则可能采取激进的方式。

    规则：
    - 评估品牌实力、市场地位或其他护城河。
    - 检查自由现金流的产生，稳定或增长的收益。
    - 分析资产负债表的健康状况（合理的债务，良好的股本回报率）。
    - 以低于内在价值的价格购买；折扣越高，信念越强。
    - 如果管理层表现不佳或存在战略改进的路径，则进行干预。
    - 提供合理的、数据驱动的建议（看涨、看跌或中立）。

    在提供您的推理时，请详细具体地说明：
    1. 详细解释企业的质量及其竞争优势。
    2. 突出最能影响您决策的具体财务指标（自由现金流、利润率、杠杆）。
    3. 讨论任何潜在的运营改进或管理变更。
    4. 提供具有数值证据的清晰估值评估。
    5. 确定可能释放价值的具体催化剂。
    6. 使用比尔·阿克曼自信、分析性强、有时具对抗性的风格。

    例如，如果看涨：“这家公司以15%的利润率产生了卓越的自由现金流，并拥有竞争对手难以复制的主导市场地位。
            目前交易价格仅为自由现金流的12倍，相对于内在价值有40%的折扣，管理层最近的资本配置决策表明……”
    例如，如果看跌：“尽管市场地位尚可，但自由现金流利润率在三年内从12%下降到8%。
            管理层继续通过追求低投资回报率的收购来做出糟糕的资本配置决策。目前以自由现金流的18倍估值交易，鉴于运营挑战，没有安全边际……”
    """

def bill_ackman(metrics,financial_line_items,market_cap):
    """
    Analyzes stocks using Bill Ackman's investing principles and LLM reasoning.
    Fetches multiple periods of data so we can analyze long-term trends.
    """

    quality_analysis = analyze_business_quality(metrics, financial_line_items)

    balance_sheet_analysis = analyze_financial_discipline(metrics, financial_line_items)

    valuation_analysis = analyze_valuation(financial_line_items, market_cap)

    # Combine partial scores or signals
    total_score = quality_analysis["score"] + balance_sheet_analysis["score"] + valuation_analysis["score"]
    max_possible_score = 15  # Adjust weighting as desired

    # Generate a simple buy/hold/sell (bullish/neutral/bearish) signal
    if total_score >= 0.7 * max_possible_score:
        signal = "bullish"
    elif total_score <= 0.3 * max_possible_score:
        signal = "bearish"
    else:
        signal = "neutral"

    analysis_data= {
        "signal": signal,
        "score": total_score,
        "max_score": max_possible_score,
        "quality_analysis": quality_analysis,
        "balance_sheet_analysis": balance_sheet_analysis,
        "valuation_analysis": valuation_analysis
    }


    prompt = """You are a Bill Ackman AI agent, making investment decisions using his principles:

              1. Seek high-quality businesses with durable competitive advantages (moats).
              2. Prioritize consistent free cash flow and growth potential.
              3. Advocate for strong financial discipline (reasonable leverage, efficient capital allocation).
              4. Valuation matters: target intrinsic value and margin of safety.
              5. Invest with high conviction in a concentrated portfolio for the long term.
              6. Potential activist approach if management or operational improvements can unlock value.


              Rules:
              - Evaluate brand strength, market position, or other moats.
              - Check free cash flow generation, stable or growing earnings.
              - Analyze balance sheet health (reasonable debt, good ROE).
              - Buy at a discount to intrinsic value; higher discount => stronger conviction.
              - Engage if management is suboptimal or if there's a path for strategic improvements.
              - Provide a rational, data-driven recommendation (bullish, bearish, or neutral).

              When providing your reasoning, be thorough and specific by:
              1. Explaining the quality of the business and its competitive advantages in detail
              2. Highlighting the specific financial metrics that most influenced your decision (FCF, margins, leverage)
              3. Discussing any potential for operational improvements or management changes
              4. Providing a clear valuation assessment with numerical evidence
              5. Identifying specific catalysts that could unlock value
              6. Using Bill Ackman's confident, analytical, and sometimes confrontational style

              For example, if bullish: "This business generates exceptional free cash flow with a 15% margin and has a dominant market position that competitors can't easily replicate. Trading at only 12x FCF, there's a 40% discount to intrinsic value, and management's recent capital allocation decisions suggest..."
              For example, if bearish: "Despite decent market position, FCF margins have deteriorated from 12% to 8% over three years. Management continues to make poor capital allocation decisions by pursuing low-ROIC acquisitions. Current valuation at 18x FCF provides no margin of safety given the operational challenges..."
              """

    intro_text = "Based on the following analysis, create an Ackman-style investment signal."

    return analysis_data, intro_text, prompt



def analyze_business_quality(metrics: list, financial_line_items: list) -> dict:
    """
    Analyze whether the company has a high-quality business with stable or growing cash flows,
    durable competitive advantages, and potential for long-term growth.
    """
    score = 0
    details = []

    if not metrics or not financial_line_items:
        return {
            "score": 0,
            "details": "Insufficient data to analyze business quality"
        }

    # 1. Multi-period revenue growth analysis
    revenues = [item.revenue for item in financial_line_items if item.revenue is not None]
    if len(revenues) >= 2:
        # Check if overall revenue grew from first to last
        initial, final = revenues[0], revenues[-1]
        if initial and final and final > initial:
            # Simple growth rate
            growth_rate = (final - initial) / abs(initial)
            if growth_rate > 0.5:  # e.g., 50% growth over the available time
                score += 2
                details.append(f"Revenue grew by {(growth_rate * 100):.1f}% over the full period.")
            else:
                score += 1
                details.append(f"Revenue growth is positive but under 50% cumulatively ({(growth_rate * 100):.1f}%).")
        else:
            details.append("Revenue did not grow significantly or data insufficient.")
    else:
        details.append("Not enough revenue data for multi-period trend.")

    # 2. Operating margin and free cash flow consistency
    # We'll check if operating_margin or free_cash_flow are consistently positive/improving
    fcf_vals = [item.free_cash_flow for item in financial_line_items if item.free_cash_flow is not None]
    op_margin_vals = [item.operating_margin for item in financial_line_items if item.operating_margin is not None]

    if op_margin_vals:
        # Check if the majority of operating margins are > 15%
        above_15 = sum(1 for m in op_margin_vals if m > 0.15)
        if above_15 >= (len(op_margin_vals) // 2 + 1):
            score += 2
            details.append("Operating margins have often exceeded 15%.")
        else:
            details.append("Operating margin not consistently above 15%.")
    else:
        details.append("No operating margin data across periods.")

    if fcf_vals:
        # Check if free cash flow is positive in most periods
        positive_fcf_count = sum(1 for f in fcf_vals if f > 0)
        if positive_fcf_count >= (len(fcf_vals) // 2 + 1):
            score += 1
            details.append("Majority of periods show positive free cash flow.")
        else:
            details.append("Free cash flow not consistently positive.")
    else:
        details.append("No free cash flow data across periods.")

    # 3. Return on Equity (ROE) check from the latest metrics
    # (If you want multi-period ROE, you'd need that in financial_line_items as well.)
    latest_metrics = metrics[0]
    if latest_metrics.return_on_equity and latest_metrics.return_on_equity > 0.15:
        score += 2
        details.append(f"High ROE of {latest_metrics.return_on_equity:.1%}, indicating potential moat.")
    elif latest_metrics.return_on_equity:
        details.append(f"ROE of {latest_metrics.return_on_equity:.1%} is not indicative of a strong moat.")
    else:
        details.append("ROE data not available in metrics.")

    return {
        "score": score,
        "details": "; ".join(details)
    }


def analyze_financial_discipline(metrics: list, financial_line_items: list) -> dict:
    """
    Evaluate the company's balance sheet over multiple periods:
    - Debt ratio trends
    - Capital returns to shareholders over time (dividends, buybacks)
    """
    score = 0
    details = []

    if not metrics or not financial_line_items:
        return {
            "score": 0,
            "details": "Insufficient data to analyze financial discipline"
        }

    # 1. Multi-period debt ratio or debt_to_equity
    # Check if the company's leverage is stable or improving
    debt_to_equity_vals = [item.debt_to_equity for item in financial_line_items if item.debt_to_equity is not None]

    # If we have multi-year data, see if D/E ratio has gone down or stayed <1 across most periods
    if debt_to_equity_vals:
        below_one_count = sum(1 for d in debt_to_equity_vals if d < 1.0)
        if below_one_count >= (len(debt_to_equity_vals) // 2 + 1):
            score += 2
            details.append("Debt-to-equity < 1.0 for the majority of periods.")
        else:
            details.append("Debt-to-equity >= 1.0 in many periods.")
    else:
        # Fallback to total_liabilities/total_assets if D/E not available
        liab_to_assets = []
        for item in financial_line_items:
            if item.total_liabilities and item.total_assets and item.total_assets > 0:
                liab_to_assets.append(item.total_liabilities / item.total_assets)

        if liab_to_assets:
            below_50pct_count = sum(1 for ratio in liab_to_assets if ratio < 0.5)
            if below_50pct_count >= (len(liab_to_assets) // 2 + 1):
                score += 2
                details.append("Liabilities-to-assets < 50% for majority of periods.")
            else:
                details.append("Liabilities-to-assets >= 50% in many periods.")
        else:
            details.append("No consistent leverage ratio data available.")

    # 2. Capital allocation approach (dividends + share counts)
    # If the company paid dividends or reduced share count over time, it may reflect discipline
    dividends_list = [item.dividends_and_other_cash_distributions for item in financial_line_items if
                      item.dividends_and_other_cash_distributions is not None]
    if dividends_list:
        # Check if dividends were paid (i.e., negative outflows to shareholders) in most periods
        paying_dividends_count = sum(1 for d in dividends_list if d < 0)
        if paying_dividends_count >= (len(dividends_list) // 2 + 1):
            score += 1
            details.append("Company has a history of returning capital to shareholders (dividends).")
        else:
            details.append("Dividends not consistently paid or no data.")
    else:
        details.append("No dividend data found across periods.")

    # Check for decreasing share count (simple approach):
    # We can compare first vs last if we have at least two data points
    shares = [item.outstanding_shares for item in financial_line_items if item.outstanding_shares is not None]
    if len(shares) >= 2:
        if shares[-1] < shares[0]:
            score += 1
            details.append("Outstanding shares have decreased over time (possible buybacks).")
        else:
            details.append("Outstanding shares have not decreased over the available periods.")
    else:
        details.append("No multi-period share count data to assess buybacks.")

    return {
        "score": score,
        "details": "; ".join(details)
    }


def analyze_valuation(financial_line_items: list, market_cap: float) -> dict:
    """
    Ackman invests in companies trading at a discount to intrinsic value.
    We can do a simplified DCF or an FCF-based approach.
    This function currently uses the latest free cash flow only, 
    but you could expand it to use an average or multi-year FCF approach.
    """
    if not financial_line_items or market_cap is None:
        return {
            "score": 0,
            "details": "Insufficient data to perform valuation"
        }

    # Example: use the most recent item for FCF
    latest = financial_line_items[-1]  # the last one is presumably the most recent
    fcf = latest.free_cash_flow if latest.free_cash_flow else 0

    # For demonstration, let's do a naive approach:
    growth_rate = 0.06
    discount_rate = 0.10
    terminal_multiple = 15
    projection_years = 5

    if fcf <= 0:
        return {
            "score": 0,
            "details": f"No positive FCF for valuation; FCF = {fcf}",
            "intrinsic_value": None
        }

    present_value = 0
    for year in range(1, projection_years + 1):
        future_fcf = fcf * (1 + growth_rate) ** year
        pv = future_fcf / ((1 + discount_rate) ** year)
        present_value += pv

    # Terminal Value
    terminal_value = (fcf * (1 + growth_rate) ** projection_years * terminal_multiple) \
                     / ((1 + discount_rate) ** projection_years)
    intrinsic_value = present_value + terminal_value

    # Compare with market cap => margin of safety
    margin_of_safety = (intrinsic_value - market_cap) / market_cap

    score = 0
    if margin_of_safety > 0.3:
        score += 3
    elif margin_of_safety > 0.1:
        score += 1

    details = [
        f"Calculated intrinsic value: ~{intrinsic_value:,.2f}",
        f"Market cap: ~{market_cap:,.2f}",
        f"Margin of safety: {margin_of_safety:.2%}"
    ]

    return {
        "score": score,
        "details": "; ".join(details),
        "intrinsic_value": intrinsic_value,
        "margin_of_safety": margin_of_safety
    }




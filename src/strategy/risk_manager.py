
from tools.api import get_prices, prices_to_df



##### Risk Management Agent #####
def risk_management_agent(prices,ticker,portfolio):


    if not prices:
        print(f"Warning: No price data found for {ticker}. Skipping.")

    prices_df = prices_to_df(prices)

    # Calculate portfolio value
    current_price = prices_df["close"].iloc[-1]

    # Calculate current position value for this ticker
    current_position_value = portfolio.get("cost_basis", {}).get(ticker, 0)

    # Calculate total portfolio value using stored prices
    total_portfolio_value = portfolio.get("cash", 0) + sum(
        portfolio.get("cost_basis", {}).get(t, 0) for t in portfolio.get("cost_basis", {}))

    # Base limit is 20% of portfolio for any single position
    position_limit = total_portfolio_value * 0.20

    # For existing positions, subtract current position value from limit
    remaining_position_limit = position_limit - current_position_value

    # Ensure we don't exceed available cash
    max_position_size = min(remaining_position_limit, portfolio.get("cash", 0))

    risk_analysis = {
        "remaining_position_limit": float(max_position_size),
        "current_price": float(current_price),
        "reasoning": {
            "portfolio_value": float(total_portfolio_value),
            "current_position": float(current_position_value),
            "position_limit": float(position_limit),
            "remaining_limit": float(remaining_position_limit),
            "available_cash": float(portfolio.get("cash", 0)),
        }
    }

    return risk_analysis

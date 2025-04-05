import json
from tools.api import call_deepseek


##### Portfolio Management Agent #####
def portfolio_management_agent(portfolio, analyst_signals, ticker):
    """Makes final trading decisions and generates orders for multiple tickers"""

    # Get position limits, current prices, and signals for every ticker
    position_limits = {}
    current_prices = {}
    max_shares = {}
    signals_by_ticker = {}


    # Get position limits and current prices for the ticker
    risk_data = analyst_signals.get("risk_management_agent", {}).get(ticker, {})
    position_limits[ticker] = risk_data.get("remaining_position_limit", 0)
    current_prices[ticker] = risk_data.get("current_price", 0)

    # Calculate maximum shares allowed based on position limit and price
    if current_prices[ticker] > 0:
        max_shares[ticker] = int(position_limits[ticker] / current_prices[ticker])
    else:
        max_shares[ticker] = 0

    # Get signals for the ticker
    ticker_signals = {}
    for agent, signals in analyst_signals.items():
        if agent != "risk_management_agent" and ticker in signals:
            ticker_signals[agent] = {"signal": signals[ticker]["signal"], "confidence": signals[ticker]["confidence"]}
    signals_by_ticker[ticker] = ticker_signals

    prompt =  """You are a portfolio manager making final trading decisions based on multiple tickers.

              Trading Rules:
              - For long positions:
                * Only buy if you have available cash
                * Only sell if you currently hold long shares of that ticker
                * Sell quantity must be ≤ current long position shares
                * Buy quantity must be ≤ max_shares for that ticker
              
              - For short positions:
                * Only short if you have available margin (50% of position value required)
                * Only cover if you currently have short shares of that ticker
                * Cover quantity must be ≤ current short position shares
                * Short quantity must respect margin requirements
              
              - The max_shares values are pre-calculated to respect position limits
              - Consider both long and short opportunities based on signals
              - Maintain appropriate risk management with both long and short exposure

              Available Actions:
              - "buy": Open or add to long position
              - "sell": Close or reduce long position
              - "short": Open or add to short position
              - "cover": Close or reduce short position
              - "hold": No action

              Inputs:
              - signals_by_ticker: dictionary of ticker → signals
              - max_shares: maximum shares allowed per ticker
              - portfolio_cash: current cash in portfolio
              - portfolio_positions: current positions (both long and short)
              - current_prices: current prices for each ticker
              - margin_requirement: current margin requirement for short positions
              """

    user_message=f"""Based on the team's analysis, make your trading decisions for each ticker.

              Here are the signals by ticker:
              {signals_by_ticker}

              Current Prices:
              {current_prices}

              Maximum Shares Allowed For Purchases:
              {max_shares}

              Portfolio Cash: {portfolio.get('cash', 0):.2f}"
              Current Positions: {json.dumps(portfolio.get('positions', {}), indent=2)}
              Current Margin Requirement: {portfolio.get('margin_requirement', 0):.2f}"

              Output strictly in JSON with the following structure:
              {{
                "decisions": {{
                  {
                    "action": "buy/sell/short/cover/hold",
                    "quantity": integer,
                    "confidence": float between 0 and 100,
                    "reasoning": "string"
                  }
      
                }}
              }}
              """
    return call_deepseek(prompt, user_message)

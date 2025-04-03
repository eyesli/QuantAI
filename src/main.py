import json

from agents.technicals import technical_analyst
from tools.api import *
from utils.ProgressBar import progress
import datetime
if __name__ == '__main__':

    progress.start()



    # prompt = "You are a helpful assistant."
    # user_message = "What is the capital of France?中文回答"
    #
    # response = call_deepseek(prompt, user_message)
    # print(response)

    # # 获取今天日期作为结束日期
    # end_date = datetime.date.today()
    # # 计算一年前的日期作为开始日期
    # start_date = end_date - datetime.timedelta(days=365)
    #
    # end_date_str = end_date.strftime('%Y-%m-%d')
    # start_date_str = start_date.strftime('%Y-%m-%d')

    prices = get_prices(ticker="AAPL", start_date="2023-01-01", end_date="2023-10-01")
    analyst = technical_analyst(prices)

    print(json.dumps(analyst, indent=4, ensure_ascii=False))

    # news = get_company_news(ticker="AAPL", start_date="2023-01-01", end_date="2023-10-01" )
    #
    # trades = get_insider_trades(ticker="AAPL", start_date="2023-01-01", end_date="2023-08-01")
    # metrics = get_financial_metrics(ticker="AAPL", end_date="2023-10-01", period="ttm")
    # cap = get_market_cap(ticker="AAPL", end_date="2023-10-01")
    # items = search_line_items(ticker="AAPL",
    #                           line_items=["earnings_per_share", "revenue", "net_income", "book_value_per_share",
    #                                       "total_assets", "total_liabilities", "current_assets", "current_liabilities",
    #                                       "dividends_and_other_cash_distributions", "outstanding_shares"],
    #                           end_date="2023-10-01", period="annual", limit=10)

    progress.stop()





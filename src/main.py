import json


from dotenv import load_dotenv
from strategy.ben_graham import ben_graham
from strategy.cathie_wood import cathie_wood
from strategy.charlie_munger import charlie_munger_agent
from strategy.fundamentals import fundamentals_agent
from strategy.sentiment import sentiment_agent
from strategy.technicals import technical_analyst
from strategy.bill_ackman import bill_ackman
from tools.api import *

from utils.ProgressBar import progress, ProgressStatus, TaskName
import datetime

from utils.constants import TEMPLATE


def main():
    ticker = "GOOGL"
    start_date = "2025-01-01"
    end_date = "2025-4-05"
    progress.update(TaskName.PREPARE_DATA, ProgressStatus.WORKING, "获取数据开始")
    # prices = get_prices( ticker=ticker, start_date=start_date, end_date=end_date)
    metrics_limit_10 = get_financial_metrics(ticker, end_date, period="annual", limit=10)
    metrics_limit_5 = get_financial_metrics(ticker, end_date, period="annual", limit=5)
    financial_line_items1 = search_line_items(ticker,["earnings_per_share",
                                               "revenue", "net_income",
                                               "book_value_per_share",
                                               "total_assets",
                                               "total_liabilities",
                                               "current_assets",
                                               "current_liabilities",
                                               "dividends_and_other_cash_distributions",
                                               "outstanding_shares"], end_date, period="annual", limit=10)
    financial_line_items2 = search_line_items(
        ticker,
        [
            "revenue",
            "operating_margin",
            "debt_to_equity",
            "free_cash_flow",
            "total_assets",
            "total_liabilities",
            "dividends_and_other_cash_distributions",
            "outstanding_shares"
        ],
        end_date,
        period="annual",  # or "ttm" if you prefer trailing 12 months
        limit=5  # fetch up to 5 annual periods (or more if needed)
    )

    financial_line_items3 = search_line_items( ticker, [
            "revenue",
            "gross_margin",
            "operating_margin",
            "debt_to_equity",
            "free_cash_flow",
            "total_assets",
            "total_liabilities",
            "dividends_and_other_cash_distributions",
            "outstanding_shares",
            "research_and_development",
            "capital_expenditure",
            "operating_expense",

        ], end_date, period="annual", limit=5)

    market_cap = get_market_cap(ticker, end_date)







    progress.update(TaskName.PREPARE_DATA, ProgressStatus.DONE, "数据获取完成")
    response = {}
    # 1 本·格雷厄姆策略
    progress.update(TaskName.BEN_GRAHAM, ProgressStatus.WORKING, TaskName.BEN_GRAHAM.chinese + "分析 开始")
    analysis_data, intro_text, prompt = ben_graham(metrics_limit_10, financial_line_items1, market_cap)
    message = TEMPLATE.format(intro=intro_text, ticker=ticker, analysis_data=analysis_data)
    response["ben_graham"] = call_deepseek(prompt, message)
    progress.update(TaskName.BEN_GRAHAM, ProgressStatus.DONE, TaskName.BEN_GRAHAM.chinese + "分析 完成")
    # 2 比尔·阿克曼策略
    progress.update(TaskName.BILL_ACKMAN, ProgressStatus.WORKING, TaskName.BILL_ACKMAN.chinese + "分析 开始")
    analysis_data, intro_text, prompt = bill_ackman(metrics_limit_5, financial_line_items2, market_cap)
    message = TEMPLATE.format(intro=intro_text, ticker=ticker, analysis_data=analysis_data)
    response["bill_ackman"] = call_deepseek(prompt, message)
    progress.update(TaskName.BILL_ACKMAN, ProgressStatus.DONE, TaskName.BILL_ACKMAN.chinese + "分析 完成")
    # 3 凯茜·伍德策略
    progress.update(TaskName.CATHIE_WOOD, ProgressStatus.WORKING, TaskName.CATHIE_WOOD.chinese + "分析 开始")
    analysis_data, intro_text, prompt=cathie_wood(metrics_limit_5, financial_line_items3, market_cap)
    message = TEMPLATE.format(intro=intro_text, ticker=ticker, analysis_data=analysis_data)
    response["cathie_wood"] = call_deepseek(prompt, message)
    progress.update(TaskName.CATHIE_WOOD, ProgressStatus.DONE, TaskName.CATHIE_WOOD.chinese + "分析 结束")
    #


    print(response)


if __name__ == '__main__':
    load_dotenv()         # 加载环境变量
    progress.start()      # 启动进度条（或类似的可视化输出）

    try:
        main()            # 执行主逻辑
    except Exception as e:
        print(f"Error: {e}")  # 捕获并打印异常
    finally:
        progress.stop()   # 无论是否报错都停止进度显示

    # # 获取今天日期作为结束日期
    # end_date = datetime.date.today()
    # # 计算一年前的日期作为开始日期
    # start_date = end_date - datetime.timedelta(days=365)
    #
    # end_date_str = end_date.strftime('%Y-%m-%d')
    # start_date_str = start_date.strftime('%Y-%m-%d')

    # prices = get_prices(ticker="AAPL", start_date="2023-01-01", end_date="2023-10-01")
    # analyst = technical_analyst(prices)
    # print(json.dumps(analyst, indent=4, ensure_ascii=False))
    #
    # agent = fundamentals_agent(ticker="AAPL", end_date="2023-10-01")
    #
    # print(json.dumps(agent, indent=4, ensure_ascii=False))


    # agent = sentiment_agent(ticker="soun", end_date="2025-03-01")
    # print(agent)
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







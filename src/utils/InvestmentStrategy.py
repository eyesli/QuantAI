from enum import Enum

class InvestmentStrategy(Enum):
    FUNDAMENTALS = ("Fundamentals", "基本面策略")
    RISK_MANAGEMENT = ("Risk Management", "风险管理策略")
    SENTIMENT = ("Sentiment", "情绪策略")
    WARREN_BUFFETT = ("Warren Buffett", "巴菲特策略")
    STANLEY_DRUCKENMILLER = ("Stanley Druckenmiller", "德鲁肯米勒策略")
    PHIL_FISHER = ("Phil Fisher", "菲尔·费舍尔策略")
    CHARLIE_MUNGER = ("Charlie Munger", "查理·芒格策略")
    CATHIE_WOOD = ("Cathie Wood", "凯茜·伍德策略")
    BILL_ACKMAN = ("Bill Ackman", "比尔·阿克曼策略")
    TECHNICAL_ANALYST = ("technical_analyst", "技术分析")

    def __init__(self, english: str, chinese: str):
        self.english = english
        self.chinese = chinese

# constants.py
TEMPLATE = """{intro}

Analysis Data for {ticker}:
{analysis_data}

返回json数据格式如下,不需要有其他任何标注，只需要json数据:reasoning 使用中文回答
{{
  "signal": "看涨 or 看跌 or 中立",
  "confidence": float (0-100),
  "reasoning": "string"
}}
"""
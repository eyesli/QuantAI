import pandas as pd
import numpy as np
import json


##### Sentiment Agent #####
def sentiment(insider_trades,company_news):
    """Analyzes market sentiment and generates trading signals for multiple tickers."""
    # Get the signals from the insider trades
    transaction_shares = pd.Series([t.transaction_shares for t in insider_trades]).dropna()
    insider_signals = np.where(transaction_shares < 0, "bearish", "bullish").tolist()


    # Get the sentiment from the company news
    sentiment = pd.Series([n.sentiment for n in company_news]).dropna()
    news_signals = np.where(sentiment == "negative", "bearish",
                            np.where(sentiment == "positive", "bullish", "neutral")).tolist()

    # Combine signals from both sources with weights
    insider_weight = 0.3
    news_weight = 0.7

    # Calculate weighted signal counts
    bullish_signals = (
            insider_signals.count("bullish") * insider_weight +
            news_signals.count("bullish") * news_weight
    )
    bearish_signals = (
            insider_signals.count("bearish") * insider_weight +
            news_signals.count("bearish") * news_weight
    )

    if bullish_signals > bearish_signals:
        overall_signal = "bullish"
    elif bearish_signals > bullish_signals:
        overall_signal = "bearish"
    else:
        overall_signal = "neutral"

    # Calculate confidence level based on the weighted proportion
    total_weighted_signals = len(insider_signals) * insider_weight + len(news_signals) * news_weight
    confidence = 0  # Default confidence when there are no signals
    if total_weighted_signals > 0:
        confidence = round(max(bullish_signals, bearish_signals) / total_weighted_signals, 2) * 100
    reasoning = f"Weighted Bullish signals: {bullish_signals:.1f}, Weighted Bearish signals: {bearish_signals:.1f}"

    sentiment_analysis= {
        "signal": overall_signal,
        "confidence": confidence,
        "reasoning": reasoning,
    }


    return sentiment_analysis


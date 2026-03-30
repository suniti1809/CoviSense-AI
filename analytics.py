def add_analytics(data):
    data = data.sort_values("Date")

    # Daily cases
    data['Daily'] = data['Cases'].diff().fillna(0)
    data['Daily'] = data['Daily'].apply(lambda x: x if x > 0 else 0)

    return data


def get_insights(data):
    current = int(data['Cases'].iloc[-1])

    # 🔥 Growth (last 7 days)
    if len(data) > 7:
        last = data['Cases'].iloc[-1]
        prev = data['Cases'].iloc[-8]

        growth = ((last - prev) / prev) * 100 if prev != 0 else 0
    else:
        growth = 0

    growth = round(growth, 2)

    avg_daily = int(data['Daily'].tail(7).mean())
    peak = int(data['Daily'].max())

    # Trend
    if growth > 10:
        trend = "📈 Rapid Growth"
        risk = "🔴 High"
    elif growth > 2:
        trend = "📈 Increasing"
        risk = "🟡 Moderate"
    elif growth < -1:
        trend = "📉 Decreasing"
        risk = "🟢 Low"
    else:
        trend = "➡ Stable"
        risk = "🟢 Low"

    return {
        "current": current,
        "growth": growth,
        "peak": peak,
        "trend": trend,
        "risk": risk,
        "avg_daily": avg_daily
    }
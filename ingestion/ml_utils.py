from .models import LogEntry


def detect_anomalies(queryset=None):
    """Detect anomalies in logs.

    This function lazily imports `pandas` and `sklearn` so the Django app
    can still start when those heavy ML packages are not installed.
    If the ML stack is unavailable it returns an empty list.
    """
    try:
        import pandas as pd
        from sklearn.ensemble import IsolationForest
    except Exception:
        return []

    if queryset is None:
        queryset = LogEntry.objects.all()

    logs = queryset.values("id", "timestamp", "service", "log_level", "message")
    df = pd.DataFrame(list(logs))

    if df.empty:
        return []

    # timestamp → numeric (seconds since epoch)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["timestamp_num"] = df["timestamp"].astype("int64") / 10**9

    # encode categorical
    df["service_code"] = df["service"].astype("category").cat.codes
    df["level_code"] = df["log_level"].astype("category").cat.codes
    df["msg_code"] = df["message"].astype("category").cat.codes

    features = df[["timestamp_num", "service_code", "level_code", "msg_code"]]

    # Isolation Forest
    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(features)

    anomalies = df[df["anomaly"] == -1]
    return [int(row["id"]) for _, row in anomalies.iterrows()]

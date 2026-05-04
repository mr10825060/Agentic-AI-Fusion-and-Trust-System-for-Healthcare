def trust_agent(data):

    scores = {}

    for name, df in data.items():

        if df is not None and not df.empty:

            missing = df.isnull().sum().sum()
            total = df.size

            if total > 0:
                score = 1 - (missing / total)
                scores[name] = round(score, 3)
            else:
                scores[name] = 0.0

        else:
            scores[name] = 0.0

    if len(scores) > 0:
        overall = sum(scores.values()) / len(scores)
    else:
        overall = 0.0

    return scores, round(overall, 3)
def history_to_float(history):
    return {k : list(map(float, list_history))
            for k, list_history in history.items()}
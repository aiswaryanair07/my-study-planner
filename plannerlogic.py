def allocate_time(df,total_hours):
    total_priority=df["priority"].sum()
    df["Allocated_Hours"] = (df["priority"] / total_priority) * total_hours
    return df
    
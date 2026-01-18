import pandas as p
def create_sub_table(data):
    df=p.DataFrame(data)
    return df

def add_priority(df):
    df["priority"]=(df["Difficulty"]*df["chapters"]/df["days_left"])
    return df

def sort_by_priority(df):
    return df.sort_values(by="priority",ascending=False)



import json
import pandas as pd
from pathlib import Path

# BASE_DIR becomes PosixPath('/usr/src/project-tracker/src/
BASE_DIR = Path(__file__).resolve().parent.parent

# DATA_PATH becomes PosixPath('/usr/src/project-tracker/src/data/progress.csv')
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "progress.csv"

# CONFIG_PATH becomes PosixPath('/usr/src/project-tracker/src/data/course_config.json
CONFIG_PATH = Path(__file__).resolve().parent.parent / "data" / "course_config.json"

def init_data():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        df = pd.DataFrame(columns=["date", "course", "videos_completed"])
        df.to_csv(DATA_PATH, index=False)
    return read_data()

def read_data():
    return pd.read_csv(DATA_PATH) if DATA_PATH.exists() else pd.DataFrame.columns(columns=["date", "course", "videos_completed"])

def make_df_orderly(df):
    """ 
    Performs these steps in the following order on the given dataframe:
    1. Sorts the dataframe as per the date column.
    2. Calculates/updates the progress column with the cumulative sum of videos done.
    3. Resets the dataframe index and drops the previous index column.
    These steps are necessary after taking the data and before using the dataframe for plotting.
    """
    df = df.sort_values(['course', 'date'])
    df['progress'] = df.groupby('course')['videos_completed'].cumsum()
    df.reset_index(drop=True, inplace=True)
    return df

def edit_progress(date, course, videos_completed):
    df = read_data()
    new_row = pd.DataFrame([[date, course, videos_completed]], columns=df.columns[:3])
    match_cols = ["date", "course"]
    mask = pd.Series(True, index=df.index)

    for col in match_cols:
        mask &= df[col] == new_row.iloc[0][col]

    df = df[~mask]
    df = pd.concat([df, new_row], ignore_index=True)
    df = make_df_orderly(df)
    
    df.to_csv(DATA_PATH, index=False)

# ---- Course Config Operations ----
def load_course_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump({}, f)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_course_config(config_dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config_dict, f, indent=2)

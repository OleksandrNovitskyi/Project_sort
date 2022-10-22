import pandas as pd


def input_black_list():
    """Read Google Sheet black list and return list of first_names and list of last_names

    black_list = "https://docs.google.com/spreadsheets/d/1lXjDSK5398p1yJuTJn3vO4Ux9KDJtqP1esar1Z9U4vc/edit#gid=0"
    """
    sheet_id = "1lXjDSK5398p1yJuTJn3vO4Ux9KDJtqP1esar1Z9U4vc"
    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    )
    first_names = df[df.columns[0]].values.tolist()
    last_names = df[df.columns[1]].values.tolist()
    positions = df[df.columns[2]].values.tolist()
    return first_names, last_names, positions

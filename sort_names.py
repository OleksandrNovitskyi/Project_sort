# import csv

# with open("test.csv", "r", encoding="utf8") as file:
#     csvreader = csv.reader(file, delimiter=",")
#     for row in csvreader:
#         print(row)

import pandas as pd


def input_black_list():
    df = pd.read_table(
        r"https://docs.google.com/spreadsheets/d/1lXjDSK5398p1yJuTJn3vO4Ux9KDJtqP1esar1Z9U4vc/edit#gid=0",
        sep="delimiter",
        skiprows=[0, 1],
    )
    print(df.head())

    col_list = df.columns.values[0].split(",")  # get list with col names
    print(col_list)

    black_dict = df.to_dict(col_list[0])
    return black_dict


print(input_black_list())


# data = pd.read_table("test.csv", sep="delimiter")
# st = data.head(0)
# t = st[0].split(",")
# print(type(st))

# black_list = []

# filename = "file.csv"
# with open(filename, "r+", encoding="utf8") as f:
#     data = f.read()
#     f.seek(0)
#     f.write(output)
#     f.truncate()


# with open(filename, "r", encoding="utf8") as fin:
#     for line in fin:
#         d[(line.strip().lower())] = 0

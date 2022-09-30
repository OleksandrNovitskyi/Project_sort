import csv
import sys
import time
import pandas as pd
import multiprocessing as mp
from fileinput import filename
from multiprocessing import Pool
from deepface import DeepFace

filename = sys.argv[1]
Res_list = []


# ---- INPUT PARAMETERS ----
limit_age = 25  # not younger than
races = [
    "black",
    "white",
    "asian",
]  # enter necessary races. List of possible races - ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']
forbidden_word = "NFT"  # a forbidden word in the current position of person


def read_file(filename):
    """Read .csv file and create list of people"""
    with open(filename, "r", encoding="utf8") as file:
        csvreader = csv.reader(
            file, delimiter=","
        )  # delimiter="," - if the data is concatenated in the first column by ','
        # delimiter=";" - if the data in the different column
        read_file_list = list(csvreader)
    return read_file_list


# def create_result_file(filename, readed_list, first_names, last_names):
#     """Create(rewrite) CSV file with short list of people"""
#     res_file_name = filename[:-4] + "_filt.csv"
#     with open(res_file_name, "w+", encoding="utf8", newline="") as res_file:
#         writer = csv.writer(res_file, delimiter=";")
#         for row in readed_list:
#             if (
#                 name_filter(row[24], first_names)
#                 and (row[25] not in last_names)
#                 and (forbidden_word not in row[43])
#                 and face_filter(row[30], limit_age, races)
#             ):
#                 writer.writerow(row)


def create_result_file(filename, res_list):
    """Create(rewrite) CSV file with short list of people"""
    res_file_name = filename[:-4] + "_filt.csv"
    with open(res_file_name, "w+", encoding="utf8", newline="") as res_file:
        writer = csv.writer(res_file, delimiter=";")
        for row in res_list:
            writer.writerow(row)


def filtering(readed_list, first_names, last_names):
    """Create short list of people"""
    for row in readed_list:
        if (
            name_filter(row[24], first_names)
            and (row[25] not in last_names)
            and (forbidden_word not in row[43])
            and face_filter(row[30], limit_age, races)
        ):
            Res_list.append(row)


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
    return first_names, last_names


def name_filter(name, black_list):
    """Filter people by name and by part of name"""
    for word in black_list:
        if len(word) <= 2:
            return word != name
        if word in name:
            return False
    return True


def face_filter(img, age=25, races=["white"]):
    """Filter people by age and race using photo

    img - path to photo
    age - no younger than "age"
    race - only one race from ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']
    """
    try:
        obj = DeepFace.analyze(img_path=img, actions=["age", "race"])
        return (obj["age"] > age) and (obj["dominant_race"] in races)
    except Exception as _ex:
        return _ex


def split(a, n):
    """Split list into n lists"""
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def main():

    print("--- START ---")
    start_time = time.time()
    first_names, last_names = input_black_list()

    read_file_list = read_file(filename)
    n = mp.cpu_count()
    a = list(split(read_file_list, n))  # a == [[list1], [list2]...]
    # create_result_file(filename, read_file_list, first_names, last_names)
    # filtering(readed_list, first_names, last_names)
    # print(filename, a[0], first_names, last_names)
    with Pool(4) as p:
        p.starmap(
            filtering,
            [
                (a[0], first_names, last_names),
                (a[1], first_names, last_names),
                (a[2], first_names, last_names),
                (a[3], first_names, last_names),
            ],
        )
    print(Res_list)
    create_result_file(filename, Res_list)
    print("Work time --- {} seconds ---".format(time.time() - start_time))


if __name__ == "__main__":
    main()

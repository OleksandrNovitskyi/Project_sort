import csv
import sys
import time
import pandas as pd
import multiprocessing as mp
from fileinput import filename
from multiprocessing import Pool
from deepface import DeepFace

filename = sys.argv[1]

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


def create_result_file(filename, readed_list, first_names, last_names):
    """Create(rewrite) CSV file with short list of people"""
    res_file_name = filename[:-4] + "_filt.csv"
    with open(res_file_name, "w+", encoding="utf8", newline="") as res_file:
        writer = csv.writer(res_file, delimiter=";")
        for row in readed_list:
            if (
                name_filter(row[24], first_names)
                and (row[25] not in last_names)
                and (forbidden_word not in row[43])
                # and face_filter(row[30], limit_age, races)
            ):
                writer.writerow(row)


# def get_short_list(filename, first_names, last_names):
#     """Read .csv file and create(rewrite) another .csv file with short list of people"""
#     n_cond = 0
#     res_file_name = filename[:-4] + "_filt.csv"
#     with open(filename, "r", encoding="utf8") as file, open(
#         res_file_name, "w+", encoding="utf8", newline=""
#     ) as res_file:
#         writer = csv.writer(res_file, delimiter=";")
#         csvreader = csv.reader(
#             file, delimiter=","
#         )  # delimiter="," - if the data is concatenated in the first column by ','
#         # delimiter=";" - if the data in the different column
#         read_file = list(csvreader)
#         num_people = len(read_file) - 1
#         print("Estimated time ~ {} seconds".format(num_people * 1.2))

#             # print(p.map(f, [1, 2, 3]))
#         # for row in read_file:
#         #     if (
#         #         name_filter(row[24], first_names)
#         #         and (row[25] not in last_names)
#         #         and (forbidden_word not in row[43])
#         #         # and face_filter(row[30], limit_age, races)
#         #     ):
#         #         writer.writerow(row)
#         #         count += 1
#         #     count_row += 1
#         #     condition = round(100 * count_row / num_people)

#         #     if (condition % 3 == 0) and (n_cond != condition):
#         #         n_cond = condition
#         #         print("---- {}% completed ----".format(n_cond))
#         print("There were", num_people, "people before filtering")
#         # print("Done, now there are", count, "people")
#         print("Results at the file '{}'".format(res_file_name))


def filter(read_file, first_names, last_names, writer):
    count = 0
    count_row = 0
    for row in read_file:
        if (
            name_filter(row[24], first_names)
            and (row[25] not in last_names)
            and (forbidden_word not in row[43])
            # and face_filter(row[30], limit_age, races)
        ):
            writer.writerow(row)
            count += 1
        count_row += 1
        condition = round(100 * count_row / num_people)

        if (condition % 3 == 0) and (n_cond != condition):
            n_cond = condition
            print("---- {}% completed ----".format(n_cond))
    # return count


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
    # n = mp.cpu_count()
    # a = list(split(read_file_list, n))  # a == [[list1], [list2]...]
    create_result_file(filename, read_file_list, first_names, last_names)

    # with Pool(n) as p:
    #     p.map(
    #         create_result_file,
    #         [
    #             (filename, a[0], first_names, last_names),
    #             (filename, a[1], first_names, last_names),
    #             (filename, a[2], first_names, last_names),
    #             (filename, a[3], first_names, last_names),
    #         ],
    # )
    print("Work time --- {} seconds ---".format(time.time() - start_time))


if __name__ == "__main__":
    main()

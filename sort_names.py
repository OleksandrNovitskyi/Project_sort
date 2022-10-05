import csv
import sys
import time
import urllib.request

from fileinput import filename
from deepface import DeepFace
import pandas as pd


filename = sys.argv[1]

# ---- INPUT PARAMETERS ----
limit_age = 25  # not younger than
races = [
    "asian",
    "black",
    "white",
]  # enter necessary races. List of possible races - ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']


def get_short_list(filename, first_names, last_names, positions):
    """Read .csv file and create(rewrite) another .csv file with short list of people"""
    count = 0
    count_row = 0
    count_no_link = 0
    n_cond = 0
    res_file_name = filename[:-4] + "_filt.csv"
    with open(filename, "r", encoding="utf8") as file, open(
        res_file_name, "w+", encoding="utf8", newline=""
    ) as res_file:
        writer = csv.writer(res_file, delimiter=";")
        csvreader = csv.reader(
            file, delimiter=","
        )  # delimiter="," - if the data is concatenated in the first column by ','
        # delimiter=";" - if the data in the different column
        first_row = next(csvreader)
        read_file = list(csvreader)
        num_people = len(read_file)
        count_name = count_last = count_pos = count_age_race = num_people
        print("--- START ---")
        print("Estimated time ~ {} minutes".format(round(num_people * 1.2 / 60)))
        writer.writerow(first_row)

        for row in read_file:
            if name_filter(row[24], first_names):
                count_name -= 1
                if row[25] not in last_names:
                    count_last -= 1
                    if position_filter(row[43], positions):
                        count_pos -= 1
                        if row[30] == "":
                            count_no_link += 1
                        else:
                            if face_filter(row[30], limit_age, races):
                                count_age_race -= 1
                                count += 1
                                writer.writerow(row)
            count_row += 1
            condition = round(100 * count_row / num_people)

            if (condition % 10 == 0) and (n_cond != condition):
                n_cond = condition
                print("---- {}% completed ----".format(n_cond))
        print("There were", num_people, "people before filtering")
        print("Done, now there are", count, "people")
        print("Results at the file '{}'".format(res_file_name))

        print("Statistic:")
        print("There are", count_no_link, "people without avatar")
        print("Delete by Name filtered {} person".format(count_name))
        print("Delete by Last name filtered {} person".format(count_last - count_name))
        print("Delete by Position filtered {} person".format(count_pos - count_last))
        print(
            "Delete by DeepFace filtered {} person".format(
                count_age_race - count_pos - count_no_link
            )
        )


def download_img(imgURL):
    urllib.request.urlretrieve(imgURL, "img.jpg")


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


def name_filter(name, black_list):
    """Filter people by name and by part of name"""
    for word in black_list:
        if len(word) <= 2:
            return word != name
        if word in name:
            return False
    return True


def position_filter(position, black_list):
    """Filter people by part of the position"""
    position = position.lower()
    for word in black_list:
        if type(word) == str:
            if word.lower() in position:
                return False
    return True


def face_filter(img, age=25, races="white"):
    """Filter people by age and race using photo

    img - path to photo
    age - no younger than "age"
    race - only one race from ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']
    """
    try:
        obj = DeepFace.analyze(img_path=img, actions=["age", "race"])
        return (obj["age"] > age) and (obj["dominant_race"] in races)
    except Exception as _ex:
        try:
            download_img(img)
            obj = DeepFace.analyze("img.jpg", actions=["age", "race"])
            return (obj["age"] > age) and (obj["dominant_race"] in races)
        except Exception as _ex2:
            return False


def main():
    start_time = time.time()
    first_names, last_names, positions = input_black_list()
    get_short_list(filename, first_names, last_names, positions)
    print("Work time --- {} minutes ---".format(round((time.time() - start_time) / 60)))


if __name__ == "__main__":
    main()

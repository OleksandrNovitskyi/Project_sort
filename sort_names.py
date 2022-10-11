import csv  # work with .csv files
import sys
import time
import urllib.request
from collections import defaultdict
from fileinput import filename

# modules
import filters
import inputs

filename = sys.argv[1]

# ---- INPUT PARAMETERS ----
LIMIT_AGE = 25  # not younger than
# enter necessary races. List of possible races - ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']
races = ["asian", "black", "white"]
DEL_PEOPLE_WITHOUT_AVATAR = False  # past 'True' or 'False'


def conditions(row, dict_races, first_names, last_names, positions):
    """Check all conditions and if row is correct - return True, else - False.
    At the same time returns a tuple with counters
    """
    counts = []
    conditions = [
        filters.name_filter(row[24], first_names),
        row[25] not in last_names,
        filters.position_filter(row[43], positions),
        (row[30] == "") and DEL_PEOPLE_WITHOUT_AVATAR,
    ]
    if filters.name_filter(row[24], first_names):
        counts.append("count_name")
        if row[25] not in last_names:
            counts.append("count_last")
            if filters.position_filter(row[43], positions):
                counts.append("count_pos")
                if (row[30] == "") and DEL_PEOPLE_WITHOUT_AVATAR:
                    counts.append("count_no_link")
                    return False, counts
                elif (row[30] == "") and not DEL_PEOPLE_WITHOUT_AVATAR:
                    counts.extend(["count", "count_no_link"])
                    return True, counts
                else:
                    age, race, curent_race = filters.face_filter(
                        row[30], LIMIT_AGE, races
                    )
                    if curent_race is not None:
                        if age:
                            counts.append("count_age")
                            dict_races[curent_race] += 1
                            if race:
                                counts.extend(["count", "count_race"])
                                return True, counts
                            return False, counts
                        return False, counts
                    counts.extend(["count_unreadable_ava", "count"])
                    return True, counts
            return False, counts
        return False, counts
    return False, counts


def counters(dict_, list_):
    """For each element in list, find same key in dict and increments it value"""
    for elem in list_:
        if elem in dict_:
            dict_[elem] += 1


def get_short_list(f_name, first_names, last_names, positions):
    """Read .csv file and create(rewrite) another .csv file with short list of people"""
    d_counters = {
        "count": 0,
        "count_no_link": 0,
        "count_unreadable_ava": 0,
        "count_name": 0,
        "count_last": 0,
        "count_pos": 0,
        "count_age": 0,
        "count_race": 0,
    }
    count_row = 0
    n_cond = 0
    d_rases = defaultdict(int)
    res_file_name = f_name[:-4] + "_filt.csv"
    res_del_file_name = f_name[:-4] + "_deleted.csv"
    with open(f_name, "r", encoding="utf8") as file, open(
        res_file_name, "w+", encoding="utf8", newline=""
    ) as res_file, open(
        res_del_file_name, "w+", encoding="utf8", newline=""
    ) as res_del_file:
        writer = csv.writer(res_file, delimiter=";")
        writer2 = csv.writer(res_del_file, delimiter=";")
        csvreader = csv.reader(
            file, delimiter=","
        )  # delimiter="," - if the data is concatenated in the first column by ','
        # delimiter=";" - if the data in the different column
        first_row = next(csvreader)
        read_file = list(csvreader)
        num_people = len(read_file)
        print("--- START ---")
        print(f"Estimated time ~ {round(num_people * 1.2 / 60)} minutes")
        writer.writerow(first_row)
        writer2.writerow(first_row)

        for row in read_file:
            result, t_counters = conditions(
                row, d_rases, first_names, last_names, positions
            )
            counters(d_counters, t_counters)
            if result:
                writer.writerow(row)
            else:
                writer2.writerow(row)
            count_row += 1
            condition = round(100 * count_row / num_people)

            if (condition % 10 == 0) and (n_cond != condition):
                n_cond = condition
                print(f"---- {n_cond}% completed ----")

        arr = [
            f"There were {num_people} people before filtering",
            f"Done, now there are {d_counters['count']} people",
            f"Results at the file '{res_file_name}', deleted people at the file '{res_del_file_name}'",
            "Statistic:",
        ]
        if DEL_PEOPLE_WITHOUT_AVATAR:
            arr.append(
                f"There are {d_counters['count_no_link']} people without avatar and they were deleted"
            )
        else:
            arr.append(
                f"There are {d_counters['count_no_link']} people without avatar and they in the result file"
            )
        arr2 = [
            f"There are {d_counters['count_unreadable_ava']} people with unreadable avatar and they in the result file",
            f"Delete by Name filtered {num_people - d_counters['count_name']} person",
            f"Delete by Last name filtered {d_counters['count_name'] - d_counters['count_last']} person",
            f"Delete by Position filtered {d_counters['count_last'] - d_counters['count_pos']} person",
            f"Delete by Age using DeepFace filter {d_counters['count_pos'] - d_counters['count_age'] - d_counters['count_no_link'] - d_counters['count_unreadable_ava']} person",
            f"Delete by Race using DeepFace filter {d_counters['count_age'] - d_counters['count_race']} person",
            f"How many people of what races made it to sorting by race {dict(d_rases)}",
        ]
        statistic = arr + arr2
        print("\n".join(statistic))


def download_img(imgURL):
    """Download IMG by URL"""
    urllib.request.urlretrieve(imgURL, "img.jpg")


def main():
    """Main excecution"""
    start_time = time.time()
    first_names, last_names, positions = inputs.input_black_list()
    get_short_list(filename, first_names, last_names, positions)
    print(f"Work time --- {round((time.time() - start_time) / 60)} minutes ---")


if __name__ == "__main__":
    main()

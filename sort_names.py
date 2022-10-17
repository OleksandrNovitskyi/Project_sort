import csv  # work with .csv files
import sys
import time
from collections import defaultdict
from fileinput import filename

# modules
import filters
import inputs

filename = sys.argv[1]

# ---- INPUT PARAMETERS ----
LIMIT_AGE = 25  # not younger than
# enter necessary races. List of possible races - ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']
races = [
    "asian",
    "black",
    "white",
]
DEL_PEOPLE_WITHOUT_AVATAR = False  # past 'True' or 'False'


def conditions(row, dict_races, first_names, last_names, positions):
    """Check all conditions and if row is correct - return True, else - False.
    At the same time returns a tuple with counters
    """
    counts = defaultdict(int)

    def filter_face():
        age, race, curent_race = filters.face_filter(row[30], LIMIT_AGE, races)
        if curent_race is not None:
            if age:
                counts["count_age"] += 1
                dict_races[curent_race] += 1
                if race:
                    counts["count"] += 1
                    counts["count_race"] += 1
        else:
            counts["count_unreadable_ava"] += 1
            counts["count"] += 1

    def iterate_count(
        str_args,
    ):  # try ```iterate_count(*str_args)``` - but it doesn't open tuple
        if isinstance(str_args, tuple):
            for str_count in str_args:
                counts[str_count] += 1
        else:
            counts[str_args] += 1

    conditions1 = [
        filters.name_filter(row[24], first_names),
        row[25] not in last_names,
        filters.position_filter(row[43], positions),
    ]
    functions1 = [
        "count_name",
        "count_last",
        "count_pos",
    ]
    for cond, func in zip(conditions1, functions1):
        if cond:
            iterate_count(func)
    if len(counts) < 3:
        iterate_count("count_simple")
        return counts
    conditions2 = [
        (row[30] == "") and DEL_PEOPLE_WITHOUT_AVATAR,
        (row[30] == "") and not DEL_PEOPLE_WITHOUT_AVATAR,
    ]
    functions2 = [
        "count_no_link",
        ("count", "count_no_link"),
    ]
    for cond, func in zip(conditions2, functions2):
        if cond:
            iterate_count(func)
    if counts["count_no_link"]:
        return counts
    filter_face()
    return counts


def counters(dict_, dict_child):
    """Find goal filter in dict_child and rewrite (increments) some values in dict_"""
    for elem in dict_child.keys():
        if dict_child[elem]:
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
        "count_simple": 0,
    }
    count_row = 0
    n_cond = 0
    d_rases = defaultdict(int)
    res_file_name = f_name[:-4] + "_filt.csv"
    res_del_file_name = f_name[:-4] + "_deleted.csv"
    with open(res_file_name, "w+", encoding="utf8", newline="") as res_file, open(
        res_del_file_name, "w+", encoding="utf8", newline=""
    ) as res_del_file:
        writer = csv.writer(res_file, delimiter=";")
        writer2 = csv.writer(res_del_file, delimiter=";")
        read_file, first_row = inputs.read_file(f_name)
        num_people = len(read_file)
        print(f"Estimated time ~ {round(num_people * 1.2 / 60)} minutes")
        writer.writerow(first_row)
        writer2.writerow(first_row)

        for row in read_file:
            d_counters_child = conditions(
                row, d_rases, first_names, last_names, positions
            )
            if d_counters_child["count"]:
                writer.writerow(row)
            else:
                writer2.writerow(row)
            count_row += 1
            counters(d_counters, d_counters_child)

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
        f"Delete by Name or Last or Position filtered {d_counters['count_simple']} person",
        f"(Find {num_people - d_counters['count_name']} inappropriate Names)",
        f"(Find {num_people - d_counters['count_last']} inappropriate Last names)",
        f"(Find {num_people - d_counters['count_pos']} inappropriate Position)",
        f"Delete by Age using DeepFace filter {num_people - d_counters['count_age'] - d_counters['count_simple'] - d_counters['count_no_link'] - d_counters['count_unreadable_ava']} person",
        f"Delete by Race using DeepFace filter {d_counters['count_age'] - d_counters['count_race']} person",
        f"How many people of what races made it to sorting by race {dict(d_rases)}",
    ]
    statistic = arr + arr2
    print("\n".join(statistic))


def main():
    """Main excecution"""
    start_time = time.time()
    print("--- START ---")
    first_names, last_names, positions = inputs.input_black_list()
    get_short_list(filename, first_names, last_names, positions)
    print(f"Work time --- {round((time.time() - start_time) / 60)} minutes ---")


if __name__ == "__main__":
    main()

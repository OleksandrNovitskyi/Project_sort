import csv
from deepface import DeepFace


def get_short_list(filename, first_names, last_names):
    """Read .csv file and create(rewrite) another .csv file with short list of people"""
    count = 0
    forbidden_word = "NFT"
    with open(filename, "r", encoding="utf8") as file, open(
        "result.csv", "w+", encoding="utf8", newline=""
    ) as res_file:
        writer = csv.writer(res_file, delimiter=" ")
        csvreader = csv.reader(file, delimiter=";")
        row1 = next(csvreader)
        for row in csvreader:
            if (
                (row[24] not in first_names)
                and (row[25] not in last_names)
                and (forbidden_word not in row[43])
                and face_filter(row[30])
            ):
                writer.writerow(row1)
                writer.writerow(row)
                count += 1
        print("Done, now there are", count, "person")


def input_black_list():
    """Read .csv black list and return list of first_names and list of last_names"""
    with open("Indusi.csv", "r", encoding="utf8") as file:
        csvreader = csv.reader(file, delimiter=",")
        first_names = []
        last_names = []
        title_t = next(csvreader)
        for row in csvreader:
            first_names.append(row[0])
            last_names.append(row[1])
    return first_names, last_names


def face_filter(img, age=25, race="white"):
    """Filter people by age and race using photo

    img - path to photo
    age - no younger than "age"
    race - only one race from ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']
    """
    try:
        obj = DeepFace.analyze(img_path=img, actions=["age", "race"])
        return (obj["age"] > age) and (obj["dominant_race"] == race)
    except Exception as _ex:
        return _ex


# print(face_verify("./media test/1516246784584.jfif"))


def main():

    filename = "test.csv"
    first_names, last_names = input_black_list()
    get_short_list(filename, first_names, last_names)


if __name__ == "__main__":
    main()

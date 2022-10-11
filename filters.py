from deepface import DeepFace


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
        return (obj["age"] > age), (obj["dominant_race"] in races), obj["dominant_race"]
    except Exception as _ex:
        try:
            download_img(img)
            obj = DeepFace.analyze("img.jpg", actions=["age", "race"])
            return (
                (obj["age"] > age),
                (obj["dominant_race"] in races),
                obj["dominant_race"],
            )
        except Exception as _ex2:
            return False, False, None

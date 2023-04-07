import json


def save_input(payload):

    json_str = {}
    name_value = payload.split('&')
    question_dictionary_started = False

    for json_object in name_value:
        name, value = json_object.split('=')

        # Creates new dictionary for list of questions
        if name.startswith("question") and not question_dictionary_started:
            json_str["question"] = {}
            question_dictionary_started = True

        if name.startswith("question"):
            question_number = (name.split("%5B")[1].split("%5D")[0])  # find question number within square brackets
            json_str["question"][question_number] = int(value)

        elif name.startswith("pets"):
            if "pets" not in json_str:
                json_str["pets"] = []
            json_str["pets"].append(value)
        else:
            json_str[name] = value

    with open('data\\input.json', 'w') as file:
        json.dump(json_str, file, indent=4, ensure_ascii=False)

    return


def create_profile():



    return

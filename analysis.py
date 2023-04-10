import json


input_data = {}


def save_input(payload):
    """ Parse the data from the form, convert to json, and save as 'input.json' """

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

        elif name.startswith("birthyear"):
            try:
                json_str[name] = int(value)
            # No value input
            except ValueError:
                json_str[name] = ''

        else:
            json_str[name] = value.replace('+', ' ')

    with open('data\\input.json', 'w') as file:
        json.dump(json_str, file, indent=4)

    global input_data
    input_data = json_str

    return


def create_profile():
    """ Analyze the data from 'input.json' and create a profile, save to 'profile.json' """
    with open('\\data\\input.json') as file:
        data = json.load(file)
        print(data)
    # print("@@@@@ DEBUG @@@@@\n" + input_data)
    #for k, v in input_data:
     #   print("key: " + k + ",     value: " + v)

    return

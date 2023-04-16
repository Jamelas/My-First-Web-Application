import json
import requests
from random import randint


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

    return


def create_profile():
    """ Analyze the data from 'input.json' and create a profile, save to 'profile.json' """

    file = open('data\\input.json')
    input_data = json.load(file)

    """ ========================================================================== """
    #

    """ Calculate psyc index score.
            At the moment this just takes the average value of the 20 valued questions.
            If time allows, give different values based on the question """
    psyc_index = 0
    for question in input_data["question"]:
        psyc_index += input_data["question"][question]
    psyc_index /= 20

    #
    """ ========================================================================== """
    #

    """ Calculate the suitability of chosen career """
    suitability = randint(1, 5)

    #
    """ ========================================================================== """
    #

    """ Movie API (based on desired job)"""
    movie_api = (requests.get("https://www.omdbapi.com/?apikey=5b76f7d0&t=" + input_data["job"])).json()

    #
    """ ========================================================================== """
    #

    """ Create the json object to store profile data """
    profile = {
        "psycho": {
            "psyc_index": psyc_index
        },
        "career": {
            "desired": input_data["job"],
            "suitability": suitability
        },
        "movies": {
            "title": movie_api["Title"],
            "year": movie_api["Year"],
            "runtime": movie_api["Runtime"],
            "genre": movie_api["Genre"],
            "director": movie_api["Director"],
            "actors": movie_api["Actors"],
            "rating": movie_api["imdbRating"],
        }
    }

    """ ========================================================================== """

    """ Begin the pet portion of the profile """
    # List of apis to retrieve random image
    dog_api = (requests.get('https://dog.ceo/api/breeds/image/random')).json()
    cat_api = (requests.get('https://api.thecatapi.com/v1/images/search')).json()
    duck_api = (requests.get('https://random-d.uk/api/v2/random')).json()

    pet_api = {
        "dog": dog_api["message"],
        "cat": cat_api[0]["url"],
        "duck": duck_api["url"]
    }

    # If a pet/s was chosen, add to the profile
    pet_chosen = False
    if "pets" in input_data:
        profile["pets"] = {}
        pet_chosen = True
    if pet_chosen:
        for pet in input_data["pets"]:
            profile["pets"][pet] = pet_api[pet]
            data = requests.get(pet_api[pet]).content
            f = open('data\\' + pet + '.jpg', 'wb')
            f.write(data)
            f.close()

    """ ========================================================================== """

    with open('data\\profile.json', 'w') as file:
        json.dump(profile, file, indent=4)
        
    return

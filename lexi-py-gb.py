import json
from difflib import get_close_matches
from difflib import SequenceMatcher

PROG_NAME = "lexi-py-gb: "
NO_MATCH = "\tWord not found.\n"

def load_lexicon():
    with open("data.json") as lexicon_data:
        return json.load(lexicon_data)

def lookup(word):
    ratio_for_lower = 0.0
    ratio_for_title = 0.0
    ratio_for_upper = 0.0
    closest_lower_match = get_close_matches(word.lower(), keys, 1)
    if closest_lower_match != []:
        ratio_for_lower = SequenceMatcher(None, closest_lower_match[0], word.lower()).ratio()
    closest_title_match = get_close_matches(word.title(), keys, 1)
    if closest_title_match != []:
        ratio_for_title = SequenceMatcher(None, closest_title_match[0], word.title()).ratio()
    closest_upper_match = get_close_matches(word.upper(), keys, 1)
    if closest_upper_match != []:
        ratio_for_upper = SequenceMatcher(None, closest_upper_match[0], word.upper()).ratio()
    best_ratio = max(ratio_for_lower, ratio_for_title, ratio_for_upper)
    if best_ratio == 0.0:
        return check([], word, None)
    elif best_ratio == ratio_for_lower:
        return check(lexicon.get(word.lower()), word.lower(), closest_lower_match[0])
    elif ratio_for_title == best_ratio:
        return check(lexicon.get(word.title()), word.title(), closest_title_match[0])
    else:
        return check(lexicon.get(word.upper()), word.upper(), closest_upper_match[0])       

def check(definitions, word, closest_match):
    if closest_match is None:
        return NO_MATCH
    elif word.lower() != closest_match.lower(): 
        return find_closest_key(word)
    else:
        print(definitions)
        return format(definitions)

def find_closest_key(word):
    closest_match = get_close_matches(word, keys, 1)
    if len(closest_match) > 0:
        yn = input(PROG_NAME + "Did you mean '%s' instead? (y/n): " % closest_match[0])
        if yn.lower() == "y":
            print(PROG_NAME + closest_match[0])
            return format(lexicon.get(closest_match[0]))
        elif yn.lower() == "n":
            return NO_MATCH
        else:
            return "\tInvalid command. Exiting.\n"

def format(definitions):
    formatted_defns = [ "\tDefn: " + defn + "\n" for defn in definitions ]
    return "".join(formatted_defns)

lexicon = load_lexicon()
keys = lexicon.keys()
word = input(PROG_NAME)
definitions = lookup(word)
print(definitions)
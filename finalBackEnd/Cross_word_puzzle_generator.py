import random
import json


# Reading Source Word DB file and converting and returning with Word Dictornary type.
def DBFileReading(file_path):
    # reading DB file with 'utf-8' encoding and storing in "data" variable.
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        data = file.readlines()

    word_dict = {}  # converting database entries to word dictonary.
    for word in data:
        k = word.split(',')
        word_dict[k[0]] = k[1].strip('\n')  # cleaning "\n"

    return word_dict


# Getting random words from Words Database, given how many random words required
def getPuzzleWords(word_count):
    words = list(word_data)
    # total_words_gird = random.randint(lower_word_limit,upper_word_limit)

    words = [random.choice(words).upper() for _ in range(word_count)]  # total_words_gird
    words_with_clues = {}
    for word in words:
        words_with_clues[word] = word_data[word]
    return words, words_with_clues


def print_gird():
    for x in range(gird_size):
        print('\t' * 5 + ' '.join(gird[x]))


def generateCrossWordGird(gird_size, words):
    global gird
    gird = [['0' for _ in range(gird_size)] for _ in range(gird_size)]
    gird_size = gird_size - 1
    orientations = ['leftright', 'updown', 'diagonalup', 'diagonaldown']
    for word in words:
        word_length = len(word)
        placed = False

        while not placed:
            orientation = random.choice(orientations)
            # print(orientation)
            if orientation == "leftright":
                step_x = 1
                step_y = 0
            if orientation == "updown":
                step_x = 0
                step_y = 1
            if orientation == "diagonaldown":
                step_x = 1
                step_y = 1
            if orientation == "diagonalup":
                step_x = 1
                step_y = -1

            x_position = random.randint(0, gird_size - 1)
            y_position = random.randint(0, gird_size - 1)

            ending_x = x_position + word_length * step_x
            ending_y = y_position + word_length * step_y

            if ending_x < 0 or ending_x >= gird_size: continue
            if ending_y < 0 or ending_y >= gird_size: continue

            failed = False

            for i in range(word_length):
                character = word[i]
                new_position_x = x_position + i * step_x
                new_position_y = y_position + i * step_y
                # print(new_position_x, new_position_y)
                character_at_new_position = gird[new_position_x][new_position_y]

                if character_at_new_position != "0":
                    if character_at_new_position == character:
                        continue
                    else:
                        failed = True
                        break

            if failed:
                continue
            else:
                for i in range(word_length):
                    character = word[i]
                    new_position_x = x_position + i * step_x
                    new_position_y = y_position + i * step_y
                    gird[new_position_x][new_position_y] = character

                placed = True


def hideWords():
    for gird_row in gird:
        indices = [i for i, x in enumerate(gird_row) if x.isalpha()]
        # blocking_index = random.sample(indices, random.randint(0,len(indices)))
        for i in indices:
            gird_row[i] = "1"



def dataConvertor():
    id = 0
    l = []
    for row in gird:
        d = {}
        i = 'row ' + str(id)
        d[i] = row
        l.append(d)
        id += 1
    return l


## ======================================================================== ##
# source Word DB file
file_path = "UK-DB.csv"
word_data = DBFileReading(file_path)

gird_size = 16
default_word_count = 15

words, words_with_clues = getPuzzleWords(default_word_count)
generateCrossWordGird(gird_size, words)
# print_gird()


gird_json_data = {}

gird_json_data['gird_with_answers'] = dataConvertor()
with open('gird_data.json', 'w', encoding='utf-8') as file:
    json.dump(gird_json_data, file, ensure_ascii=False, indent=4)

gird_json_data = {}
hideWords()
gird_json_data['hidden_words_in_gird'] = dataConvertor()
gird_json_data['words_with_clue'] = words_with_clues

with open('gird_data.json', 'a', encoding='utf-8') as file:
    json.dump(gird_json_data, file, ensure_ascii=False, indent=4)
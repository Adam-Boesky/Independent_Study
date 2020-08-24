import pickle
import sys
from nltk.corpus import stopwords
from numpy import *
from nlpApp import status_bar

# from translate.storage.tmx import tmxfile
def format_file(path_name):
    corpus_file = open(path_name, "r")
    corpus_text = corpus_file.read(-1)

    parallels = [[] for y in range(3)]
    alignment = ['' * 33334]

    counter = 1
    secondCounter = 0
    lines = corpus_text.split("\n")
    lang_1_lines = []
    lang_2_lines = []
    for i in range(len(lines)):
        if (counter) % 3 == 0:
            secondCounter = counter

        if counter - secondCounter == 0:
            lang_1_lines.append(lines[i])
        elif counter - secondCounter == 1:
            lang_2_lines.append(lines[i])
        elif counter - secondCounter == 2:
            alignment.append(lines[i])
        counter += 1

    # REMOVE ALL UNWANTED CHARACTERS:
    # Language 1:
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','ñ','é','í','á','ó','ú','\'',' ']
    for i in range(len(alignment)):
        replacement = ''
        for position in range(len(alignment[i])):
            is_letter = False
            for letter in alphabet:
                if alignment[i][position:position + 1] == letter:
                    is_letter = True
            if is_letter:
                replacement = replacement + alignment[i][position:position + 1]
        alignment[i] = replacement

    # Language 2:
    for i in range(len(lang_2_lines)):
        replacement = ''
        for position in range(len(lang_2_lines[i])):
            is_letter = False
            for letter in alphabet:
                if lang_2_lines[i][position:position + 1] == letter:
                    is_letter = True
            if is_letter:
                replacement = replacement + lang_2_lines[i][position:position + 1]
        lang_2_lines[i] = replacement

    # Put lines into the parallels array:
    # Alignments:
    for i in range(len(lang_1_lines)):
        parallels[2].append(lang_1_lines[i])

    # Language 2:
    for i in range(len(lang_2_lines)):
        parallels[1].append(lang_2_lines[i])

    # Language 1:
    for i in range(len(alignment)):
        parallels[0].append(alignment[i])


    # # TRANSFER LINES OF LANGS TO INDIVIDUAL WORDS:
    # for i in range(len(lang_1_lines)):
    #     # Alignments:
    #     words_lang_1 = lang_1_lines[i].split(" ")
    #     for j in range(len(words_lang_1)):
    #         parallels[2].append(words_lang_1[j])
    #
    #     # Language 2:
    #     words_lang_2 = lang_2_lines[i].split(" ")
    #     for j in range(len(words_lang_2)):
    #         parallels[1].append(words_lang_2[j])
    #
    #     # Language 1:
    #     alignment_individuals = alignment[i].split(" ")
    #     for j in range(len(alignment_individuals)):
    #         parallels[0].append(alignment_individuals[j])
    #
    # if path_name == '/Users/student/PycharmProjects/IndependentStudy/Corpora/alignment-en-fr.txt':
    #     parallels[0].pop(0)
    #
    # # REMOVE ALL EMPTY STRINGS:
    # adjuster = 0
    # for i in range(len(parallels[0])):
    #     if parallels[0][i - adjuster] == '':
    #         parallels[0].pop(i - adjuster)
    #         adjuster += 1
    #
    # adjuster = 0
    # for i in range(len(parallels[1])):
    #     if parallels[1][i - adjuster] == '':
    #         parallels[1].pop(i - adjuster)
    #         adjuster += 1

    # Make everything lowercase:
    for i in range(2):
        for j in range(len(parallels[i])):
            parallels[i][j] = parallels[i][j].lower()
    print(parallels[0])
    print(parallels[1])
    print(parallels[2])

    parallels_file = open(path_name[len(path_name) - 9:len(path_name) - 4], 'ab')
    pickle.dump(parallels, parallels_file)
    parallels_file.close()


def get_all_words(file_name):
    parallel_file = open(file_name, 'rb')
    parallels = pickle.load(parallel_file)
    words = [[] for y in range(3)]

    # TRANSFER LINES OF LANGS TO INDIVIDUAL WORDS:
    for i in range(len(parallels[2])):
        # Alignments:
        words_lang_1 = parallels[2][i].split(" ")
        for j in range(len(words_lang_1)):
            words[2].append(words_lang_1[j])

        # Language 2:
        words_lang_2 = parallels[1][i].split(" ")
        for j in range(len(words_lang_2)):
            words[1].append(words_lang_2[j])

        # Language 1:
        alignment_individuals = parallels[0][i].split(" ")
        for j in range(len(alignment_individuals)):
            words[0].append(alignment_individuals[j])

    print(words[0])
    print(words[1])
    print(words[2])

    en_stop_words = set(stopwords.words('english'))
    fr_stop_words = set(stopwords.words('french'))
    de_stop_words = set(stopwords.words('german'))

    adjuster = 0
    # Get rid of stop words:
    for i in range(2):
        for j in range(len(words[i])):
            status_bar("Hello:", len(words[i]), j)
            if words[i][j - adjuster] in fr_stop_words or words[i][j - adjuster] in en_stop_words or words[i][j - adjuster] in de_stop_words:
                words[i].pop(j - adjuster)
                adjuster += 1

    # REMOVE ALL EMPTY STRINGS:
    adjuster = 0
    for i in range(len(words[0])):
        if words[0][i - adjuster] == '':
            words[0].pop(i - adjuster)
            adjuster += 1

    adjuster = 0
    for i in range(len(words[1])):
        if words[1][i - adjuster] == '':
            words[1].pop(i - adjuster)
            adjuster += 1

    word_file = open(file_name + '_words', 'ab')
    pickle.dump(words, word_file)
    word_file.close()


def translate_all(parallel_file_name, word_file_name):
    parallel_file = open(parallel_file_name, 'rb')
    fr_stop_words = set(stopwords.words('french'))
    de_stop_words = set(stopwords.words('german'))
    parallels = pickle.load(parallel_file)
    word_file = open(word_file_name, 'rb')
    words = pickle.load(word_file)

    # Translate all of the words in the word file:
    for i in range(len(words[0])):
        if words[0][i] != '' and words[0][i] != ' ' and words[0][i] != 'l\'' and words[0][i] != 'd\'' and words[0][i] != 'c\'' and words[0][i] not in fr_stop_words and words[0][i] not in de_stop_words:
            translate(words[0][i], parallel_file_name)

    parallel_file.close()
    word_file.close()


def number_translate_section(section_size, file_name):
    for i in range(section_size):
        number_translate(file_name, i, 2)


def comparitive_translator(file_name):
    numerator = 0
    denominator = 0
    parallels_file = open(file_name, 'rb')
    parallels = pickle.load(parallels_file)
    parallels[0].pop(0)  # This is an adjuster because the first string of the de-en parallel was empty

    # Stop word files:
    fr_stop_words = set(stopwords.words('french'))
    de_stop_words = set(stopwords.words('german'))
    en_stop_words = set(stopwords.words('english'))
    punctuation = ['\'', '.', ',', '/', ' ', '-', '?', '!', '']

    # TRANSLATE ALL LINES:
    translating = True
    line_number = 0
    used_words = []
    while translating:

        # Get each of the sections' words:
        lang_1_words = parallels[0][line_number].split(' ')
        lang_2_words = parallels[1][line_number].split(' ')
        number_translations = parallels[2][line_number].split(' ')
        word_number_translations = []

        # Translate the words using both methods:
        for j in range(len(lang_1_words)):
            for i in range(len(number_translations)):
                temp_numbers = number_translations[i].split('-')
                if int(temp_numbers[1]) == j:
                    word_number_translations.append(number_translations[j])

            if word_number_translations != []: # Make sure that there is a translation given
                temp_numbers = word_number_translations[0].split('-')
                translation_word = lang_1_words[int(temp_numbers[1])]  # Get the word that is being translated

                # Translate with both methods:
                if translation_word not in de_stop_words and translation_word not in fr_stop_words and translation_word not in en_stop_words and translation_word not in used_words and translation_word not in punctuation and not translation_word.isnumeric():
                    my_translation = comparative_translate(translation_word, file_name)
                    number_translation = comparative_number_translate(lang_2_words, word_number_translations)
                    denominator += 1
                    if my_translation == number_translation:
                        numerator += 1
                    print("Translation of \'", translation_word, "\':\n", "Me: ", my_translation, "\nActual: ", number_translation, "\nCurrent Accuracy = ", (numerator/denominator) * 100, "%\n \n")
                word_number_translations.clear()
                used_words.append(translation_word)

        line_number += 1


def comparative_number_translate(lang_2_words, word_number_translations):
    translation_string = ''
    for i in range(len(word_number_translations)):  # Tie all of the translation words together
        translation_string = translation_string + lang_2_words[int(word_number_translations[i][0:1])]

    return translation_string

def number_translate(file_name, line_number, word_number):
    parallels_file = open(file_name, 'rb')
    parallels = pickle.load(parallels_file)
    parallels[0].pop(0)  # This is an adjuster because the first string of the de-en parallel was empty

    lang_1_words = parallels[0][line_number].split(' ')
    lang_2_words = parallels[1][line_number].split(' ')
    print("lang 1", lang_1_words)
    print("lang 2", lang_2_words)
    number_translations = parallels[2][line_number].split(' ')
    word_number_translations = []
    print(number_translations)

    for i in range(len(number_translations)):
        if int(number_translations[i][2:3]) == word_number:
            word_number_translations.append(number_translations[i])

    translation_word = lang_1_words[int(word_number_translations[0][2:3])]  # Get the word that is being translated

    translation_string = ''
    for i in range(len(word_number_translations)):  # Tie all of the translation words together
        translation_string = translation_string + lang_2_words[int(word_number_translations[i][0:1])]

    print('\'', translation_word, '\'', 'best translation is', translation_string)


def comparative_translate(word, file_name):
    parallels_file = open(file_name, 'rb')
    parallels = pickle.load(parallels_file)

    place = 0
    translation_word = word
    places = []

    # Find all of the sentences with the word in it:
    counter = 0
    for spanish_parallel in parallels[0]:
        counter = counter + 1
        if " " + translation_word + " " in spanish_parallel:
            places.append(place)
        place = place + 1

    # Find the frequency of all of the words in the sentences containing the word of interest:
    counter = 0
    frequency = []
    fr_stop_words = set(stopwords.words('french'))
    de_stop_words = set(stopwords.words('german'))
    de_stop_words.add('fr')

    for i in range(len(places)):
        words = parallels[1][places[counter]].split(" ")
        for k in range(len(words)):
            already_counting = False
            for j in range(len(frequency)):
                if frequency[j][0] == words[k]:
                    location_in_frequency = j
                    already_counting = True
            if already_counting:
                frequency[location_in_frequency][1] = frequency[location_in_frequency][1] + 1
            elif words[k] not in de_stop_words and words[
                k] not in fr_stop_words:  # Making sure that it is not a stop word too
                frequency.append([words[k], 1])
        counter = counter + 1

    # Set the number of appearances for stop words equal to zero:
    stop_words = set(stopwords.words('english'))
    for i in range(len(frequency)):
        if frequency[i][0] in stop_words:
            frequency[i][1] = 0
        if frequency[i][0] == '':
            frequency[i][1] = 0

    best = 0
    for i in range(len(frequency)):
        if frequency[best][1] <= frequency[i][1]:
            best = i
    return frequency[best][0]


def translate(word, file_name):
    parallels_file = open(file_name, 'rb')
    parallels = pickle.load(parallels_file)

    place = 0
    translation_word = word
    print("Now translating: ", translation_word)
    places = []

    # Find all of the sentences with the word in it:
    counter = 0
    for spanish_parallel in parallels[0]:
        counter = counter + 1
        if " " + translation_word + " " in spanish_parallel:
            places.append(place)
        place = place + 1

    # Find the frequency of all of the words in the sentences containing the word of interest:
    counter = 0
    frequency = []
    fr_stop_words = set(stopwords.words('french'))
    de_stop_words = set(stopwords.words('german'))

    for i in range(len(places)):
        words = parallels[1][places[counter]].split(" ")
        for k in range(len(words)):
            already_counting = False
            for j in range(len(frequency)):
                if frequency[j][0] == words[k]:
                    location_in_frequency = j
                    already_counting = True
            if already_counting:
                frequency[location_in_frequency][1] = frequency[location_in_frequency][1] + 1
            elif words[k] not in de_stop_words and words[k] not in fr_stop_words: # Making sure that it is not a stop word too
                frequency.append([words[k], 1])
        counter = counter + 1

    # Set the number of appearances for stop words equal to zero:
    stop_words = set(stopwords.words('english'))
    for i in range(len(frequency)):
        if frequency[i][0] in stop_words:
            frequency[i][1] = 0
        if frequency[i][0] == '':
            frequency[i][1] = 0

    print(translation_word, "best translation:")
    best = 0
    for i in range(len(frequency)):
        if frequency[best][1] <= frequency[i][1]:
            best = i
    print(frequency[best][0])

    # Check if the best also has the translation word as its best translation:
    second_frequency = []
    counter = 0

    for i in range(len(places)):
        words = parallels[1][places[counter]].split(" ")
        for k in range(len(words)):
            already_counting = False
            for j in range(len(second_frequency)):
                if second_frequency[j][0] == words[k]:
                    location_in_frequency = j
                    already_counting = True
            if already_counting:
                second_frequency[location_in_frequency][1] = second_frequency[location_in_frequency][1] + 1
            else:
                second_frequency.append([words[k], 1])
        counter = counter + 1


def main():
    # format_file('/Users/student/PycharmProjects/IndependentStudy/Corpora/alignment-en-fr.txt')
    # get_all_words('en-fr')
    # format_file('/Users/student/PycharmProjects/IndependentStudy/Corpora/alignment-de-en.txt')
    # get_all_words('de-en')
    # translate_all('de-en', 'de-en_words')
    # translate_all('en-fr', 'en-fr_words'
    # number_translate('de-en', 0, 2)
    comparitive_translator('de-en')



if __name__ == '__main__':
    main()


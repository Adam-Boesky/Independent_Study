import pickle
import sys
from nltk.corpus import stopwords
from numpy import *


# from translate.storage.tmx import tmxfile
def format_file():
    corpus_file = open("/Users/student/PycharmProjects/IndependentStudy/enEs.txt", "r")
    corpus_text = corpus_file.read(-1)

    parallels = [["" for x in range(21007)] for y in range(2)]

    for i in range(21007):
        # Take the english data:
        parallels[0][i] = corpus_text[5:corpus_text.find("</seg>")]
        corpus_text = corpus_text[corpus_text.find("</seg>") + 6:]
        # Take the spanish data:
        parallels[1][i] = corpus_text[5:corpus_text.find("</seg>")]
        corpus_text = corpus_text[corpus_text.find("</seg>") + 6:]

    # REMOVE ALL NON-LETTERS FROM THE SENTENCES:
    # English:
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ','ñ','é','í','á','ó','ú']
    for i in range(len(parallels[0])):
        replacement = ''
        for position in range(len(parallels[0][i])):
            is_letter = False
            for letter in alphabet:
                if parallels[0][i][position:position + 1] == letter:
                    is_letter = True
            if is_letter:
                replacement = replacement + parallels[0][i][position:position + 1]
            elif parallels[0][i][position:position + 5] == '&quot':
                position = position + 5
        parallels[0][i] = replacement

    # Spanish:
    for i in range(len(parallels[1])):
        replacement = ''
        for position in range(len(parallels[1][i])):
            is_letter = False
            for letter in alphabet:
                if parallels[1][i][position:position + 1] == letter:
                    is_letter = True
            if is_letter:
                replacement = replacement + parallels[1][i][position:position + 1]
        parallels[1][i] = replacement

    # Make everything lowercase:
    for i in range(2):
        for j in range(len(parallels[i])):
            parallels[i][j] = parallels[i][j].lower()

    parallels_file = open('parallelFile', 'ab')
    pickle.dump(parallels, parallels_file)
    parallels_file.close()


def translate_all():
    word_file = open('wordFile', 'rb')
    words = pickle.load(word_file)

    # Translate all of the words in the word file:
    for i in range(len(words)):
        if words[i] != '' and words[i] != ' ':
            translate(words[i])
    word_file.close()


def status_bar(bar_name, final, progress):
    if progress == 0:
        print(bar_name)
    period_number = math.floor((progress/final) * 50)
    periods = '.' * period_number
    spaces = ' ' * (50 - period_number)
    print('|', periods, spaces, '|')


def get_all_words(file_name):
    parallels_file = open(file_name, 'rb')
    parallels = pickle.load(parallels_file)
    spanish_stop_words = set(stopwords.words('spanish'))
    english_stop_words = set(stopwords.words('english'))
    words = []

    # Add all of the words in the file to an array making sure that none of them are stop words:
    for i in range(len(parallels[1])):
        status_bar("Spanish Stop Words", len(parallels[1]) - 1, i)
        sentence_words = parallels[1][i].split(" ")
        for j in range(len(sentence_words)):
            if sentence_words[j] not in words and sentence_words[j] not in spanish_stop_words and sentence_words[j] not\
                    in english_stop_words:
                words.append(sentence_words[j])

    parallels_file.close()
    word_file = open('wordFile', 'ab')
    pickle.dump(words, word_file)
    word_file.close()


def translate(word):
    print("\n")
    parallels_file = open('parallelFile', 'rb')
    parallels = pickle.load(parallels_file)

    place = 0
    translation_word = word
    print("Now translating: ", translation_word)
    places = []

    # Find all of the sentences with the word in it:
    counter = 0
    for spanish_parallel in parallels[1]:
        counter = counter + 1
        if " " + translation_word + " " in spanish_parallel:
            places.append(place)
        place = place + 1

    # Find the frequency of all of the words in the sentences containing the word of interest:
    counter = 0
    frequency = []

    for i in range(len(places)):
        words = parallels[0][places[counter]].split(" ")
        for k in range(len(words)):
            already_counting = False
            for j in range(len(frequency)):
                if frequency[j][0] == words[k]:
                    location_in_frequency = j
                    already_counting = True
            if already_counting:
                frequency[location_in_frequency][1] = frequency[location_in_frequency][1] + 1
            else:
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

    # Set the number of stop words equal to zero
    spanish_stop_words = set(stopwords.words('spanish'))
    for i in range(len(second_frequency)):
        if second_frequency[i][0] in spanish_stop_words:
            second_frequency[i][1] = 0
        if second_frequency[i][0] == '':
            second_frequency[i][1] = 0


    second_best = 0
    for i in range(len(second_frequency)):
        if second_frequency[second_best][1] < second_frequency[i][1]:
            second_best = i
    if second_frequency[second_best][0] == translation_word:
        print("The converse translation also works")
    else:
        print("The converse translation does not work")

    parallels_file.close()


def main():
    format_file()
    get_all_words('parallelFile')
    translate_all()


if __name__ == '__main__':
    main()



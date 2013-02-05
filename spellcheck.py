#!/usr/bin/env python
from optparse import OptionParser
import re, signal, sys
from utils import load_file_and_index, signal_handler, get_first_letter_of, get_last_letter_of, VOWELS

# VOWELS = ["a", "e", "i", "o", "u", "y"]

def signal_handler(signal, frame):
        print 'Goodbye!'
        sys.exit(0)

def correct_case(word) :
    return word.lower()

def word_count(word_list):
    words = {}
    for word in word_list :
        if word not in words :
            words[word] = {"count" : 0, "length" : len(word)} 
        words[word]["count"] += 1
    return words.items()

def compress_word(word):
    word = correct_case(word)
    compressed = [word[0]]
    for i in range(len(word)) :
        if not compressed[-1:][0] ==word[i] :
            compressed.append(word[i])
    return compressed

def generate_regex_to_correct_repeating_letters(word):
    word = correct_case(word)
    compressed_word = compress_word(word)
    regex = r"^"
    for letter in compressed_word :
        # regex = 
        regex += r"({}+)".format(letter)
    regex = regex + r"$"
    return regex

def generate_regex_to_correct_vowels(word):
    word = correct_case(word)
    compressed_word = compress_word(word)
    regex = r"^"
    for letter in word :
        if letter in VOWELS : 
            regex += r"([aeiouy]+)"
        else :
            regex += r"({}+?)".format(letter)
    regex = regex + r"$"
    return regex

def generate_regex_to_correct_both_vowels_and_repeating_letters(word):
    word = correct_case(word)
    compressed_word = compress_word(word)
    regex = r"^"
    for letter in compressed_word :
        if letter in VOWELS : 
            regex += r"([aeiouy]+)"
        else :
            regex += r"({}+?)".format(letter)
    regex = regex + r"$"
    return regex

def spellcheck_suggestions_for_repeating_letters(word, fl_index):
    repeating_letters_regex = generate_regex_to_correct_repeating_letters
    key = get_first_letter_of(word) + get_last_letter_of(word)
    return [i for i in fl_index[key] if re.match(repeating_letters_regex(word), i)]

def spellcheck_suggestions_for_vowels(word, fl_index):
    vowels_regex = generate_regex_to_correct_vowels
    key = get_first_letter_of(word) + get_last_letter_of(word)
    return [i for i in fl_index[key] if re.match(vowels_regex(word), i)]

def spellcheck_suggestions_for_repeating_and_vowels(word, fl_index):
    repeating_and_vowels_regex = generate_regex_to_correct_both_vowels_and_repeating_letters(word)
    key = get_first_letter_of(word) + get_last_letter_of(word)
    return [i for i in fl_index[key] if re.match(repeating_and_vowels_regex, i)]

def get_spellcheck_from_all_spellcheckers_for(word, fl_index):
    word = correct_case(word)
    key = get_first_letter_of(word) + get_last_letter_of(word) 
    repeating_checker = spellcheck_suggestions_for_repeating_letters(word, fl_index)
    vowels_checker = spellcheck_suggestions_for_vowels(word, fl_index)
    combined_checker = spellcheck_suggestions_for_repeating_and_vowels(word, fl_index)
    all_results = []
    map(lambda x : all_results.extend(x), [repeating_checker, vowels_checker, combined_checker])
    return all_results


def recommend_correction(word, fl_index):
    if word :
        suggested_corrections = get_spellcheck_from_all_spellcheckers_for(word, fl_index)
        if suggested_corrections :
            counted_words = word_count(suggested_corrections)
            counted_words.sort(key=lambda x : x[1], reverse=True)
            counted_words = sorted(counted_words, key=lambda d: (-d[1]["count"], -d[1]["length"], d[0] ))
            return counted_words[0][0]
    return  "NO SUGGESTION" 

if __name__ == "__main__":
    print "at the prompt enter the word you want spelledchecked.  Ctrl+C to exit."
    signal.signal(signal.SIGINT, signal_handler)
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="location of a file with english words", metavar="FILE", default="/usr/share/dict/words")
    ###    
    (options, args) = parser.parse_args()
    # parse file 
    raw_data = []
    inverted_index = {}
    filename = options.filename
    inverted_index = load_file_and_index(filename)
    while True :
        try :
            word = raw_input("> ")
            print recommend_correction(word, inverted_index)
        except EOFError:
            sys.exit(0)







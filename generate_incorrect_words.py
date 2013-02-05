#!/usr/bin/env python
# AND 
# Final step: Write a second program that *generates* words with spelling mistakes of the above form
# , starting with correctly spelled English words. Pipe its output into the first program 
# and verify that there are no occurrences of "NO SUGGESTION" in the output.
#!/usr/bin/env python
from optparse import OptionParser
import signal, sys
from utils import signal_handler, load_file_and_index, VOWELS, \
    get_last_letter_of, get_first_letter_of
import random
from subprocess import Popen, PIPE, STDOUT

def choose_word_from_index(index):
    index_as_list = index.items()
    row = random.randrange(len( index_as_list ))
    column = random.randrange(len( index_as_list[row][1] ))
    return index_as_list[row][1][column]

def multiply_letter(letter): 
    by_factor_of = random.randrange(1,3)
    return letter*by_factor_of

def substitute_vowel(letter): 
    if letter in VOWELS :
        vowels_copy = VOWELS[:]
        # remove current letter
        letter_position = vowels_copy.index(letter)
        vowels_copy.pop(letter_position)
        # return random substitute
        chosen_one = random.randrange(len( vowels_copy ))
        return vowels_copy[chosen_one]
    return letter

def multiply_letter_upper(letter): 
    return multiply_letter(letter).upper()

def substitute_vowel_upper(letter): 
    return substitute_vowel(letter).upper()

def upper_case_letter(letter):
    return letter.upper()

def leave_unchanged(letter):
    return letter

def apply_random_transformation(letter, func_list):
    chosen_one = random.randrange(len(func_list))
    transformation = func_list[chosen_one]
    return transformation(letter)

def generate_errors_in_word(word):
    # take word from list
    # for each letter randomly double or tripple the letter, upper case it, or if a vowel swap for another random vowel
    transformations_for_ends = [
        upper_case_letter, 
        multiply_letter, 
        multiply_letter_upper, 
        leave_unchanged]
    all_transformations = [
        upper_case_letter, 
        multiply_letter, 
        substitute_vowel, 
        substitute_vowel_upper, 
        multiply_letter_upper]
    word_length = len(word)
    if word_length > 2 :
        
        new_word_letters = [
            apply_random_transformation(get_first_letter_of(word), transformations_for_ends),
            apply_random_transformation(get_last_letter_of(word), transformations_for_ends)
        ] 
        for letter in word[1:word_length-1]:
            new_letter = apply_random_transformation(letter, all_transformations)
            new_word_letters.insert(-1, new_letter)
        return "".join(new_word_letters)
    return "".join([apply_random_transformation(letter, transformations_for_ends) for letter in word])



def pipe_in_spell_check(word):
    # pipe word into spell check
    # look at output make sure it is not "NO SUGGESTION"
    pass

def main(args):
    # generate X words
    # pipe each word in spell check and check 
    pass

if __name__ == "__main__":
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
    random_word = choose_word_from_index(inverted_index)
    child = Popen(["./spellcheck.py"], stdin=PIPE, stdout=PIPE,stderr=PIPE)
    cmd = "{}".format(generate_errors_in_word(random_word))
    print "input word : ", cmd
    output = child.communicate(cmd)
    result = output[0].split("\n")[1]
    if "NO SUGGESTION" not in result :
        print "result : ", result.replace("> ", "")
    else :
        print "Failed to generate result"
    
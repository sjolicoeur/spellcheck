import signal, sys

VOWELS = ["a", "e", "i", "o", "u", "y"]


def signal_handler(signal, frame):
    print 'Goodbye!'
    sys.exit(0)

def get_first_letter_of(word):
    return word[0]

def get_last_letter_of(word):
    return word[-1:][0]

def generate_index_by_first_and_last_letter(data):
    fl_index = {}
    for word in data :
        word = word.lower()
        key = get_first_letter_of(word) + get_last_letter_of(word) # do a first and a last func
        if key not in fl_index :
            fl_index[key] = []
        fl_index[key].append(word)
    return fl_index

def load_file_and_index(filename):
    raw_data = []
    inverted_index = {}
    try :
        with open(filename, 'r') as f:
            raw_data = [line.split("\n")[0] for line in f.readlines()]
            inverted_index = generate_index_by_first_and_last_letter(raw_data)
            return inverted_index
    except IOError :
        print "Error while opening the file... Check location or permissions"
        sys.exit(0)
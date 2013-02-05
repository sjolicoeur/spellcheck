import random
import unittest
from spellcheck import compress_word, spellcheck_suggestions_for_repeating_letters , \
     spellcheck_suggestions_for_vowels, spellcheck_suggestions_for_vowels, \
     spellcheck_suggestions_for_repeating_and_vowels, get_spellcheck_from_all_spellcheckers_for, \
     recommend_correction
from mocks import MOCK_INDEX


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        #self.seq = range(10)
        self.fl_index = MOCK_INDEX

    def test_remove_letter_that_repeat_no_matter_the_case(self):
        # removes letter that are repeat in a row
        test_words_and_expected_results = [ 
            ("jjjjooobbb", ["j", "o", "b"]), 
            ("JjJooBBB", ["j", "o", "b"]), 
            ("jkjjoooukoobb",["j", "k", "j", "o", "u", "k", "o", "b"])]
        for word, expected in test_words_and_expected_results :
            result = compress_word(word)
            assert result == expected, "expected {} got {}".format(expected, result)

    def test_get_suggestion_for_repeating_letters(self):
        suggestions = spellcheck_suggestions_for_repeating_letters("jooob", self.fl_index)
        expected_output = ['job', 'job']
        #assert len(suggestions) == len(expected_output), "suggestion is not of the same length as the expected output"
        assert suggestions == expected_output
        expected_output = []
        suggestions = spellcheck_suggestions_for_repeating_letters("peeple", self.fl_index)
        assert suggestions == expected_output

    def test_get_suggestion_for_vowels(self):
        suggestions = spellcheck_suggestions_for_vowels("job", self.fl_index)
        expected_output = ['jab', 'jaob', 'jib', 'job', 'job']
        #assert len(suggestions) == len(expected_output), "suggestion is not of the same length as the expected output"
        assert suggestions == expected_output
        suggestions = spellcheck_suggestions_for_vowels("peeple", self.fl_index)
        expected_output = ['people']
        #assert len(suggestions) == len(expected_output), "suggestion is not of the same length as the expected output"
        assert suggestions == expected_output
        
    def test_get_suggestion_for_vowels_and_repeating_letters(self):
        suggestions = spellcheck_suggestions_for_repeating_and_vowels("job", self.fl_index)
        expected_output = ['jab', 'jaob', 'jib', 'job', 'job']
        #assert len(suggestions) == len(expected_output), "suggestion is not of the same length as the expected output"
        assert suggestions == expected_output
        suggestions = spellcheck_suggestions_for_repeating_and_vowels("peeple", self.fl_index)
        expected_output = ['people']
        #assert len(suggestions) == len(expected_output), "suggestion is not of the same length as the expected output"
        assert suggestions == expected_output

    def test_get_suggestion_from_all_spellcheckers(self):
        suggestions = get_spellcheck_from_all_spellcheckers_for("jjjooobbb", self.fl_index)
        expected_output = ['job', 'job', 'jab', 'jaob', 'jib', 'job', 'job']
        #assert len(suggestions) == len(expected_output), "suggestion is not of the same length as the expected output"
        assert suggestions == expected_output
        suggestions = get_spellcheck_from_all_spellcheckers_for("peeple", self.fl_index)
        expected_output = ['people', 'people']
        #assert len(suggestions) == len(expected_output), "suggestion is not of the same length as the expected output"
        assert suggestions == expected_output

    def test_on_erroneous_input_make_no_recommendation(self):
        expected_output = "NO SUGGESTION"
        input_string = "" 
        output = recommend_correction(input_string, self.fl_index)
        assert output == expected_output, output
        input_string = "sheeple"
        output = recommend_correction(input_string, self.fl_index)
        assert output == expected_output, output

    def test_expect_people(self) :
        assert recommend_correction("peeple", self.fl_index) == 'people'

    def test_expect_sheep(self) :
        assert recommend_correction("sheeep", self.fl_index) == 'sheep'

    def test_expect_wake(self) :   
        assert recommend_correction("weke", self.fl_index) == 'wake'

    def test_expect_conspiracy(self) :
        assert recommend_correction("CUNsperrICY", self.fl_index) == 'conspiracy'

    def test_expect_sheeppen(self) :
        assert recommend_correction("sheeppan", self.fl_index) == 'sheeppen'


if __name__ == '__main__':
    unittest.main()

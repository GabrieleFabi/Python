import countWords

def test_one():
    assert countWords.count_word_occurrence_in_string("AAA BBB", "AAA") == 1
    
def test_two():
    assert countWords.count_word_occurrence_in_string("AAA AAA", "AAA") == 1
    
def test_three():
    assert countWords.count_word_occurrence_in_string("AAA AAA", "AAA") == 2
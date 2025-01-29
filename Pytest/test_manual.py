def odd(n):
    if n % 2 == 0:
        return False
    else:
        return True
    
def test_answer():
    assert odd(14) == True
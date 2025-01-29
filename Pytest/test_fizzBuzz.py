def fizzbuzz(number):
    if not isinstance(number, int):
        raise TypeError
    if number < 1:
        raise ValueError
    elif number % 15 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return number
    
def test_one():
    assert fizzbuzz(15) == "FizzBuzz"

def test_two():
    assert fizzbuzz(5) == "Buzz"

def test_three():
    assert fizzbuzz(11) == "FizzBuzz"
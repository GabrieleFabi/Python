import alligator
import crocodile

def test_safe_to_grab_alligator():
    assert alligator.safe_to_grab(0.5) == True

def test_unsafe_to_grab_alligator():
    assert alligator.safe_to_grab(1.5) == False

def test_unsafe_to_grab_crocodile():
    assert crocodile.safe_to_grab(0.5) == False

def test_unsafe_to_grab_crocodile_2():
    assert crocodile.safe_to_grab(0.1) == True
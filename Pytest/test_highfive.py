import highfive

def test_one():
    assert highfive.is_highfive(105)

def test_two():
    assert not highfive.is_highfive(100)

def test_three():
    assert not highfive.is_highfive(106) 
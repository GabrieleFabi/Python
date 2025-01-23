import pytest


def expensive_computation():
    print("running expensive computation...")


@pytest.fixture
def mydata(pytestconfig):
    val = pytestconfig.cache.get("example/value", None)
    if val is None:
        expensive_computation()
        val = 42
        pytestconfig.cache.set("example/value", val)
    return val


def test_function(mydata):
    assert mydata == 23
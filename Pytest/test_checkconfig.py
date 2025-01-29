import pytest


def checkconfig(x):
    __tracebackhide__ = True
    if not hasattr(x, "config"):
        pytest.fail(f"not configured: {x}")


def test_something():
    checkconfig(42)
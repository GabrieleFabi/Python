import unittest

import pytest


class MyTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initdir(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)  # change to pytest-provided temporary directory
        tmp_path.joinpath("samplefile.ini").write_text("# testdata", encoding="utf-8")

    def test_method(self):
        with open("samplefile.ini", encoding="utf-8") as f:
            s = f.read()
        assert "testdata" in s
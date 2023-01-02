import pytest


def f():
    raise SystemExit(1)


class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")

    def test_mytest(self):
        with pytest.raises(SystemExit):
            f()

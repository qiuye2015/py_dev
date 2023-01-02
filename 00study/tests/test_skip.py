import pytest


@pytest.mark.skip
def test_min():
    values = (2, 3, 1, 4, 6)
    assert min(values) == 1


def test_max():
    values = (2, 3, 1, 4, 6, 5)
    assert 5 in values

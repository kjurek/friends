import pytest
from src.app import dummy

def test_dummy():
    assert dummy() == True
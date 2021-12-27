try:
    import config
except ImportError:
    # assume remote server enters the application in test_str_concat/, home would be test_str_concat/..
    import sys
    import os

    test_dir = os.path.dirname(__file__)
    home = os.path.join(test_dir, os.path.pardir)

    sys.path.append(home)
    sys.path.append(os.path.join(home, "src"))
else:
    config.add_src_to_path()

import pytest

from flynt import state


@pytest.fixture(autouse=True)
def reset_state():
    """
    Fixture to reset the global state between each test
    """
    state._reset()


@pytest.fixture()
def aggressive(monkeypatch):
    monkeypatch.setattr(state, "aggressive", True)
    yield

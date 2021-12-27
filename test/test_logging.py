import pytest

from flynt.transform.FstringifyTransformer import fstringify_node
from flynt.transform.transform import transform_chunk


@pytest.mark.parametrize(
    "s",
    (
        "logging.info('foo')",
        "logging.info('foo', 'bar')",
        "logging.info('foo %s')",
        "logging.info('foo %s', *vars)",
        "logging.addLevelName('foo %s', var)",
    ),
)
def test_noop_logging_calls(s, aggressive):
    new, changed = transform_chunk(s)
    assert not changed
    assert new == s


@pytest.mark.parametrize(
    ("s", "expected"),
    (
        ("logging.info('foo %s', var)", "logging.info(f'foo {var}')"),
        ("logging.info('foo %s %s', var1, var2)", "logging.info(f'foo {var1} {var2}')"),
        ("logging.info('foo %d', var)", "logging.info(f'foo {int(var)}')"),
    ),
)
def test_format_string_logging_calls(s, expected, aggressive):
    new, changed = transform_chunk(s)
    assert changed
    assert new == expected


def test_format_string_logging_call_not_aggressive():
    code = "logging.info('foo %s', var)"
    new, changed = transform_chunk(code)
    assert not changed
    assert new == code

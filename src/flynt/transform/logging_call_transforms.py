import ast

from flynt.transform.percent_transformer import _transform_tuple

# TODO: support log(), which takes an extra initial positional arg
FUNCTIONS = ('debug', 'info', 'warning', 'error', 'critical', 'exception')


def matching_call(node) -> bool:
    """
    Check if an ast Node is a logging call with more than one positional arg.
    """
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == 'logging'
        # TODO: Logger objects
        # and isinstance(node.func.value.ctx, ast.Load)
        # and [is it a Logger? is that impossible with ast alone?)
        and node.func.attr in FUNCTIONS
        and len(node.args) > 1
    )


def joined_args(fmt_call: ast.Call) -> ast.Call:
    """ Transform a %-format logging call into an f-string call."""

    assert len(fmt_call.args) > 1
    fmt_call.args = [_transform_tuple(fmt_call.args[0].value, fmt_call.args[1:])]
    return fmt_call

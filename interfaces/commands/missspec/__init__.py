from .capture import register_capture_command


def register_commands(tree):
    register_capture_command(tree)

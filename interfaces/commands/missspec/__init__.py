from .capture import register_capture_command
from .list_message import register_list_message_command


def register_commands(tree):
    register_capture_command(tree)
    register_list_message_command(tree)

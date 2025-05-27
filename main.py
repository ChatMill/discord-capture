# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Entry point for the discord-capture application.

from infrastructure.config.settings import settings


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("DISCORD_TOKEN:", settings.DISCORD_TOKEN)
    print("DISCORD_CLIENT_ID:", settings.DISCORD_CLIENT_ID)
    print("GUILD_IDS:", settings.GUILD_IDS)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

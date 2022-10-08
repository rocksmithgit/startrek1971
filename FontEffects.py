import random
class colours:
    """Colours class:
    reset all colours settings with colors.reset;
    two sub classes fg for foreground and bg for background; use as colours.subclass.colour mname.
    i.e. colours.fg.red or colours.bg.green
    The generic bold, disable, underline, reverse, strikethrough, and invisible work with the main class
    i.e. colours.bold
    """
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    italic = '\033[03m'
    underline = '\033[04m'
    flashing = '\033[05m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    normal = '\033[22m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
        random = random.choice(['\033[31m', '\033[33m', '\033[35m', '\033[91m', '\033[93m', '\033[95m'])

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
        darkgrey = '\033[100m'
        lightred = '\033[101m'
        lightgreen = '\033[1022m'
        yellow = '\033[103m'
        lightblue = '\033[1044m'
        pink = '\033[1055m'
        lightcyan = '\033[106m'

# print(colours.bg.green, "Some text", colours.fg.red, "Some other text")
# print(colours.bg.lightgrey, "Some text", colours.fg.red, "Some other text")

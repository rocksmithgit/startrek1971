import random

DAMAGE_PREFIX = [
    "The main ",
    "That @#$#@& ",
    "Our cheap ",
    "Darn-it captain, that ",
    "Yikes, the ",
    ]
DAMAGE_SUFFIX = [
    " has died. We're on it!",
    " is out. We're working on it!",
    " is almost repaired!",
    " is dead.",
    " is fried. Working as fast as we can!",
    " is toast. Working as fast as I can!",
    " is being replaced.",
    " is dead. Please leave a message.",
    ]
DEFEAT_PREFIX = [
    "A defeated ",
    "The vengeful ",
    "An angry ",
    "The ejecting ",
    "A confused ",
    "Another ",
    "Yet another ",
    ]
DEFEAT_SUFFIX = [
    " says: `I'll be back!`",
    " cries: ... 'a lucky shot!'",
    " sighs bitterly.",
    " dies.",
    " is rescued.",
    " is history.",
    " is no more.",
    " is recycled.",
    " is eliminated.",
    " was aborted. Few lives, matter?",
    " ejects.",
    " crew is rescued.",
    " crew is spaced.",
    " crew is recycled.",
    " crew is recovered.",
    " yells: 'Thy mother mates poorly!'",
    " snarls: 'Lucky shot.'",
    " laughs: 'You'll not do THAT again!'",
    " says nothing.",
    " screams: 'Thy father is a Targ!'",
    " yells: 'Your parents eat bats!'",
    " snarls: 'Thy people eat vermin!'",
    " yells: 'May you create social disease!'",
    " curses: 'Thy fathers spreadeth pox!'",
    " yells: 'Your mother is progressive!'",
    ]

class Quips():
    
    @staticmethod
    def jibe(noun, prefix, suffix):
        prand = random.randrange(0, len(prefix) - 1)
        srand = random.randrange(0, len(suffix) - 1)
        return prefix[prand] + noun + suffix[srand]
    
    @staticmethod
    def jibe_damage(noun):
        if random.randrange(0, 100) > 25:
            return f"{noun.capitalize()} damaged. Repairs are underway."
        return Quips.jibe(noun, DAMAGE_PREFIX, DAMAGE_SUFFIX)
    
    @staticmethod
    def jibe_defeat(noun):
        if random.randrange(0, 100) > 25:
            return f"Another {noun.lower()} defeated."
        return Quips.jibe(noun, DEFEAT_PREFIX, DEFEAT_SUFFIX)






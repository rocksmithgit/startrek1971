import abc

class abs_display(abc.ABC):
    '''
    The plan is to have several places to 
    display information. The goal is to 
    use only one display, to display a 
    certain type of message. Networked
    screens would also be a great idea.
    Logging would be in there somewhere,
    as well.
    '''

    ST_DEFAULT = 'd'
    ST_CONSOLE = 'c'
    ST_NETWORK = 'n'
    
    def __init__(self, type_ = ST_DEFAULT, width = 80, height = 24):
        super().__init__()
        self.screen_type = type_
        self.width = width
        self.height = height
        self.xpos = self.ypos = -1

    @abc.abstractmethod
    def display(self, message):
        pass


    def print_strings(self, string_list):
        for string in string_list:
            self.display(string)
        self.display()


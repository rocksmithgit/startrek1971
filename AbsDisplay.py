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


class Con(abs_display):
    '''
    The best place to start is by encapsulating the default
    display. Will add screen metadata for it all, later.
    '''
    def __init__(self):
        super().__init__(abs_display.ST_CONSOLE)

    def display(self, message = ''):
        print(message)

    def read(self, prompt=''):
        return input(prompt)

    def read_double(self, prompt):
        text = input(prompt)
        try:
            value = float(text)
            return value
        except:
            pass
        return False




if __name__ == '__main__':
    con = Con()
    con.display("Testing!")





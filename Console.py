from AbsDisplay import abs_display
from Points import *
import sys
from time import sleep


class Con(abs_display):
    """
    The best place to start is by encapsulating the default
    display. Will add screen metadata for it all, later.
    """
    def __init__(self):
        super().__init__(abs_display.ST_CONSOLE)

    def display(self, message=''):
        print(message)

    def display_moving_photon(self, message=''):
        print(f"\r{message}", end='')
        sys.stdout.flush()
        sleep(0.15)

    def display_reset(self):
        print(end='\n')

    def read(self, prompt=''):
        return input(prompt)

    def read_double(self, prompt):
        text = input(prompt)
        try:
            value = float(text)
            return value
        except ValueError:
            pass
        return False

    def read_xypos(self, prompt="Location (alpha,num)"):
        """
        Parse: [a-h], ypos 
                or 
                #,#  
           Return None on error
        Example: b,4 
        """
        text = input(prompt + ': ')
        return SubDest.parse(text)

    def read_sector(self, prompt="Helm: sector 1-64, speed 1.0-9.0?"):
        text = input(prompt + ': ')
        return WarpDest.parse(text)

    def read_xypos(self, prompt="Helm: a-h, 1-8?"):
        text = input(prompt + ': ')
        return SubDest.parse(text)


if __name__ == '__main__':
    con = Con()
    con.display("Testing!")
    con.show_banner(["Testing, too!"])
    con.show_banner(["Testing", " .......... too!"])

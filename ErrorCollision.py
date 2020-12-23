class ErrorEnterpriseCollision(Exception):
    '''
    ... because some problems simpy have to wait ... =)
    '''
    def __init__(self, glyph):
        super().__init__()
        self.glyph = glyph





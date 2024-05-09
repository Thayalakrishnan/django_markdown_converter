from .base import BaseBlockifier


class HRBlockifier(BaseBlockifier):
    """ Process Horizontal Rules. """
    def getProps(self, *args, **kwargs):
        return {}
    
    def getData(self, *args, **kwargs):
        return " "


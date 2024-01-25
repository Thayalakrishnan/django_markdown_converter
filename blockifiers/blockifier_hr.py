from blockifiers.base_blockifier import BaseBlockifier


class HRBlockifier(BaseBlockifier):
    """ Process Horizontal Rules. """
    def getProperties(self, *args, **kwargs):
        return {}
    
    def getData(self, *args, **kwargs):
        return " "


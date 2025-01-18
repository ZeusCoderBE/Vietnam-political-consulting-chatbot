class Articles:
    def __init__(self,links):
        self._links = links 
    @property
    def links(self):
        return self._links

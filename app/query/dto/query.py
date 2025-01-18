from typing import List
class Query:
    def __init__(self,query,keyword:List[str]):
        self._query=query
        self._keyword=keyword
    @property
    def query(self)->str:
        return self._query
    @property
    def keyword(self) ->List[str]:
        return self._keyword
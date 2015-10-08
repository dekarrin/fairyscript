from ..ns import qn
from ..simpletypes import (ST_DecimalNumber, ST_String)
from ..xmlchemy import (
    BaseOxmlElement, RequiredAttribute
)

class CT_BookmarkStart(BaseOxmlElement):

    id = RequiredAttribute('w:id', ST_DecimalNumber)
    name = RequiredAttribute('w:name', ST_String)
    
    @property
    def name(self):
        var = self.get(qn('w:name'))
        return var
    
    @name.setter
    def name(self, wName):
        self.set(qn('w:name'), wName)
        
    @property
    def id(self):
        return self.get(qn('w:id'))
        
    @id.setter
    def id(self, wid):
        self.set(qn('w:id'), wid)
        
class CT_BookmarkEnd(BaseOxmlElement):
    id = RequiredAttribute('w:id', ST_DecimalNumber)
    
    @property
    def id(self):
        return self.get(qn('w:id'))
        
    @id.setter
    def id(self, wid):
        self.set(qn('w:id'), wid)
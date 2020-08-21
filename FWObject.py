class FWObject:
    def __init__(self,check:bool): 
        self._context = [None]*10
        self.check = check
        if self.check==True:
            for i in range(0,10,2):
                self.context.append("<W>")
                self.context.append("<T>")
    @property
    def context(self):
        return self._context
     # setting the values     
    @context.setter 
    def context(self, value): 
        self._context = value 
       
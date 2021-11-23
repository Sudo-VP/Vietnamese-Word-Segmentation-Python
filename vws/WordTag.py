class WordTag:
    def __init__(self,iword,itag):
        self._word = iword.lower()
        self._form = iword
        self._tag = itag

    @property
    def word(self):
        return self._word
    @property
    def form(self):
        return self._form
    @property
    def tag(self):
        return self._tag
    @word.setter
    def word(self,value):
        self._word =value
    @form.setter
    def form(self,value):
        self._form =value
    @tag.setter
    def tag(self,value):
        self._tag =value

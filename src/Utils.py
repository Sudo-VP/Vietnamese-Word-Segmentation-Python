import FWObject
import Node
import WordTag
class Utils:
    def __init__(self):
        self._NORMALIZER = {}
        self._NORMALIZER["òa"]= "oà"
        self._NORMALIZER["óa"]="oá"
        self._NORMALIZER["ỏa"]="oả"
        self._NORMALIZER["õa"]="oã"
        self._NORMALIZER["ọa"]="oạ"
        self._NORMALIZER["òe"]= "oè"
        self._NORMALIZER["óe"]="oé"
        self._NORMALIZER["ỏe"]= "oẻ"
        self._NORMALIZER["õe"]= "oẽ"
        self._NORMALIZER["ọe"]= "oẹ"
        self._NORMALIZER["ùy"]= "uỳ"
        self._NORMALIZER["úy"]= "uý"
        self._NORMALIZER["ủy"]= "uỷ"
        self._NORMALIZER["ũy"]= "uỹ"
        self._NORMALIZER["ụy"]= "uỵ"
        self._NORMALIZER["Ủy"]= "Uỷ"
    def getCondition(self,strCondition:str)->FWObject:
        condition = FWObject.FWObject(False)
        # print( strCondition.split(" and "))
        for rule in strCondition.split(" and "): 
            rule = rule.strip()
            # print(rule)

            # print(rule.index(".")+1,rule.index(" "))
            key = rule[rule.index(".") + 1: rule.index(" ")]
            value = self.getConcreteValue(rule)

            if key == "prevWord2":
                condition.context[4] = value
            else: 
                if key == "prevTag2" :
                    condition.context[5] = value
                else: 
                    if key == "prevWord1":
                        condition.context[2] = value
                    else:
                        if key == "prevTag1":
                            condition.context[3] = value
                        else: 
                            if key == "word":
                                condition.context[1] = value
                            else: 
                                if key == "tag":
                                    condition.context[0] = value
                                else: 
                                    if key == "nextWord1":
                                        condition.context[6] = value
                                    else:
                                        if key == "nextTag1":
                                            condition.context[7] = value
                                        else:
                                            if key == "nextWord2":
                                                condition.context[8] = value
                                            else:
                                                if key == "nextTag2":
                                                    condition.context[9] = value
           

        return condition

    def  getObject(self,wordtags:list,  size:int,  index:int)->FWObject:
        object =  FWObject.FWObject(True)

        if index > 1:
            object.context[4] = wordtags[index-2].word
            object.context[5] = wordtags[index-2].tag

        if index > 0:
            object.context[2] = wordtags[index-1].word
            object.context[3] = wordtags[index-1].tag

        currentWord = wordtags[index].word
        currentTag = wordtags[index].tag

        object.context[1] = currentWord
        object.context[0] = currentTag

        if index < size - 1:
            object.context[6] = wordtags[index+1].word
            object.context[7] = wordtags[index+1].tag

        if index < size - 2:
            object.context[8] = wordtags[index+2].word
            object.context[9] = wordtags[index+2].tag

        return object

    def getConcreteValue(self,strs:str)->str:
        if "\"\"" in strs:
            if "Word" in strs:
                return "<W>"
            else:
                return "<T>"
        conclusion = strs[strs.index("\"") + 1: len(strs) - 1]
        return conclusion
    @property
    def NORMALIZER(self):
        return self._NORMALIZER
    @property
    def NORMALIZER_KEYS(self):
        return self._NORMALIZER.keys()


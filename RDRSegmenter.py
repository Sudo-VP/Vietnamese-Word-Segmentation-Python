from Node import Node
from Utils import Utils
from FWObject import FWObject
from WordTag import WordTag
from Vocabulary import Vocabulary
from Tokenizer import  Tokenizer
import time

utils = Utils()

class RDRSegmenter:
    def __init__(self):
        self._root = None
        try:
            self.constructTreeFromRulesFile("Model.RDR")
        except IOError as e:
            raise e
    @property
    def root(self):
        return self._root
    @root.setter
    def root(self,value:Node):
        self._root = value
    def constructTreeFromRulesFile(self, rulesFilePath:str):

        self.root = Node(FWObject(False), "NN", None, None, None, 0)

        currentNode = self.root
        currentDepth = 0
        with open(rulesFilePath,'r',encoding='utf8') as rulesFile:
            for indexFileRule,line in enumerate(rulesFile):
                depth = 0
                for i in range(0,6):
                    if line[i] == '\t':
                        depth += 1
                    else:
                        break
                if indexFileRule==0:
                    continue
                line = line.strip()
                if len(line) == 0:
                    continue

                if "cc:" in line:
                    continue
                # print(line.split(" : ")[0].strip())
                condition = utils.getCondition(line.split(" : ")[0].strip())
                conclusion = utils.getConcreteValue(line.split(" : ")[1].strip())

                node = Node(condition, conclusion, None, None, None, depth)

                if depth > currentDepth:
                    currentNode.setExceptNode(node)
                else:
                    if depth == currentDepth:
                        currentNode.setIfnotNode(node)
                    else:
                        while currentNode.depth != depth:
                            currentNode = currentNode.fatherNode
                            currentNode.setIfnotNode(node)
                node.setFatherNode(currentNode)

                currentNode = node
                currentDepth = depth

    def findFiredNode(self,object:FWObject)->Node:
        currentN = self._root
        firedN = None
        while True:
            if currentN.satisfy(object):
                firedN = currentN
                if currentN.exceptNode == None :
                    break
                else :
                    currentN = currentN.exceptNode
            else:
                if currentN.ifnotNode == None:
                    break
                else :
                    currentN = currentN.ifnotNode
        return firedN
    def allIsLetter(self,strs:str)->bool:

        for char in strs:
            if char.isalpha() ==False:
                return False
        return True
    def allIsUpper(self,strs:str)->bool:

        for char in strs:
            if char.isupper() ==False:
                return False
        return True
    def getInitialSegmentation(self,sentence:str)->list:
        wordtags = []
        vocab = Vocabulary()
        for regex in utils.NORMALIZER_KEYS:
            if regex in sentence:
                sentence = sentence.replace(regex, utils.NORMALIZER[regex])
        tokens = sentence.split()
        lowerTokens = sentence.lower().split()
        senLength = len(tokens)
        i = 0
        while i < senLength :
            token = tokens[i]
            if self.allIsLetter(token) :
                if token[0].islower() and (i + 1) < senLength:
                    if tokens[i + 1][0].isupper():
                        wordtags.append(WordTag(token, "B"))
                        i+=1
                        continue
                isSingleSyllabel = True
                for j in range(min(i + 4, senLength), i + 1,-1):
                    word = " ".join(lowerTokens[i: j])
                    if word in vocab.VN_DICT or word in vocab.VN_LOCATIONS or word in vocab.COUNTRY_L_NAME:
                        wordtags.append(WordTag(token, "B"))
                        for k in range(i+1,j):
                            wordtags.append(WordTag(tokens[k], "I"))

                        i = j - 1
                        isSingleSyllabel = False
                        break

                if isSingleSyllabel :
                    lowercasedToken = lowerTokens[i]

                    if lowercasedToken in vocab.VN_FIRST_SENT_WORDS    \
                            or token[0].islower()   \
                            or self.allIsUpper(token)   \
                            or lowercasedToken in vocab.COUNTRY_S_NAME \
                            or lowercasedToken in vocab.WORLD_COMPANY :    \

                        wordtags.append(WordTag(token, "B"))
                        i+=1
                        continue
                    ilower = i + 1
                    for ilower in range(i + 1 ,min(i + 4, senLength)):
                        ntoken = tokens[ilower]
                        if ntoken.islower() \
                                or not self.allIsLetter(ntoken) \
                                or ntoken=="LBKT" or ntoken=="RBKT" :
                            break

                    if ilower > i + 1:
                        isNotMiddleName = True
                        if lowercasedToken in vocab.VN_MIDDLE_NAMES and i >= 1:
                            prevT = tokens[i-1]
                            if prevT[0].isupper():
                                if prevT.lower() in vocab.VN_FAMILY_NAMES:
                                    wordtags.append(WordTag(token, "I"))
                                    isNotMiddleName = False
                        if isNotMiddleName:
                            wordtags.append(WordTag(token, "B"))
                        for  k in range(i+1,ilower):
                            wordtags.append( WordTag(tokens[k], "I"))

                        i = ilower - 1
                    else:
                        wordtags.append(WordTag(token, "B"))
            else:
                wordtags.append(WordTag(token, "B"))
            i+=1
        return wordtags

    def segmentTokenizedString(self,strs :str)->str:
        sb = ""
        line = ''.join(strs).strip()
        if len(line) == 0:
            return "\n"

        wordtags = self.getInitialSegmentation(line)
        size = len(wordtags)
        for i in range(0,size) :
            object = utils.getObject(wordtags, size, i)
            firedNode = self.findFiredNode(object)
            if firedNode.depth > 0:
                if firedNode.conclusion=="B":
                    sb=sb+" " + wordtags[i].form
                else:
                    sb=sb+"_" + wordtags[i].form
            else:
                if wordtags[i].tag == "B":
                    sb=sb+" " + wordtags[i].form
                else:
                    sb=sb+"_" + wordtags[i].form
        return sb.strip()

    # def segmentRawString(self,strs:str)->str:
    #     return self.segmentTokenizedString(" ".join(Tokenizer.tokenize(strs)))
    def segmentRawSentences(self,tokenizer:Tokenizer,strs:str):
        sentence = tokenizer.joinSentences(tokenizer.tokenize(strs))
        return self.segmentTokenizedString(sentence)


if __name__ == "__main__":
    rdrsegment = RDRSegmenter()
    tokenizer = Tokenizer()
    t=time.time()
    output = rdrsegment.segmentRawSentences(tokenizer,"Lượng khách Thái bắt đầu gia tăng từ đầu năm 2005. Bên cạnh đó, kể từ tháng 10-2005 đến nay, từ khi được phép của VN, các đoàn caravan của Thái Lan cũng đã ồ ạt đổ vào VN.")
    print(output,time.time()-t)

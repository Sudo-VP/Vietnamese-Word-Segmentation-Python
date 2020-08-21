import string
import re
# from enum import E/num

class Tokenizer:
    def __init__(self):
        self.name = 'Tokenizer'
    def hasPunctuation(self,strs:str):
        for char in strs:
            # print(char)
            if not char.isalpha():
                # print(char)
                return True
        return False

    def tokenize(self,s):
        if s == None or s.strip()=="":
            return []

        tempTokens = s.strip().split()
        # print(tempTokens)
        if len(tempTokens) == 0:
            return []

        tokens = []
        for token in tempTokens:
            # print(len(token))

            if len(token) == 1 or self.hasPunctuation(token):
                tokens.append(token)
                continue

            if token.endswith(","):

                for t in self.tokenize(token[0, len(token) - 1]):
                    tokens.append(t)
                    tokens.append(",")
                continue
            if token in StringUtils().VN_abbreviation:
                tokens.append(token)
                continue

            if token.endswith(".") and token[len(token) - 2].isalpha():
                if len(token) == 2 and token[len(token) - 2].isupper() or re.search(Regex.SHORT_NAME,token):
                    tokens.append(token)
                    continue
                for t in tokenize(token[0, len(token) - 1]):
                    tokens.append(t)
                tokens.add(".")
                continue

            if token in StringUtils().VN_exception:
                tokens.append(token)
                continue

            tokenContainsAbb = False
            for e in StringUtils().VN_abbreviation:
                try:
                    i = token.index(e)
                except Exception as e:
                    continue

                tokenContainsAbb = True
                tokens = recursive(tokens, token, i, i + e.length())
                break
            if tokenContainsAbb:
                continue

            tokenContainsExp = False
            for e in StringUtils()._VN_exception:
                try:
                    i = token.index(e)
                except Exception as e:
                    continue

                tokenContainsExp = True
                tokens = recursive(tokens, token, i, i + e.length())
                break
            if tokenContainsExp:
                continue

            regexes = Regex().getRegexList()

            matching = False
            for regex in regexes:
                # print(regex,token)
                if re.search(regex,token):
                    tokens.append(token)
                    matching = True
                    break
            if matching:
                continue

            for i in range(0, len(regexes)):
                pattern = re.compile(regexes[i])
                matcher = matcher.search(token)
                if matcher:
                    if i == Regex.getRegexIndex("url"):
                        elements = token.split(".")
                        hasURL = True
                        for ele in elements:
                            if len(ele) == 1 and ele[0].isupper():
                                hasURL = False
                                break
                            for j in range(0,len(ele)):
                                if ele[j] >= 128:
                                    hasURL = False
                                    break
                        if hasURL:
                            tokens = recursive(tokens, token, matcher.start(), matcher.end())
                        else:
                            continue

                    else:
                        if i == Regex.getRegexIndex("month"):
                            start = matcher.start()

                            hasLetter = False

                            for j in range(0, start):
                                if token[j].isalpha():
                                    tokens = recursive(tokens, token, matcher.start(), matcher.end())
                                    hasLetter = True
                                    break


                            if not hasLetter:
                                tokens.append(token)

                        else:
                            tokens = self.recursive(tokens, token, matcher.start(), matcher.end())

                    matching = True
                    break

            if matching:
                continue
            else:
                tokens.append(token)

        return tokens

    def recursive( tokens, token,  beginMatch,  endMatch):
        if beginMatch > 0:
            for t in tokenize(token[0, beginMatch]):
                tokens.append(t)
        for t in tokenize(token[beginMatch, endMatch]):
                tokens.append(t)

        if endMatch < len(token):
            for t in tokenize(token[endMatch]):
                tokens.append(t)

        return tokens

    def joinSentences(self,tokens):
        sentences =[]
        sentence = []
        for i in range(0,len(tokens)):
            token = tokens[i]
            nextToken = None
            if i != len(tokens)- 1:
                nextToken = tokens[i + 1]
            beforeToken = None
            if i > 0:
                beforeToken = tokens[i - 1]

            # print(token)
            sentence.append(token)

            if i == len(tokens)- 1:
                sentences.append(self.joinSentence(sentence))
                return sentences

            if i < len(tokens)- 2 and token == StringConst.COLON:
                if nextToken.isnumeric() and tokens[i+2]==StringConst.STOP  \
                        or tokens[i+2] == StringConst.COMMA:
                    sentences.append(self.joinSentence(sentence))
                    sentence = ''
                    continue


            if re.match(Regex().EOS_PUNCTUATION,token):

                if nextToken == "\"" or nextToken=="''":
                    count = 0
                    for senToken in sentence:
                        if senToken=="\"" or senToken=="''":
                            count += 1
                    if count % 2 == 1:
                        continue

                if StringUtils.isBrace(nextToken) or nextToken=="" or nextToken[0].islower()    \
                        or nextToken==StringConst.COMMA or nextToken[0].isnumeric():
                    continue

                if len(sentence) == 2 and token==StringConst.STOP:
                    if beforeToken[0].isnumeric():
                        continue
                    if beforeToken[0].islower():
                        continue
                    if beforeToken[0].isupper():
                        if len(beforeToken) == 1:
                            continue


                sentences.append(self.joinSentence(sentence))
                sentence = ""
        return sentences

    def joinSentence(self,tokens):
        sent = []
        stringConst = StringConst()
        length = length = len(tokens)
        token = ""
        for i in range(0,length):
            token = tokens[i]
            if token=="" or token == None or token==stringConst.SPACE:
                continue
            sent.append(token)
            if i < length - 1:
                sent.append(stringConst.SPACE)
        return ''.join(sent).strip()

class StringConst:
    @property
    def BOS(self):
        return "<s>"
    @property
    def EOS(self):
        return "</s>"
    @property
    def SPACE(self):
        return " "
    @property
    def COMMA(self):
        return ","
    @property
    def STOP(self):
        return "."
    @property
    def COLON(self):
        return ":"
    @property
    def UNDERSCORE(self):
        return "_"

class StringUtils:
    def __init__(self):
        self._VN_abbreviation={"M.City"}
        self._VN_abbreviation.add("V.I.P")
        self._VN_abbreviation.add("PGS.Ts")
        self._VN_abbreviation.add("MRS.")
        self._VN_abbreviation.add("Mrs.")
        self._VN_abbreviation.add("Man.United")
        self._VN_abbreviation.add("Mr.")
        self._VN_abbreviation.add("SHB.ĐN")
        self._VN_abbreviation.add("Gs.Bs")
        self._VN_abbreviation.add("U.S.A")
        self._VN_abbreviation.add("TMN.CSG")
        self._VN_abbreviation.add("Kts.Ts")
        self._VN_abbreviation.add("R.Madrid")
        self._VN_abbreviation.add("Tp.")
        self._VN_abbreviation.add("T.Ư")
        self._VN_abbreviation.add("D.C")
        self._VN_abbreviation.add("Gs.Tskh")
        self._VN_abbreviation.add("PGS.KTS")
        self._VN_abbreviation.add("GS.BS")
        self._VN_abbreviation.add("KTS.TS")
        self._VN_abbreviation.add("PGS-TS")
        self._VN_abbreviation.add("Co.")
        self._VN_abbreviation.add("S.H.E")
        self._VN_abbreviation.add("Ths.Bs")
        self._VN_abbreviation.add("T&T.HN")
        self._VN_abbreviation.add("MR.")
        self._VN_abbreviation.add("Ms.")
        self._VN_abbreviation.add("T.T.P")
        self._VN_abbreviation.add("TT.")
        self._VN_abbreviation.add("TP.")
        self._VN_abbreviation.add("ĐH.QGHN")
        self._VN_abbreviation.add("Gs.Kts")
        self._VN_abbreviation.add("Man.Utd")
        self._VN_abbreviation.add("GD-ĐT")
        self._VN_abbreviation.add("T.W")
        self._VN_abbreviation.add("Corp.")
        self._VN_abbreviation.add("ĐT.LA")
        self._VN_abbreviation.add("Dr.")
        self._VN_abbreviation.add("T&T")
        self._VN_abbreviation.add("HN.ACB")
        self._VN_abbreviation.add("GS.KTS")
        self._VN_abbreviation.add("MS.")
        self._VN_abbreviation.add("Prof.")
        self._VN_abbreviation.add("GS.TS")
        self._VN_abbreviation.add("PGs.Ts")
        self._VN_abbreviation.add("PGS.BS")
        self._VN_abbreviation.add("﻿BT.")
        self._VN_abbreviation.add("Ltd.")
        self._VN_abbreviation.add("ThS.BS")
        self._VN_abbreviation.add("Gs.Ts")
        self._VN_abbreviation.add("SL.NA")
        self._VN_abbreviation.add("Th.S")
        self._VN_abbreviation.add("Gs.Vs")
        self._VN_abbreviation.add("PGs.Bs")
        self._VN_abbreviation.add("T.O.P")
        self._VN_abbreviation.add("PGS.TS")
        self._VN_abbreviation.add("HN.T&T")
        self._VN_abbreviation.add("SG.XT")
        self._VN_abbreviation.add("O.T.C")
        self._VN_abbreviation.add("TS.BS")
        self._VN_abbreviation.add("Yahoo!")
        self._VN_abbreviation.add("Man.City")
        self._VN_abbreviation.add("MISS.")
        self._VN_abbreviation.add("HA.GL")
        self._VN_abbreviation.add("GS.Ts")
        self._VN_abbreviation.add("TBT.")
        self._VN_abbreviation.add("GS.VS")
        self._VN_abbreviation.add("GS.TSKH")
        self._VN_abbreviation.add("Ts.Bs")
        self._VN_abbreviation.add("M.U")
        self._VN_abbreviation.add("Gs.TSKH")
        self._VN_abbreviation.add("U.S")
        self._VN_abbreviation.add("Miss.")
        self._VN_abbreviation.add("GD.ĐT")
        self._VN_abbreviation.add("PGs.Kts")
        self._VN_abbreviation.add("St.")
        self._VN_abbreviation.add("Ng.")
        self._VN_abbreviation.add("Inc.")
        self._VN_abbreviation.add("Th.")
        self._VN_abbreviation.add("N.O.V.A")

        self._VN_exception={"Wi-fi"}
        self._VN_exception.add("17+")
        self._VN_exception.add("km/h")
        self._VN_exception.add("M7")
        self._VN_exception.add("M8")
        self._VN_exception.add("21+")
        self._VN_exception.add("G3")
        self._VN_exception.add("M9")
        self._VN_exception.add("G4")
        self._VN_exception.add("km3")
        self._VN_exception.add("m/s")
        self._VN_exception.add("km2")
        self._VN_exception.add("5g")
        self._VN_exception.add("4G")
        self._VN_exception.add("8K")
        self._VN_exception.add("3g")
        self._VN_exception.add("E9")
        self._VN_exception.add("U21")
        self._VN_exception.add("4K")
        self._VN_exception.add("U23")
        self._VN_exception.add("Z1")
        self._VN_exception.add("Z2")
        self._VN_exception.add("Z3")
        self._VN_exception.add("Z4")
        self._VN_exception.add("Z5")
        self._VN_exception.add("Jong-un")
        self._VN_exception.add("u19")
        self._VN_exception.add("5s")
        self._VN_exception.add("wi-fi")
        self._VN_exception.add("18+")
        self._VN_exception.add("Wi-Fi")
        self._VN_exception.add("m2")
        self._VN_exception.add("16+")
        self._VN_exception.add("m3")
        self._VN_exception.add("V-League")
        self._VN_exception.add("Geun-hye")
        self._VN_exception.add("5G")
        self._VN_exception.add("4g")
        self._VN_exception.add("Z3+")
        self._VN_exception.add("3G")
        self._VN_exception.add("km/s")
        self._VN_exception.add("6+")
        self._VN_exception.add("u21")
        self._VN_exception.add("WI-FI")
        self._VN_exception.add("u23")
        self._VN_exception.add("U19")
        self._VN_exception.add("6s")
        self._VN_exception.add("4s")

    def isBrace(self,string):
        if string=="”" or string=="�" or string=="'" or string==")" \
                or string=="}" or string=="]":
            return True
        return False
    @property
    def VN_abbreviation(self):
        return self._VN_abbreviation
    
    @property
    def VN_exception(self):
        return self._VN_exception
class Regex:
    def __init__(self):
        self._regexes = None
        self._regexIndex=None
    @property
    def ELLIPSIS(self):
        return "\\.{2,}"

    @property
    def EMAIL(self):
        return "([\\w\\d_\\.-]+)@(([\\d\\w-]+)\\.)*([\\d\\w-]+)"

    @property
    def FULL_DATE(self):
        return "(0?[1-9]|[12][0-9]|3[01])(\\/|-|\\.)(1[0-2]|(0?[1-9]))((\\/|-|\\.)\\d{4})"

    @property
    def MONTH(self):
        return "(1[0-2]|(0?[1-9]))(\\/)\\d{4}"

    @property
    def DATE(self):
        return "(0?[1-9]|[12][0-9]|3[01])(\\/)(1[0-2]|(0?[1-9]))"

    @property
    def TIME(self):
        return "(\\d\\d:\\d\\d:\\d\\d)|((0?\\d|1\\d|2[0-3])(:|h)(0?\\d|[1-5]\\d)(’|'|p|ph)?)"

    @property
    def MONEY(self):
        return "\\\p{Sc}\\d+([\\.,]\\d+)*|\\d+([\\.,]\\d+)*\\\p{Sc}"

    @property
    def PHONE_NUMBER(self):
        return "(\\(?\\+\\d{1,2}\\)?[\\s\\.-]?)?\\d{2,}[\\s\\.-]?\\d{3,}[\\s\\.-]?\\d{3,}"

    @property
    def URL(self):
        return "(((https?|ftp):\\/\\/|www\\.)[^\\s/$.?#].[^\\s]*)|(https?:\\/\\/)?(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)"

    @property
    def NUMBER(self):
        return "[-+]?\\d+([\\.,]\\d+)*%?\\\p{Sc}?"

    @property
    def PUNCTUATION(self):
        return ",|\\.|:|\\?|!||-|_|\"|'|“|”|\\\or\\(|\\)|\\[|\\]|\\{|\\}|âŸ¨|âŸ©|Â«|Â»|\\\\|\\/|\\â€˜|\\â€™|\\â€œ|\\â€�|â€¦|…|‘|’|·"

    @property
    def SPECIAL_CHAR(self):
        return "\\~|\\@|\\#|\\^|\\&|\\*|\\+|\\-|\\â€“|<|>|\\|"

    @property
    def EOS_PUNCTUATION(self):
        return "(\\.+|\\?|!|…)"

    @property
    def NUMBERS_EXPRESSION(self):
        return "[-+]?\\d+([\\.,]\\d+)*%?\\\p{Sc}?" + "([\\+\\-\\*\\/]" + "[-+]?\\d+([\\.,]\\d+)*%?\\\p{Sc}?" + ")*"

    @property
    def SHORT_NAME(self):
        return "([\\\p{L}]+([\\.\\-][\\\p{L}]+)+)|([\\\p{L}]+-\\d+)"

    @property
    def ALLCAP(self):
        return "[A-Z]+\\.[A-Z]+"
    @property
    def regexes(self):
        return self._regexes
    @regexes.setter
    def regexes(self,value):
        self._regexes = value
    @property
    def regexIndex(self):
        return self._regexIndex
    @regexIndex.setter
    def regexIndex(self,value):
        self._regexIndex = value
    
    def getRegexList(self):
        regex_ = Regex()
        if self._regexes == None:
            self._regexes = []
            self._regexIndex = []

            self._regexes.append(regex_.ELLIPSIS)
            self._regexIndex.append("ELLIPSIS")

            self._regexes.append(regex_.EMAIL)
            self._regexIndex.append("EMAIL")

            self._regexes.append(regex_.URL)
            self._regexIndex.append("URL")

            self._regexes.append(regex_.FULL_DATE)
            self._regexIndex.append("FULL_DATE")

            self._regexes.append(regex_.MONTH)
            self._regexIndex.append("MONTH")

            self._regexes.append(regex_.DATE)
            self._regexIndex.append("DATE")

            self._regexes.append(regex_.TIME)
            self._regexIndex.append("TIME")

            self._regexes.append(regex_.MONEY)
            self._regexIndex.append("MONEY")

            self._regexes.append(regex_.PHONE_NUMBER)
            self._regexIndex.append("PHONE_NUMBER")

            self._regexes.append(regex_.SHORT_NAME)
            self._regexIndex.append("SHORT_NAME")

            self._regexes.append(regex_.NUMBERS_EXPRESSION)
            self._regexIndex.append("NUMBERS_EXPRESSION")

            self._regexes.append(regex_.NUMBER)
            self._regexIndex.append("NUMBER")

            self._regexes.append(regex_.PUNCTUATION)
            self._regexIndex.append("PUNCTUATION")

            self._regexes.append(regex_.SPECIAL_CHAR)
            self._regexIndex.append("SPECIAL_CHAR")

            self._regexes.append(regex_.ALLCAP)
            self._regexIndex.append("ALLCAP")

        return self._regexes

    def getRegexIndex(self,regex):
        return self._regexIndex.index(regex.upper())

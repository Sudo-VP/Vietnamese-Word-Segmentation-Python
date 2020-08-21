import FWObject

class Node:
    def __init__(self,inCondition:FWObject,inConclusion:str,  inFatherNode, inExceptNode,
             inIfnotNode,  inDepth:int):
        self.condition = inCondition
        self.conclusion = inConclusion
        self.fatherNode = inFatherNode
        self.exceptNode = inExceptNode
        self.ifnotNode = inIfnotNode
        self.depth = inDepth
    def setIfnotNode(self, node):
        self.ifnotNode = node

    def setExceptNode(self, node):
        self.exceptNode = node

    def setFatherNode(self, node):
        self.fatherNode = node
    def countNodes(self)->int:
        count = 1
        if self.exceptNode != None:
            count += self.exceptNode.countNodes()
        if self.ifnotNode != None :
            count += self.ifnotNode.countNodes()
        return count
    def satisfy(self, object:FWObject):
        check = True
        for i in range(0,10):
            key = self.condition.context[i]
            if key != None:
                if not key == object.context[i] :
                    check = False
                    break
        return check
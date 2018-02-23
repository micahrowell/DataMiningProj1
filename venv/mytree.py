#!/usr/bin/env python

import sys
import math

class Node:
    def __init__(self):
        self.nodes = []
        self.__data = None
        self.__i = 0
    def __str__(self,level=0):
        ret = '|  ' * level
        if level > 0:
            ret += '|__'
        ret += str(self.__data) + '\n'
        for node in self.nodes:
            ret += node.__str__(level + 1)
        return ret
    def data(self):
        return self.__data
    def setData(self,value):
        self.__data = value
    def currentNode(self):
        return self.nodes[self.__i]
    def iterate(self):
        if self.__i + 1 != len(self.nodes):
            self.__i += 1

# since this code has to run given several different conditions I figured it would be best to make it a function
def findMaxClass(maxClassData):
    D = list(maxClassData)
    classes = {}
    for i in range(len(D)):
        key = D[i]['class']
        if key in classes:
            classes[key] += 1.0
        else:
            classes[key] = 1.0
    maxClass = 0
    maxName = ''
    for c in classes:
        if classes[c] > maxClass:
            maxClass = classes[c]
            maxName = c
    return maxName

def gainRatio(data,attrList):
    D = list(data)
    attributeList = list(attrList)
    n = len(D)
    classes = {}
    gains = {}
    gainRatios = {}
    for i in range(len(data)):
        key = data[i]['class']
        if key in classes:
            classes[key] += 1.0
        else:
            classes[key] = 1.0
    infoD = 0.0
    for k in classes:
        fraction = classes[k] / float(n)
        infoD -= fraction * math.log(fraction,2)
    for j in attributeList:
        types = {}
        infoAttrD = 0.0
        for r in D:
            thisType = r[j]
            if thisType not in types:
                types[thisType] = {}
                types[thisType]['total'] = 0.0
                for k in classes:
                    types[thisType][k] = 0.0
            else:
                thisClass = r['class']
                types[thisType][thisClass] += 1.0
                types[thisType]['total'] += 1.0
        for t in types:
            logs = 0.0
            total = types[t]['total']
            if total == 0:
                continue
            for c in types[t]:
                if c != 'total':
                    fraction = types[t][c] / total
                    if fraction == 0:
                        continue
                    logs -= fraction * math.log(fraction,2)
            infoAttrD += (total/n) * logs
        attrTypes[j] = types
        gains[j] = infoD - infoAttrD
    maxVal = 0
    maxAttr = ''
    for e in gains:
        """
        # this is my attempt at gain ratio but I couldn't get it to work
        partitions = attrTypes[e]
        splitInfo = 0.0
        for p in partitions:
            typeCount = 0.0
            for d in range(len(D)):
                if p in D[d]:
                    typeCount += 1.0
            ratio = typeCount / len(D)
            if ratio == 0:
                continue
            splitInfo -= ratio * math.log(ratio,2)
        if splitInfo == 0:
            gainRatios[e] = 0
        else:
            gainRatios[e] = gains[e] / splitInfo
        """
        if gains[e] > maxVal:
            maxVal = gains[e]
            maxAttr = e
    return maxAttr

"""
# gain ratio prototype where I laid out the logic
def gainRatio(subData):
    splitInfo = 0.0
    for i in subData:
        ratio = len(subData[i]) / len(data)
        splitInfo -= ratio * math.log(ratio,2)
"""

def generateDecisionTree(data,attrListNames):
    D = list(data)
    attrList = list(attrListNames)
    N = Node()
    className = str(D[0]['class'])
    allSameClass = True
    for i in range(len(D)):
        if str(D[i]['class']) != className:
            allSameClass = False
            break
    if allSameClass == True:
        N.setData(className)
        return N
    if len(attrList) == 0:
        maxName = findMaxClass(D)
        N.setData(maxName)
        return N
    attr = gainRatio(D,attrList)
    N.setData(attr)
    # implement step 8
    attrList.remove(attr)
    for t in attrTypes[attr]:
        newData = []
        for d in range(len(D)):
            if D[d][attr] == t:
                newData.append(D[d])
        if len(newData) == 0:
            newNode = Node()
            newNode.setData(findMaxClass(D))
            N.nodes.append(newNode)
        else:
            newNode = generateDecisionTree(newData,attrList)
            N.nodes.append(newNode)
    return N

"""
# this code is not used but is being kept to display my logic as part of the process
def treeToArray(node,array,depth):
    string = ''
    depthString = ''
    nodeData = node.data()
    for i in range(depth):
        if i != depth - 1:
            depthString += '|  '
    string += depthString + str(nodeData) + '\n'
    if nodeData not in attrTypes:
        string = depthString + '|__' + str(nodeData) + '\n'
        array.append(string)
    else:
        array.append(string)
        for t in attrTypes[nodeData]:
            string = depthString + '|__' + str(t) + '\n'
            array.append(string)
            treeToArray(node.currentNode(),array,depth+1)
            node.iterate()
"""

finName = sys.argv[1] # change 1 to 0
attrToTest = sys.argv[2] # change 2 to 1
attrToTest = attrToTest.strip('\n')
attrToTest = attrToTest.split(',')

inData = open(finName,'r')
outData = open('output.txt','w')

# the first line will be names of each attribute, need to store them separately
attributes = inData.readline()
attributes = attributes.strip('\n')
attributes = attributes.split(',')

data = []

for line in inData:
    line = line.strip('\n')
    line = line.replace(' ','')
    line = line.split(',')
    row = {}
    # making an array of dictionaries, it will be much easier to access each element this way
    for e in range(len(line)):
        if e == len(line) - 1:
            row['class'] = line[e] # the last element will always be the thing to classify to
        else:
            row[attributes[e]] = line[e]
    data.append(row)

attrToTestNames = []

for a in attrToTest:
    attrToTestNames.append(attributes[int(a) - 1])

attrTypes = {}

tree = generateDecisionTree(data,attrToTestNames)
#printArr = []
#treeToArray(tree,printArr,0)

#string = treeToString(tree)

outData.write(str(tree))

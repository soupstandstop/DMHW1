#!/usr/bin/env python
# coding: utf-8

# In[8]:


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None

        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):

        self.count += numOccur

    def disp(self, ind=1):

        for child in self.children.values():
            child.disp(ind+1)


def loadSimpDat():
    simpDat = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
            ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
            ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        if not retDict in trans:
            retDict[frozenset(trans)] = 1
        else:
            retDict[frozenset(trans)] += 1
    return retDict


def updateHeader(nodeToTest, targetNode):
   
    while (nodeToTest.nodeLink is not None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def updateTree(items, inTree, headerTable, count):
    
    if items[0] in inTree.children:
        
        inTree.children[items[0]].inc(count)
    else:
        
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
       
        if headerTable[items[0]][1] is None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)


def createTree(dataSet, Sup=0.001):
    
    headerTable = {}
    word_count=[]
    
    for trans in dataSet:
        
        for item in trans:
            
            if item in word_count:
                word_count = word_count
            else:
                word_count.append(item)
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
   
    for k in word_count:
        if headerTable[k] < Sup:
            del(headerTable[k])

    
    freqItemSet = set(headerTable.keys())
    
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        
        headerTable[k] = [headerTable[k], None]

    
    retTree = treeNode('Null Set', 1, None)
   
    for tranSet, count in dataSet.items():
       
        localD = {}
        for item in tranSet:
            
            if item in freqItemSet:
               
                localD[item] = headerTable[item][0]
        
        if len(localD) > 0:
           
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
           
            updateTree(orderedItems, retTree, headerTable, count)

    return retTree, headerTable


def ascendTree(leafNode, prefixPath):

    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):

    condPats = {}

    while treeNode is not None:
        prefixPath = []

        ascendTree(treeNode, prefixPath)

        if len(prefixPath) > 1:

            condPats[frozenset(prefixPath[1:])] = treeNode.count

        treeNode = treeNode.nodeLink

    return condPats


def eTree(inTree, headerTable, Sup, preFix, freqItemList):

    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]

    for basePat in bigL:

        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)


        freqItemList.append(newFreqSet)

        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])

        myCondTree, myHead = createTree(condPattBases, Sup)

        if myHead is not None:
            myCondTree.disp(1)

            eTree(myCondTree, myHead, Sup, newFreqSet, freqItemList)


import pandas as pd
from sklearn import preprocessing
import time
t = time.clock()

def load_data_set():
    with open('test3.txt', "r") as fi:  
        datadict = {}
        for i in fi.readlines():  
            temp = i.split()      
            name, num = temp[0], temp[1]

            if name in datadict:      
                datadict[name].append(num)
            else:               
                datadict[name] = [num]
        

        vallist = []
        for key, value in datadict.items():
            vallist.append(value)
    return vallist

gen = load_data_set()
print(gen)

if __name__ == "__main__":

    simpDat = load_data_set()

    initSet = createInitSet(simpDat)
    print (initSet)

    myFPtree, myHeaderTab = createTree(initSet, 0.1)
    myFPtree.disp()



    freqItemList = []
    i = 0
    eTree(myFPtree, myHeaderTab, 80, set([]), freqItemList)
    for item in freqItemList:
        i = i+1
        con = "frozenset:"
        print(i,con,item)

e = time.clock()
print(e)


# In[9]:


get_ipython().system('jupyter nbconvert --to script FPGrowth.ipynb')


# In[ ]:





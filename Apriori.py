#!/usr/bin/env python
# coding: utf-8

# In[177]:


import time


# In[108]:


def ProcessData():
    with open('/home/user/桌面/test3.txt', "r") as fi:  # Data read from a text file is a string
        datadict = {}
        for i in fi.readlines():  # So you split the line into a list
            temp = i.split()      # So, temp = [1 42]
            name, num = temp[0], temp[1]

            if name in datadict:       # Check if name in d's key
                datadict[name].append(num)
            else:               # Add a key
                datadict[name] = [num]
        
        # Transfer value in dic. to a list(vallist)
        vallist = []
        for key, value in datadict.items():
            vallist.append(value)
    return vallist


# In[169]:


def createC1(dataSet):
    C1 = set()
    for transaction in dataSet:
        for item in transaction:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1


# In[195]:


def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can]=1
                else: 
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


# In[205]:


def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList


# In[207]:


def apriori(dataset, minSupport=0.001):
    C1 = createC1(dataSet)
    D = list(map(set,dataSet))
   # D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


# In[200]:


L1, suppData0 = scanD(D, C1, 0.000000001)


# In[210]:


len(L)


# In[208]:


L, suppData = apriori(dataSet)
L


# In[ ]:


def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i>1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


# In[ ]:


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet-conseq]
        if conf >= minConf:
            print(freqSet-conseq, '-->', conseq, 'conf:', conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


# In[ ]:


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet)) > (m+1):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


# In[ ]:





# In[ ]:





# In[ ]:





# In[105]:


get_ipython().system('jupyter nbconvert --to script Apriori.ipynb')


# In[ ]:





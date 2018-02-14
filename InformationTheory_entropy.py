
import string
import heapq
import time

from math import log2
from sre_constants import CHCODES



def textfileload(filename):    
    
    delStr = str.maketrans(dict.fromkeys(string.punctuation + string.digits))
    
    docfile = open(filename,encoding='utf_8',errors='ignore')
    textstr = docfile.read()
    textstr = textstr.lower()
    textstr = textstr.translate(delStr)
    textstr = textstr.lower()
    textstr = textstr.split()
    textstr = "".join(textstr)
    
    return textstr



def calculate_entropy(fredict,numsub=1):
    
    pdict = fredict.copy()
    
    
    
    for key in fredict.keys():
        p = fredict[key]/numsub
        pdict[key] = -log2(p)*p
    
    return sum(pdict.values())

def dictcount(dict,s,independent_ch_len = 1):  # @DontTrace @ReservedAssignment
    
    steplen = independent_ch_len
    numsub = 0
    
    for i in range(0,len(s),steplen):
        
        sub = s[i:i+steplen]
        #print(sub)
        if sub in dict.keys():
            dict[sub] += 1
        else:
            dict[sub] = 1
        
        numsub+=1
    
    return numsub

def testEntropy(numgram=1):
    
    filename = "sawyr10.txt"

    str = textfileload(filename)  # @ReservedAssignment
    frequencydict = {}
    numsub = dictcount(frequencydict,str,numgram)
    entro = calculate_entropy(frequencydict,numsub)
    
    #print(frequencydict)
    
    print("length of string:",len(str))
    print("sum of gram:",numsub)
    print("entropy:",entro)    
    print("num of types:",len(frequencydict.keys()))
    print("ideal size of bits",numsub*entro)
    print("ASCII code size",len(str)*8)      

    
    return 
    
    

class huffmanNode:
    
    def __init__ (self,freq,ch=None):
        self.ch = ch
        self.freq = freq
        self.left = None
        self.right = None
        self.parent = None
        
    def __le__(self,other):
        return self.freq <= other.freq    
    def __ge__(self,other):
        return self.freq >= other.freq
    def __lt__(self,other):
        return self.freq < other.freq
    def __gt__(self,other):
        return self.freq > other.freq
        
    
    @classmethod
    def buildtree(cls, freqdict):
        
        leaflist = []
        for key in freqdict.keys():
            #print("freq:",freqdict[key])
            heapq.heappush(leaflist,(freqdict[key],huffmanNode(freqdict[key],key)))
            #print("key",key)
        
        while(len(leaflist)>1):
            
            right = heapq.heappop(leaflist)[1]
            left = heapq.heappop(leaflist)[1]
            
            #print(right.freq)
            #print(left.freq)            
            
            parent = huffmanNode(right.freq+left.freq)
            #print("parent.ch",parent.ch)
            parent.left = left
            parent.right = right
            
            right.parent = parent
            left.parent = parent
            
            heapq.heappush(leaflist,(parent.freq,parent))
            
        leaflist[0][1].parent = None
        
        
        return leaflist[0][1]
    
    @classmethod
    def traversal(cls,node):
        
        #print(node.freq)
        if (node.ch is not None):
            print(node.freq)
            print(node.ch)
            return
        else:
            huffmanNode.traversal(node.left)
            huffmanNode.traversal(node.right)
        
        
        return
    
    @classmethod
    def encode(cls,node,codedict,parentcode=None):
        
        if node.ch is not None:
            
            
            #print(node.ch,"parentcode",parentcode)           
            codedict[node.ch] = parentcode

            return
                    
        if node.parent is None:
            
            leftcode = '0'
            rightcode = '1'
            huffmanNode.encode(node.left,codedict,leftcode)
            huffmanNode.encode(node.right,codedict,rightcode)
            
        else:
            leftcode = parentcode + '0'
            rightcode = parentcode + '1'          
            huffmanNode.encode(node.left,codedict,leftcode)
            huffmanNode.encode(node.right,codedict,rightcode)
        
        return codedict
    
    @classmethod
    def decode_str(cls,root,codedstr):
        first = 0
        chcodesize = 0
        result = ""
        sumchar = 0
        
        #print(codedstr)
        
        while (first<len(codedstr)):
            
            #print(codedstr[first])            
            char,chcodesize = huffmanNode.decode_char(root,codedstr,first,chcodesize)
            #print(char)
            result+=char
            first+=chcodesize
            chcodesize = 0
        
        #print(sumchar)
        return result
    
    @classmethod
    def decode_char(cls,node,codedstr,first,chcodesize):
        
        result = None        
        
        if node.ch is None:
            
            #print("first",first,"chcodedsize",chcodesize,"code",codedstr[first+chcodesize])
 
            if codedstr[first+chcodesize] == '0':
                chcodesize+=1
                result,chcodesize = huffmanNode.decode_char(node.left,codedstr,first,chcodesize)
            elif codedstr[first+chcodesize] == '1':
                chcodesize+=1
                result,chcodesize = huffmanNode.decode_char(node.right,codedstr,first,chcodesize)
                
        else:
            #print(node.ch)
            result = node.ch            
            return result,chcodesize        
        
        return result,chcodesize       
        
        

def textfileload_ASCII(filename):    
    
    #delStr = str.maketrans(dict.fromkeys(string.punctuation + string.digits))
    
    docfile = open(filename,encoding='utf_8',errors='ignore')
    textstr = docfile.read()

    
    return textstr
    
def testHuffman(numgram=1):
    
    filename = "sawyr10.txt"

    str = textfileload(filename)  # @ReservedAssignment
    frequencydict = {}
    numsub = dictcount(frequencydict,str,numgram)
     
    starttime = time.clock()
    huffmantree = huffmanNode.buildtree(frequencydict)
    endtime = time.clock()
    print("compress",endtime-starttime)

    codedict = {}
    huffmanNode.encode(huffmantree, codedict)
    
    codedstr = ""
    codednum = 0
    
    for ch_i in range(0,len(str),numgram):
        
        codedstr += codedict[str[ch_i:ch_i+numgram]]
        codednum += 1        
        
   
    
    print(numsub,codednum)    
    print(len(frequencydict.keys()))
    #print(codedict)
    print(len(codedstr),codedstr[0:10])
    
    
    #print(codedict['nd'])
    #print(codedict['we']) 
    starttime = time.clock()    
    decodedstr = huffmanNode.decode_str(huffmantree, codedstr)
    endtime = time.clock()
    print("decompress",endtime-starttime)
    
    print(len(str),len(decodedstr),decodedstr[0:10])
    
    print("compress radio", len(codedstr)/(len(str)*8))

    
    
    return



class LZ78_pair:
    
    def __init__ (self,pointer,length=1,lastch=None,testch = None):
        
        self.pointer = pointer
        self.length = length
        self.lastch = lastch
        self.testch = testch
        
    def __str__(self):
        
        return ""+str(self.pointer)+","+self.lastch 
        
    
    @classmethod    
    def LZ78Encode(cls,rawstr):
    
        codedict = {}
        coderesult =  []
        index = 1
        i = 0
        
        while i<len(rawstr):
            
            if rawstr[i] in codedict.keys():
                
                maxsublength = 1
                tempch = rawstr[i]
                tempindex = codedict[rawstr[i]]
                    
                for j in range(i+1,len(rawstr)):
                    if rawstr[i:j] in codedict.keys():                        
                        maxsublength = j-i+1                        
                        tempch = rawstr[j]
                        tempindex = codedict[rawstr[i:j]]                        
                    else:
                        maxsublength = j-i  
                        codedict[rawstr[i:j]] = index                       
                        index += 1
                        break
                
                pair = LZ78_pair(tempindex,maxsublength,tempch)
                coderesult.append(pair)
                i+=maxsublength

            else:
                pair = LZ78_pair(0,1,rawstr[i])                
                codedict[rawstr[i]] = index
                coderesult.append(pair)
              
                index += 1
                i+=1

        return coderesult
    
    @classmethod
    def LZ78Decode(cls,LZ78code):
        
        ostr = ""
        reverseddict = LZ78_pair.recovercodedict(LZ78code)
        
        for pair in LZ78code:
            if pair.pointer is 0:
                ostr += pair.lastch
            else:
                ostr += str(reverseddict[pair.pointer])
                ostr += str(pair.lastch)
        return ostr
    
    @classmethod
    def recovercodedict(cls,resultpairs):
        codedict = {}
        index = 1
        
        for pair in resultpairs:
            if pair.pointer is 0:
                codedict[index] = pair.lastch
                index+=1
            else:
                codedict[index] = codedict[pair.pointer]+pair.lastch
                index+=1
    
        
        return codedict
                
                

def testLZ78(testnum = 500, length = 100):

    filename = "sawyr10.txt"
    rawstr = textfileload(filename)
   
    starttime = time.clock() 
    coderesult = LZ78_pair.LZ78Encode(rawstr)
    endtime = time.clock()
    print("compress",endtime-starttime)
    
    
    reverseddict = LZ78_pair.recovercodedict(coderesult)
    
    starttime = time.clock() 
    result = LZ78_pair.LZ78Decode(coderesult)
    endtime = time.clock()
    print("decompress",endtime-starttime)

    
    print("Test with origin and decoded")
    print(rawstr[testnum:testnum+length])
    print(result[testnum:testnum+length])
    print(len(reverseddict))
    
    
    strbit = 24*len(coderesult)  
    
    print(strbit,len(coderesult),strbit/(8*len(rawstr)))

    return

def calculatewordentropy():
    
    freqvector = [ 0.1/i for i in range(1,12368)]
    entro = 0
    
    for p in freqvector:
        
        entro += -log2(p)*p
        
    print(entro)
    
    return


starttime = 0
endtime = 0

numgram = 3
#change this to change the number of gram, 3 denote trigram

print("Q1:")
starttime = time.clock()
testEntropy(numgram)
endtime = time.clock()
print("time",endtime-starttime)

print("Q2:")
testHuffman(numgram)

print("Q3:")
testLZ78(0,10)

print("Q5:")
calculatewordentropy()
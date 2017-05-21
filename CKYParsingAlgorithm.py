import numpy as np
### Developed by fromme0528@gmail.com
### Date : 17.05.18
### CKY(Cocke-Kasami-Younger) Parsing Algorithm used in NLP
### input : one sentence, grammar(CNF)
### output : parsing table

#Grammar class
class Grammar:
    head = None
    tail = []

#find a head and append tails
def findAndAdd(grammars, head, tail):
    flag = 0
    for grammar in grammars:
        if(grammar.head == head):
            grammar.tail.append(tail)
            flag = 1
            break
    if (flag == 0):
        g = Grammar()
        g.head = head
        g.tail = [tail]
        grammars.append(g)
    return grammars    

# construct grammar by input txt file
def readGrammer(filename) :
    f = open(filename,'r')
    grammars = []
    lines = f.readlines()
    for line in lines:
        a = line.split()
        findAndAdd(grammars,a[0],a[2])
        f.close()
    return grammars

#construct one sentence by input txt file
def readwords(filename):
    f = open(filename,'r')
    lines = f.readlines()
    result = lines[0].split()
    f.close()
    return result

#CKY Algorithm
#input : one sentence, grammar
#return parsing table
def CKYalgorithm(words, grammars):
    
    words_length  = len(words)
    
    #create table
    table = np.zeros((words_length, words_length+1,1))
    table = table.tolist()
    for i in range(0,words_length):
        for j in range(0,words_length+1):
            if 0 in table[i][j]:
                table[i][j].remove(0)
    
    #initial
    for i in range(1,words_length+1):
        for grammar in grammars:
            for tail in grammar.tail:
                if (words[i-1] == tail):
                    table[i-1][i].append(grammar.head)
    
    # parsing table
    for j in range(2,words_length+1):
        for i in range(j-2,-1,-1):
            for k in range(i+1,j):
                for w1 in table[i][k]:
                    for w2 in table[k][j]:                        
                        for grammar in grammars:
                            for tail in grammar.tail:
                                if (w1+w2 == tail):
                                    table[i][j].append(grammar.head)                
    return table

#main process
if __name__ == "__main__":
    print("---------------input----------------")

    grammars = readGrammer("CKY_CNF.txt")
    for grammar in grammars:
        print (grammar.head, grammar.tail)
    words = readwords("CKY_sentence.txt")
    words_length = len(words)
    print(words)
    
    print("---------------table----------------")

    table = CKYalgorithm(words, grammars)
   
    #print table
    for i in range(words_length):
        for j in range(words_length+1):
            print(table[i][j],end = "")
        print()
        
    print("---------------result----------------")
    if ('S' in table[0][words_length]):
        print("Accept")
    else:
        print("Denied")

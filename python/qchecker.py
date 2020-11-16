import crawling as cr
from collections import OrderedDict
import json
import aQlist

vlist = []
slist = []
slistlen = 0
elist = []

def makeResult():
    data = OrderedDict()
    data['alistlen'] = slistlen+len(vlist)
    data['vlistlen'] = len(vlist)
    data['vlist'] = vlist
    return json.dumps(data,ensure_ascii=False,indent="\t")

def getJSON(href,fname,query,war):
    data = OrderedDict()
    data["url"] = href.baseurl + href.url
    data["fname"] = fname
    data["query"] = query
    data["war"] = war
    return json.dumps(data,ensure_ascii=False,indent="\t")

def checkVOper(href): #check operater is worked in query
    global slistlen
    retlist = []
    for s in href.arglist :
        if(s.atype == "digit"):
            cq = str(( int(s.oval)+1)) + '-1'
            res1 = href.classmember(s.oval)
            res2 = href.classmember(cq)    
            if checkResSame(res1,res2) : 
                vlist.append(getJSON(href,s.name,cq,"low"))
            else : 
                slistlen += 1

def checkNormal(href,q):
    an = makeAnormal(href)
    res = href.classmember(q)
    # compare with anormal result.
    if checkResSame(an,res) : #this result is anormal 
        return False
    else :  #this result is normal 
        return True
        
def makeAnormal(href) : #find anormal result
    qlist = ['1','2','3','4','5','a','b','c','d','-1','a1','1a']
    nq = [] #save requests return  
    an = [] #save anormally returns
    
    for q in qlist :
        res = href.classmember(q)
        if checkError(res) :
            nq.append(res)
        # else :
        #     elist.append(getJSON(href,))

    rlen = len(nq)

    for i in range(0,rlen) :
        for j in range(0,rlen) :
            if i != j : 
                if checkResSame(nq[i],nq[j]) : 
                    an.append(nq[i])
                    an.append(nq[j])
                
    an = list(set(an))    
    nq = list(set(nq))
    qlist.remove(an)
    qlist.remove(nq)
    print(qlist)

    print(an)
    return an[0]

def checkResSame(res1,res2): #check res1 and res2 request result is same
    # res1 = href.classmember(q1)
    # res2 = href.classmember(q2)    
    q1 = res1[2]
    q2 = res2[2]
    
    if (res1[1] != res2[1])  : # two results return code is not same
        return False
    elif not (checkError(res1) and checkError(res1)) : 
        return False

    if len(q1) > len(q2): #check if string has includes the other one.
        q3 = q1.replace(q2,'')
    else : 
        q3 = q2.replace(q1,'')

    res = cr.show_diff(res1[0],res2[0])
    for s in res[1] : #s is differ parts
        if ((q1 != s ) and (q2 != s )  and (q3 != s )) : # two results are not same 
            return False
    # two results are same 
    return True 


def checkError(res): #check return code is 200 , sql error has not acquired
    error = ['Warning','mysql','error']
       
    if res[1] == 200 :
        if any(word in res[0] for word in error ) :
            return False 
        else :  #error was not acquired
            return True
    else :
        return False

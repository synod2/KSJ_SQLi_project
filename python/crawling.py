#-*- coding:utf-8 -*- 
from bs4 import BeautifulSoup as bs
import requests ,json, difflib, chardet
import sys
from tld import get_tld

global foo 

# ------------------------------------------------------------------
# -------------- SQL Injection Automation Tool V.0.01--------------- 
# ---------------- by KSJ 5th / Dragon Compass Team----------------- 
# ------------------------------------------------------------------
    # 단순 타이틀 출력
def title_print(sub, main):
    print("\n" + "="*100)
    print("                              *** [{}] {} *** ".format(sub, main))
    print("="*100)

def getinfo(url) :
    # gbaseurl 변수가 생성되고 인자로 받은 url이 저장된다.
    global gbaseurl
    gbaseurl = url
    
    # pageset 클래스에 gbaseurl을 인자로 넘겨서 mainpage 객체를 반환한다.
    mainpage = pageset(gbaseurl)
    return mainpage



# ------------------------------------------------------------------
# ----------------------- class declaration ------------------------ 
# ------------------------------------------------------------------


class pageset(): 
    def __init__ (self,url):

        # getsoup함수를 통해 soup객체와 정리된 url을 저장한다.
        self.soup,self.url = getsoup(url)         

        # getform함수를 통해 formset object list들을 flist에 저장한다. 
        self.flist = getform(self.soup)

        
        self.hreflist = getlinks(self.soup,self.url)
        
    def showdata(self): #make pageinfo
        print ("========== parent page ==========")
        print ("URL : "+gbaseurl)
        print ("============== forms ==============")
        i = 0
        for s in self.flist :
            print("target url "+"["+str(i)+"]"+" : ")
            s.showdata()
            i += 1
        i = 0
        print ("============== childpages ==============")
        for s in self.hreflist : 
            # s.getformset() # get childpages form information
            s.showdata()            
        print ("========================================")

    def setval(self,uidx,aidx,val) :
        self.flist[uidx].setval(aidx,val)       

    def dosqli(self,uidx) : 
        global s
        global cookies
        
        tmp = gbaseurl.rfind('/')
        target = gbaseurl[:tmp+1] + self.flist[uidx].url
        # print("gbase = "+gbaseurl[:tmp+1])
        attack_data = {}
        target = target.replace("https://","")
        target = target.replace("http://","")
        i = 0
        for f in self.flist[uidx].namelist : 
            attack_data[f] = self.flist[uidx].vallist[i]
            i += 1
        
        if self.flist[uidx].method == "POST" : 
            try :
                attack  = s.post("https://"+target,data=attack_data,cookies=cookies)
                normal  = s.post("https://"+target,cookies=cookies)
            except : 
                attack  = s.post("http://"+target,data=attack_data,cookies=cookies)
                normal  = s.post("http://"+target,cookies=cookies)
        else : 
            pass 

        attack.encoding = 'utf-8'
        normal.encoding = 'utf-8'

        diffres = show_diff(normal.text,attack.text)
        print(type(diffres[1]))
        return diffres

class formset(): #form dataset object
    def __init__ (self,url,name,ftype,method) : 
        self.url = url
        self.method = method
        self.namelist = []
        self.ftypelist = []
        self.vallist = []

        self.namelist.append(name)
        self.ftypelist.append(ftype)
        self.vallist.append("")

    def showdata(self):
        i = 0
        print (self.url + " \nmethod : " + self.method)
        print ("----- input info ----- ")
        for s in self.namelist : 
            print("["+str(i)+"]name : " + s + "\n   type : " + self.ftypelist[i])
            if(self.vallist[i] == "") : 
                print("   value : none")
            else : 
                print("   value : " + self.vallist[i])
            i += 1
             
    def addform(self,name,ftype):
        self.namelist.append(name)
        self.ftypelist.append(ftype)
        self.vallist.append("")

    def setval(self,idx,val) :
        self.vallist[idx] = val

class hrefset(): #sub href link dataset object
    def __init__ (self,url,baseurl) :
        self.url = url
        self.baseurl = baseurl
        self.formlist = []
        self.arglist = []
        self.Actionurl = ""
        self.method="GET"        
    
    def showdata(self):
        print ("----- href page info -----")
        print ("URL : "+self.url)
        print("URL2 : "+self.baseurl)
        if len(self.formlist) != 0 :
            print ("◇--- forms ---◇")
            for s in self.formlist :
                s.showdata()
        if len(self.arglist) != 0 :
            print ("◆--- args ---◆")
            for s in self.arglist : 
                s.showdata()
        print ("-------------------------")

    def getformset(self):
        self.tmppage = pageset(self.baseurl+self.url)
        for s in self.tmppage.flist:
            self.formlist.append(s)


# 수정해야함!!!!!!!!!!!!!!!!!!!!! http인지 https인지 끝에 붙여야 보낼수있음... 
    def classmember(self,args): #it returned response text, return code, query
        params = {}
        # print("="*30)
        URL = "http://" + self.baseurl + self.url
        # print(URL)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
        #AppleWebKit/537.36\
        #(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
        if(type(args) == "<class 'list'>"): 
            if(len(self.arglist) > len(args) ):
                for i in range(len(self.arglist)-len(args)) :
                    args.append("")
            else :
                for i in range(len(args)-len(self.arglist)) :
                    self.arglist.append("")
            i = 0
            for a in self.arglist:
                params[a.name] = args[i]
                i += 1
        else : 
            params = {self.arglist[0].name : args}
        info = s.get(URL, params = params ,headers = headers)
        # print("="*30)
        # print(params)
        return info.text, info.status_code, args
    
    def addargs(self,args):
        if self.findargs(args) :
            pass
        else : 
            # print ("argname : " + args.name)
            self.arglist.append(args)

    def findargs(self,args): #find same args already in this lists
        for s in self.arglist : 
            if s.name == args.name :
                return 1
        return 0
                    

class argset():
    def __init__ (self,atype,oval,name="none",url=""):
        self.atype = atype
        self.oval = oval
        self.name = name        
        self.url = url

    def showdata(self) :
        print ("args name : "+ self.name + " | args type : " + self.atype )

        
# ---------------------------------------------------------------------
# ----------------------- class declaration end ----------------------- 
# ---------------------------------------------------------------------

#sql 구분모듈. class 자체를 생성해서 쓴다기보다는 객체를 값 자체를 리넌받아서 사용
# 1. 이스케이프 사용여부 판단
# 2. http? https? 

# ---------------------------------------------------------------------
# ----------------------- funciton declaration ------------------------ 
# ---------------------------------------------------------------------

def show_diff(text, n_text):
    """
    http://stackoverflow.com/a/788780
    Unify operations between two compared strings seqm is a difflib.
    SequenceMatcher instance whose a & b are strings
    """
    seqm = difflib.SequenceMatcher(None, text, n_text)
    output= []
    diff = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("\033[31m" + seqm.b[b0:b1] + "\033[0m")
            diff.append(seqm.b[b0:b1])
        elif opcode == 'delete':
            output.append("\033[34m" + seqm.a[a0:a1] + "\033[0m")
            diff.append(seqm.a[a0:a1])
        elif opcode == 'replace':
            # seqm.a[a0:a1] -> seqm.b[b0:b1]
            output.append("\033[32m" + seqm.b[b0:b1] + "\033[0m")
            diff.append(seqm.b[b0:b1])
        else:
            print("unexpected opcode")
    return ''.join(output),diff

def parsescript(data,funcname):
    global gbaseurl

    # tmp에 gbaseur의 url을 대상으로 마지막/ 를 기준으로 잘라내서 저장한다.
    # http://pingu6615.phps.kr/ksj/legacy_admin.php
    # url => http://pingu6615.phps.kr/ksj/
    tmp = gbaseurl.rfind('/')
    title_print("main", tmp)
    url = gbaseurl[:tmp+1]
    title_print("url", url)

    #script = data = soup object
    scripts = data


    #soup객체에서 script를 찾는다.
    for s in scripts.findAll("script") : 
        try :
            #soup객체의 script => src속성을 loadjs에 저장
            loadjs = s.attrs['src'] #find from imported javascript files 
            if "http" in loadjs :
                req = requests.get(loadjs) 
            else : 
                req = requests.get(url+loadjs)                
            s = str(s)+req.text
        except:
            s = str(s)
        if funcname in s : 
            for l in s.split("\n") :
                # print("line"+l)
                if "action" in l : #find action target url in javascript function
                    target =  (l.split("\"")[1]) 
                if "method" in l : #find form method in javascript function
                    method =  (l.split("\"")[1]) 
                if "url" in l : #find target url in AJAX function 
                    target = (l.split("\"")[1]) 
                if "type" in l : #find form method in AJAX function 
                    method = (l.split("\"")[1]) 
    return target,method                 











def getsoup(baseurl): #for getting soup object 

    # baseurl을 인자로 글로벌 s, cookies 변수를 선언한다.
    global s
    global cookies


    # tmpURL에 baseurl을 백업하고 filter_str안의 html 헤더정보들을 공백으로 치환한다
    tmpURL = baseurl
    filter_str = ["https://","http://","www."]

    for f in filter_str:
        tmpURL = tmpURL.replace(f,"")

    requests.encoding = 'utf-8'


    # 세션을 생성한 후 해당 url의 정보를 req에 저장한다.
    s = requests.Session()
    try :
        req = s.post("http://"+tmpURL)
    except : 
        req = s.post("https://"+tmpURL)


    # 생성된 세션 정보는 cookeis 변수에 저장하고 req를 대상으로 soup객체를 생성한다.
    cookies = s.cookies.get_dict()
    soup = bs(req.text,'html.parser')


    # 최종적으로, soup객체와 tmpURL을 반환한다.
    return soup,tmpURL











def getform(data):    
    lists = [] 

    # data = soup객체
    soup = data
    getmethod = ""
    
    # input폼을 모두 찾는다. 
    for inputs in soup.findAll("input"):
        # 일반 폼일 경우
        try : 
            # 찾은 input의 부모엘리먼트 폼의 액션과 메소드, input의 이름을 각각 저장한다.
            getpar = inputs.find_parent('form')['action'] 
            getname = inputs.attrs['name']
            getmethod = inputs.find_parent('form')['method'] 

        # 부모엘리먼트가 form이 아니거나, 또는 온보드나 Ajax 객체일 경우
        # form에 action이 존재하지 않는다.
        except : 
            try : 
                # <input type="button" value="전송" onclick="doAction(this.form)">
                # => "doAction"
                getclick = inputs.attrs['onclick'].split("(")[0]

                # parsescript함수에 soup객체와 onclik폼 정보를 보낸다. //ma, mb 분석필요
                getpar,getmethod = parsescript(soup,getclick)                 
            except: 
                # 단순히 부모엘리먼트가 form이 아니어서 예외처리가 발생한 경우 패스
                pass 
            else : 
                # soup객체를 대상으로 검색을 진행해 input의 부모엘리먼트가 form 인지 div인지
                # 판별하여 tagtype에 저장한다.
                try :
                    inputs.find_parent('form').findAll("input")
                    tagtype = 'form'
                except : 
                    inputs.find_parent('div').findAll("input")
                    tagtype = 'div'
                

                for i in inputs.find_parent(tagtype).findAll("input") :
                    try : #filter form args
                        getname = i.attrs['name'] 
                    except :
                        pass
                    else :     
                        try : 
                            gettype = i.attrs['type']
                        except : 
                            gettype = "none"
                        isin = 0
                        for s in lists : 
                            # getpar과 s.url이 일치한다면 firmset클래스를 통해 addform = 리스트들을
                            # 추가하고 break ...
                            if getpar == s.url :
                                s.addform(getname,gettype)
                                isin = 1
                                break
                        if isin == 0 :
                            #formset 클래스들을 lists에 저장 / lists = formset class
                            # 달리지는 gettype을 기준으로 lists 리스트에 전부 추가
                            lists.append(formset(getpar,getname,gettype,getmethod))                           

        else :
            try : 
                gettype = inputs.attrs['type']
            except :
                gettype = "none"
            isin = 0
            for s in lists : 
                if getpar == s.url :
                    s.addform(getname,gettype)
                    isin = 1
                    break
            if isin == 0 :
                lists.append(formset(getpar,getname,gettype,getmethod))            

    # 최종적으로, formset object list들을 반환
    return lists 





def getlinks(data,url): #data : soup object
    linklist = [] 
    lists = [] # list wiil return 
    baseurl = url
    soup = data
    for link in soup.findAll("a") : #links filtering / sorting 
        if 'href' in link.attrs:
            tmp = link.attrs['href']
            if tmp in linklist :
                pass
            else :
                tmp = tmp.split(baseurl)
                if len(tmp) == 2 :
                    tmp = tmp[1]
                else :
                    tmp = tmp[0]

                tmp = tmp.split("?")               
                if(len(tmp) == 2) :  #if it contain GET method arguments
                    tmplist = tmp[1].split("&")
                    tmp = tmp[0]
                    for s in tmplist :
                        if (len(s.split("=")) != 1): 
                            argname = s.split("=")[0]
                            argval = s.split("=")[1]
                            if len(tmp)> 1 : 
                                if tmp[-1] == "/" : 
                                    tmp = tmp[:-1]
                            
                            if argval.isdigit() :
                                tmpArg = (argset("digit",argval,name=argname))
                            elif argval.isalnum() :
                                tmpArg = (argset("alnum",argval,name=argname))                            
                            else :
                                tmpArg = (argset("alpha",argval,name=argname))
                            
                            if(len(lists) == 0) : 
                                tmpset = hrefset(tmp,url)
                                tmpset.addargs(tmpArg)
                                lists.append(tmpset)
                            else :
                                isin = 0
                                for s in lists :
                                    if tmp == s.url :
                                        s.addargs(tmpArg)
                                        isin = 1
                                        break
                                if isin == 0:
                                    if "http" in tmp : #filter outer sites links
                                        pass 
                                    else :
                                        tmpset = hrefset(tmp,url)
                                        tmpset.addargs(tmpArg)
                                        lists.append(tmpset)                        
                else : #if it contain non-method arguments 
                    tmp = tmp[0]
                    n = tmp.rfind('/')
                    if tmp[n+1:].isdigit() :  # if it contain arguments 
                        isin = 0
                        tmpArg = (argset("digit",tmp[n+1:]))
                        tmp = tmp[:n]
                        for s in lists :
                            if tmp == s.url :
                                s.addargs(tmpArg)
                                isin = 1
                                break
                        if isin == 0:
                            if "http" in tmp : #filter outer sites links
                                pass 
                            else :
                                tmpset = hrefset(tmp,url)
                                tmpset.addargs(tmpArg)
                                lists.append(tmpset)
                    else : 
                        if len(tmp) > 1 : 
                            if tmp[-1] == "/" : 
                                tmp = tmp[:-1]
                            if tmp[0] == '#' or tmp == '/' or tmp[0] == ' ' :
                                pass
                            else : 
                                linklist.append(tmp)
    linklist = set(linklist)
    for res in linklist :
        if "http" in res : #filter outer sites links
            # print(res)
            pass
        else :
            lists.append(hrefset(res,url))
    # for s in lists : 
    #     print (s.url)
    return lists #return is hrefset object list



def getprotocol(tmpURL):
    s = requests.Session()
    try :
        req = s.post("http://"+tmpURL)
    except :
        req = s.post("https://"+tmpURL)



# ---------------------------------------------------------------------
# ----------------------- funciton declaration end -------------------- 
# ---------------------------------------------------------------------

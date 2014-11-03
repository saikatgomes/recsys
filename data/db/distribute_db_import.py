#!/usr/bin/python

import sys,glob,io,requests,json,time,datetime,os.path,socket,random,re
from lxml import html
from random import shuffle, randint

BASE_URL="http://imdb.com"
DATA_DIR="../data/tweet"
OUT_DIR="../data/imdb/parts"

RATING_ONLY=0;

C_COUNT=0
M_COUNT=0

MOVIES=[]

# current time for logging
def getTime(f=1):
    ts = time.time()
    fmt='%Y-%m-%d--%H-%M-%S-%f'
    dt=""
    if f==0:
        dt = datetime.datetime.fromtimestamp(ts).strftime(fmt)
    else:
        dt = datetime.datetime.fromtimestamp(ts).strftime(fmt)+"|"+socket.gethostname()+"|"+str(C_COUNT)+"|"+str(M_COUNT)+"|"
    return dt


def process():
    DIR="../imdb/parts"
    fileList=glob.glob(DIR+'/*.json')
    ln=len(fileList)
    idx=range(0,ln)
    shuffle(idx)
    for i in range(0,ln):
        aFile=fileList[idx[i]]
        f_num=aFile[aFile.find("_")+1:aFile.find(".json")]
        out_file=DIR+"/movies_"+f_num+".db_done"
        print("SRG: outfile->"+out_file)
        if os.path.isfile(out_file):
            print(getTime(1)+"Aleady processed "+aFile)
        else:
            lockfile=aFile+".lock"
            #print lockfile
            if os.path.isfile(lockfile):
                with open(lockfile,'r') as lk:
                    msg=lk.read()
                print(getTime(1)+aFile+" is "+msg)
            else:
                with open(lockfile,"w") as lk:
                    lk.write("Currently proccessed by "+socket.gethostname()) 
                print(getTime(1)+"Processing "+aFile)
                try:
                    #get_movie_url(aFile,out_file)
                    #CALL YOUR FUNCTION HERE
                    #ONCE IT IS DONE IMPORTING CREATE out_file
                    print("WILL BE PROCESSING "+aFile)
                except:
                    print "ERRR"
                    e=sys.exc_info()[0]
                    print e
                    fail_file=DIR+"/movies_"+f_num+".db_fail"
                    with open(fail_file,"w") as fl:
                        fl.write("Failed at "+socket.gethostname())
                        fl.write("ERROR:")
                        fl.write(e)
                os.remove(lockfile)


if __name__ == "__main__":
    process()
    #get_movie_url()

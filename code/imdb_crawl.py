import requests,json,time,datetime,os.path,socket,random,re
from lxml import html
from random import shuffle, randint

BASE_URL="http://imdb.com"
DATA_DIR="../data/tweet"

C_COUNT=0

MOVIES=[]

# current time for logging
def getTime(f=1):
    ts = time.time()
    fmt=""
    if f==1:
        fmt='%Y-%m-%d--%H-%M-%S-%f'
    else:
        fmt='%Y%m%d%H%M%S%f'
    dt = datetime.datetime.fromtimestamp(ts).strftime(fmt)+"--["+str(C_COUNT)+"]"
    return dt


def get_movie_url():
    global MOVIES
    movie_fName=DATA_DIR+"/movies.dat"
    try:
        with open(movie_fName,'r') as f:
            for line in f:
                myData=re.split('::',line)
                id=myData[0]
                title=myData[1][:len(myData[1])-7]
                year=myData[1][len(myData[1])-5:len(myData[1])-1]
                cat=re.split('\|',myData[2][:len(myData[2])-1])
                find_url=BASE_URL+"/find?ref_=nv_sr_fn&q="+title.replace(' ','+')+"&s=tt"
                find_url2=BASE_URL+"/find?q="+title.replace(' ','+')+"&s=tt"
                MOVIES.append({'id':id,'title':title,'year':year,'genre':cat,'url':find_url,'url2':find_url2})
            f.close()
            movie_json=DATA_DIR+"/movies.json"
            with open(movie_json,'w') as out_f:
                json.dump({'movies':MOVIES},out_f,indent=2,ensure_ascii=False,sort_keys=True)
            out_f.close()
    except (OSError, IOError) as e:
        print(getTime()+"ERROR: File "+movie_fName+" not found!")
        print(getTime()+"ERROR: Please run get_movie_tweeting_data.sh to get the Tweet Data")



if __name__ == "__main__":
    get_movie_url()

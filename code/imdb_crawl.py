import requests,json,time,datetime,os.path,socket,random,re
from lxml import html
from random import shuffle, randint

BASE_URL="http://imdb.com"
DATA_DIR="../data/tweet"
OUT_DIR="../data/imdb"

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


def get_movie_url():
    global MOVIES, M_COUNT
    movie_fName=DATA_DIR+"/movies.dat"
    err_fName=OUT_DIR+"/err_"+getTime(0)+".dat"
    err_file=open(err_fName,'w')
    try:
        with open(movie_fName,'r') as f:
            for line in f:
                M_COUNT=M_COUNT+1
                myData=re.split('::',line)
                id=myData[0]
                title=myData[1][:len(myData[1])-7]
                year=myData[1][len(myData[1])-5:len(myData[1])-1]
                cat=re.split('\|',myData[2][:len(myData[2])-1])
                find_url=BASE_URL+"/find?ref_=nv_sr_fn&q="+title.replace(' ','+')+"&s=tt"
                find_url2=BASE_URL+"/find?q="+title.replace(' ','+')+"&s=tt"
                cast_url=BASE_URL+"/title/tt"+id+"/fullcredits?ref_=tt_cl_sm#cast"
                main_url=BASE_URL+"/title/tt"+id+"/"
                main_page=requests.get(main_url)
                print(getTime()+"Crawling url: "+main_url)
                print(getTime()+"\t\tID: "+id)
                print(getTime()+"\t\tTitle: "+title)
                print(getTime()+"\t\tYear: "+year)
                msg=", ".join(cat)
                print(getTime()+"\t\tGenre: "+msg)
                tree = html.fromstring(main_page.text)
                # GET RATINGS
                rating = ""
                dom_rating=tree.xpath("//span[@itemprop='ratingValue']/text()")
                if len(dom_rating)==1:
                    rating=dom_rating[0]
                else:
                    err_file.write(getTime()+"ID:"+id+"|MSG:No_Ratings_Found")
                print(getTime()+"\t\tRatings: "+rating)
                # GET CAST ETC
                director=[]
                dom_dir=tree.xpath("//div[@itemprop='director']/a/span[@itemprop='name']/text()")
                if len(dom_dir)>0:
                    for d in dom_dir:
                        director.append(d)
                else:
                    err_file.write(getTime()+"ID:"+id+"|MSG:No_Directors_Found")
                msg=", ".join(director)
                print(getTime()+"\t\tDirector: "+msg)
                stars=[]
                dom_stars=tree.xpath("//div[@itemprop='actors']/a/span[@itemprop='name']/text()")
                if len(dom_stars)>0:
                    for d in dom_stars:
                        stars.append(d)
                else:
                    err_file.write(getTime()+"ID:"+id+"|MSG:No_Actors_Found")
                msg=", ".join(stars)
                print(getTime()+"\t\tActors: "+msg)
                # GET OTHERS
                recs=[]
                dom_recs=tree.xpath("//div[starts-with(@class,'rec_item')]/@data-tconst")
                if len(dom_recs)>0:
                    for d in dom_recs:
                        recs.append(d[2:])
                else:
                    err_file.write(getTime()+"ID:"+id+"|MSG:No_Recommendations_Found")
                msg=", ".join(recs)
                print(getTime()+"\t\tRecs: "+msg)
                MOVIES.append({'id':id,'title_tweet':title,'year_tweet':year,'genre_tweet':cat,'find_url':find_url,'find_url2':find_url2,'cast_url':cast_url,'url':main_url,'rating_imdb':rating})
            movie_json=OUT_DIR+"/movies.json"
            with open(movie_json,'w') as out_f:
                json.dump({'movies':MOVIES},out_f,indent=2,ensure_ascii=False,sort_keys=True)
    except (OSError, IOError) as e:
        print(getTime()+"ERROR: File "+movie_fName+" not found!")
        print(getTime()+"ERROR: Please run get_movie_tweeting_data.sh to get the Tweet Data")



if __name__ == "__main__":
    get_movie_url()

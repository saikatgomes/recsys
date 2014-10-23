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

def get_value(tree,scrap_str,err_file,id,att_name):
    aValue=""
    dom_obj=tree.xpath(scrap_str)
    if len(dom_obj)==1:
        aValue=dom_obj[0]
    else:
        err_file.write(getTime()+"ID:"+id+"|MSG:No_"+att_name+"_Found\n")
    print(getTime()+"\t\t\t"+att_name+": "+aValue)
    return aValue

def get_value_list(tree,scrap_str,err_file,id,att_name,PRINT=1):
    aValue=[]
    dom_obj=tree.xpath(scrap_str)
    if len(dom_obj)>0:
        for d in dom_obj:
            aValue.append(d)
    else:
        err_file.write(getTime()+"ID:"+id+"|MSG:No_"+att_name+"_Found\n")
    if PRINT==1:
        msg=", ".join(aValue)
        print(getTime()+"\t\t\t"+att_name+": "+msg)
    return aValue

def get_simple_value(obj,scrapy_str):
    value=""
    d=obj.xpath(scrapy_str)
    if len(d)>2:
        value=d[1].strip(" \n")
    return value

def get_link_value(obj,scrapy_str):
    value=""
    d=obj.xpath(scrapy_str)
    if len(d)>0:
        value=d[0]
    return value

def get_movie_url():
    global MOVIES, M_COUNT
    movie_fName=DATA_DIR+"/movies.dat"
    err_fName=OUT_DIR+"/err_"+getTime(0)+".dat"
    err_file=open(err_fName,'w')
    try:
        with open(movie_fName,'r') as f:
            for line in f:
                M_COUNT=M_COUNT+1
                # Parse Tweet Data
                myData=re.split('::',line)
                id=myData[0]
                title=myData[1][:len(myData[1])-7]
                year=myData[1][len(myData[1])-5:len(myData[1])-1]
                cat=re.split('\|',myData[2][:len(myData[2])-1])
                # URLs
                find_url=BASE_URL+"/find?ref_=nv_sr_fn&q="+title.replace(' ','+')+"&s=tt"
                find_url2=BASE_URL+"/find?q="+title.replace(' ','+')+"&s=tt"
                cast_url=BASE_URL+"/title/tt"+id+"/fullcredits?ref_=tt_cl_sm#cast"
                main_url=BASE_URL+"/title/tt"+id+"/"
                main_page=requests.get(main_url)
                tree = html.fromstring(main_page.text)
                print(getTime()+"Crawling url: "+main_url)
                print(getTime()+"\t\tTweet Data:")
                print(getTime()+"\t\t\tID: "+id)
                print(getTime()+"\t\t\tTitle: "+title)
                print(getTime()+"\t\t\tYear: "+year)
                msg=", ".join(cat)
                print(getTime()+"\t\t\tGenre: "+msg)
                # SCRAP FOR DATA
                print(getTime()+"\t\tIMDB Data:")
                rating = get_value(tree,"//span[@itemprop='ratingValue']/text()",err_file,id,"Ratings")
                director = get_value_list(tree,"//div[@itemprop='director']/a/span[@itemprop='name']/text()",err_file,id,"Director")
                stars=get_value_list(tree,"//div[@itemprop='actors']/a/span[@itemprop='name']/text()",err_file,id,"Actors")
                recs=get_value_list(tree,"//div[starts-with(@class,'rec_item')]/@data-tconst",err_file,id,"Recs")
                mpaa=get_value(tree,"//span[@itemprop='contentRating']/text()",err_file,id,"MPAA")
                keywords=get_value_list(tree,"//div[@id='titleStoryLine']/div[@itemprop='keywords']/a/span[@itemprop='keywords']/text()",err_file,id,"Keywords")
                lang=""
                gross=""
                runtime=""
                color=""
                aka=""
                budget=""
                details=get_value_list(tree,"//div[@id='titleDetails']/div[@class='txt-block']",err_file,id,"Detials",0)
                for d in details:
                    d_name=d.xpath("h4/text()")
                    if len(d_name)>0:
                        name=d_name[0]
                        if name=="Color:":
                            color=get_link_value(d,"a/text()")
                        elif name=="Budget:":
                            budget=get_simple_value(d,"text()")
                        elif name=="Language:":
                            lang=get_link_value(d,"a/text()")
                        elif name=="Gross:":
                            gross=get_simple_value(d,"text()")
                        elif name=="Runtime:":
                            runtime=get_link_value(d,"time/text()")
                        elif name=="Also Known As:":
                            aka=get_simple_value(d,"text()")
                print(getTime()+"\t\t\tLanguage: "+lang)
                print(getTime()+"\t\t\tColor: "+color)
                print(getTime()+"\t\t\tRuntime: "+runtime)
                print(getTime()+"\t\t\tBudget: "+budget)
                print(getTime()+"\t\t\tGross: "+gross)
                print(getTime()+"\t\t\tKnow As: "+aka)
                # STORE!
                MOVIES.append({\
                            'id':id,'title_tweet':title,'year_tweet':year,'genre_tweet':cat,'url':main_url, \
                            'rating_imdb':rating,'director_imdb':director,'actors_imdb':stars,'recs_imdb':recs, \
                            'mpaa_imdb':mpaa,'keywords':keywords,'language_imdb':lang,'color_imdb':color, \
                            'runtime_imdb':runtime,'budget_imdb':budget,'gross_imdb':gross,'also-known-as_imdb':aka \
                            })
            movie_json=OUT_DIR+"/movies.json"
            with open(movie_json,'w') as out_f:
                json.dump({'movies':MOVIES},out_f,indent=2,ensure_ascii=False,sort_keys=True)
    except (OSError, IOError) as e:
        print(getTime()+"ERROR: File "+movie_fName+" not found!")
        print(getTime()+"ERROR: Please run get_movie_tweeting_data.sh to get the Tweet Data")



if __name__ == "__main__":
    get_movie_url()

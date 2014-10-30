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

def get_link_value_list(obj,scrapy_str):
    value=[]
    d=obj.xpath(scrapy_str)
    if len(d)>0:
        value=d
    return value

def process():
    DIR="../data/imdb/parts"
    fileList=glob.glob(DIR+'/*.dat')
    ln=len(fileList)
    idx=range(0,ln)
    shuffle(idx)
    for i in range(0,ln):
        aFile=fileList[idx[i]]
        f_num=aFile[aFile.find("_")+1:aFile.find(".dat")]
        out_file=DIR+"/movies_"+f_num+".json"
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
                    get_movie_url(aFile,out_file)
                except:
                    print "ERRR"
                    e=sys.exc_info()[0]
                    print e
                    fail_file=DIR+"/movies_"+f_num+".fail"
                    with open(fail_file,"w") as fl:
                        fl.write("Failed at "+socket.gethostname())
                        fl.write("ERROR:")
                        fl.write(e)
                os.remove(lockfile)

def get_rating_info(id,err_file,rating,rating_count):
    rating_info=[]
    url="http://www.imdb.com/title/tt"+id+"/ratings?"
    print(getTime()+"\tCrawling url: "+url)
    main_page=requests.get(url)
    tree = html.fromstring(main_page.text)
    aLine=get_value_list(tree,"//div[@id='tn15content']/p/text()",err_file,id,"line1",0)
    line1=aLine[0]
    if (line1.startswith("No breakdown available for IMDb users.")):
       print(getTime()+"\t\tNo Ratings info avaiable")
       err_file.write(getTime()+"ID:"+id+"|MSG:No_RATINGS_Found\n")
    else:
       x=line1.find("IMDb")
       usr_count=line1[:x-1]
       r_count=rating_count.replace(',','')
       d=tree.xpath("//div[@id='tn15content']/table")
       t1=d[0]
       t2=d[1]
       #demo breakdown
       d1=t1.xpath("tr")
       d2=t2.xpath("tr")
       rating_value=[]
       rating_report=[]

       for X in range (1,len(d1)):
           n=d1[X].xpath("td/text()")
           rating_value.append({'value':n[2],'count':n[0]});
       Z=len(d2)-2
       for Y in range (1,len(d2)):
           if Y!=Z:           
               tb=d2[Y].xpath('td')
               if Y==(Z+1):
                   lbl=tb[0].xpath('text()')[0]
                   if lbl.startswith(" IMDb users"):
                       lbl="IMDb users"
                   else:
                       print(getTime()+"\t\t'IMDb users' expected but got '"+lbl+"'")
                       err_file.write(getTime()+"ID:"+id+"|MSG:No_IMDb_Users_Found\n")
               else:
                   lbl=tb[0].xpath('a/text()')[0]
               vote=tb[1].xpath('text()')[0]
               ave=tb[2].xpath('text()')[0]
               rating_report.append({'type':lbl,'votes':vote[1:],'average':ave[1:]})

       rating_info.append({'rating':rating,'rating_count':usr_count, \
                        'url':url,'ratings_breakdown':rating_value,'demo_breakdown':rating_report})
    return rating_info 


def get_movie_url(aFile,out_file):
    global MOVIES, M_COUNT
    movie_fName=aFile
    movie_json=out_file
    err_fName=OUT_DIR+"/err_"+getTime(0)+".err"
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
                print(getTime()+"Getting Info for ID="+id+" TITLE="+title+" YEAR="+year)
                # URLs
                find_url=BASE_URL+"/find?ref_=nv_sr_fn&q="+title.replace(' ','+')+"&s=tt"
                find_url2=BASE_URL+"/find?q="+title.replace(' ','+')+"&s=tt"
                cast_url=BASE_URL+"/title/tt"+id+"/fullcredits?ref_=tt_cl_sm#cast"
                main_url=BASE_URL+"/title/tt"+id+"/"
                main_page=requests.get(main_url)
                tree = html.fromstring(main_page.text)
                print(getTime()+"\t\tTweet Data:")
                print(getTime()+"\t\t\tID: "+id)
                print(getTime()+"\t\t\tTitle: "+title)
                print(getTime()+"\t\t\tYear: "+year)
                msg=", ".join(cat)
                print(getTime()+"\t\t\tGenre: "+msg)
                # SCRAP FOR DATA
                print(getTime()+"\tCrawling url: "+main_url)
                print(getTime()+"\t\tIMDB Data:")
                rating = get_value(tree,"//span[@itemprop='ratingValue']/text()",err_file,id,"Ratings")
                rating_count = get_value(tree,"//span[@itemprop='ratingCount']/text()",err_file,id,"Ratings_Count")
                #rating_count = rating_count.repace(',','')
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
                rel_date=""
                prod_co=""
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
                        elif name=="Release Date:":
                            rel_date=get_simple_value(d,"text()")
                        elif name=="Gross:":
                            gross=get_simple_value(d,"text()")
                        elif name=="Runtime:":
                            runtime=get_link_value(d,"time/text()")
                        elif name=="Also Known As:":
                            aka=get_simple_value(d,"text()")
                            aka=aka.strip(" \n")
                        elif name=="Production Co:":
                            prod_co=get_link_value_list(d,"span[@itemprop='creator']/a/span[@itemprop='name']/text()")
                print(getTime()+"\t\t\tLanguage: "+lang)
                print(getTime()+"\t\t\tRelease: "+rel_date)
                print(getTime()+"\t\t\tColor: "+color)
                print(getTime()+"\t\t\tRuntime: "+runtime)
                print(getTime()+"\t\t\tBudget: "+budget)
                print(getTime()+"\t\t\tGross: "+gross)
                print(getTime()+"\t\t\tKnow As: "+aka)
                msg = ", ".join(prod_co)
                print(getTime()+"\t\t\tProd Co: "+msg)
                #RATINGS
                rating_info=get_rating_info(id,err_file,rating,rating_count)
                # STORE!
                MOVIES.append({\
                            'id':id,'title_tweet':title,'year_tweet':year,'genre_tweet':cat,'url':main_url, \
                            'rating_imdb':rating,'director_imdb':director,'actors_imdb':stars,'recs_imdb':recs, \
                            'mpaa_imdb':mpaa,'keywords':keywords,'language_imdb':lang,'color_imdb':color, \
                            'runtime_imdb':runtime,'budget_imdb':budget,'gross_imdb':gross,'also-known-as_imdb':aka, \
                            'release_date_imdb':rel_date,'production_co_imdb':prod_co,'ratings_info_imdb':rating_info \
                            })
                if M_COUNT%3==0:
                    time.sleep(1)
            print(getTime()+"Writing to file ...")
            with open(movie_json,'w') as out_f:
                time.sleep(1)
                json.dump({'movies':MOVIES},out_f,indent=2,sort_keys=True) #.encode('utf8')
    except (OSError, IOError) as e:
        print(getTime()+"ERROR: File "+movie_fName+" not found!")
        print(getTime()+"ERROR: Please run get_movie_tweeting_data.sh to get the Tweet Data")
    err_file.close()


if __name__ == "__main__":
    process()
    #get_movie_url()

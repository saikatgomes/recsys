import json,time,datetime,os.path,glob

DATA=[]

IN_DIR="../data/imdb/parts"
OUT_DIR="../data/imdb"

L_COUNT=0
T_COUNT=0

fileList=glob.glob(IN_DIR+"/movies_*.json")
fileList.sort()
t=len(fileList)
c=0

for file in fileList:
    c=c+1
    json_data=open(file)
    data=json.load(json_data)
    aList=data.get('movies')
    L_COUNT=len(aList)
    T_COUNT=T_COUNT+L_COUNT
    print(str(c)+"/"+str(t)+"\tProcessing "+file+" \t\t[movie count="+str(L_COUNT)+"] \t[total count="+str(T_COUNT)+"]")
    DATA.extend(aList)

with open(OUT_DIR+'/all_movies.json',"w") as f:
    print("Writing to file ..")
    json.dump({'movies':DATA},f,indent=4)
    print("Done!!!")

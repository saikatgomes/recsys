import json
import sys,glob,io,requests,time,datetime,os.path,socket,random,re
from lxml import html
from random import shuffle, randint

DATA=[]

IN_DIR="../data/new"
OUT_DIR="../data/imdb"
IN_FILE="training.dat"
OUT_FILE="new_tweet_data.json"

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

def read_the_dataset(the_dataset_file,outfile):
    tweets = list()
    header = True
    count=0;
    with file(the_dataset_file,'r') as infile:
        for line in infile:
            if header:
                header = False
                continue #skip the CSV header line
            count=count+1
            line_array = line.strip().split(',')
            user_id = line_array[0]
            item_id = line_array[1]
            rating = line_array[2]
            scraping_time = line_array[3]
            tweet = ','.join(line_array[4:])
            json_obj = json.loads(tweet) # Convert the tweet data string to a JSON object
            print(str(count)+"] Reading user_id="+user_id+" item_id="+item_id+" rating="+rating);
            tweets.append((user_id, item_id, rating, scraping_time, json_obj))
    with open(outfile,"w") as f:
		print("Writing to file ..")
		json.dump({'Tweets':tweets},f,indent=4)
    print("Done!!!")  


if __name__ == "__main__":
	global IN_DIR,IN_FILE,OUT_DIR,OUT_FILE
	read_the_dataset(IN_DIR+"/"+IN_FILE,OUT_DIR+"/"+OUT_FILE)

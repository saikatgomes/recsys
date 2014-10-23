import io,requests,json,time,datetime,os.path,socket,random,re

IN_DIR="../data/tweet"
OUT_DIR="../data/imdb/parts"

SPLITS=25

def combine_files():
    movie_fName=IN_DIR+"/movies.dat"
    count=1;
    try:
        with open(movie_fName,'r') as in_f:
            out_fName=OUT_DIR+"/movies_"+str(count)+".dat"
            out_f=open(out_fName,'w')
            print("INFO: Writing to "+out_fName)
            for l in in_f:
                out_f.write(l)
                count=count+1
                if count%SPLITS==0:
                    out_f.close()
                    out_fName=OUT_DIR+"/movies_"+str(count)+".dat"
                    out_f=open(out_fName,'w')
                    print("INFO: Writing to "+out_fName)
            out_f.close()
    except (OSError, IOError) as e:
        print("ERROR: File "+movie_fName+" not found!")
        print("ERROR: Please run get_movie_tweeting_data.sh to get the Tweet Data")

















if __name__ == "__main__":
    combine_files()

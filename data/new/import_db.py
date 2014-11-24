import json
import sqlite3

conn = sqlite3.connect('../recsys.db')
print "database opened successfully"


f = open("missing_imdb_data.txt", 'w')

#refer http://www.tutorialspoint.com/sqlite/sqlite_python.htm

#json_data = open("small_tweet_data.json").read()
json_data = open("new_tweet_data.json").read()
data = json.loads(json_data).get("Tweets")
t_id = 1

for x in data:
	user_id = x[0]
	item_id = x[1]
	rating = x[2]
	scrap_time = x[3]
	
	tweet_data = x[4]
	favorite_count = tweet_data['favorite_count']
	retweeted = tweet_data['retweeted']
	
	user_info = tweet_data['user']
	followers_count = user_info['followers_count']
	friends_count = user_info['friends_count']
	statuses_count = user_info['statuses_count']
	language = user_info['lang']
	favourites_count = user_info['favourites_count']
	created_at = user_info['created_at']
	time_zone = user_info['time_zone']
	listed_count = user_info['listed_count']

	tweet_created_at = tweet_data['created_at']
	
	insert_stmnt = "INSERT INTO TWEETER VALUES(" + str(t_id) +"," + str(user_id) + "," +  str(item_id) + "," + str(rating) + "," + str(scrap_time) + ","  + str(favorite_count) + ",\"" + str(retweeted) + "\"," + str(followers_count) + "," + str(friends_count) + "," +  str(statuses_count) + ",\"" + str(language) + "\"," + str(favourites_count) + ",\"" + str(created_at) + "\",\"" + str(time_zone) + "\"," + str(listed_count) + ",\"" + str(tweet_created_at) + "\");"
	print insert_stmnt
#	print insert_stmnt
  	conn.execute(insert_stmnt)
	conn.commit();
	print t_id
	t_id += 1	
	
	select_stmnt = "SELECT * FROM MOVIES WHERE M_id = " + str(item_id) + ";"
        exist = conn.execute(select_stmnt).fetchall();
	if len(exist) == 0:
		f.write(item_id + "\n")
f.close()
conn.close()
print "All done"	

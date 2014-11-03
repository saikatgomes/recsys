import json
import sqlite3

conn = sqlite3.connect('recsys.db')
print "database opened successfully"

#refer http://www.tutorialspoint.com/sqlite/sqlite_python.htm

json_data = open("all_movies.json").read()
#json_data = open("small.json").read()
data = json.loads(json_data).get("movies")
#global variables
g_id = 1;
d_id = 1;
a_id = 1;
p_id = 1;
r_id = 1;

f = open("duplicated_m_id.txt", 'w')
f1 = open("value_changed.txt", 'w')
for x in data:

	# MOVIES
	M_id = x['id']
	select_stmnt = "SELECT * from MOVIES WHERE M_id = " + str(M_id) + ";"
	exist = conn.execute(select_stmnt).fetchall();
	print "M_id is " + M_id
	if len(exist) == 0:
		insert_stmnt = "INSERT INTO MOVIES VALUES ("+ M_id + ",\"" + x['budget_imdb'] + "\",\"" + x['color_imdb'] + "\",\"" + x['title_tweet'] + "\",\"" + x['mpaa_imdb'] + "\",\""+ x['url'] + "\",\"" + x['gross_imdb'] + "\",\"" + x['language_imdb'] + "\",\""+ x['also-known-as_imdb'] + "\","+ x['year_tweet'] + ",\""+ x['runtime_imdb'] + "\",\"" + x['release_date_imdb'] + "\");";
		conn.execute(insert_stmnt);

	elif len(exist) == 1:
		f.write(M_id + "\n")

#RECS
	rank = 1;
	for rec in x['recs_imdb']:
		insert_stmnt = "INSERT INTO RECS VALUES (" + str(M_id) + ",\"" + rec[2:] + "\"," + str(rank) + ");"
		conn.execute(insert_stmnt)
		rank += 1;

#GENRE & GENRE_LIST
	for g_name in x['genre_tweet']:
		select_stmnt = "SELECT G_id from GENRE WHERE G_name = \"" + g_name + "\";"
		exist = conn.execute(select_stmnt).fetchall();
	
		if len(exist) == 0:
			insert_stmnt = "INSERT INTO GENRE VALUES (" + str(g_id) + ",\"" + g_name + "\");"
			conn.execute(insert_stmnt);
			cur_id = g_id;
			g_id += 1;
		elif len(exist) == 1:
			cur_id = exist[0][0];
		else:
			print "Heads up: error"
			sys.exit(0)
	
	#insert into GENRE_LIST
		insert_stmnt = "INSERT INTO GENRE_LIST VALUES (" + str(M_id) + "," + str(cur_id) + ");"
		conn.execute(insert_stmnt)
	
# DIRECTOR & DIRECTOR_LIST
	for d_name in x['director_imdb']:
		select_stmnt = "SELECT D_id from DIRECTOR WHERE D_name = \"" + d_name + "\";"
		exist = conn.execute(select_stmnt).fetchall();
	
		if len(exist) == 0:
			insert_stmnt = "INSERT INTO DIRECTOR VALUES (" + str(d_id) + ",\"" + d_name + "\");"
			conn.execute(insert_stmnt);
			cur_id = d_id;
			d_id += 1;
		elif len(exist) == 1:
			cur_id = exist[0][0];
		else:
			print "Heads up: error"
			sys.exit(0)
	
	#insert into DIRECTOR_LIST
		insert_stmnt = "INSERT INTO DIRECTOR_LIST VALUES (" + str(M_id) + "," + str(cur_id) + ");"
		conn.execute(insert_stmnt)
	
# ACTOR & ACTOR_LIST
	for a_name in x['actors_imdb']:
		select_stmnt = "SELECT A_id from ACTOR WHERE A_name = \"" + a_name + "\";"
		exist = conn.execute(select_stmnt).fetchall();
	
		if len(exist) == 0:
			insert_stmnt = "INSERT INTO ACTOR VALUES (" + str(a_id) + ",\"" + a_name + "\");"
			conn.execute(insert_stmnt);
			cur_id = a_id;
			a_id += 1;
		elif len(exist) == 1:
			cur_id = exist[0][0];
		else:
			print "Heads up: error"
			sys.exit(0)
	
	#insert into ACTOR_LIST
		insert_stmnt = "INSERT INTO ACTOR_LIST VALUES (" + str(M_id) + "," + str(cur_id) + ");"
		conn.execute(insert_stmnt)
	
# KEYWORDS_LIST
	for keyword in x['keywords']:
		if "'" in keyword and "\"" in keyword:
			f1.write(M_id + ": [keywords] " + keyword)
			var = "'" + keyword.replace("'", "\"") + "'"
			f1.write("<---->" + keyword + "\n")
                elif "'" in keyword:
                        var = "\"" + keyword + "\""
                else:
                        var = "\'" + keyword + "\'"
		insert_stmnt = "INSERT INTO KEYWORDS_LIST VALUES (" + str(M_id) + "," + var + ");"
		conn.execute(insert_stmnt)

# PRODUCTION & PRODUCTION_LIST
	for p_name in x['production_co_imdb']:
		if "'" in p_name and "\"" in p_name:
			f1.write(M_id + ": [production co] " + p_name )
			var = "'" + p_name.replace("'", "\"") + "'"
			f1.write("<---->" + p_name + "\n")
		elif "'" in p_name:
			var = "\"" + p_name + "\""
		else:
			var = "\'" + p_name + "\'"
		select_stmnt = "SELECT P_id from PRODUCTION WHERE P_name = " + var + ";"
			
		exist = conn.execute(select_stmnt).fetchall();

		if len(exist) == 0:
			insert_stmnt = "INSERT INTO PRODUCTION VALUES (" + str(p_id) + "," + var + ");"
			conn.execute(insert_stmnt);
			cur_id = p_id;
			p_id += 1;
		elif len(exist) == 1:
			cur_id = exist[0][0];
		else:
			print "Heads up: error"
			sys.exit(0)

		#insert into DIRECTOR_LIST
		insert_stmnt = "INSERT INTO PRODUCTION_LIST VALUES (" + str(M_id) + "," + str(cur_id)+ ");"
		conn.execute(insert_stmnt)

# Ratings
#print "test is" + x['ratings_info_imdb']
	if x['ratings_info_imdb']:
		ratings = x['ratings_info_imdb'][0]
		#	print  ratings
		# RATING_INFO
		insert_stmnt = "INSERT INTO RATING_INFO VALUES (" + str(M_id) + "," + str(r_id) + ",\""+ ratings['url'] + "\",\"" + ratings['rating'] + "\",\"" + ratings['rating_count'] + "\");"
		conn.execute(insert_stmnt);

	# RATING_BREAKDOWNS
		if ratings['ratings_breakdown']:
			r_bd = ratings['ratings_breakdown']
			for pair in r_bd:
				insert_stmnt = "INSERT INTO RATING_BREAKDOWNS VALUES (" + str(r_id) + ",\"" + pair['count'] + "\",\"" + pair['value'] + "\");"
				conn.execute(insert_stmnt);

#DEMO_BREAKDOWN
		if ratings['demo_breakdown']:
			d_bd = ratings['demo_breakdown']
			for pair in d_bd:
				insert_stmnt = "INSERT INTO DEMO_BREAKDOWN VALUES (" + str(r_id) + ",\"" + pair['average'] + "\",\"" + pair['type'] + "\",\"" + pair['votes'] + "\");"
				conn.execute(insert_stmnt);

		r_id += 1;

#conn.execute(insert_stmnt); 

#commit for every data['movies'] array
	conn.commit();

conn.close()
f.close()
f1.close()
print "All done"


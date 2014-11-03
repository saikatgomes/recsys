BEGIN TRANSACTION;
CREATE TABLE MOVIES(M_id int,
		    Budget VARCHAR (255),
		    Color VARCHAR (255),
		    Title VARCHAR(2048),
		    Mpaa VARCHAR (255),
		    Url VARCHAR(1023),
		    Gross VARCHAR(255),
		    Language VARCHAR(255),
		    AKA VARCHAR(255),
		    Year int,
		    Runtime VARCHAR(255),
		    Release_date_country VARCHAR(255),
		    PRIMARY KEY (M_id));
CREATE TABLE RECS(M_id int,
		  R_id int,
		  rank VARCHAR(255),
		  FOREIGN KEY (M_id) REFERENCES MOVIES(M_id));
CREATE TABLE GENRE(G_id int,
		   G_name VARCHAR(255),
		   PRIMARY KEY(G_id));
CREATE TABLE GENRE_LIST(M_id int,
			G_id int,
			FOREIGN KEY (M_id) REFERENCES MOVIES(M_id),
			FOREIGN KEY (G_id) REFERENCES GENRE(G_id));
CREATE TABLE DIRECTOR(D_id int, 
		      D_name VARCHAR (255),
		      PRIMARY KEY (D_id));
CREATE TABLE DIRECTOR_LIST(M_id int,
			   D_id int, 
			   FOREIGN KEY(M_id) REFERENCES MOVIES(M_id),
			   FOREIGN KEY(D_id) REFERENCES DIRECTOR(D_id));
CREATE TABLE ACTOR (A_id int,
		    A_name VARCHAR (255),
		    PRIMARY KEY (A_id));
CREATE TABLE ACTOR_LIST(M_id int,
			A_id int, 
			FOREIGN KEY(M_id) REFERENCES MOVIES(M_id),
			FOREIGN KEY(A_id) REFERENCES ACTOR(A_id));
CREATE TABLE KEYWORDS_LIST(M_id int,
			   KeyWord VARCHAR(255),
			   FOREIGN KEY(M_id) REFERENCES MOVIES(M_id));
CREATE TABLE PRODUCTION(P_id int, 
       	     	        P_name VARCHAR(255),
    			PRIMARY KEY (P_id));
CREATE TABLE PRODUCTION_LIST(M_id int, 
       	     	             P_id int, 
			     FOREIGN KEY (M_id) REFERENCES MOVIES(M_id),
			     FOREIGN KEY (P_id) REFERENCES PRODUCTION(P_id));
CREATE TABLE RATING_INFO(M_id int, 
       	     		 R_id int, 
			 Url VARCHAR(255),
			 Rating float,
			 Rating_count int,
			 PRIMARY KEY (R_id),
			 FOREIGN KEY (M_id) REFERENCES MOVIES(M_id));
CREATE TABLE  RATING_BREAKDOWNS(R_id int, 
       	      			Count int, 
				Value int,
				FOREIGN KEY (R_id) REFERENCES RATING_INFO(R_id));
CREATE TABLE DEMO_BREAKDOWN (R_id int, 
       	     		     Average float,
			     Type VARCHAR(255),
			     Votes int,
			     FOREIGN KEY (R_id) REFERENCES RATING_INFO(R_id));
       	      			     
END TRANSACTION;

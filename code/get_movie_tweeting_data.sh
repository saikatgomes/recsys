mkdir -p ../data
mkdir -p ../data/tweet
mkdir -p ../data/tweet/backup
mkdir -p ../data/imdb
mkdir -p ../data/imdb/parts
mkdir -p ../data/imdb/parts/backup
mkdir -p ../data/db

cd ../data/tweet
cp --backup=numbered *.dat backup/.

wget -N https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/movies.dat
wget -N https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/users.dat
wget -N https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/ratings.dat

ls -lrth

cd ../imdb/parts
cp --backup=numbered *.dat backup/.
#hopefully no lock files
rm -f movies*.dat

cd ../../../code

python split_movies_list.py 



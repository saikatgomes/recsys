mkdir -p logs
#cmd="cd `pwd`; echo \`pwd\` >&2; python crawl_kbb.py"
cmd="#!/bin/bash
cd /afs/cs.wisc.edu/u/s/a/saikat/public/html/projects/recsys/code; 
echo \`pwd\` >&2;
python imdb_crawl.py;
"
echo $1
sleep_time=1000000
if [ "$1" = "kill" ];
then
    echo "Killing all"
    cmd="
#!/bin/bash
kill -9 \`ps -ef | grep imdb_crawl.py | grep -v 'grep' | awk '{print \$2}'\`
"
    sleep_time=100000
fi

echo $cmd
for X in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20
do
    Y=adelie-$X
    Z=galapagos-$X
    ssh $USER@$Y 'bash -s' "$cmd" > logs/remote_log_$Y.txt &
    usleep $sleep_time
    ssh $USER@$Z 'bash -s' "$cmd" > logs/remote_log_$Z.txt &
    usleep $sleep_time
done


#!/bin/bash
procID=`ps -aux | awk '$11=="python"{print $1,$2, $11,$12}' | grep 'crawler_run'`
if [ "" == "$procID" ];
then
killall -9 phantomjs
killall -9 python
python /home/lml/webcrawler/webcrawler-nlp/crawler/crawler/crawler_run.py start
fi



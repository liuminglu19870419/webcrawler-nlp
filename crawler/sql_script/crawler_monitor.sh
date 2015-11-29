#!/bin/bash
procID=`pgrep "python /home/lml/webcrawler/webcrawler-nlp/crawler/crawler/crawler_run.py start"`
if [ "" == "$procID" ];
then
python /home/lml/webcrawler/webcrawler-nlp/crawler/crawler/crawler_run.py start
fi



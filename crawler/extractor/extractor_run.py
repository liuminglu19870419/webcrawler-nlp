#encoding: utf-8
'''
Created on 2015年11月18日

@author: lml
'''

import sys
import traceback
from extractor.HuanQiuExtractor import HuanQiuExtractor
sys.path.append("../")
sys.path.append("../../")
sys.path.append("/home/lml/webcrawler/webcrawler-nlp/crawler/")

from extractor.YouminExtractor import YouminExtractor
from extractor.NetEaseExtractor import NetEaseExtractor
from extractor.NetEaseExtractorA import NetEaseExtractorA
from utils.daemon import Daemon, daemon_main
import os
from config.LogConfig import LOGGER_EXTRACTOR as LOGGER
from extractor.NetEaseExtractorTech import NetEaseExtractorTech
from extractor.NetEaseExtractorPlay import NetEaseExtractorPlay
from extractor.NetEaseExtractorMili import NetEaseExtractorMili
from extractor.SinaExtractor import SinaExtractor
from extractor.SinaExtractorRoll import SinaExtractorRoll
from extractor.SinaExtractorGame import SinaExtractorGame
from extractor.SinaExtractorGamer import SinaExtractorGamer
from extractor.SinaExtractorGameTV import SinaExtractorGameTV
from extractor.SinaExtractorNewGame import SinaExtractorNewGame
from extractor.ChinaNewsExtractor import ChinaNewsExtractor

extractor_source_url_config = [
         {
          "url": "http://news.163.com/world/",
          "extractor": NetEaseExtractor,
          "tag":"163",
          "sub_tag":"world",
          "period": 10
          },
                                    
         {
          "url": "http://news.163.com/domestic/",
          "extractor": NetEaseExtractorA,
          "tag":"163",
          "sub_tag":"domestic",
          "period": 10
          },
                                    
         {
          "url": "http://news.163.com/shehui/",
          "extractor": NetEaseExtractorA,
          "tag":"163",
          "sub_tag":"shehui",
          "period": 10
          },
    
         {
          "url": "http://tech.163.com/latest",
          "extractor": NetEaseExtractorTech,
          "tag":"163",
          "sub_tag":"tech",
          "period": 10
          },
   
          {
          "url": "http://play.163.com/",
          "extractor": NetEaseExtractorPlay,
          "tag":"163",
          "sub_tag":"play",
          "period": 10
          },
   
          {
          "url": "http://war.163.com/special/millatestnews/",
          "extractor": NetEaseExtractorMili,
          "tag":"163",
          "sub_tag":"mili",
          "period": 10
          },
                                 
          {
          "url": "http://ol.gamersky.com/",
          "extractor": YouminExtractor,
          "tag":"youmin",
          "sub_tag":"online",
          "period": 10
          },
                                
         {
          "url": "http://www.gamersky.com/pcgame/",
          "extractor": YouminExtractor,
          "tag":"youmin",
          "sub_tag":"pcgame",
          "period": 10
          },
                                
         {
          "url": "http://tv.gamersky.com/",
          "extractor": YouminExtractor,
          "tag":"youmin",
          "sub_tag":"tvgame",
          "period": 10
          },
  
        {
         "url": "http://roll.news.sina.com.cn/s/channel.php?ch=01#col=90&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=1",
         "extractor": SinaExtractorRoll,
         "tag":"sina",
         "sub_tag":"domestic",
         "period": 10
         },
                                 
        {
         "url": "http://roll.news.sina.com.cn/s/channel.php?ch=01#col=91&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=1",
         "extractor": SinaExtractorRoll,
         "tag":"sina",
         "sub_tag":"world",
         "period": 10
         },
                                 
        {
         "url": "http://roll.news.sina.com.cn/s/channel.php?ch=01#col=92&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=1",
         "extractor": SinaExtractorRoll,
         "tag":"sina",
         "sub_tag":"shehui",
         "period": 10
         },
   
        {
         "url": "http://roll.news.sina.com.cn/s/channel.php?ch=01#col=93&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=1",
         "extractor": SinaExtractorRoll,
         "tag":"sina",
         "sub_tag":"mili",
         "period": 10
         },            
  
         {
          "url": "http://roll.news.sina.com.cn/s/channel.php?ch=01#col=94&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=1",
          "extractor": SinaExtractorRoll,
          "tag":"sina",
          "sub_tag":"sport",
          "period": 10
          },
                                 
         {
          "url": "http://roll.news.sina.com.cn/s/channel.php?ch=01#col=95&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=1",
          "extractor": SinaExtractorRoll,
          "tag":"sina",
          "sub_tag":"yule",
          "period": 10
          },
         {
         "url": "http://roll.news.sina.com.cn/s/channel.php?ch=01#col=96&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=1",
         "extractor": SinaExtractorRoll,
         "tag":"sina",
         "sub_tag":"tech",
         "period": 10
         },                      
        {
         "url": "http://games.sina.com.cn/y/",
         "extractor": SinaExtractorGame,
         "tag":"sina",
         "sub_tag":"play",
         "period": 10
         },     
  
        {
        "url": "http://api.g.sina.com.cn/pgame/get_kan_news_index/?index=1",
        "extractor": SinaExtractorGamer,
        "tag":"sina",
        "sub_tag":"play",
        "period": 10
        },     
              
        {
        "url": "http://kf.games.sina.com.cn/dianwan/dianwan/iframe_hot_news",
        "extractor": SinaExtractorGameTV,
        "tag":"sina",
        "sub_tag":"play",
        "period": 10
        },    
        {
        "url": "http://games.sina.com.cn/newgame/",
        "extractor": SinaExtractorNewGame,
        "tag":"sina",
        "sub_tag":"play",
        "period": 10
        },     
 
        {
        "url": "http://www.chinanews.com/importnews.html",
        "extractor": ChinaNewsExtractor,
        "tag":"chinanews",
        "sub_tag":"yaowen",
        "period": 10
        },     
                                        {
         "url": "http://www.chinanews.com/china.shtml",
         "extractor": ChinaNewsExtractor,
         "tag":"chinanews",
         "sub_tag":"domestic",
         "period": 10
         },     
                                        {
         "url": "http://www.chinanews.com/world/",
         "extractor": ChinaNewsExtractor,
         "tag":"chinanews",
         "sub_tag":"world",
         "period": 10
         },     
                                        {
         "url": "http://www.chinanews.com/society.shtml",
         "extractor": ChinaNewsExtractor,
         "tag":"chinanews",
         "sub_tag":"shehui",
         "period": 10
         },     
                                        {
         "url": "http://www.chinanews.com/sports.shtml",
         "extractor": ChinaNewsExtractor,
         "tag":"chinanews",
         "sub_tag":"sport",
         "period": 10
         },     
         {
         "url": "http://www.chinanews.com/mil/news.shtml",
         "extractor": ChinaNewsExtractor,
         "tag":"chinanews",
         "sub_tag":"mili",
         "period": 10
         },     
        {
         "url": "http://www.chinanews.com/it/news.shtml",
         "extractor": ChinaNewsExtractor,
         "tag":"chinanews",
         "sub_tag":"tech",
         "period": 10
         },     
        {
         "url": "http://www.chinanews.com/entertainment.shtml",
         "extractor": ChinaNewsExtractor,
         "tag":"chinanews",
         "sub_tag":"yule",
         "period": 10
         },     
                               
        {
         "url": "http://china.huanqiu.com/article/",
         "extractor": HuanQiuExtractor,
         "tag":"huanqiu",
         "sub_tag":"domestic",
         "period": 10
         },     
       {
         "url": "http://society.huanqiu.com/socialnews/",
         "extractor": HuanQiuExtractor,
         "tag":"huanqiu",
         "sub_tag":"shehui",
         "period": 10
         },   
                                      {
         "url": "http://world.huanqiu.com/exclusive/",
         "extractor": HuanQiuExtractor,
         "tag":"huanqiu",
         "sub_tag":"world",
         "period": 10
         },   
     ]


class Extractor(Daemon):
    
    def __init__(self, pidfile, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull ):
        super(Extractor, self).__init__(pidfile , stdin, stdout, stderr)
    
    def run(self):
        """
        run the extractor use dict
        """
        try:
            LOGGER.debug("start the extractor")
            for elem in extractor_source_url_config:
                extractor = elem["extractor"](elem)
                extractor.extract_links()
        except Exception, e:
            LOGGER.error(traceback.format_exc())
        finally:
            LOGGER.info("finished extractor")

if __name__ == '__main__':
#     daemon_main(Extractor, './ ', sys.argv)
    extractor = Extractor("./")
    extractor.run()
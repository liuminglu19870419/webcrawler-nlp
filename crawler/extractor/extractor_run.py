#encoding: utf-8
'''
Created on 2015年11月18日

@author: lml
'''
from extractor.NetEaseExtractor import NetEaseExtractor
from utils.daemon import Daemon, daemon_main
import os
import sys
from config.LogConfig import LOGGER

extractor_source_url_config = [{
         "url": "http://news.163.com/world/",
         "extractor": NetEaseExtractor,
         "tag":"163",
         "sub_tag":"world",
         "period": 10
         }, ]

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
            pass
        finally:
            pass
if __name__ == '__main__':
#     daemon_main(Extractor, './ ', sys.argv)
    extractor = Extractor("./")
    extractor.run()
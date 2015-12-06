#encoding: utf-8
'''
Created on 2015年12月6日

@author: lml
'''
import os  
import time  
import tarfile  
import zipfile 

path = "/home/lml/backup/"
db_host="192.168.1.100"  
db_user="root"  
db_passwd="lml19870419"  
db_name="test"  
db_charset="utf8"  
filename = "%s"%(time.strftime("%Y%m%d%H%M"))
db_backup_name= path + "news_%s.sql" % filename 
zip_src = db_backup_name
zip_dest = zip_src + ".zip"

mongo_host = db_host
mongo_name = "tdb"
mongo_col = "tcoll"
mongo_backup_name= path + "news_%s" %(filename)
zip_src_mongo = mongo_backup_name
zip_dest_mongo = zip_src_mongo + ".zip"


def zip_files(zip_dest, zip_src):
    f = zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED)
    f.write(zip_src)
    f.close()

def zip_dir(dirname,zipfilename):

    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()

if __name__ == '__main__':
    print "back up mysql database: %s"%db_backup_name
    os.system("mysqldump -h%s -u%s -p%s %s --default_character-set=%s > %s"\
               %(db_host, db_user, db_passwd, db_name, db_charset, db_backup_name))
    zip_files(zip_dest, zip_src)
    os.system("mongodump -h %s -d %s -c %s -o %s "\
              %(mongo_host+ ":27017", mongo_name, mongo_col, mongo_backup_name))
    zip_dir(zip_src_mongo, zip_dest_mongo)
    os.system("rm -rf %s"%(zip_src_mongo))
    os.system("rm -rf %s"%(zip_src))
    print "finished"
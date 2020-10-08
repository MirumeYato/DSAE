#!/usr/bin/env python
# coding: utf-8
import sqlite3
import re
import sys
import time             
import logging 
from datetime import datetime
logger = logging.getLogger('MainLogger')
fh = logging.FileHandler(datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.debug("Program started")


def FileTagPars(filename): # return smth like link. You should use .group(x) (int x=0-3)
                            # 0-full sring, 1 - name of variation, 2 - mass, 3 - charge, 4 - difference (flout)
    i=0
    file=open(filename, 'r')
    for line in file:
        strRE = re.compile("AnalysisAlg\W*INFO\W*The .(.*). variation was applied, so we compare the final efficiencies for M(.*)Z(.*): difference is (.\d*\..*)%")
        if strRE.search(line):
            i=i+1
            return strRE.search(line) 
    if i==0:
        print("Error occurred: Variation wasn`t applied. Restart modeling")
        return 0

def CreateBase(name):
    conn = sqlite3.connect(name+".db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    # Создание таблицы
    cursor.execute("""CREATE TABLE AE_DATA
        (variation_name text, compilation_date text, charge integer, 
        energy integer, difference real)""")
    print("Base "+name+ ".db was created sucsessfuly!")
    return 0

def ImportDateInBase(file,name,time, M,Z,dif):
    conn = sqlite3.connect(file+".db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    albums = [(name, time ,Z, M, dif)]
    cursor.executemany("INSERT INTO AE_DATA VALUES (?,?,?,?,?)", albums)
    conn.commit()
    return 0


def ExportDateInBase(file):
    conn = sqlite3.connect(file+".db")
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    sql = "SELECT * FROM AE_DATA WHERE charge=?"
    cursor.execute(sql, [(1)])
    print(cursor.fetchall()) # or use fetchone()

    print("Here's a listing of all the records in the table:")
    for row in cursor.execute("SELECT rowid, * FROM AE_DATA ORDER BY charge"):
        print(row)

    return 0


def main():
    import os
    
    
    #Start programm
    h=input("Do you want to start?(y/n): ")
    if h =="y":
        while True:
            h=input("Do you want to create base, update existing or print existing?(c/u/p): ")
            h1=input("name of your base: ")
            if h=="c" : 
                try:
                    CreateBase(h1)
                except Exception:
                    print("ERROR: "+h1+".db"+" already exists.")
                    continue
                
            if h=="u":
                print("this func doesn`t work now. sorry.")
            if h=="p":
                print("we continue.")
            break
        while True:
            path=input("enter the path to file-system of modeling, like <D:/Download/variationJobs_24Sept2020>")
            if not os.path.isdir(path):
                print("ERROR: dir <"+path+"> doesn`t exist")
                continue
            else:
                break
                
        file=open('Directory_list.txt', 'w+')
        h2=0
        
        print("Processing...")
        logger.debug("Processing...")
        for line in os.listdir(path):
            file.write(line + '\n')
            strRE = re.compile("submitDir_(.*)_M(.*)_Z(.*)_(.+)")
            if strRE.search(line):
                h2=h2+1
                q=strRE.search(line)
                if os.path.exists(path+"/"+str(q.group(0))+"/submit/log-0.out"):
                    b=FileTagPars(path+"/"+str(q.group(0))+"/submit/log-0.out")
                else:
                     logger.error("ERROR: in dir <"+path+"/"+str(q.group(0))+"/submit/> file <log-0.out> doesn`t exist\n")
                if (q!=0 and b!=0):
                    ImportDateInBase(h1,str(b.group(1)),str(q.group(1)),int(b.group(2)),int(b.group(3)),float(b.group(4)))
                else:
                    if b==0:
                        logger.error("error occured in "+path+"/"+str(q.group(0))+"/submit/log-0.out\n")
        if h2==0:
            print("ERROR:Crashed directory")
            logger.error("ERROR: Crashed directory. Seems like if there aren`t any directory named <submitDir>")
        file.close()

        #Export
        ExportDateInBase(h1)
        
    else:
        print("end of programm")


main()




#!/usr/bin/env python3
# coding: utf-8
import sqlite3
import re
import sys
import time             
import logging 
import os
import logging.handlers
import logging.config
import datetime
import click
import configparser
from shutil import copyfile


#Internal functions:
def conf_copy():
    try:
        if os.path.exists("config/Settings.ini"):    
            copyfile("config/Settings.ini", "config/Settings_copy.ini")
            logger.info("File Settings.ini copied successfully.")
        return 0
    except Exception:
        click.echo("[ERROR]: save copy crushed. Reboot program.")
        return click.abort  

def updb(path,pathdb,namedb):
    #print("DO SMTH UP")
    logger.debug("Uprade_db booted")
    if not os.path.exists(pathdb+namedb):
            print("[ERROR]: Error occurred."+pathdb+namedb+" doesn`t exist.")
            logger.error("Error occurred."+pathdb+namedb+" doesn`t exist.")
            raise BaseException
    
    logger.info("Pre-start")
    #start func    
    file=open('config/Directory_list_'+namedb.split(".db")[0]+'.txt', 'w+')
    logger.info("Created Directory_list\n")
    #marckers
    h2=0 #all files
    h3=0 #old skiped files
    h4=0 #buged files
    print("Processing...")
    logger.info("Processing...\n")
    with click.progressbar(os.listdir(path)) as bar:
        for line in bar:
            file.write(line + '\n')
            
            strRE1 = re.compile("submitDir_(.*)(...ns)_M(.*)_Z(.*)_(.+)__1(.*)") # down\up trig
            strRE2 = re.compile("submitDir_(.*)(...ns)_M(.*)_Z(.*)_(.+)")       #without
            
            if strRE1.search(line):
                h2=h2+1
                q=strRE1.search(line)
                
                #logger.debug(q.group(1)+"-q1")
                #logger.debug(Delta_data(q.group(1)))
                if (Delta_data(str(q.group(1))) > 30): #"update, for old" check
                    #logger.debug("skiped in 1")
                    h2=h2-1
                    h3=h3+1
                    continue
                    
                if os.path.exists(path+"/"+str(q.group(0))+"/submit/log-0.out"): #parsing files
                    b=FileTagPars(path+"/"+str(q.group(0))+"/submit/log-0.out")
                else:
                    logger.error("In dir <"+path+"/"+str(q.group(0))+"/submit/> file <log-0.out> doesn`t exist\n")
                    h4=h4+1
                    
                if (q!=0 and b!=0): # add in base
                    ImportDateInBase(pathdb+namedb,str(b.group(1)),str(q.group(1))+str(q.group(2)),int(b.group(2)),int(b.group(3)),float(b.group(4)),str(q.group(6)))
                else:
                    if b==0:
                        logger.error("error occured in "+path+"/"+str(q.group(0))+"/submit/log-0.out\n")
                        h4=h4+1
                        
            elif strRE2.search(line):
                h2=h2+1
                q=strRE2.search(line)
                
                #logger.debug(q.group(1)+"-q1")
                #logger.debug(Delta_data(q.group(1)))
                if (Delta_data(str(q.group(1))) > 30): #"update, for old" check
                    #logger.debug("skiped in 2")
                    h2=h2-1
                    h3=h3+1
                    continue
                    
                if os.path.exists(path+"/"+str(q.group(0))+"/submit/log-0.out"): #parsing files
                    b=FileTagPars(path+"/"+str(q.group(0))+"/submit/log-0.out")
                else:
                    logger.error("In dir <"+path+"/"+str(q.group(0))+"/submit/> file <log-0.out> doesn`t exist\n")
                    h4=h4+1
                    
                if (q!=0 and b!=0): # add in base
                    ImportDateInBase(pathdb+namedb,str(b.group(1)),str(q.group(1))+str(q.group(2)),int(b.group(2)),int(b.group(3)),float(b.group(4)), "")
                else:
                    if b==0:
                        logger.error("error occured in "+path+"/"+str(q.group(0))+"/submit/log-0.out\n")
                        h4=h4+1
    if h2==0:
        print("[ERROR]:Crashed directory")
        logger.error(" Crashed directory. Seems like if there aren`t any directory named <submitDir>")
        print("[INFO]:It`s possible, that all files are too old and there are not enything new to add")
        logger.info(" It`s possible, that all files are too old and there are not enything new to add")
        raise BaseException
    file.close()
    
    #Export
    ExportDateInBase(pathdb+namedb)
    
    
def makedb(path,pathdb,namedb,c,dest):
    #print("DO SMTH MK")
    #Creating file .db
    logger.debug("Make_db booted")
    if not os.path.exists(pathdb+namedb):
        try:
            CreateBase(pathdb+namedb)
        except Exception:
            print("[ERROR]: Error occurred while db was creating.")
            logger.error("Error occurred while db was creating.")
            raise BaseException
    #Rewriting file .db
    else:
        os.remove(pathdb+namedb)
        try:
            CreateBase(pathdb+namedb)
        except Exception:
            print("[ERROR]: Error occurred while db was creating.")
            logger.error("Error occurred while db was rewriting.")
            raise BaseException
        
    logger.info("Pre-start")
    #start func    
    file=open('config/Directory_list_'+namedb.split(".db")[0]+'.txt', 'w+')
    logger.info("Created Directory_list\n")
    #marckers
    h2=0 #all files
    h3=0 #old skiped files
    h4=0 #buged files
    print("Processing...")
    logger.info("Processing...\n")
    with click.progressbar(os.listdir(path)) as bar:
        for line in bar:
            file.write(line + '\n')
            
            strRE1 = re.compile("submitDir_(.*)(...ns)_M(.*)_Z(.*)_(.+)__1(.*)") # down\up trig
            strRE2 = re.compile("submitDir_(.*)(...ns)_M(.*)_Z(.*)_(.+)")       #without
            
            if strRE1.search(line):
                h2=h2+1
                q=strRE1.search(line)
                
                #logger.debug(q.group(1)+"-q1 c-"+str(c))
                #logger.debug(Delta_data(q.group(1)))
                if c and (Delta_data(str(q.group(1))) > 30): #"create, for old" check
                    h2=h2-1
                    h3=h3+1
                    continue
                    
                if os.path.exists(path+"/"+str(q.group(0))+"/submit/log-0.out"): #parsing files
                    b=FileTagPars(path+"/"+str(q.group(0))+"/submit/log-0.out")
                else:
                    logger.error("In dir <"+path+"/"+str(q.group(0))+"/submit/> file <log-0.out> doesn`t exist\n")
                    h4=h4+1
                    
                if (q!=0 and b!=0): # add in base
                    ImportDateInBase(pathdb+namedb,str(b.group(1)),str(q.group(1))+str(q.group(2)),int(b.group(2)),int(b.group(3)),float(b.group(4)),str(q.group(6)))
                else:
                    if b==0:
                        logger.error("error occured in "+path+"/"+str(q.group(0))+"/submit/log-0.out\n")
                        h4=h4+1
                        
            elif strRE2.search(line):
                h2=h2+1
                q=strRE2.search(line)
                
                if c and (Delta_data(str(q.group(1))) > 30): #"create, for old" check
                    h2=h2-1
                    h3=h3+1
                    continue
                    
                if os.path.exists(path+"/"+str(q.group(0))+"/submit/log-0.out"): #parsing files
                    b=FileTagPars(path+"/"+str(q.group(0))+"/submit/log-0.out")
                else:
                    logger.error("In dir <"+path+"/"+str(q.group(0))+"/submit/> file <log-0.out> doesn`t exist\n")
                    h4=h4+1
                    
                if (q!=0 and b!=0): # add in base
                    ImportDateInBase(pathdb+namedb,str(b.group(1)),str(q.group(1))+str(q.group(2)),int(b.group(2)),int(b.group(3)),float(b.group(4)), "")
                else:
                    if b==0:
                        logger.error("error occured in "+path+"/"+str(q.group(0))+"/submit/log-0.out\n")
                        h4=h4+1
    if h2==0:
        print("[ERROR]:Crashed directory")
        logger.error(" Crashed directory. Seems like if there aren`t any directory named <submitDir>")
        if c:
            print("[INFO]:It`s possible, that all files are too old")
            logger.info(" It`s possible, that all files are too old")
        raise BaseException
    file.close()
    
    #Export
    ExportDateInBase(pathdb+namedb)
    

def Delta_data(date1):
    now=datetime.datetime.now()
    date1 = datetime.datetime.strptime(date1, '%Y-%B-%d_%Hh%Mm%Ss%f')
    date2 = datetime.datetime.strptime(now.strftime('%Y-%B-%d_%Hh%Mm%Ss%f'), '%Y-%B-%d_%Hh%Mm%Ss%f')
    delta = date1 - date2 if date1 > date2 else date2 - date1
    return(delta.days)    

def FileTagPars(filename):      # return smth like link. You should use .group(x) (int x=0-3)
                                # 0-full sring, 1 - name of variation, 2 - mass, 3 - charge, 4 - difference (flout)
    i=0
    file=open(filename, 'r')
    for line in file:
        strRE2 = re.compile("AnalysisAlg\W*INFO\W*The .(.*). variation was applied, so we compare the final efficiencies for M(.*)Z(.*): difference is (.\d*\..*)%")
        strRE1 = re.compile("AnalysisAlg\W*INFO\W*The .(.*)__1.*. variation was applied, so we compare the final efficiencies for M(.*)Z(.*): difference is (.\d*\..*)%")
        if strRE1.search(line):
            i=i+1
            return strRE1.search(line)
        elif strRE2.search(line):
            i=i+1
            return strRE2.search(line)
    if i==0:
        print("[ERROR]: Variation wasn`t applied. Restart modeling")
        logger.error("Variation wasn`t applied. Restart modeling "+ filename)
        return 0
        
def CreateBase(name):
    conn = sqlite3.connect(name) # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    # CREATE TABLE
    cursor.execute("""CREATE TABLE AE_DATA
        (variation_name text, compilation_date text UNIQUE ON CONFLICT IGNORE, charge integer, 
        energy integer, difference real, key text)""")
    print("Base "+name+ " was created successfully!")
    conn.commit()
    conn.close()
    return 0

def ImportDateInBase(file,name,time, M,Z,dif,pref):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    albums = [(name, time ,Z, M, dif, pref)]
    cursor.executemany("INSERT INTO AE_DATA VALUES (?,?,?,?,?,?)", albums)
    conn.commit()
    conn.close()
    return 0
    
def ExportDateInBase(file):
    conn = sqlite3.connect(file)
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    sql = "SELECT * FROM AE_DATA WHERE charge=?"
    cursor.execute(sql, [(1)])
    print(cursor.fetchall()) # or use fetchone()

    print("Here's a listing of all the records in the table:")
    for row in cursor.execute("SELECT rowid, * FROM AE_DATA ORDER BY charge"):
        print(row)
    conn.commit()
    conn.close()
    return 0

#settings func. Save your default paths for work with.
def Settings():
    """Change settings of DSAE. (settings paths)"""
    conf_copy()
    try:
        print("\n   [Settings opened]\n")
        logger.info("Settings opened")
        if not os.path.isdir("config"):
            os.mkdir("config")
        file=open('config/Settings.ini', 'w')
        
        #Path to file-system of modeling
        while True:
            path=input("\nEnter the path to file-system of modeling, you can use .h for get help : \n\n[DSAE]: ")
            if path == '.h':
                sys.stdout.write('''
                
   ----internal-help-------------------------------------------
  | Enter the path to file-system of modeling, like:           |
  |                                                            |
  |<D:/Download/variationJobs_24Sept2020> (full path, win),    |
  |</afs/cern.ch/user/public/data2015_2018_analysis> (linux)   |
  |  also you can use <~,./,../>? like:                        |
  |<~user/public/data2015_2018_analysis/>                      |
  |<./Database/OCT2020/                                        |
  |                                                            |
  |    [special commands]:                                     |
  |                                                            |
  | .pwd     if you want to see current path                   |
  | .ls      if want to see another directories in current dir |
  | .h       print this help                                   |
  | ^C(^Z)   means "^" as ctrl.Close app and clear settings.ini|
   ------------------------------------------------------------
   
   
''')
                continue
            elif path == '.ls':
                print(list(filter(os.path.isdir, os.listdir())))
            elif path == '.pwd':
                print (os.getcwd())
            elif not os.path.exists(os.path.abspath(os.path.expanduser(os.path.expandvars(path)))):
                print("[ERROR]: dir <"+path+"> doesn`t exist")
                continue
            elif  path=='':
                print ("[ERROR]: nothing was entered")
                continue
            else:
                break
                
        #Path to directory where you want to save database
        while True:
            try:
                pathdb=input("\nDo you wanna save database in DSAE`s directory [y/n] or [yes/no]: ")
            except Exception:
                continue
            if (pathdb=="y" or pathdb=="yes"):
                pathdb="./Databases"
                if not os.path.exists(pathdb):
                    os.mkdir(pathdb)
                print("[INFO]: dir <"+os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))+"> have chosen as DEFAULT")
                logger.info("dir <"+os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))+"> have chosen as DEFAULT")
                break
            elif(pathdb=="n" or pathdb=="no"):
                while True:
                    try:
                        pathdb=input("\nEnter the path to directory where you want to save database, .h for get help:\n\n[DSAE]: ")
                        if pathdb == '.h':
                            sys.stdout.write('''
                
   ----internal-help-------------------------------------------
  | Enter the path to file-system of modeling, like:           |
  |                                                            |
  |<D:/Download/variationJobs_24Sept2020> (full path, win),    |
  |</afs/cern.ch/user/public/data2015_2018_analysis> (linux)   |
  |  also you can use <~,./,../>? like:                        |
  |<~user/public/data2015_2018_analysis/>                      |
  |<./Database/OCT2020/                                        |
  |                                                            |
  |    [special commands]:                                     |
  |                                                            |
  | .pwd     if you want to see current path                   |
  | .ls      if want to see another directories in current dir |
  | .h       print this help                                   |
  | ^C(^Z)   means "^" as ctrl.Close app and clear settings.ini|
   ------------------------------------------------------------
   
   
''')
                            continue
                        elif pathdb == '.ls':
                            print(list(filter(os.path.isdir, os.listdir())))
                            continue
                        elif pathdb == '.pwd':
                            print (os.getcwd())
                            continue
                        elif  path=='':
                            print ("[ERROR]: nothing was entered")
                            continue
                        elif not os.path.exists(os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))):
                            os.mkdir(os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb))))
                            print("[INFO]: dir <"+os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))+"> successfully created and have chosen as DEFAULT")
                            logger.info("dir <"+os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))+"> successfully created and have chosen as DEFAULT")
                        else:
                            print("[INFO]: dir <"+os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))+"> saved and have chosen as DEFAULT")
                            logger.info("dir <"+os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))+"> have chosen as DEFAULT")
                    except Exception:
                        print("[ERROR]: smth went wrong. Try enter path correctly.")
                        logger.error("smth went wrong. Try enter path correctly. Entered was: " +pathdb)
                        continue
                    else:
                        break
                break
            else:
                print("[ERROR]: please enter only [y/n] or [yes/no]")
                continue
        
        #Name of database
        while True:
            try:
                namedb=input("\nDo you wanna name database or use DEFAULT [y/n] or [yes/no]: ")
            except Exception:   
                continue
            if (namedb=="y" or namedb=="yes"):
                namedb="DEFAULT.db"
                print("[INFO]: name <"+namedb+"> have chosen as DEFAULT")
                logger.info("name <"+namedb+"> have chosen as DEFAULT")
                break
            elif(namedb=="n" or namedb=="no"):
                while True:
                    try:
                        namedb=input("\nEnter the name of database\n\n[DSAE]: ")
                        if  namedb=='':
                            print ("[ERROR]: nothing was entered")
                            continue
                        else:
                            namedb=namedb+".db"
                            print("[INFO]: name <"+namedb+"> saved and have chosen as DEFAULT")
                            logger.info("name <"+namedb+"> have chosen as DEFAULT")
                    except Exception:
                        print("[ERROR]: smth went wrong. Try again.")
                        logger.error("smth went wrong. Entered was: " +namedb)
                        continue
                    else:
                        break
                break
            else:
                print("[ERROR]: please enter only [y/n] or [yes/no]")
                continue
        file.write("[Settings]\nDirectory_of_results_modeling = "+os.path.abspath(os.path.expanduser(os.path.expandvars(path)))+"\nDirectory_for_saving_db = "+os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))+"\nName_of_db = "+namedb)
        file.close()
        print("\n   [Settings successfully changed]")
        print("   if smth went wronk try <dsae.py settings> again\n   or you can check './config/Settings.ini'\n")
        logger.info("Settings successfully changed")
        
    except BaseException:
        print("\n[ERROR]: smth went wrong or force shutdown occurred. Reboot program.")
        logger.error("Smth went wrong. Program crushed by wrong input or force shutdown occurred.")
        file.close()
        os.remove("config/Settings.ini")
        if os.path.exists("config/Settings.ini"):
            os.remove("config/Settings.ini")
        if os.path.exists("config/Settings_copy.ini"):
            os.rename("config/Settings_copy.ini", "config/Settings.ini")




#External functions:
@click.group("DSAE")
@click.version_option("0.1.0")
def cli():
    """ DSAE CLI application """
    pass


@click.command()
def ReadMe():
    """Opens ReadMe. It contains more detailed help """
    file=open("ReadMe.txt", 'r')
    for line in file:
        print(line)
    os.system('pause')

cli.add_command(ReadMe)


@click.command() #CreateDB - default: fast creating without input (use only settings)
@click.option("-d", "--default", is_flag=True, help="compile all posible files using config (settings) data")
@click.option("-up", "--upgrade", is_flag=True, help="upgrade existing db by files created month and earlier ")
@click.option("-cr", "--create", is_flag=True, help="create (it`s quicker than default) new by files created month and earlier")
@click.argument("dest", required=False)
def mkdb(default,upgrade,create, dest):
    """Makes database from file system with results of modeling"""
    
        
    try:
        #User Check settings
        config = configparser.ConfigParser() 
        config.read("config/settings.ini")
        path=(config["Settings"]["directory_of_results_modeling"]).replace(os.sep, '/')
        pathdb=(config["Settings"]["directory_for_saving_db"]+"/").replace(os.sep, '/')
        namedb=config["Settings"]["name_of_db"]
        print("\n   --Path------------------------------------------------------\n   "+path)
        print("   "+pathdb+namedb+"\n   ------------------------------------------------------------\n")
        if click.confirm('Are you sure your settings correct? \n(Mention, that in UPGRADE mode name wouldn`t change, but in CREATE mode will)', default=True, abort=False, show_default=True):
            click.echo('   [Settings applied]\n')
        else:
            click.echo('\nUse: dsae.py config (-d/--default)')
            logger.info("User decided to change settings")
            return click.Abort
        
        
        #Start
        click.echo('we`ve gone through horisont')
        logger.info("we`ve gone through horisont")
        
        #UPGRADE
        if upgrade:
            print("   [DB comilation in UPGRADE mode]\n")
            logger.info("DB comilation in UPGRADE mode")
            #smth hard, not just boot default with flag
            conf_copy()
            updb(path,pathdb,namedb)
            return click.Abort
            
        #CREATE    
        elif create:
            print("   [DB comilation in CREATE mode]\n")
            logger.info("DB comilation in CREATE mode")
            
            #rewrite .db or create new one
            if click.confirm('Do you wanna rewrite current '+namedb+' file?', default=False, abort=False, show_default=True):
                
                #start rewrited
                click.echo('   [Settings applied]\n')
                logger.info("File "+namedb+" will be rewrited")
                
                #Copy .db
                try:
                    if os.path.exists(pathdb+namedb):    
                        if not os.path.exists("./Databases"):  
                            os.makedirs("./Databases")
                        copyfile(pathdb+namedb, "Databases/Copy_"+namedb)
                        logger.info("File "+pathdb+namedb+" copied successfully.")
                except Exception:
                    click.echo("[ERROR]: save copy crushed. Reboot program.")
                    return click.abort
                    
            #start create
            else:
                conf_copy()
                #new name
                namedb=click.prompt("Enter the name of database", default=None, prompt_suffix='\n\n[DSAE]: ', show_default=True)
                namedb=namedb+".db"
                config.set("Settings", "name_of_db", namedb)
                with open("config/settings.ini", 'w') as configfile:
                    config.write(configfile)
                click.echo('[INFO]: '+pathdb+namedb+' set as DEFAULT')
                logger.info(pathdb+namedb+' set as DEFAULT')
                
                
        #DEFAULT
        else:
            print("   [DB comilation in DEFAULT mode]\n")
            logger.info("DB comilation in DEFAULT mode")
            conf_copy()
            #Copy .db
            try:
                if os.path.exists(pathdb+namedb):    
                    if not os.path.exists("./Databases"):  
                        os.makedirs("./Databases")
                    copyfile(pathdb+namedb, "Databases/Copy_"+namedb)
                    logger.info("File "+pathdb+namedb+" copied successfully.")
            except Exception:
                click.echo("[ERROR]: save copy crushed. Reboot program.")
                return click.abort
                
        
        #main part
        makedb(path,pathdb,namedb,create,dest)
    
    except BaseException:
        print("\n[ERROR]: smth went wrong or force shutdown occurred. Reboot program.")
        logger.error("Smth went wrong. Program crushed by sm reason. Probably force shutdown occurred")
        if os.path.exists(pathdb+namedb):
            os.remove(pathdb+namedb)
        if os.path.exists("Databases/Copy_"+namedb):
            os.rename("Databases/Copy_"+namedb, pathdb+namedb)
        if os.path.exists("config/Settings_copy.ini"):
            if os.path.exists("config/Settings.ini"):
                os.remove("config/Settings.ini")
            os.rename("config/Settings_copy.ini", "config/Settings.ini")
           
        
    
cli.add_command(mkdb)

#PrintDB



@click.command() #settings func. Save your default paths for work with.
@click.option("-d", "--default", is_flag=True, help="makes set settings faster.")
def config(default):
    """Get and set repository or global options."""
    if default:
        print("   [Settings in DEFAULT mode]\n")
        logger.info("Settings opened in DEFAULT mode")
        conf_copy()
            
        try:
            while True:
                path=input("\nEnter the path to file-system of modeling, you can use .h for get help : \n\n[DSAE]: ")
                if path == '.h':
                    sys.stdout.write('''
                    
   ----internal-help-------------------------------------------
  | Enter the path to file-system of modeling, like:           |
  |                                                            |
  |<D:/Download/variationJobs_24Sept2020> (full path, win),    |
  |</afs/cern.ch/user/public/data2015_2018_analysis> (linux)   |
  |  also you can use <~,./,../>? like:                        |
  |<~user/public/data2015_2018_analysis/>                      |
  |<./Database/OCT2020/                                        |
  |                                                            |
  |    [special commands]:                                     |
  |                                                            |
  | .pwd     if you want to see current path                   |
  | .ls      if want to see another directories in current dir |
  | .h       print this help                                   |
  | ^C(^Z)   means "^" as ctrl.Close app and clear settings.ini|
   ------------------------------------------------------------
   
   
''')
                    continue
                elif path == '.ls':
                    print(list(filter(os.path.isdir, os.listdir())))
                elif path == '.pwd':
                    print (os.getcwd())
                elif  path=='':
                    print ("[ERROR]: nothing was entered")
                    continue
                elif not os.path.exists(os.path.abspath(os.path.expanduser(os.path.expandvars(path)))):
                    print("[ERROR]: dir <"+path+"> doesn`t exist")
                    continue
                else:
                    break
            app_dir = os.path.abspath(os.path.expanduser(os.path.expandvars("./config")))
    
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
            cfg = os.path.join(app_dir, "Settings.ini")
            
            config = configparser.ConfigParser()
            config.read(cfg)
            if not config.has_section("Settings"):
                config.add_section("Settings")
            config.set("Settings", "Directory_of_results_modeling", os.path.abspath(os.path.expanduser(os.path.expandvars(path))))
            pathdb="./Databases"
            if not os.path.exists(pathdb):
                os.mkdir(pathdb)
            logger.info("dir <"+os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb)))+"> have chosen as DEFAULT")
            config.set("Settings", "Directory_for_saving_db", os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb))))
            config.set("Settings", "Name_of_db", "DEFAULT.db")
            
            with open(cfg, "w") as configfile:
                config.write(configfile)
            print("\n   [Settings successfully changed]")
            print("   if smth went wronk try <dsae.py settings> again\n   or you can check './config/Settings.ini'\n")
            logger.info("Settings successfully changed")
        except BaseException:
            print("\n[ERROR]: smth went wrong or force shutdown occurred. Reboot program.")
            logger.error("Smth went wrong. Program crushed by wrong input or force shutdown occurred.")
            if os.path.exists("config/Settings.ini"):
                os.remove("config/Settings.ini")
            if os.path.exists("config/Settings_copy.ini"):
                os.rename("config/Settings_copy.ini", "config/Settings.ini")
    else:
        Settings()


        
        

cli.add_command(config)


if __name__ == "__main__":  

    # Logger creating
    if not os.path.isdir("log"):
        os.mkdir("log")
    
    name2='log/'+datetime.datetime.now().strftime('%Y-%b-%d_%Hh%Mm%Ss')+'.log'
    
    # Get the logger specified in the file
    logger = logging.getLogger(__name__)
    logger .setLevel(logging.DEBUG)
    f_handler = logging.FileHandler(name2)
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter('%(asctime)s |     %(levelname)-10s %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    # Logger check
    logger.debug("Program started")


    # Boot settings control
    if(os.path.exists("./config/Settings.ini")):
        sys.stdout.write('''
   ------------------------------------------------------------
  | Welcome back in DSAE 0.1.5                                 |
  |                                  (c) 2020, The DSAE Team   |
  |                                                            |
  |  [Settings set as DEFAULT  or like in a previous session]  |
   ------------------------------------------------------------
   
   
''')   
        
        #If settings is correct click will activate
        cli()
    else:
        while True:
            try:
                first=input("\nAre you new for DSAE or do you want to boot full settings? [y/n] or [yes/no]: ")
            except Exception:
                continue
            if (first=="y" or first=="yes"):
                try:
                    sys.stdout.write('''
   ------------------------------------------------------------
  | Welcome in DSAE 0.1.5                                      |
  |                                  (c) 2020, The DSAE Team   |
  |                                                            |
  |      [Let`s set settings for correct program work!]        |
   ------------------------------------------------------------
   
   
''')    
                    file=open("ReadMe.txt", 'r')
                    for line in file:
                        print(line)
                    os.system('pause')
                    Settings()
                except BaseException :
                    print('[Error]: Automaticly Rebooted')
                    print('[Error]: If nothing happend try to reboot program without arguments (like <config>)')
                
                break
            elif(first=="n" or first=="no"):
                sys.stdout.write('''
   ------------------------------------------------------------
  | Welcome back in DSAE 0.1.0                                 |
  |                                  (c) 2020, The DSAE Team   |
  |                                                            |
  |  [Settings set as DEFAULT  or like in a previous session]  |
   ------------------------------------------------------------
   
   
''')
                cli()
                break
            else:
                print("[ERROR]: please enter only [y/n] or [yes/no]")
                continue
        
    
    


    

#!/usr/bin/env python3
# coding: utf-8
import sqlite3
import csv
import re
import sys
import time             
import logging 
import os
import logging.handlers
import logging.config
import datetime
#import click
from tqdm import tqdm
import configparser
from shutil import copyfile
from math import sqrt
#import numpy
import ROOT


def Settings_bug_check():
    app_dir = os.path.abspath(os.path.expanduser(os.path.expandvars("./config")))
    cfg = os.path.join(app_dir, "Settings.ini")    
    if(os.path.exists(cfg)):
        config = configparser.ConfigParser()
        config.read(cfg)
        if not config.has_section("Settings"):
            logger.error("Settings.ini crushed inside") 
            return Exception
        else:
            logger.info("All ok with Settings.ini")
            path1=(config["Settings"]["directory_of_results_modeling"]).replace(os.sep, '/')
            pathdb=(config["Settings"]["directory_for_saving_db"]+"/").replace(os.sep, '/')
            config.set("Settings", "directory_of_results_modeling",  os.path.abspath(os.path.expanduser(os.path.expandvars(path1))).replace(os.sep, '/'))
            config.set("Settings", "directory_for_saving_db",  os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb))).replace(os.sep, '/'))
            with open(cfg, "w") as configfile1:
                config.write(configfile1)
            print("\n   [Settings successfully changed]")
            print("   if smth went wrong you can check './config/Settings.ini'\n") 
            logger.info("Settings successfully changed")
            return 0
    else:
        print("Settings.ini doesn`t exist. Please to recover it.")
        logger.error("Settings.ini doesn`t exist")
        return Exception


def csv_writer(path,file,Z_end,Z_step,flag):

    #file="databases/DEFAULT.db" #db name
    time_like=""
    var_list=[None,None,None,"pT",None,"S(pixel dE/dx)",None,"TRT fHT",None,"N overflowing IBL clusters",None,"S(TRT dE/dx)",None,"S(MDT dE/dx)",None,None,"beta variation",None,"t variation",
        None,None,"Statistical variation",None,"Systematical variation",None,None,None,"single-muon trigger","MET trigger","late-muon trigger",None,None,None,"MUON_ID",None,"MUON_MS",None,"MUON_SCALE",None,"MUON_EFF_RECO_STAT",
        None,"MUON_EFF_RECO_STAT_LOWPT",None,"MUON_SAGITTA_RESBIAS",None,"MUON_EFF_RECO_SYS",None,"MUON_EFF_RECO_SYS_LOWPT",None,"MUON_SAGITTA_RHO",None,"TRK_BIAS_D0_WM","TRK_BIAS_QOVERP_SAGITTA_WM",
        "TRK_BIAS_Z0_WM","TRK_EFF_LOOSE_GLOBAL","TRK_EFF_LOOSE_IBL","TRK_EFF_LOOSE_PHYSMODEL","TRK_EFF_LOOSE_PP0","TRK_FAKE_RATE_LOOSE","TRK_FAKE_RATE_LOOSE_ROBUST","TRK_RES_D0_DEAD","TRK_RES_D0_MEAS",
        "TRK_RES_Z0_MEAS","TRK_RES_Z0_DEAD",None,"up","down",None,None,None,None,None,None]
    var_list_older=[None,None,None,"pT",None,"S(pixel dE/dx)",None,"TRT fHT",None,"N IBL overflown clusters",None,"S(TRT dE/dx)",None,"S(MDT dE/dx)",None,None,"beta variation",None,"t variation",
        None,None,"Statistical variation",None,"Systematical variation",None,None,None,"Local","Global",None,None,"MUON_ID",None,"MUON_MS",None,"MUON_SCALE",None,"MUON_EFF_STAT",
        None,"MUON_EFF_STAT_LOWPT",None,"MUON_SAGITTA_RESBIAS",None,"MUON_EFF_SYS",None,"MUON_EFF_SYS_LOWPT",None,"MUON_SAGITTA_RHO",None,"TRK_BIAS_D0_WM","TRK_BIAS_QOVERP_SAGITTA_WM",
        "TRK_BIAS_Z0_WM","TRK_EFF_LOOSE_GLOBAL","TRK_EFF_LOOSE_IBL","TRK_EFF_LOOSE_PHYSMODEL","TRK_EFF_LOOSE_PP0","TRK_FAKE_RATE_LOOSE","TRK_RES_D0_DEAD","TRK_RES_D0_MEAS","TRK_RES_Z0_MEAS",
        "TRK_RES_Z0_DEAD",None,"up","down",None,None,None,None,None,None]
    up_list=[None,None,None,"up","down","up","down","up","down","up","down","up","down","up","down",None,"up","down",
        "up","down",None,"up","down","up","down",None,None,None,None,None,None,None,None,"up","down","up","down","up","down","up","down","up","down","up","down","up","down","up","down",
        "up","down",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
    
    Only_res_file=[["Charge z","Mass [GeV]",None,"Result on the data/MC agreement uncertainty","Result on the RPC scaling uncertainty",
        "Result on the basic muon trigger efficiency uncertainty","Limited MC statistics","Result on the trigger uncertainty","Result on the tracking uncertainty",
        "Result on the pile-up reweighting uncertainty","Potentially unknown material budget in calos","PDF parametrization uncertainty","Overall sum"],
        [None,None,None,None,None,None,None,None,None,None,None,None,None]]
    
    db_var_list=Export_var_list(file) #Debug list
    db_var_list_c=db_var_list.copy()
    
    
    """
    Write data to a CSV file path
    """
    path=path+".csv"
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        
        #flag=1 old or new header (0 or 1)
        
        if flag==1:
            up_list.insert(60, None)
            header=[["Charge z","Mass [GeV]",None,"Limited agreement of key variables between data and MC",None,None,None,None,None,None,None,None,None,None,None,"Result on the data/MC agreement uncertainty",
                "RPC trigger efficiency scaling uncertainty",None,None,None,"Result on the RPC scaling uncertainty","Basic muon trigger efficiency uncertainty",None,None,None,
                "Result on the basic muon trigger efficiency uncertainty","Limited MC statistics","Inclusive trigger-selection efficiencies [%]",None,None,"MET trigger uncertainties","Late-muon-trigger uncertainty",
                "Result on the trigger uncertainty","Tracking uncertainty",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,"Result on the tracking uncertainty","Pile-up reweighting uncertainty",None,
                "Result on the pile-up reweighting uncertainty","Potentially unknown material budget in calos","PDF parametrization uncertainty",None,None,"Overall sum"],
                var_list,up_list,[None,None,None,None,None,None,None,None,None,None,
                None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,
                None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        else:
            header=[["Charge z","Mass [GeV]",None,"Limited agreement of key variables between data and MC",None,None,None,None,None,None,None,None,None,None,None,"Result on the data/MC agreement uncertainty",
                "RPC trigger efficiency scaling uncertainty",None,None,None,"Result on the RPC scaling uncertainty","Basic muon trigger efficiency uncertainty",None,None,None,
                "Result on the basic muon trigger efficiency uncertainty","Limited MC statistics","MET trigger uncertainties",None,"Fraction of events in D triggered only by the MET trigger",
                "Result on the trigger uncertainty","Tracking uncertainty",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,"Result on the tracking uncertainty","Pile-up reweighting uncertainty",None,
                "Result on the pile-up reweighting uncertainty","Potentially unknown material budget in calos","PDF parametrization uncertainty",None,None,"Overall sum"],
                var_list_older,up_list,[None,None,None,None,None,None,None,None,None,None,None,None,None,
                None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,
                None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
            var_list=var_list_older
        logger.info("Start creation .csv")
        for line in header:    
            writer.writerow(line) 
            
        Z=2.0           #Initial charge
        var_list=[None,None,None,"PRIVATE_SYST_LIMITEDDATAMCAGREEMENT_pT",None,"PRIVATE_SYST_LIMITEDDATAMCAGREEMENT_SPIXELDEDX",None,"PRIVATE_SYST_LIMITEDDATAMCAGREEMENT_TRTFHT",
            None,"PRIVATE_SYST_LIMITEDDATAMCAGREEMENT_NOVERFLOWINGIBLCLUSTERS",None,"PRIVATE_SYST_LIMITEDDATAMCAGREEMENT_STRTDEDX",None,"PRIVATE_SYST_LIMITEDDATAMCAGREEMENT_SMDTDEDX",
            None,None,"PRIVATE_SYST_BETAINRPCEFFSFCALC",None,"PRIVATE_SYST_SCALINGTIMEINRPCEFFSFCALC",None,None,"MUON_EFF_TrigStatUncertainty", None,"MUON_EFF_TrigSystUncertainty",
            None,None,"Limited_MC_statistics","single_muon_trigger","MET_trigger","late_muon_trigger","PRIVATE_SYST_METTRIGGEREFFICIENCY",None,None,"MUON_ID",None,"MUON_MS",None,"MUON_SCALE",None,"MUON_EFF_RECO_STAT",None,
            "MUON_EFF_RECO_STAT_LOWPT",None,"MUON_SAGITTA_RESBIAS",None,"MUON_EFF_RECO_SYS",None,"MUON_EFF_RECO_SYS_LOWPT",None,"MUON_SAGITTA_RHO",None,"TRK_BIAS_D0_WM","TRK_BIAS_QOVERP_SAGITTA_WM",
            "TRK_BIAS_Z0_WM","TRK_EFF_LOOSE_GLOBAL","TRK_EFF_LOOSE_IBL","TRK_EFF_LOOSE_PHYSMODEL","TRK_EFF_LOOSE_PP0","TRK_FAKE_RATE_LOOSE","TRK_FAKE_RATE_LOOSE_ROBUST","TRK_RES_D0_DEAD",
            "TRK_RES_D0_MEAS","TRK_RES_Z0_MEAS","TRK_RES_Z0_DEAD",None,"PRW_DATASF",None,None,None,None,None,None,None]
        up_list[65]="up"
        up_list[66]="down"
        logger.info("\n")
        logger.info("<Logging for errors in var_list>\n")
        #print(Export_M_list(file))
        while Z <= Z_end:  #Final charge
            for M in Export_M_list(file):
                if M==500:
                    dif_list=[Z, 500,None]
                else:
                    dif_list=[None,M,None]
                v=3
                for var in var_list[3:72+flag]:
                    if var==None and up_list[v]==None:
                        dif_list.append(None)
                    elif var==None and up_list[v]=="down":
                        #dif_list.append(var_list[v-1]+"__"+up_list[v])
                        dif_list.append(ExportDateInBase(file,var_list[v-1], str(M),str(Z),up_list[v], time_like))
                        try:
                            db_var_list_c.remove(var_list[v-1])
                        except Exception:
                            pass
                        if db_var_list.count(var_list[v-1])==0:
                            logger.error(var_list[v-1] + " not found")
                    else:
                        #dif_list.append(str(var)+"__"+str(up_list[v]))
                        dif_list.append(ExportDateInBase(file,var, str(M),str(Z),up_list[v],time_like))
                        try:
                            db_var_list_c.remove(var) 
                        except Exception:   
                            pass
                        if db_var_list.count(var)==0:
                            logger.error(var + " not found")
                    v+=1
                #dif_list +=[None for i in range(22)]
                #strange columns
                #dif_list[26]=0 #Limited MC statistics ~ysmirnov/public/data2015_2018_analysis/Grigory_uncertainties/getUncertaintiesDueToLimitedMcStats.py
                #dif_list[27]=0 #Inclusive trigger-selection efficiencies [%]		 ~ysmirnov/public/data2015_2018_analysis/Grigory_uncertainties/getInclusiveTriggerEfficiencies.py
                #dif_list[28]=0 #Inclusive trigger-selection efficiencies [%]		
                #dif_list[29]=0 #Inclusive trigger-selection efficiencies [%]		
                dif_list[31]=0 #ILate-muon-trigger uncertainty		
                #dif_list[62+flag]=0 #Pile-up reweighting uncertainty (up)
                #dif_list[63+flag]=0 #Pile-up reweighting uncertainty (down)
                dif_list[67+flag]=0 #Potentially unknown material budget in calos
                dif_list[68+flag]=0 #PDF parametrization uncertainty
                
                
                #Equations for items
                dif_list[15]=  sqrt(sum_err(dif_list[3:15],2)) #Result on the data/MC agreement uncertainty
                dif_list[20]=  sqrt(sum_err(dif_list[16:20],2)) #Result on the RPC scaling uncertainty
                dif_list[25]=  sqrt(sum_err(dif_list[21:25],2)) #Result on the muon-trigger-efficiency uncertainty
                #dif_list[32]=0
                try:
                    dif_list[32]=  sqrt((dif_list[25]*dif_list[27]/(dif_list[27]+dif_list[28]+dif_list[29]))**2+(dif_list[30]*dif_list[28]/(dif_list[27]+dif_list[28]+dif_list[29]))**2+(dif_list[31]*dif_list[29]/(dif_list[27]+dif_list[28]+dif_list[29]))**2) #Result on the trigger uncertainty
                except Exception:
                    dif_list[32]=0
                #(1.0-dif_list[29]/100.0))**2+(sqrt(dif_list[27]**2+dif_list[28]**2)*dif_list[29]/100.0)**2) old
                dif_list[63+flag]=  sqrt(sum_err(dif_list[33:51],2)+sum_err(dif_list[51:63+flag],1)) #Result on the tracking uncertainty
                dif_list[66+flag]=  sqrt(sum_err(dif_list[64+flag:66+flag],2)) #Result on the pile-up reweighting uncertainty
                #Overall sum
                dif_list[71+flag]=  sqrt(dif_list[15]**2+dif_list[20]**2+dif_list[25]**2+dif_list[26]**2+dif_list[32]**2+dif_list[63+flag]**2+dif_list[66+flag]**2+dif_list[67+flag]**2+dif_list[68+flag]**2)
                
                #Only important items table
                Only_res_file.append(dif_list[0:3]+[dif_list[15]]+[dif_list[20]]+[dif_list[25]]+[dif_list[26]]+[dif_list[32]]+[dif_list[63+flag]]+[dif_list[66+flag]]+[dif_list[67+flag]]+[dif_list[68+flag]]+[dif_list[71+flag]])
                
                writer.writerow(dif_list)
            Z=Z+Z_step #cycle step
    logger.info("Start creation .csv (Only important items)")
    #Only important items table file creating
    with open(path.split(".csv")[0]+"_res.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in Only_res_file:    
            writer.writerow(line)        
    logger.info("Start creation .csv (Only summary items)")
    #Only summary items table file creating
    file_sum=open(path.split(".csv")[0]+"_sum_res.txt", 'w+')
    for line in Only_res_file:
        if line[0]=="Charge z":
            file_sum.write("%-5s" % "Z" +"%-5s" % "M"+"|   " +str(line[12])+"\n")
            continue
        if line[1]==None:
            file_sum.write("===============================\n")
            continue
        if line[0]!=None:
            file_sum.write("===============================\n")   
        file_sum.write("%-5s" % str(line[0]) +"%-5s" % str(line[1])+"|   " +str(line[12])+"\n")
    file_sum.close()  

    
    print("list of variations, which exist only in database or only in table`s template: "+str(db_var_list_c))
    logger.info("list of variations, which exist only in database or only in table`s template: "+str(db_var_list_c))
    #print("list of variations, which exist only in database or only in table`s template: "+str(db_var_list_c))
    logger.info("list of variations: "+str(db_var_list))
        
def sum_err(err_l,k):
    sq_sum=0
    i=0
    while i!=len(err_l):
        err_l[i]=abs(err_l[i])
        err_l[i+k-1]=abs(err_l[i+k-1])
        sq_sum+=max(err_l[i:i+k])**2
        i+=k
    return sq_sum
        
def Export_M_list(file):
    try:
        conn = sqlite3.connect(file)
        #conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT energy FROM AE_DATA ORDER BY energy")
        data=cursor.fetchall()
        #print(data[0])
        if data==None:
            raise BaseException
    
        conn.commit()
        return Type_changer(data)
    except BaseException:
        return 0
    finally:
        conn.close()
        
def Export_var_list(file):
    try:
        conn = sqlite3.connect(file)
        #conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT variation_name FROM AE_DATA ORDER BY variation_name")
        data=cursor.fetchall()
        #print(data[0])
        if data==None:
            raise BaseException
    
        conn.commit()
        return Type_changer(data)
    except BaseException:
        return 0
    finally:
        conn.close()
                   
def Type_changer(data):
    data_new=[]
    for tuple in data:
        data_new.append(tuple[0])
    return data_new

def ExportDateInBase(file,name, M,Z,pref,time):
    try:
        conn = sqlite3.connect(file)
        #conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        time_s="%"+time+"%"
        
        logger.info(" Name: "+ name+" M: "+ M+" Z: "+ Z+" key: "+str(pref))
        if pref==None:
            pref=""
        sql = "SELECT difference FROM AE_DATA WHERE( charge=? AND variation_name=? AND energy=? AND key=? AND compilation_date LIKE ?) ORDER BY compilation_date DESC"
        #sql = "SELECT difference FROM AE_DATA WHERE variation_name=? ORDER BY compilation_date"
        cursor.execute(sql,[(Z),(name),(M),(pref),(time_s)])
        data=cursor.fetchone() # or use fetchone()\etchall()
        #print(data[0])
        if data==None:
            #checker on existing (logging error)
            raise BaseException
        
        conn.commit()
        return data[0]
    except BaseException:
        return 0
    finally:
        conn.close()



#Internal functions:

def conf_copy():
    try:
        if os.path.exists("config/Settings.ini"):    
            copyfile("config/Settings.ini", "config/Settings_copy.ini")
            logger.info("File Settings.ini copied successfully.")
        return 0
    except Exception:
        print("[ERROR]: save copy crushed. Reboot program.")
        return Exception 

    
def makedb(path,pathdb,namedb,c): #
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
    for line in tqdm(os.listdir(path)):
        file.write(line + '\n')
        strRE1 = re.compile("submitDir_(.*)(...)ns_M(.*)_Z(.*)_(.+)__1(.*)") # down\up trig
        strRE2 = re.compile("submitDir_(.*)(...)ns_M(.*)_Z(.*)_(.+)")       #without
        strRE3 = re.compile("submitDir_(.*)(...)ns_M(.*)_Z(.*)_")
        
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
                ImportDateInBase(pathdb+namedb,str(b.group(1)),str(q.group(1)),str(q.group(2)),int(b.group(2)),int(b.group(3)),float(b.group(4)),str(q.group(6)))
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
                ImportDateInBase(pathdb+namedb,str(b.group(1)),str(q.group(1)),str(q.group(2)),int(b.group(2)),int(b.group(3)),float(b.group(4)), "")
            else:
                if b==0:
                    logger.error("error occured in "+path+"/"+str(q.group(0))+"/submit/log-0.out\n")
                    h4=h4+1
        elif strRE3.search(line):
            h2=h2+1
            q=strRE3.search(line)
            
            if c and (Delta_data(str(q.group(1))) > 30): #"create, for old" check
                h2=h2-1
                h3=h3+1
                continue
            if (str(q.group(3))=="500" or str(q.group(3))=="800"):
                fileName=path+"/"+str(q.group(0))+"/fetch/hist-m0"+str(q.group(3))+"z"+str(q.group(4))+"-0.root"
            else:
                fileName=path+"/"+str(q.group(0))+"/fetch/hist-m"+str(q.group(3))+"z"+str(q.group(4))+"-0.root"
            #logger.info("all looks all right " +fileName+"\n")
            if os.path.exists(fileName): #parsing files
                f = ROOT.TFile.Open(fileName)
            else:
                logger.error("In dir <"+path+"/"+str(q.group(0))+"/fetch/> file <hist-m"+str(q.group(3))+"z"+str(q.group(4))+"-0.root> doesn`t exist\n")
                h4=h4+1
            
            if ((f or not f.IsZombie()) and q!=0): # add in base
                h_cutflow = f.Get("h_cutflow")
                if not h_cutflow:
                    logger.error('Error: unable to find the histogram you requested inside the \'', fileName, '\' - check file content and/or histogram name!')
                else:
                    s_trig=h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("#Sigma muon-trigger SFs (MC only)")) / h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with 1 primary vertex")) * 100
                    m_trig=h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with MET trigger fired")) / h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with 1 primary vertex")) * 100
                    l_trig=h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with late-muon trigger fired")) / h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with 1 primary vertex")) * 100
                    #logger.info("s_trig " +str(s_trig)+" m_trig " +str(m_trig)+" l_trig " +str(l_trig)+"\n")
                    ImportDateInBase(pathdb+namedb,"single_muon_trigger",str(q.group(1)),str(q.group(2)),int(q.group(3)),int(q.group(4)),float(s_trig), "")
                    ImportDateInBase(pathdb+namedb,"MET_trigger",str(q.group(1)),str(q.group(2))+"1",int(q.group(3)),int(q.group(4)),m_trig, "")
                    ImportDateInBase(pathdb+namedb,"late_muon_trigger",str(q.group(1)),str(q.group(2))+"2",int(q.group(3)),int(q.group(4)),l_trig, "")
                    
                # histogram for the numerator of the TEfficiency object
                    h_SoWOfEventsAfterFinalSelection = ROOT.TH1D("h_SoWOfEventsAfterFinalSelection", ";Bin;Sum of weights of events after final selection", 1, 0, 1)
                    h_SoWOfEventsAfterFinalSelection.SetBinContent(1, h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(45)))
                    h_SoWOfEventsAfterFinalSelection.SetBinError(1, h_cutflow.GetBinError(h_cutflow.GetXaxis().FindFixBin(45)))
                
                # histogram for the denominator of the TEfficiency object
                    h_SoWOfEventsInXaods = ROOT.TH1D("h_SoWOfEventsInXaods", ";Bin;Sum of weights of all events in xAODs", 1, 0, 1)
                    h_SoWOfEventsInXaods.SetBinContent(1, h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(2)))
                    absoluteUncertaintyOnNEventsInXaods = ROOT.TMath.Sqrt(h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(1))) # because the regular uncertainty on the content of this bin is busted (the content of this bin is changed once we move to another file, not just to another event), so we have to recalculate it
                    relativeUncertaintyOnNEventsInXaods = absoluteUncertaintyOnNEventsInXaods/h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(1))
                    h_SoWOfEventsInXaods.SetBinError(1, relativeUncertaintyOnNEventsInXaods*h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(2)))
                
                # TEfficiency object
                    e_finalSelection = ROOT.TEfficiency(h_SoWOfEventsAfterFinalSelection, h_SoWOfEventsInXaods)
                    e_finalSelection.SetStatisticOption(ROOT.TEfficiency.kFNormal) # to suppress a warning from ROOT
                    LMC_stat=e_finalSelection.GetEfficiencyErrorLow(1)/e_finalSelection.GetEfficiency(1)*100
                    #logger.info("LMC_stat " +str(LMC_stat)+"\n")
                    ImportDateInBase(pathdb+namedb,"Limited_MC_statistics",str(q.group(1)),str(q.group(2))+"3",int(q.group(3)),int(q.group(4)),LMC_stat, "")
            else:
                logger.info("Unexpected error occured in "+fileName+"\n")
            f.Close()
        
    if h2==0:
        print("[ERROR]:Crashed directory")
        logger.error(" Crashed directory. Seems like if there aren`t any directory named <submitDir>")
        if c:
            print("[INFO]:It`s possible, that all files are too old")
            logger.info(" It`s possible, that all files are too old")
        raise BaseException
    file.close()
    
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
        (variation_name text, compilation_date text UNIQUE ON CONFLICT IGNORE, charge real, 
        energy integer, difference real, key text)""")
    print("Base "+name+ " was created successfully!")
    conn.commit()
    conn.close()
    return 0

def ImportDateInBase(file,name,time,t2, M,Z,dif,pref):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    time = datetime.datetime.strptime(time, '%Y-%B-%d_%Hh%Mm%Ss%f')
    time= time.strftime("%Y-%m-%d %H:%M:%S,%f")
    albums = [(name, time+t2 ,Z, M, dif, pref)]
    cursor.executemany("INSERT INTO AE_DATA VALUES (?,?,?,?,?,?)", albums)
    conn.commit()
    conn.close()
    return 0





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
    
    sys.stdout.write('''
   ------------------------------------------------------------
  | Welcome to in DSAE_Short 0.2.7 (spec)                      |
  |                                  (c) 2020, The DSAE Team   |
  |                                                            |
  |  [Settings set as DEFAULT in config/settings.ini]          |
   ------------------------------------------------------------
   
   
''')
    try:
        app_dir = os.path.abspath(os.path.expanduser(os.path.expandvars("./config")))
        cfg = os.path.join(app_dir, "Settings.ini")    
        config = configparser.ConfigParser()
        config.read(cfg)
        if Settings_bug_check()!=0:
            raise Exception
        conf_copy()
        #User Check settings
        path=(config["Settings"]["directory_of_results_modeling"]).replace(os.sep, '/')
        pathdb=(config["Settings"]["directory_for_saving_db"]+"/").replace(os.sep, '/')
        namedb=config["Settings"]["name_of_db"]
        print("\n   --Path------------------------------------------------------\n   "+path)
        print("   "+pathdb+namedb+"\n   ------------------------------------------------------------\n")
        
        
        print("   [DB comilation in DEFAULT mode]\n")
        logger.info("DB comilation in DEFAULT mode")
        
        #Copy .db
        try:
            if os.path.exists(pathdb+namedb):
                if not os.path.exists("./Databases"):  
                    os.makedirs("./Databases")
                copyfile(pathdb+namedb, "Databases/Copy_"+namedb)
                logger.info("File "+pathdb+namedb+" copied successfully.")
        except Exception:
            print("[ERROR]: save copy crushed. Reboot program.")
            raise Exeption
            
        
        #MAKE DATA BASE
        c=False #skip old files flag (impact only on db. Even true will use the newest result in equations)
        makedb(path,pathdb,namedb,c)
        
        
        #PRINT DATA BASE
        conf_copy()
        flag=True
        #User Check settings
        app_dir = os.path.abspath(os.path.expanduser(os.path.expandvars("./config")))
        cfg = os.path.join(app_dir, "Settings.ini")    
        config = configparser.ConfigParser()
        config.read(cfg)
        
        print("   [Table print in DEFAULT mode]\n")
        logger.info("Table print started in DEFAULT mode")
        #directory where you chose db for printing
        pathdb=(config["Settings"]["directory_for_saving_db"]+"/").replace(os.sep, '/') 
        if not config.has_section("Out"): #if it first time printing
            config.add_section("Out")
            logger.info("<Out> section doesn`t exist, so it was created and filled by default meanings")
            
            #Project name
            prog_name="default"
            config.set("Out", "name_of_prog", prog_name)
            #Project saving path 
            path="./output/"+prog_name
            if not os.path.exists(path):
                    os.makedirs(path)
            path=os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
            config.set("Out", "directory_for_saving_res",  os.path.abspath(os.path.expanduser(os.path.expandvars(path))))
            #db name -> path to printing db
            pathdb=(config["Settings"]["directory_for_saving_db"]+"/").replace(os.sep, '/')
            config.set("Out", "used_db_with_path",  os.path.abspath(os.path.expanduser(os.path.expandvars(pathdb+namedb))))
            path=(config["Out"]["directory_for_saving_res"]+"/").replace(os.sep, '/') 
            

            with open(cfg, "w") as configfile1:
                config.write(configfile1)
            print("\n   [Settings successfully changed]")
            print("   if smth went wrong you can check './config/Settings.ini'\n") 
            logger.info("Settings successfully changed")
        else:
            path=(config["Out"]["directory_for_saving_res"]+"/").replace(os.sep, '/')
            prog_name=config["Out"]["name_of_prog"]
            pathdb=(config["Out"]["used_db_with_path"]).replace(os.sep, '/')
            #print("\n   --Path------------------------------------------------------\n   "+pathdb)
            #print("   "+path+"\n   Project name: "+prog_name+".***\n   ------------------------------------------------------------\n")
         
            
            
        #Start
        pathdb=(config["Out"]["used_db_with_path"]).replace(os.sep, '/').split(namedb)[0]
        #Z_end
        Z_end=7.0
        #Z_step
        Z_step=1.0
        #flag
        flag1=1
        #column
        #time_like
        logger.info("Config works properly")
        csv_writer(path+prog_name,pathdb+namedb,Z_end,Z_step,flag1)
        
        
        
    
    
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

    

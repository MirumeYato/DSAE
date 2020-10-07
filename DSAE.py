#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


def Menu(f):
    print("Hi! Welcom to the DSAE (Data Science Analysis Error for multiple charged particle modeling programm)\nThis is mini-prog which helps you to get data from modeling logs\nand view it different ways you like\n\n\nFirst of all, lets choose the path to logs.")
    
    #General settings
    try:
        path=print("Enter the path to your logs repository variationJobs_24Sept2020\npls, use / (slash)")
    except Exception:
        print('SyntaxError')
        
    #Main menu
    import click
    
        #Full data update
        #Partial data update
            #...
        #View
            #full table
            #partial table
                #...
        
        
    return 0


# In[15]:


def FileTagPars(filename): # return smth like link. You should use .group(x) (int x=0-3)
    import sys             # 0-full sring, 1 - name of variation, 2 - "M"+(mass)+"Z"+(charge), 3 - difference (flout)
    import re
    file=open(filename, 'r')
    for line in file:
        strRE = re.compile("AnalysisAlg\W*INFO\W*The (.*) variation was applied, so we compare the final efficiencies for (M.*): difference is (.\d*\.\d*)%")
        if strRE.search(line):
            return strRE.search(line)
        else:
            print("Error occurred: Variation wasn`t applied. Restart modeling")
            return 0


# In[ ]:


def ExportDateInBase(f):
    
    return 0


# In[ ]:


def main():
    
    path=input("enter the path to file, like <D:/Sci/model>")
    err=FileTagPars(path+"/log-0.out")


main()


# In[14]:


def func():
    a, b, c = 12, 13, 14
    return a, b, c

a, b, c = func()

print(a)
print(b)
print(c)
a = func()

print(a[2])


# In[ ]:





# In[4]:


def f():
    import sys
    import re
    file=open("D:/Users/gree-/Desktop/log-0.out", 'r')
    for line in file:
        strRE = re.compile("AnalysisAlg\W*INFO\W*The (.*) variation was applied, so we compare the final efficiencies for (M.*): difference is (.\d*\.\d*)%")
        if strRE.search(line):
            return strRE.search(line)
b= f()
for i in range(4):
    print(str(b.group(i)))
    
    


# In[ ]:





# In[16]:


import click

@click.command()
def g():
    print("I'm a beautiful CLI ")

if __name__ == "__main__":
    g()


# In[ ]:





# In[ ]:





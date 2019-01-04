
# coding: utf-8

# In[58]:


import os
import json
import sys
import re


# In[59]:


ori_path = "subtitle_processed1"
pre_path = "subtitle_processed2"
total_episode = 2


# In[61]:


for i in range(1, total_episode):
    path = ori_path+"/"
    data_list = os.listdir(path)
    
    for j in range(0, len(data_list)):
        f = open(path + data_list[j], "r", encoding='utf-8')
        print(data_list[j])
        lines = f.readlines()
        f.close()
        k = 0
        while True:
            if k >= len(lines):
                break
            b = lines[k].replace('-->', '')
            b = b.replace('(주)', '')
            a = re.sub(r'</?[Ff][Oo][Nn][Tt][\w\s=#"]*>', '', b)
            a = re.sub(r'\[[가-힣\s\w\-/\'()A-Za-z:\".<>,?]*\]', '', a)
            lines[k] = a
            first_tab = lines[k].find('\t')
            second_tab = lines[k][first_tab+1:].find('\t')
            temp = lines[k][:first_tab+second_tab+2]
            lines[k] = lines[k][first_tab+second_tab+2:].replace("\t", " ")
            lines[k] = temp + lines[k]
            z = re.compile(r"[\s]*\-[\sa-zA-z가-힣?!\"\'.,/0-9:]*<br>[\s]*\-")
            if z.search(lines[k])!=None:
                inf = lines[k].split('\t')
                sp = int(inf[0])
                ep = int(inf[1])
                sn = lines[k].find("-")
                n = lines[k].find("<br>")
                seq1 = n-sn
                n1 = lines[k][n:].find("-")
                tmp = lines[k][n+n1+1:]
                seq2 = len(tmp)
                mp = int(  sp + (float(seq1 * (ep - sp)) / (seq1 + seq2)))
                tmp = tmp.replace("\t", " ", 1)
                lines[k] = lines[k][:n] + "\n"
                lines[k] = lines[k].replace("-", "", 1)
                lines[k] = lines[k].replace("<br>", "", 1)
                lines.insert(k+1, str(mp)+"\t"+str(ep)+"\t"+tmp)
                lines[k+1] = lines[k+1].replace("-", "", 1)
                lines[k] = lines[k].replace(inf[1], str(mp), 1)
            
        
            z1 = re.compile(r"[\s]*\-[\sa-zA-z가-힣?!\"\'.,/0-9:]*/[\s]*\-")
            if z1.search(lines[k])!=None:
                inf = lines[k].split('\t')
                sp = int(inf[0])
                ep = int(inf[1])
                sn = lines[k].find("-")
                n = lines[k].find("/")
                seq1 = n-sn
                n1 = lines[k][n:].find("-")
                tmp = lines[k][n+n1+1:]
                seq2 = len(tmp)
                mp = int(  sp + (float(seq1 * (ep - sp)) / (seq1 + seq2)))
                tmp = tmp.replace("\t", " ", 1)
                lines[k] = lines[k][:n] + "\n"
                lines[k] = lines[k].replace("-", "", 1)
                lines[k] = lines[k].replace("/", "", 1)
                lines.insert(k+1, str(mp)+"\t"+str(ep)+"\t"+tmp)
                lines[k+1] = lines[k+1].replace("-", "", 1)
                lines[k] = lines[k].replace(inf[1], str(mp), 1)
            
            z2 = re.compile("/")
            if z2.search(lines[k])!=None:
                inf = lines[k].split('\t')
                sp = int(inf[0])
                ep = int(inf[1])
                sn = 0
                n = lines[k].find("/")
                seq1 = n-sn
                tmp = lines[k][n+1:]
                seq2 = len(tmp)
                mp = int(  sp + (float(seq1 * (ep - sp)) / (seq1 + seq2)))
                tmp = tmp.replace("\t", " ", 1)
                lines[k] = lines[k][:n] + "\n"
                lines[k] = lines[k].replace("/", "", 1)
                lines.insert(k+1, str(mp)+"\t"+str(ep)+"\t"+tmp)
                lines[k] = lines[k].replace(inf[1], str(mp), 1)
                
            z3 = re.compile(r"-[$\sa-zA-z가-힣?!\"\'.,/0-9:]*<br>\-")
            if z3.search(lines[k])!=None:
                inf = lines[k].split('\t')
                sp = int(inf[0])
                ep = int(inf[1])
                sn = 0
                n = lines[k].find("<br>")
                seq1 = n-sn
                n1 = lines[k][n:].find("-")
                tmp = lines[k][n+n1+1:]
                seq2 = len(tmp)
                mp = int(  sp + (float(seq1 * (ep - sp)) / (seq1 + seq2)))
                tmp = tmp.replace("\t", " ", 1)
                lines[k] = lines[k][:n] + "\n"
                lines[k] = lines[k].replace("-", "", 1)
                lines[k] = lines[k].replace("<br>", "", 1)
                lines.insert(k+1, str(mp)+"\t"+str(ep)+"\t"+tmp)
                lines[k+1] = lines[k+1].replace("-", "", 1)
                lines[k] = lines[k].replace(inf[1], str(mp), 1)
                
            z4 = re.compile(r"-[$\sa-zA-z가-힣?!\"\'.,/0-9:]*<BR>[\s]*\-")
            if z4.search(lines[k])!=None:
                inf = lines[k].split('\t')
                sp = int(inf[0])
                ep = int(inf[1])
                sn = 0
                n = lines[k].find("<BR>")
                seq1 = n-sn
                n1 = lines[k][n:].find("-")
                tmp = lines[k][n+n1+1:]
                seq2 = len(tmp)
                mp = int(  sp + (float(seq1 * (ep - sp)) / (seq1 + seq2)))
                tmp = tmp.replace("\t", " ", 1)
                lines[k] = lines[k][:n] + "\n"
                lines[k] = lines[k].replace("-", "", 1)
                lines[k] = lines[k].replace("<BR>", "", 1)
                lines.insert(k+1, str(mp)+"\t"+str(ep)+"\t"+tmp) 
                lines[k+1] = lines[k+1].replace("-", "", 1)
                lines[k] = lines[k].replace(inf[1], str(mp), 1)
                             
            z5 = re.compile(r"<BR>")
            y = re.compile(r"<br>")
                             
            if z5.search(lines[k])!=None:
                inf = lines[k].split('\t')
                n = lines[k].find("<BR>")
                tmp = lines[k][n+4:]
                tmp = tmp.replace("\t", " ", 1)
                lines[k] = lines[k][:n]+ "\n"
                lines[k] = lines[k].replace("<BR>", "", 1)
                lines.insert(k+1, inf[0]+"\t"+inf[1]+"\t"+tmp)
            if y.search(lines[k])!=None:
                inf = lines[k].split('\t')
                n = lines[k].find("<br>")
                tmp = lines[k][n+4:]
                tmp = tmp.replace("\t", " ", 1)
                lines[k] = lines[k][:n] + "\n"
                lines[k] = lines[k].replace("<br>", "", 1)
                lines.insert(k+1, inf[0]+"\t"+inf[1]+"\t"+tmp)
                
            k += 1
        p = re.compile('[^\s]+')
        f = open(pre_path+'/'+ data_list[j], "w", encoding='utf-8')
        for line in lines:
            first_tab = line.find('\t')
            second_tab = line[first_tab+1:].find('\t')
            if p.search(line[first_tab+second_tab+2:])==None:
                print(path + data_list[j],"error", line)
                continue
            
            f.write(line)
        f.close()


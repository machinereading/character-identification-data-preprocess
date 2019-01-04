
# coding: utf-8

# In[30]:


import re
import json
import os


# In[31]:


p1 ="subtitle_processed2"
p2 = "subtitle_final"
total_episode = 2


# In[32]:


z = re.compile(r"[!?\.]+[ \t\r\f\v]+")
for x in range(1, total_episode):
    data_path = p1 + str(x)+"/"
    data_path = p1 + "/"
    data_list = os.listdir(data_path)
#     int(len(data_list)/2)
    for y in range(0, int(len(data_list))):
        f = open(data_path + data_list[y], "r", encoding='utf-8')
        print(data_path + data_list[y], "processing...")
        flines = f.readlines()
        f.close()
        
        k = 0
        
        while True:
            if k>= len(flines):
                break
            inf = flines[k].split('\t')
            pattern_list = [m.end(0) for m in re.finditer(z,inf[2])]
            if pattern_list != []:
                string = inf[0] + "\t" + inf[1] + "\t" + inf[2][:pattern_list[0]] + "\n"
                flines[k] = string
                
                flines.insert(k+1, inf[0] + "\t" + inf[1] + "\t" + inf[2][pattern_list[0]:])
            k += 1
                
        p = re.compile('[^\s]+')
        f = open(p2+'/'+ data_list[y], "w", encoding='utf-8')
        for line in flines:
            if line=="\n":
                continue
            first_tab = line.find('\t')
            second_tab = line[first_tab+1:].find('\t')
            if p.search(line[first_tab+second_tab+2:])==None:
                continue        
            f.write(line)
        f.close()
            


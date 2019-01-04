
# coding: utf-8

# In[65]:


import os
import json
import re


# In[66]:


#data_path = "C:/Users/ADMIN/VTT/n/Friends Season 1/"
#preprocessed_path = "C:/Users/ADMIN/VTT/preprocessed/Friends Season 1/"

data_path = "origin_subtitle/"
preprocessed_path = "subtitle_processed1/"



# In[67]:


data_list = os.listdir(data_path)

for na in range(0, len(data_list)):
    if data_list[na] == '.ipynb_checkpoints':
        continue
    
    f = open(data_path + data_list[na], "r")
    lines = f.readlines()
    KR_list = []
    EN_list = [] 
    templist = []
    optional_number = 0
    for line in lines:
        if optional_number == 1 and line.find('P Class=E') != -1 and EN_list == [] and templist[0] == 'KR':
            optional_number = 0
            templist = []

        if line[0:5] == '<SYNC' and optional_number == 0:
            endmark = line.find('>')
            start_point = int(line[12:endmark])
            if line[-6:-1] == 'KRCC>':
                templist.append('KR')
                templist.append(start_point)
                optional_number = 1
            elif line[-4:-1] == 'CC>':
                templist.append('EN')
                templist.append(start_point)
                optional_number = 1

            else:
                mark = line.find('CC>') + 3
                if line[mark-5:mark-3] == 'KR':
                    templist.append('KR')
                else:
                    templist.append('EN')

                string = line[mark:-1]
                templist.append(start_point)
                templist.append(string)
                optional_number = 1

        elif line[0:5] == '<SYNC'and optional_number == 1:
            endmark = line.find('>')
            end_point = int(line[12:endmark])
            templist.append(end_point)
            if templist[0] == 'KR':
                KR_list.append(templist[1:])
            else:
                EN_list.append(templist[1:])
            templist = []
            if line[-7:-1] == '&nbsp;':
                optional_number = 0
            else:
                if line[-4:-1] == 'CC>':
                    if line[-6:-4] == 'KR':
                        templist.append('KR')
                    else:
                        templist.append('EN')
                    templist.append(end_point)
                    optional_number = 1

                else:
                    stringmark = line.find('CC>') + 3
                    string = line[stringmark:-1]
                    if line[stringmark-5:stringmark-3] == 'KR':
                        templist.append('KR')
                    else:
                        templist.append('EN')
                    templist.append(end_point)
                    templist.append(string)
                    optional_number = 1


        elif optional_number == 1:
            if line[0:6] == '&nbsp;' and len(line) > 7:
                templist.append(line[6:-1])
                optional_number = 1

            elif line[0:6] == '&nbsp;':
                optional_number = 0
                templist = []
                continue

            elif line[0:5] == '<SYNC':
                templist = []
                endmark = line.find('>')
                start_point = int(line[12:endmark])
                if line[-6:-1] == 'KRCC>':
                    templist.append('KR')
                    templist.append(start_point)
                    optional_number = 1
                elif line[-4:-1] == 'CC>':
                    templist.append('EN')
                    templist.append(start_point)
                    optional_number = 1

                else:
                    mark = line.find('CC>') + 3
                    if line[mark-5:mark-3] == 'KR':
                        templist.append('KR')
                    else:
                        templist.append('EN')

                    string = line[mark:-1]
                    templist.append(start_point)
                    templist.append(string)
                    optional_number = 1

            elif line[0:4] != '<!--' and line != '<!--\n' and line !='-->' and line != 'Korean Subtitle End\n'             and line != 'English Subtitle\n' and line != 'Korean Subtitle\n' and line != 'English Subtitle End\n':
                templist.append(line[:-1])
                optional_number = 1


    f.close()
    f = open(preprocessed_path+data_list[na]+"KR_Season"+".txt", "w", encoding='utf-8')
    for KR in KR_list:
        string = ""
        string += str(KR[0])
        string += "\t"
        string += str(KR[-1])
        string += "\t"
        for j in range(1, len(KR)-1):
            string += KR[j]
            string += "\t"
        string += "\n"
        f.write(string)
    f.close()

    f = open(preprocessed_path+data_list[na]+"EN_Season"+".txt", "w", encoding='utf-8')
    for EN in EN_list:
        string = ""
        string += str(EN[0])
        string += "\t"
        string += str(EN[-1])
        string += "\t"
        for j in range(1, len(EN)-1):
            string += EN[j]
            string += "\t"
        string += "\n"
        f.write(string)
    f.close()


# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 15:19:24 2018

@author: Ashley
"""

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
from datetime import datetime
import numpy as np

outpath= 'D:/Python/Insight/csv_data/all_data/'

def firstname_check(code):
    
    if code == 'bennima01' or code == 'carlema01':
        newname = 'matthew'
        
    else:
        newname = []
    return newname    

page_link = 'https://www.hockey-reference.com/leagues/NHL_2017_skaters.html'

page_response = requests.get(page_link, timeout=30)

soup = BeautifulSoup(page_response.content, "html.parser")

# Get player URL
url_list=[]
for link in soup.find_all('a'):
    url_list.append(link.get('href'))


lst_s = [pos for pos, char in enumerate(url_list) if '/leagues/NHL_2017_deaths.html' in char]        
lst_e = [pos for pos, char in enumerate(url_list) if '/leagues/NHL_2017_standings.html' in char]
refined_list =  url_list[lst_s[1]+1:lst_e[-1]-1]
regex=re.compile("/players/") # Find locations in refined list of those that are players and not teams
locs, names = zip(*[(idx, string) for idx, string in enumerate(refined_list) if re.match(regex, string)]) # Then pull out list of names and locations
    

# Get player name
name_list=[] 
first_name=[]
last_name=[]   
#for link in soup.find_all('td', {"class":"left "}):
#    row = str(link)
#    if "csk=" in row:
#        ind_quote= [pos for pos, char in enumerate(row) if char == '"']
#        ind_comma = [pos for pos, char in enumerate(row) if char == ',']
#        
#        
#        
#        last_name.append(row[ind_quote[2]+1:ind_comma[0]])
#        first_name.append(row[ind_comma[0]+1:ind_quote[3]])

    
#names=['/players/s/simpsdi01.html']   
    
# Now run through all player htmls
for i in range(0,len(names)):
    
    idi = [pos for pos, char in enumerate(names[i]) if char == '.']
    code = names[i][11:idi[0]]
    
    player_url = "https://www.hockey-reference.com" + names[i]
   
    page_response = requests.get(player_url, timeout=30)

    soup = BeautifulSoup(page_response.content, "html.parser")
    
    url_list=[]
    
    # Get first last name
    info = str(soup.find_all('a',{'href': names[i]}))
    idi = [pos for pos, char in enumerate(info) if char == '>']
    idi2 =[pos for pos, char in enumerate(info) if char == '<']
    
    found_name = info[idi[1]+1:idi2[2]]
   # found_name = 'Ed-bel conf'
    
    if '.' in found_name:
        
        idi= [pos for pos, char in enumerate(found_name) if char == '.']
        idi2 = [pos for pos, char in enumerate(found_name) if char == ' ']
        
        if int(idi[0])>int(idi2[0]): # dot in the lastname
            first_name.append(found_name[:idi2[0]])
            last_name.append(found_name[idi2[0]+1:])
        else: # dot in first name
            if len(idi)>=1:
                first_name.append(found_name[:idi[1]+1])
                last_name.append(found_name[idi2[0]+1:])
            else:
                first_name.append(found_name[:idi[0]+1])
                last_name.append(found_name[idi2[0]+1:])
                    
    elif '-' in found_name:
        idi= [pos for pos, char in enumerate(found_name) if char == '-']
        idi2 = [pos for pos, char in enumerate(found_name) if char == ' ']
        
        if int(idi[0])>int(idi2[0]): # - in the lastname
            first_name.append(found_name[:idi2[0]])
            last_name.append(found_name[idi2[0]+1:])
        else:
            first_name.append(found_name[:idi2[0]])
            last_name.append(found_name[idi2[0]+1:])
      
    
    elif ' ' in found_name:
        
        idi= [pos for pos, char in enumerate(found_name) if char == ' ']
        if len(idi)<2:
            first_name.append(found_name[:idi[0]])
            last_name.append(found_name[idi[0]+1:])
        else:
            first_name.append(found_name[:idi[0]])
            last_name.append(found_name[idi[0]+1:])
        
        
    print(first_name[i] + ' ' + last_name[i])    
    
    for link in soup.find_all('p'):
        row = str(link)
        
        # Get position, shooting hand
        if 'Position' in row:
            z1 = [pos for pos, char in enumerate(row) if char == ':']
            position = row[z1[0]+2:z1[0]+4]
            if len(z1)>1:
                shoots   = row[z1[1]+2:z1[1]+3]
            else:
                shoots   = "N"
            
        elif 'strong>Draft</strong' in row:
            
            info = [pos for pos, char in enumerate(row) if char == ',']
            draft_pos = row[info[0]+2:info[1]]
            idi = [pos for pos, char in enumerate(draft_pos) if char == 'r']
            idi2 = [pos for pos, char in enumerate(draft_pos) if char == '(']
            idi3 = [pos for pos, char in enumerate(draft_pos) if char == '\xa0']
            
            if idi[0] < 5:
                roundp = int(draft_pos[0])
            else:
                roundp = int(draft_pos[0:2])
             
            posi = draft_pos[idi2[0]+1:idi3[0]]
            
            if len(posi)<4:
                posi = draft_pos[idi2[0]+1:idi2[0]+2]
            elif len(posi)<5:
                posi = draft_pos[idi2[0]+1:idi2[0]+3]
            elif len(posi)<6:
                posi = draft_pos[idi2[0]+1:idi2[0]+4]
                
            draft_pos = float(roundp) + float(posi)/1000   
                
            
            
            info = [pos for pos, char in enumerate(row) if char == '_']
            draft_year = row[info[0]+1:info[1]]
            
            
            
        elif '<p><strong>Current salary' in row:
            
            idi = [pos for pos, char in enumerate(row) if char == '$']
            idi2 = [pos for pos, char in enumerate(row) if char == '<']
            salary = row[idi[0]+1:idi2[-1]]
            
        elif '<p><strong>Current cap hit' in row:
            
            idi = [pos for pos, char in enumerate(row) if char == '$']
            idi2 = [pos for pos, char in enumerate(row) if char == '<']
            cap_hit = row[idi[0]+1:idi2[-1]] 
            
            
            
        
    
    # Team
    info = str(soup.find_all('span',{'itemprop':'affiliation'}))
    idi = [pos for pos, char in enumerate(info) if char == '/']
    if idi!=[]:
        team = info[idi[1]+1:idi[2]]
    else:
        team = 'NNN'
    
    # Height        
    info = str(soup.find_all('span',{'itemprop':'height'}))
    idi = [pos for pos, char in enumerate(info) if char == '<']
    height = info[25:idi[1]]
    if len(height) <=3:
        height = round(int(height[0])*12*2.54 + int(height[2])*2.54)
    else:
        height = round(int(height[0])*12*2.54 + int(height[2:4])*2.54)
        
        
    
    
    # Weight        
    info = str(soup.find_all('span',{'itemprop':'weight'}))
    idi = [pos for pos, char in enumerate(info) if char == '<']
    weight = info[25:idi[1]-2]
    
    # DOB        
    info = str(soup.find_all('span',{'itemprop':'birthDate'}))
    if (info != []) and info != '[]':
        idi = [pos for pos, char in enumerate(info) if char == '"']
        dob = info[idi[0]+1:idi[1]]
    else:
        dob = '1993-07-01'
    
    # country        
    info = str(soup.find_all('span',{'class':'f-i'}))
    if info == '[]':
        country = 'Other'
    else:
        idi = [pos for pos, char in enumerate(info) if char == '-']
        country = info[idi[1]+1:idi[1]+3].upper()
        
    
    # pob        
    info = str(soup.find_all('span',{'itemprop':'birthPlace'}))
    if info!='[]':
        pob='Other'
    else:
        idi = [pos for pos, char in enumerate(info) if char == '>']
        idi2= [pos for pos, char in enumerate(info) if char == '<']
        pob = info[idi[1]+1:idi2[2]]
        
    
    # Obtain standard stats
    years=[]
    teams=[]
    games=[]
    goals=[]
    assists=[]
    points=[]
    plus_minus=[]
    pen_min=[]
    goals_ev=[]
    goals_pp=[]
    goals_sh=[]
    goals_gw=[]
    assists_ev=[]
    assists_pp=[]
    assists_sh=[]
    shots=[]
    shot_pct=[]
    shots_attempted=[]
    time_on_ice=[]
    time_on_ice_avg=[]
    faceoff_wins=[]
    faceoff_losses=[]
    faceoff_pct=[]
    hits=[]
    blocks=[]
    takeaways=[]
    giveaways=[]
    
    
    
    
    for row in soup.findAll("td"):
        
        rows = str(row)
        
        if "/leagues/NHL_" in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '_']
            years.append(rows[idi[1]+1:idi[1]+5])
            
        elif 'a href="/teams' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '/']
            teams.append(rows[idi[1]+1:idi[1]+4])
            
        elif ">TOT<" in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            teams.append(rows[idi[0]+1:idi[0]+4])
        
        elif 'games_played' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                games.append(rows[idi[1]+1:idi2[2]])
            else:    
                games.append(rows[idi[0]+1:idi2[1]])
            
        elif '"goals"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                goals.append(rows[idi[1]+1:idi2[2]]) 
            else:
                goals.append(rows[idi[0]+1:idi2[1]]) 
            
        elif '"assists"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                assists.append(rows[idi[1]+1:idi2[2]]) 
            else:
                assists.append(rows[idi[0]+1:idi2[1]]) 
            
        elif '"points"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                points.append(rows[idi[1]+1:idi2[2]])
            else:
                points.append(rows[idi[0]+1:idi2[1]])  
            
        elif '"plus_minus"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                plus_minus.append(rows[idi[1]+1:idi2[2]])
            else:
                plus_minus.append(rows[idi[0]+1:idi2[1]])
            
        elif '"pen_min"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                pen_min.append(rows[idi[1]+1:idi2[2]])
            else:
                pen_min.append(rows[idi[0]+1:idi2[1]])  
            
        elif '"goals_ev"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                goals_ev.append(rows[idi[1]+1:idi2[2]])
            else:
                goals_ev.append(rows[idi[0]+1:idi2[1]])
            
        elif '"goals_pp"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                goals_pp.append(rows[idi[1]+1:idi2[2]])
            else:
                goals_pp.append(rows[idi[0]+1:idi2[1]]) 
            
        elif '"goals_sh"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                goals_sh.append(rows[idi[1]+1:idi2[2]])
            else:
                goals_sh.append(rows[idi[0]+1:idi2[1]])
            
        elif '"goals_gw"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                goals_gw.append(rows[idi[1]+1:idi2[2]])
            else:
                goals_gw.append(rows[idi[0]+1:idi2[1]])
            
        elif '"assists_ev"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                assists_ev.append(rows[idi[1]+1:idi2[2]])
            else:
                assists_ev.append(rows[idi[0]+1:idi2[1]])
            
        elif '"assists_pp"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                assists_pp.append(rows[idi[1]+1:idi2[2]])
            else:
                assists_pp.append(rows[idi[0]+1:idi2[1]])
            
        elif '"assists_sh"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                assists_sh.append(rows[idi[1]+1:idi2[2]])
            else:
                assists_sh.append(rows[idi[0]+1:idi2[1]])    
            
        elif '"shots"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                shots.append(rows[idi[1]+1:idi2[2]]) 
            else:
                shots.append(rows[idi[0]+1:idi2[1]])    
            
        elif '"shot_pct"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                shot_pct.append(rows[idi[1]+1:idi2[2]]) 
            else:
                shot_pct.append(rows[idi[0]+1:idi2[1]]) 
            
        elif '"shots_attempted"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                shots_attempted.append(rows[idi[1]+1:idi2[2]]) 
            else:
                shots_attempted.append(rows[idi[0]+1:idi2[1]])    
            
        elif '"time_on_ice"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                time_on_ice.append((rows[idi[1]+1:idi2[2]]).replace(':','.'))
            else:
                time_on_ice.append((rows[idi[0]+1:idi2[1]]).replace(':','.'))   
            
        elif '"time_on_ice_avg"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                time_on_ice_avg.append((rows[idi[1]+1:idi2[2]]).replace(':','.'))
            else:
                time_on_ice_avg.append((rows[idi[0]+1:idi2[1]]).replace(':','.'))
            
        elif '"faceoff_wins"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                faceoff_wins.append(rows[idi[1]+1:idi2[2]])
            else:
                faceoff_wins.append(rows[idi[0]+1:idi2[1]]) 
            
        elif '"faceoff_losses"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                faceoff_losses.append(rows[idi[1]+1:idi2[2]])
            else:
                faceoff_losses.append(rows[idi[0]+1:idi2[1]])
            
        elif '"faceoff_percentage"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                faceoff_pct.append(rows[idi[1]+1:idi2[2]])
            else:
                faceoff_pct.append(rows[idi[0]+1:idi2[1]])    
            
        elif '"hits"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                hits.append(rows[idi[1]+1:idi2[2]])
            else:
                hits.append(rows[idi[0]+1:idi2[1]])  
            
        elif '"blocks"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                blocks.append(rows[idi[1]+1:idi2[2]]) 
            else:
                blocks.append(rows[idi[0]+1:idi2[1]]) 
            
        elif '"takeaways"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                takeaways.append(rows[idi[1]+1:idi2[2]])
            else:
                takeaways.append(rows[idi[0]+1:idi2[1]]) 
            
        elif '"giveaways"' in rows:
            
            idi = [pos for pos, char in enumerate(rows) if char == '>']
            idi2 = [pos for pos, char in enumerate(rows) if char == '<']
            
            if '<strong>' in rows:
                giveaways.append(rows[idi[1]+1:idi2[2]])
            else:
                giveaways.append(rows[idi[0]+1:idi2[1]])     
            
    # Advanced stats
    pdo=[]
    ozs=[]
    dzs=[]
    ops=[]
    dps=[]
    years_misc=[]
    
    for row in soup.findAll("div",{'id':'all_skaters_advanced'}):
        
        rows = str(row)
        rows=rows.split('=')
        
        for j in range(0,len(rows)):
            if '"pdo"' in rows[j]:
                
                new_row=rows[j]
                idi = [pos for pos, char in enumerate(new_row) if char == '>']
                idi2 = [pos for pos, char in enumerate(new_row) if char == '<']
                
                if '<strong>' in rows:
                    pdo.append((new_row[idi[1]+1:idi2[1]]))
                else:
                    pdo.append((new_row[idi[0]+1:idi2[0]]))
         
            elif '"zs_offense_pct"' in rows[j]:
                new_row=rows[j]
                idi = [pos for pos, char in enumerate(new_row) if char == '>']
                idi2 = [pos for pos, char in enumerate(new_row) if char == '<']
                
                if '<strong>' in rows:
                    ozs.append((new_row[idi[1]+1:idi2[1]]))
                else:
                    ozs.append((new_row[idi[0]+1:idi2[0]]))
                
            elif '"zs_defense_pct"' in rows[j]:
                new_row=rows[j]
                idi = [pos for pos, char in enumerate(new_row) if char == '>']
                idi2 = [pos for pos, char in enumerate(new_row) if char == '<']
                
                if '<strong>' in rows:
                    dzs.append((new_row[idi[1]+1:idi2[1]]))
                else:
                    dzs.append((new_row[idi[0]+1:idi2[0]]))
                
            elif '"/leagues/NHL_' in rows[j]:
                new_row=rows[j]
                years_misc.append(new_row[14:18])
                
     
    # Miscellaneous stats
    
    for row in soup.findAll("div",{'id':'all_stats_misc_plus_nhl'}):
        rows = str(row)
        rows=rows.split('=')
        
        for j in range(0,len(rows)):
            if '"ops" >' in rows[j]:
                
                new_row=rows[j]
                idi = [pos for pos, char in enumerate(new_row) if char == '>']
                idi2 = [pos for pos, char in enumerate(new_row) if char == '<']
                
                if '<strong>' in new_row:
                    ops.append((new_row[idi[1]+1:idi2[1]]))
                else:
                    ops.append((new_row[idi[0]+1:idi2[0]]))
                
            elif '"dps" >' in rows[j]:
                
                new_row=rows[j]
                idi = [pos for pos, char in enumerate(new_row) if char == '>']
                idi2 = [pos for pos, char in enumerate(new_row) if char == '<']
                if '<strong>' in new_row:
                    dps.append((new_row[idi[1]+1:idi2[1]])) 
                else:
                    dps.append((new_row[idi[0]+1:idi2[0]])) 
    # Bi of a clean up of missing values
    pdo             = ['0.0' if v is '' else v for v in pdo] # correct for some naughtyness. '' values will not convert to floats!
    ozs             = ['0.0' if v is '' else v for v in ozs]
    dzs             = ['0.0' if v is '' else v for v in dzs]
    giveaways       = ['0' if v is '' else v for v in giveaways]
    takeaways       = ['0' if v is '' else v for v in takeaways]
    hits            = ['0' if v is '' else v for v in hits]
    faceoff_pct     = ['0.0' if v is '' else v for v in blocks]
    faceoff_losses  = ['0' if v is '' else v for v in faceoff_losses]
    faceoff_wins    = ['0' if v is '' else v for v in faceoff_wins]
    time_on_ice_avg = ['0.0' if v is '' else v for v in time_on_ice_avg]
    time_on_ice     = ['0.0' if v is '' else v for v in time_on_ice]
    shots_attempted = ['0' if v is '' else v for v in shots_attempted]
    shot_pct        = ['0.0' if v is '' else v for v in shot_pct]
    assists_sh      = ['0' if v is '' else v for v in assists_sh]
    assists_pp      = ['0' if v is '' else v for v in assists_pp]
    assists_ev      = ['0' if v is '' else v for v in assists_ev]
    goals_gw        = ['0' if v is '' else v for v in goals_gw]
    goals_sh        = ['0' if v is '' else v for v in goals_sh]
    goals_pp        = ['0' if v is '' else v for v in goals_pp]
    goals_ev        = ['0' if v is '' else v for v in goals_ev]
    pen_min         = ['0' if v is '' else v for v in pen_min]
    plus_minus      = ['0' if v is '' else v for v in plus_minus]
    points          = ['0' if v is '' else v for v in points]
    assists         = ['0' if v is '' else v for v in assists]
    goals           = ['0' if v is '' else v for v in goals]
    games           = ['0' if v is '' else v for v in games]
    ops             = ['0.0' if v is '' else v for v in ops]
    dps             = ['0.0' if v is '' else v for v in dps]
    blocks          = ['0' if v is '' else v for v in blocks]
    
    myBirthday = datetime(int(dob[0:4]),int(dob[5:7]),int(dob[8:10]))
    now = datetime.now()

    difference  = now - myBirthday
    age = float(((difference.days + difference.seconds/86400)/365.2425))
 
    # Get Capdata and salary data
    
    path = "D:/Python/Insight/csv_data/players/"
    
    
    newname= firstname_check(code)
    
    if newname !=[]:
    
        url = 'https://www.capfriendly.com/players/' + newname + '-' + last_name[i].lower()
        
    else:
        
         url = 'https://www.capfriendly.com/players/' + first_name[i].lower() + '-' + last_name[i].lower() 
         
    page_response = requests.get(url, timeout=30)

    soup = BeautifulSoup(page_response.content, "html.parser")
    
    salary_years=[]
    cap_hit=[]
    salary=[]
    bonus=[]
    
    rows = str(soup)
    rows=rows.split('\n')
    idi1 = [pos for pos, char in enumerate(rows) if '$' in char and 'AHL' in char]
    idi1.reverse()
    if idi1 !=[]:
        for j in range(0,len(idi1)):    
            rows1 = rows[idi1[j]]
            rows1 = rows1.split('td')
            idi = [pos for pos, char in enumerate(rows1) if ' class="left">20' in char]
            
            for k in range(0,len(idi)):
                salary_years.append('20'+ rows1[idi[k]][19:21])
                
                if len(rows1[idi[k]:-1])>=4:
                
                    helpp = [pos for pos, char in enumerate(rows1[idi[k]+4]) if char == '<']
                    helpp1 = [pos for pos, char in enumerate(rows1[idi[k]+4]) if char == '$']
                    if helpp1==[]:
                        cap_hit.append('-999')
                    else:
                        cap_hit.append((rows1[idi[k]+4][helpp1[0]+1:helpp[0]]).replace(',',''))
                else:
                    cap_hit.append('-999')
              
                if len(rows1[idi[k]:-1])>=14:
                
                    helpp = [pos for pos, char in enumerate(rows1[idi[k]+14]) if char == '<']
                    helpp1 = [pos for pos, char in enumerate(rows1[idi[k]+14]) if char == '$']
                    if helpp1==[]:
                        salary.append('-999')
                    else:
                        salary.append((rows1[idi[k]+14][helpp1[0]+1:helpp[0]]).replace(',',''))
                else:
                    salary.append('-999')
        
        new_salary=['-999']*len(years) 
        new_cap = new_salary
        for j in range(0,len(years)):
            
            for k in range(0,len(salary_years)):
                
                if years[j] == salary_years[k]:
                    
                    new_salary[j]=salary[k]
                    new_cap[j] = cap_hit[k]
                
        
        
        salary  = new_salary
        cap_hit = new_cap 
        
    else:
        salary = ['-999']*len(years) 
        cap_hit =['-999']*len(years) 
    
       
    if os.path.exists(path + code + '.txt'):
        print(path + code + '.txt already exists')
    else:
        g = open(path + code + '.txt','w')
        g.write(code + "\n")
        g.write(first_name[i] + "\n")
        g.write(last_name[i] + "\n")
        g.write(position + "\n")
        g.write(shoots + "\n")
        g.write(draft_year + "\n")
        g.write(str(draft_pos) + "\n")
        g.write(str(age) + "\n")
        #g.write(salary + "\n")
        #g.write(cap_hit + "\n")
        g.write(team + "\n")
        g.write(str(height) + "\n")
        g.write(weight + "\n")
        g.write(dob + "\n")
        g.write(country + "\n")
        g.write(pob + "\n")
        
        g.write("\n")
        
        g.write('Year,' + 'Team,' + 'Games,' + 'Goals,' + 'Assists,' + 'Points,' + 'PM,' + 'Pen,' + 'Gev,' + 'Gpp,' + 'Gsh,' + 'Ggw,' 
                + 'Aev,' + 'App,' + 'Ash,' + 'S,' + 'SA,' + 'TOI,' + 'TOIavg,' + 'FOw,' + 'FOl,' + 'H,' + 'Bks,' + 'Tky,' 
                + 'Gvy,' + 'pdo,' + 'ozs,' + 'dzs,' + 'ops,' + 'dps,' + 'salary,' + 'cap_hit,' '\n')
        
        for k in range(0,len(years)):
            if int(years[k])>=2008:
                diff = len(years) - len(years_misc) # AS ADVANCED STATS STARTED IN 2008, LENGHTS OF ARRAYS WILL BE DIFFERENT IF PLAYER WAS ACTIVE BEFORE 2008. HERE WE ACCOUNT FO THIS
                g.write(years[k] + ',' + teams[k] + ',' + games[k] + ',' + goals[k] + ',' + assists[k] + ',' + points[k] + ',' + plus_minus[k] + ',' +  pen_min[k] + ',' +  goals_ev[k] + ',' + goals_pp[k] + ',' + goals_sh[k] + ',' + goals_gw[k] + ',' + assists_ev[k] + ',' + assists_pp[k]+ ',' + assists_sh[k] + ',' + shots[k] + ',' + shots_attempted[k] + ',' + time_on_ice[k] + ',' + time_on_ice_avg[k]+ ',' + faceoff_wins[k] + ',' + faceoff_losses[k] + ',' + hits[k] + ',' + blocks[k] + ',' + takeaways[k]+ ',' +  giveaways[k] + ',' + pdo[k-diff] + ',' + ozs[k-diff] + ',' + dzs[k-diff] + ',' + ops[k] + ',' + dps[k] + ',' + salary[k] + ',' + cap_hit[k] + '\n')
        
                fields = 'code','first_name','last_name','position','shoots','draft_year','draft_pos','height','weight','dob','age','country','pob',\
                    'years','teams','games','goals','assists','points','plus_minus',\
                    'pen_min','goals_ev','goals_pp','goals_sh','goals_gw','assists_ev','assists_pp',\
                    'assists_sh','shots','shots_attempted','time_on_ice','time_on_ice_avg',\
                    'faceoff_wins','faceoff_losses','hits','blocks','takeaways','giveaways',\
                    'pdo','ozs','dzs','ops','dps','salary','cap_hit'
                    
                data_field = code, first_name[i], last_name[i], position, shoots, int(draft_year), draft_pos, int(height), int(weight), dob, age, country, pob, \
                    int(years[k]),teams[k],int(games[k]),int(goals[k]),int(assists[k]),int(points[k]),int(plus_minus[k]), \
                    int(pen_min[k]), int(goals_ev[k]),int(goals_pp[k]),int(goals_sh[k]),int(goals_gw[k]),int(assists_ev[k]),int(assists_pp[k]), \
                    int(assists_sh[k]),int(shots[k]),int(shots_attempted[k]),float(time_on_ice[k]),float(time_on_ice_avg[k]), \
                    int(faceoff_wins[k]),int(faceoff_losses[k]),int(hits[k]),int(blocks[k]),int(takeaways[k]), int(giveaways[k]),\
                    float(pdo[k-diff]),float(ozs[k-diff]),float(dzs[k-diff]),float(ops[k]),float(dps[k]),int(salary[k]),int(cap_hit[k])
               
                with open(outpath + 'data.csv', 'a', newline='') as csv_file:
                    wr = csv.writer(csv_file, delimiter=',')
                    wr.writerow(data_field)
        
        g.close()
        
        
        
        
    
        
        
      

    
    
    
    
   
    
               
        
        
    
    
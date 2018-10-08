
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# ## Load individual CSVs from corsica

# In[2]:


df_2018 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2018.txt')
df_2017 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2017.txt')
df_2016 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2016.txt')
df_2015 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2015.txt')
df_2014 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2014.txt')
df_2013 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2013.txt')
df_2012 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2012.txt')
df_2011 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2011.txt')
df_2010 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2010.txt')
df_2009 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2009.txt')
df_2008 = pd.read_csv('D:/Python/Insight/csv_data/corsica/raw/2008.txt')

df = pd.concat([df_2018,df_2017,df_2016,df_2015,df_2014,df_2013,df_2012,df_2011,df_2010,df_2009,df_2008])

df = df.reset_index(drop=True)


# ## Match name tag/keys

# In[3]:


firstname= []
lastname = []

for i in range(0,len(df)):
    
    name = df['Player'][i]
    
    if '.' in name:
        if '..' in name:
            idi= [pos for pos, char in enumerate(name) if char == '.']
            firstname.append(name[:idi[0]][0] + '.' + name[:idi[0]][2] + '.')
            lastname.append(name[idi[1]+1:])
        elif '.' in name:
            idi= [pos for pos, char in enumerate(name) if char == '.']
            idi2= [pos for pos, char in enumerate(name) if char == ' ']
            firstname.append(name[:idi2[0]])
            lastname.append(name[idi2[0]+1:])
    elif '-' in name:
        idi= [pos for pos, char in enumerate(name) if char == '-']
        idi2= [pos for pos, char in enumerate(name) if char == ' ']
        if int(idi[0]) > int(idi2[0]): # Surname
            firstname.append(name[:idi2[0]])
            lastname.append(name[idi2[0]+1:])
        else:
            firstname.append(name[:idi2[0]])
            lastname.append(name[idi2[0]+1:])
    elif '(' in name:
        idi= [pos for pos, char in enumerate(name) if char == '(']
        idi2= [pos for pos, char in enumerate(name) if char == ')']
        idi3=  [pos for pos, char in enumerate(name) if char == ' ']

        name = name[:idi[0]-1] + name[idi2[0]+1:]
        firstname.append(name[:idi3[0]])
        lastname.append(name[idi3[0]+1:])

    elif ' ' in name:
        idi=  [pos for pos, char in enumerate(name) if char == ' ']
        firstname.append(name[:idi[0]])
        lastname.append(name[idi[0]+1:])
 

df['Firstname'] = firstname
df['Lastname']  = lastname
df['Lastname'] = df.Lastname.str.capitalize()
df['Firstname'] = df.Firstname.str.capitalize()


# In[4]:


df1=df.reset_index(drop=True)


# In[5]:


df1['Lastname_1'] = df1.Lastname.str.replace('-' , '')
df1['Lastname_1'] = df1.Lastname_1.str.replace('.' , '')
df1['Lastname_1'] = df1.Lastname_1.str.replace('(' , '')
df1['Lastname_1'] = df1.Lastname_1.str.replace(')' , '')
df1['Lastname_1'] = df1.Lastname_1.str.replace(' ' , '')
df1['Lastname_1'] = df1.Lastname_1.str.replace(r"[']" , '')

df1['Firstname_1'] = df1.Firstname.str.replace('-' , '')
df1['Firstname_1'] = df1.Firstname_1.str.replace('.' , '')
df1['Firstname_1'] = df1.Firstname_1.str.replace(')' , '')
df1['Firstname_1'] = df1.Firstname_1.str.replace('(' , '')
df1['Firstname_1'] = df1.Firstname_1.str.replace(' ' , '')
df1['Firstname_1'] = df1.Firstname_1.str.replace(r"['']", '')


# In[6]:


codes=[]
years=[]


for i in range(0,len(df1)):
    
   
    codes.append((df1['Lastname_1'][i][0:5] + df1['Firstname_1'][i][0:2]).lower())
    idi= [pos for pos, char in enumerate(df['Season'][i]) if char == '-']
    years.append(2000 + int(df['Season'][i][idi[0]+1:]))
df1['Code'] = codes
df1['Years'] = years

df1 = df1.reset_index(drop=True)


# In[7]:


df1 = df1.sort_values(['Lastname','Years']).reset_index(drop=True)
df1.head(50)


# ## Load hockey-ref. and salary data
# 
# 

# In[8]:


df2 = pd.read_csv('D:/Python/Insight/csv_data/all_data/All_data_HRef - data.csv') 
df2.head()


# In[9]:


df2.Year


# ## Remove 'TOT' from data. This is data for years when a player played on more than one team

# In[10]:


df2_edit = df2[df2.Team != 'TOT'].reset_index(drop=True)
df2_edit=df2.copy()


# ## Plan to concat corsica to hockey-ref, hence adding required variables

# In[11]:


df2_edit['P/60'] = [np.nan]*len(df2_edit)
df2_edit['P1/60'] = [np.nan]*len(df2_edit)
df2_edit['GS/60'] = [np.nan]*len(df2_edit)
df2_edit['CF'] = [np.nan]*len(df2_edit)
df2_edit['CA'] = [np.nan]*len(df2_edit)
df2_edit['CF%'] = [np.nan]*len(df2_edit)
df2_edit['Rel CF%'] = [np.nan]*len(df2_edit)
df2_edit['GF'] = [np.nan]*len(df2_edit)
df2_edit['GA'] = [np.nan]*len(df2_edit)
df2_edit['xGF'] = [np.nan]*len(df2_edit)
df2_edit['xGA'] = [np.nan]*len(df2_edit)
df2_edit['xGF%'] = [np.nan]*len(df2_edit)
df2_edit['Rel xGF%'] = [np.nan]*len(df2_edit)
df2_edit['Rel CF%'] = [np.nan]*len(df2_edit)
df2_edit['iPENT'] = [np.nan]*len(df2_edit)
df2_edit['iPEND'] = [np.nan]*len(df2_edit)
df2_edit['iSh%'] = [np.nan]*len(df2_edit)
df2_edit['ixGF'] = [np.nan]*len(df2_edit)
df2_edit['ixGF/60'] = [np.nan]*len(df2_edit)
df2_edit['ZSR'] = [np.nan]*len(df2_edit)
df2_edit['TOI%'] = [np.nan]*len(df2_edit)
df2_edit['TOI% QoT'] = [np.nan]*len(df2_edit)
df2_edit['CF% QoT'] = [np.nan]*len(df2_edit)
df2_edit['TOI% QoC'] = [np.nan]*len(df2_edit)
df2_edit['CF% QoC'] = [np.nan]*len(df2_edit)
df2_edit['GP'] = [np.nan]*len(df2_edit)
df2_edit['TOI'] = [np.nan]*len(df2_edit)
df2_edit['G'] = [np.nan]*len(df2_edit)
df2_edit['A'] = [np.nan]*len(df2_edit)
df2_edit['P'] = [np.nan]*len(df2_edit)
df2_edit['P1'] = [np.nan]*len(df2_edit)
df2_edit['GS'] = [np.nan]*len(df2_edit)
df2_edit['C+/-'] = [np.nan]*len(df2_edit)
df2_edit['G+/-'] = [np.nan]*len(df2_edit)
df2_edit['GF%'] = [np.nan]*len(df2_edit)
df2_edit['xGF%'] = [np.nan]*len(df2_edit)
df2_edit['xG+/-'] = [np.nan]*len(df2_edit)
df2_edit['iP+/-'] = [np.nan]*len(df2_edit)
df2_edit['iCF'] = [np.nan]*len(df2_edit)
df2_edit['iCF/60'] = [np.nan]*len(df2_edit)

df2_edit.index.name = 'Ind'
df2_edit.head(20)


# ## Add new variables

# In[12]:


for i in range(0,len(df1)):

    year = df1['Years'][i]
    team = df1['Team'][i]

    potentials = df2_edit[df2_edit.Code.str.contains(df1['Code'][i], regex='True')]
    uniques = potentials['Code'].unique()

    if len(uniques) < 2:
        
        info= potentials[potentials['Year'] == year]
        idi = info.index.values.tolist()
        #df2_edit['CF% QOC'][idi] = df1['CF% QoC'][i]
        
        df2_edit['P/60'][idi]     = df1['P/60'][i]    
        df2_edit['P1/60'][idi]    = df1['P1/60'][i]   
        df2_edit['GS/60'][idi]    = df1['GS/60'][i]   
        df2_edit['CF'][idi]       = df1['CF'][i]      
        df2_edit['CA'][idi]       = df1['CA'][i]      
        df2_edit['CF%'][idi]      = df1['CF%'][i]     
        df2_edit['Rel CF%'][idi]  = df1['Rel CF%'][i] 
        df2_edit['GF'][idi]       = df1['GF'][i]      
        df2_edit['GA'][idi]       = df1['GA'][i]      
        df2_edit['xGF'][idi]      = df1['xGF'][i]     
        df2_edit['xGA'][idi]      = df1['xGA'][i]     
        df2_edit['xGF%'][idi]     = df1['xGF%'][i]    
        df2_edit['Rel xGF%'][idi] = df1['Rel xGF%'][i]
        df2_edit['Rel CF%'][idi]  = df1['Rel CF%'][i] 
        df2_edit['iPENT'][idi]    = df1['iPENT'][i]   
        df2_edit['iPEND'][idi]    = df1['iPEND'][i]
        df2_edit['iSh%'][idi]     = df1['iSh%'][i]
        df2_edit['ixGF'][idi]     = df1['ixGF'][i]
        df2_edit['ixGF/60'][idi]  = df1['ixGF/60'][i] 
        df2_edit['ZSR'][idi]      = df1['ZSR'][i]     
        df2_edit['TOI%'][idi]     = df1['TOI%'][i]    
        df2_edit['TOI% QoT'][idi] = df1['TOI% QoT'][i]
        df2_edit['CF% QoT'][idi]  = df1['CF% QoT'][i] 
        df2_edit['TOI% QoC'][idi] = df1['TOI% QoC'][i]
        df2_edit['CF% QoC'][idi]  = df1['CF% QoC'][i] 
        df2_edit['GP'][idi]       = df1['GP'][i]
        df2_edit['TOI'][idi]      = df1['TOI'][i]
        df2_edit['G'][idi]        = df1['G'][i]
        df2_edit['A'][idi]        = df1['A'][i]
        df2_edit['P'][idi]        = df1['P'][i]
        df2_edit['P1'][idi]       = df1['P1'][i]
        df2_edit['GS'][idi]       = df1['GS'][i]
        df2_edit['C+/-'][idi]     = df1['C+/-'][i]
        df2_edit['G+/-'][idi]     = df1['G+/-'][i]
        df2_edit['GF%'][idi]      = df1['GF%'][i]
        df2_edit['xGF%'][idi]     = df1['xGF%'][i]
        df2_edit['xG+/-'][idi]   = df1['xG+/-'][i]
        df2_edit['iP+/-'][idi]    = df1['iP+/-'][i]
        df2_edit['iCF'][idi]     = df1['iCF'][i]
        df2_edit['iCF/60'][idi]   = df1['iCF/60'][i]

    else:
        
        for j in range(0,len(uniques)):
            
            player = df2_edit[df2_edit['Code'] == uniques[j]]
            
            info = player[(player['Team'] == team) & (player['Year'] == year)] 
            
            if not info.empty:
                
                idi = info.index.values.tolist()
                
                df2_edit['P/60'][idi]     = df1['P/60'][i]    
                df2_edit['P1/60'][idi]    = df1['P1/60'][i]   
                df2_edit['GS/60'][idi]    = df1['GS/60'][i]   
                df2_edit['CF'][idi]       = df1['CF'][i]      
                df2_edit['CA'][idi]       = df1['CA'][i]      
                df2_edit['CF%'][idi]      = df1['CF%'][i]     
                df2_edit['Rel CF%'][idi]  = df1['Rel CF%'][i] 
                df2_edit['GF'][idi]       = df1['GF'][i]      
                df2_edit['GA'][idi]       = df1['GA'][i]      
                df2_edit['xGF'][idi]      = df1['xGF'][i]     
                df2_edit['xGA'][idi]      = df1['xGA'][i]     
                df2_edit['xGF%'][idi]     = df1['xGF%'][i]    
                df2_edit['Rel xGF%'][idi] = df1['Rel xGF%'][i]
                df2_edit['Rel CF%'][idi]  = df1['Rel CF%'][i] 
                df2_edit['iPENT'][idi]    = df1['iPENT'][i]   
                df2_edit['iPEND'][idi]    = df1['iPEND'][i]
                df2_edit['iSh%'][idi]     = df1['iSh%'][i]
                df2_edit['ixGF'][idi]     = df1['ixGF'][i]
                df2_edit['ixGF/60'][idi]  = df1['ixGF/60'][i] 
                df2_edit['ZSR'][idi]      = df1['ZSR'][i]     
                df2_edit['TOI%'][idi]     = df1['TOI%'][i]    
                df2_edit['TOI% QoT'][idi] = df1['TOI% QoT'][i]
                df2_edit['CF% QoT'][idi]  = df1['CF% QoT'][i] 
                df2_edit['TOI% QoC'][idi] = df1['TOI% QoC'][i]
                df2_edit['CF% QoC'][idi]  = df1['CF% QoC'][i]
                df2_edit['GP'][idi]       = df1['GP'][i]
                df2_edit['TOI'][idi]      = df1['TOI'][i]
                df2_edit['G'][idi]        = df1['G'][i]
                df2_edit['A'][idi]        = df1['A'][i]
                df2_edit['P'][idi]        = df1['P'][i]
                df2_edit['P1'][idi]       = df1['P1'][i]
                df2_edit['GS'][idi]       = df1['GS'][i]
                df2_edit['C+/-'][idi]     = df1['C+/-'][i]
                df2_edit['G+/-'][idi]     = df1['G+/-'][i]
                df2_edit['GF%'][idi]      = df1['GF%'][i]
                df2_edit['xGF%'][idi]     = df1['xGF%'][i]
                df2_edit['xG+/-'][idi]   = df1['xG+/-'][i]
                df2_edit['iP+/-'][idi]    = df1['iP+/-'][i]
                df2_edit['iCF'][idi]     = df1['iCF'][i]
                df2_edit['iCF/60'][idi]   = df1['iCF/60'][i]


 


# In[13]:


df1.keys()


# In[14]:


#potentials = df2_edit[df2_edit.Code.str.contains('adamscr', regex='True')]
#ids = potentials.index.values.tolist()
#uniques = potentials['Code'].unique()


# In[15]:


#df2_edit[(df2_edit['First_name'] == 'Marcel') & (df2_edit['Team'] == 'NYR') ]


# ## Replace empty data with nans

# In[16]:


df2_edit[df2_edit==-999]=np.nan
#df2_edit[df2_edit==-'999']=np.nan
df2_edit[df2_edit=='--']=np.nan


# In[17]:


df2_edit.head()


# ## Save to file

# In[18]:


df2_edit.to_csv('out.csv', sep=',')


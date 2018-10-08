
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import plotly
plotly.tools.set_credentials_file(username='w9641432', api_key='LDqLiys5zhXKvdyZc6J1')

import plotly.plotly as py

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# For Notebooks
init_notebook_mode(connected=True)

import cufflinks as cf
cf.go_offline()


# ## Load in Scraped Data
# 

# In[2]:


df = pd.read_csv('D:/Python/Insight/csv_data/all_data/final/out.csv')

df.info()  


# ## Do some data filtering that was missed in scraping

# In[3]:


df2=df.copy()
df2=df2.rename(columns = {'CF% QoC':'CFQoC'})
df2=df2.rename(columns = {'CF% QoT':'CFQoT'})
df2=df2.rename(columns = {'TOI% QoT':'TOIQoT'})

tmplst = list(df2['TOI% QoC'])
del df2['TOI% QoC']
df2['TOIQoC'] = tmplst

df2['Age_dot'] = df2['Age']
del df2['Age']
age = []
nsalary = []
maxvalue=[]
tps = [] 
dp=[]

for i in range(0,len(df2)):
    
    age.append((df2['Year'][i] -df2['Draft_year'][i]) + 18)
     
    temp = df2[df2['Year'] == df2['Year'][i]]
    maxvalue = temp['Salary'].max()
    nsalary.append(df2['Salary'][i]/maxvalue)
    tps.append(df2['OPS'][i] + df2['DPS'][i])
    
    #dp.append(df2['Draft_round'][i][0])
   
df2['Age'] = age  
df2['Salary_norm'] = nsalary
df2['TPS'] = tps

df2['CodeL'] = (np.nan)*len(df2)

codesu = df2['Code'].unique()
values=[]
for i in range(0,len(codesu)):
    info= df2[df2['Code'] == codesu[i]]
    idi = info.index.values.tolist()
    df2['CodeL'][idi]     = int(i+1)  
    
     
    
    


#df2['Round'] = dp

#df2 = df2[df2.Salary != -999].reset_index(drop=True)
#df2 = df2[df2.Year != 2018].reset_index(drop=True)
#df2018 = df2[df2.Year == 2018].reset_index(drop=True)


#df2['Round'] = df2[['Round']].astype(int)

#df2['Position']=df2[df2.Position =='C/']='C'
#df2['Position'] = df2[df2.Position =='W']='LW'

df2.info() 
df3 = df2.dropna().reset_index(drop=True)


# ## Salary distribution

# In[5]:


plt.figure(figsize=(16,12),dpi=300)
ax = df['Salary'].hist(bins=30)

ax.set_ylabel('Frequency', size=20)
ax.set_xlabel('USD [Million]', size=20)
ax.xaxis.set_tick_params(labelsize=15)
ax.yaxis.set_tick_params(labelsize=15)


# ## Look at Age vs Salary
# 
# 

# In[19]:


g = sns.JointGrid(x="Age_dot", y="Salary", data=df3)
g.plot_joint(plt.scatter, color=".1", edgecolor="white")
g.plot_marginals(sns.distplot, kde=True, color="b")
g.fig.set_figwidth(12)
g.fig.set_figheight(10)
g.set_axis_labels('Age [Years]', 'Salary [USD Million]', fontsize=20)
g.set_tick_params(axis="both", labelsize=15)
sns.despine()
plt.tight_layout()


# ## So remove the kids under 22

# ## How about some logical key metrics vs Salary?

# In[21]:


g = sns.jointplot('Points', 'Salary', data=df3, kind="reg")
g.fig.set_figwidth(16)
g.fig.set_figheight(4)
h = sns.jointplot('Points', 'Salary', data=df3, kind="resid")
h.fig.set_figwidth(16)
h.fig.set_figheight(4)
i = sns.jointplot('TPS', 'Salary', data=df3, kind="reg")
i.fig.set_figwidth(16)
i.fig.set_figheight(4)


# ## A closer look at TPS vs Salary

# In[7]:


LW = df3[df3['Position']=='LW']
C =  df3[df3['Position']=='C']
RW = df3[df3['Position']=='RW']
D =  df3[df3['Position']=='D']

fig = {
    'data': [
        {'x': LW.Points, 'y': LW.Salary, 'text': LW.Last_name, 'mode': 'markers', 'name': 'LW'},
        {'x': C.Points, 'y': C.Salary, 'text': C.Last_name, 'mode': 'markers', 'name': 'C'},
        {'x': RW.Points, 'y': RW.Salary, 'text': RW.Last_name, 'mode': 'markers', 'name': 'RW'},
        {'x': D.Points, 'y': D.Salary, 'text': D.Last_name, 'mode': 'markers', 'name': 'D'}
       
    ],
    'layout': {
        'xaxis': {'title': 'TPS', 'type': 'linear'},
        'yaxis': {'title': "Salary"}
    }
}
py.iplot(fig)


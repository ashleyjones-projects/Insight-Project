
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

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import r2_score
import statsmodels.formula.api as sm


# In[2]:


df = pd.read_csv('D:/Python/Insight/csv_data/all_data/final/out.csv')


# In[4]:


df2=df.copy()
df2=df2.rename(columns = {'CF% QoC':'CFQoC'})
df2=df2.rename(columns = {'CF% QoT':'CFQoT'})
df2=df2.rename(columns = {'TOI% QoT':'TOIQoT'})

tmplst = list(df2['TOI% QoC'])
del df2['TOI% QoC']
df2['TOIQoC'] = tmplst

del df2['Age']
age = []
nsalary = []
maxvalue=[]
tps = [] 
dp=[]
new_year=[]

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
df2['New_year'] = df2['Year'] - 2007
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


# In[6]:


#df3 = df3[(df3.Age >=22)].reset_index(drop=True)
#or i in range(0,len(df3)):
#    if (df3['Salary_norm'][i] < 0.16) &  (df3['TPS'][i] > 5): #(df3['Points'][i] > 41):
#        df3['TPS'][i] = np.nan

#df3 = df3[(df3.Salary_norm >0.4)].reset_index(drop=True)        
df3.dropna()        


# In[7]:


df4=df3.copy()

arr =  np.array([0.0, 0.45, 1])
Bins   = arr.searchsorted(df3.Salary_norm) 
Salary = df3['Salary']
Salary_norm = df3['Salary_norm']
df3.drop(['Salary','Salary_norm','Cap_hit','DOB','Place','Position','Code','First_name','Last_name','Place','Team','G_pp','G_sh','A_pp','A_sh','Ind','Height','Draft_round','ZSR'], axis=1, inplace = True)


# In[8]:


data1 = df4[df4['Position'] != 'D']
data = np.array(data1[['OZS','CFQoC']])

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)

kmeans.fit(data)
kmeans.cluster_centers_
labels = kmeans.labels_

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True,figsize=(18,6))
ax2.set_title('K Means')
ax2.scatter(data[:,0],data[:,1],c=kmeans.labels_,cmap='rainbow')
ax2.set_xlabel('Offensive Zone Starts')
ax2.set_ylabel('Quality of Competition')
ax1.set_title("Original")
ax1.scatter(data[:,0],data[:,1])
ax1.set_xlabel('Offensive Zone Starts')
ax1.set_ylabel('Quality of Competition')


# In[9]:


df4['Role'] = [np.nan]*len(df4)
df4['Role'].loc[df4['Position'] != 'D'] = labels


# In[10]:


data1 = df4[df4['Position'] == 'D']
data = np.array(data1[['OZS','CFQoC']])

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2)

kmeans.fit(data)
kmeans.cluster_centers_
labels = kmeans.labels_

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True,figsize=(18,6))
ax2.set_title('K Means')
ax2.scatter(data[:,0],data[:,1],c=kmeans.labels_,cmap='rainbow')
ax2.set_xlabel('Offensive Zone Starts')
ax2.set_ylabel('Quality of Competition')
ax1.set_title("Original")
ax1.scatter(data[:,0],data[:,1])
ax1.set_xlabel('Offensive Zone Starts')
ax1.set_ylabel('Quality of Competition')

df4['Role'].loc[df4['Position'] == 'D'] = labels


# In[11]:



DDguys = df4[(df4['Position'] == 'D') & (df4['Role'] == 0)];del DDguys['Salary_norm']
ODguys = df4[(df4['Position'] == 'D') & (df4['Role'] == 1)];del ODguys['Salary_norm']

DFguys = df4[(df4['Position'] != 'D') & (df4['Role'] == 1)];del DFguys['Salary_norm']
toF    = df4[(df4['Position'] != 'D') & (df4['Role'] == 0)];del toF['Salary_norm']
OFguys = df4[(df4['Position'] != 'D') & (df4['Role'] == 2)];del OFguys['Salary_norm']

DDguys = DDguys.reset_index(drop=True)
DFguys = DFguys.reset_index(drop=True)
toF = toF.reset_index(drop=True)
ODguys = ODguys.reset_index(drop=True)
OFguys = OFguys.reset_index(drop=True)

Defense = df4[df4['Position'] == 'D']
Offense = df4[df4['Position'] != 'D']


# In[12]:



nsalary = []

for i in range(0,len(DDguys)):
     
    temp = Defense[Defense['Year'] == DDguys['Year'][i]]
    maxvalue = temp['Salary'].max()
    
    nsalary.append(DDguys['Salary'][i]/maxvalue)

DDguys['Salary_norm'] = nsalary; nsalary=[]


for i in range(0,len(DFguys)):
     
    temp = Offense[Offense['Year'] == DFguys['Year'][i]]
    maxvalue = temp['Salary'].max()
    nsalary.append(DFguys['Salary'][i]/maxvalue)    

DFguys['Salary_norm'] = nsalary; nsalary=[] 

for i in range(0,len(toF)):
     
    temp = Offense[Offense['Year'] == toF['Year'][i]]
    maxvalue = temp['Salary'].max()
    nsalary.append(toF['Salary'][i]/maxvalue)    

toF['Salary_norm'] = nsalary; nsalary=[]    

for i in range(0,len(ODguys)):
     
    temp = Defense[Defense['Year'] == ODguys['Year'][i]]
    maxvalue = temp['Salary'].max()
    nsalary.append(ODguys['Salary'][i]/maxvalue)

ODguys['Salary_norm'] = nsalary; nsalary=[]

aren = list(range(2008,2019))

for i in range(0,len(OFguys)):
     
    temp = Offense[Offense['Year'] == OFguys['Year'][i]]
    maxvalue = temp['Salary'].max()
    nsalary.append(OFguys['Salary'][i]/maxvalue)

OFguys['Salary_norm'] = nsalary; nsalary=[]

Offense = pd.concat([OFguys,toF,DFguys]).sort_values(by=['Code','Year']).reset_index(drop=True)
Defense = pd.concat([ODguys,DDguys]).sort_values(by=['Code','Year']).reset_index(drop=True)


# In[13]:


data = Offense.copy()

raised = (data[data['Salary'].diff() > 0])


##idi = raised.index-1

#raised = data.ix[idi]


data=raised

data.dropna(inplace=True)
data=data.reset_index(drop=True)


# In[14]:


import scipy as sp
val=data
ck = np.column_stack([val['Age'],val['HIT'],val['Draft_round'],val['CFQoC'],val['TKY'],val['BLK'],val['OPS'],val['CFQoT'],val['GWY'],val['Rel CF%'],val['OZS'],val['TOI_avg']])
cc = sp.corrcoef(ck, rowvar=False)
VIF = np.linalg.inv(cc)
VIF.diagonal()


# In[17]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import r2_score
import statsmodels.formula.api as sm

# construct our linear regression model


data1=data.copy()
data1['OPS2'] = 2* data1['OPS']
data1['TOI_avg2'] = data1['TOI_avg']**2
data1['Age2'] = data1['Age']**2


#X = 2*data.OPS  + 2*data.TOI_avg + (1-data.Draft_round) + data.Age + data.CFQoC + data.TOIQoT 
r2=[]
rmse=[]
coeffs=[]
f, ax = plt.subplots(figsize=(16, 10))
for i in range(0,1):
    X = data1[['OPS2','TOI_avg2','Age2','Age','CFQoC','TOIQoT','Draft_year','GWY','BLK','HIT','Rel CF%','OZS']]

    y = data1['Salary_norm']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)


    # Initialise the linear regression
    model = LinearRegression()
    # fit our model to the data
    model.fit(X_train, y_train)

    # and let's plot what this relationship looks like 
    predictions = model.predict(X_test)
    coeffs.append(model.coef_)


    
    plt.xlabel('Test [Normalized Salary USD]',size=20)
    plt.ylabel('Predicted [Normalized Salary USD]', size=20)
    r2.append(metrics.r2_score(y_test, predictions))
    rmse.append(np.sqrt(metrics.mean_squared_error(y_test, predictions)))
    
    plt.plot(y_test,predictions,'bo',[0,1],[0,1])
   

print((np.sum(rmse))/1000)
print((np.sum(r2))/1000)
print(np.sum(coeffs,0)/1000)


# In[18]:




plt.hist(y_test - predictions, bins=20)


# In[41]:


np.sum(coeffs,0)/2000


# In[20]:


model.intercept_


# ## Offense

# In[72]:




from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import r2_score
import statsmodels.formula.api as sm
import statsmodels.api as smi

data1=data.copy()
data1['OPS2'] = 2* data1['OPS']
data1['TOI_avg2'] = data1['TOI_avg']**2
data1['Age2'] = data1['Age']**2
data1['RelCF'] = data1['Rel CF%']
pves=[]
r2=[]
for i in range(0,1000):

    X = data1[['OPS2','OPS','Points','TOI_avg','TOI_avg2','Age','Age2','CFQoC','TOIQoT','Draft_round','GWY','BLK','HIT','TKY','RelCF','OZS']]
    y = data1['Salary_norm' ]
    
    X = smi.add_constant(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    
    

    y_df = pd.DataFrame(data=y_train, columns=['Salary_norm'])
    dummyset = pd.concat([y_df,X_train],axis=1)

    md = sm.ols("Salary_norm ~ Points + TOI_avg2 + Age + Age2 + TOIQoT + Draft_round + BLK + OZS", dummyset)

    mdf = md.fit()
    
    pves.append(mdf.pvalues)
    r2.append(mdf.rsquared)

print(mdf.summary())


# In[73]:


print(np.mean(pves,0))
print(np.mean(r2,0))


# ## Defence
# 

# In[68]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import r2_score
import statsmodels.formula.api as sm

data1=data.copy()
data1['OPS2'] = 2* data1['OPS']
data1['TOI_avg2'] = data1['TOI_avg']**2
data1['Age2'] = data1['Age']**2
data1['RelCF'] = data1['Rel CF%']
pves=[]
r2=[]
for i in range(0,1000):

    X = data1[['OPS2','OPS','Points','TOI_avg','TOI_avg2','Age','Age2','CFQoC','TOIQoT','Draft_round','GWY','BLK','HIT','TKY','RelCF','OZS']]
    y = data1['Salary_norm' ]

    X = smi.add_constant(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    y_df = pd.DataFrame(data=y_train, columns=['Salary_norm'])
    dummyset = pd.concat([y_df,X_train],axis=1)

    md = sm.ols("Salary_norm ~ Points + TOI_avg2 + Age + Age2 + Draft_round + BLK", dummyset)

    mdf = md.fit()
    
    pves.append(mdf.pvalues)
    r2.append(mdf.rsquared)

print(mdf.summary())


# In[69]:


print(np.mean(pves,0))
print(np.mean(r2,0))


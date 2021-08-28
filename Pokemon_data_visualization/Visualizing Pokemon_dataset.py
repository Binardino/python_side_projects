#!/usr/bin/env python
# coding: utf-8

# **Goals of the Notebook**

# This Notebook aims at craeting cool
# Following previous [Ironhack challenges focused on the Pokemon dataset](https://github.com/Binardino/IronHack-Data-Analysis-Module-1-Python/blob/master/Pandas%20-%20df_calculation_%26_transformation%20Sales%20%26%20Pokemon%20-%203%20challenges/your-code/challenge-2-Pokemon_Types%26Correlation.ipynb), I am using that dataset anew in order to produce various types of data visualizations.
# The idea is to mix various data visualzations libraries : Seaborn, Plotly & classical Matplotlib
# 
# **Key question to answer**
# - which are the strongest & weakest pokemons ? 
# - which types - and which type combinations - have the strongest ones ?
# - are the different characteristics correlated ?

# **Importing libraries**

# In[2]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import re
import random
import os

# **Setting sns style**

# In[3]:


# sns.set_style(style='GnBu_d')
sns.set(style = 'darkgrid', palette='deep', rc = {'figure.figsize':(20,10)}) 
#figsize is not a param for sns.set BUT using rc & a dict, possible to add new params


# **Importing dataset**

# In[84]:

curdir = os.getcwd()

#os.walk()

#os.chdir('/data')
df_pokemon = pd.read_csv('D:/python_side_projects_GIT_transfer/Pokemon_data_visualization/data/Pokemon.csv')
#df_pokemon = pd.read_csv(r'pokemon.csv')

os.getcwd()

# In[85]:


df_pokemon.head(20)


# **Data Wrangling**

# In[86]:


# cleaning row with junk names where Mega pokemons have name doubled
# e.g "VenusaurMega Venusaur" should be "Mega Venusaur; "CharizardMega Charizard X" = "Mega Charizard X".
# same issue with doubling name "Hoopa" - e.g. cf. line 797 & 798

df_pokemon['Name'] = df_pokemon['Name'].apply(lambda row: re.sub(r'\w+Mega', 'Mega', row))

df_pokemon['Name'] = df_pokemon['Name'].apply(lambda row: re.sub(r'(HoopaHoopa)(.+)', 'Hoopa'+r'\2', row))


df_pokemon.tail(10)


# In[87]:


# #dropping the '#' column : useless for the following dataviz work
# df_pokemon.drop(columns='#', inplace=True)


# # Part I - Basic Descriptive Statistics

# **Analyzing main features**
# - classical .describe()
# - finding out strongest & weakest ones

# In[88]:


df_pokemon.describe().astype(float).round(decimals=2)


# In[89]:


df_pokemon.isnull().sum()


# In[90]:


#counting amount of Pokemon per Generation
df_pokemon['Generation'].value_counts()


# In[91]:


#Many Pokemon have only One Type but no Type 2
# filling Type 2 = NaN with None

df_pokemon['Type 2'].fillna(value='', inplace=True)


# In[92]:


# function to create new 'Combo Type' column, mixing up two existing Types
def combo_type_creator(row):
    if row['Type 2'] =='':
        return row['Type 1']
    else:
        return row['Type 1'] + '-' + row['Type 2']


# In[93]:


df_pokemon['Combo_Type'] = df_pokemon.apply(lambda row: combo_type_creator(row), axis=1)


# In[94]:


df2 = pd.Series(df_pokemon['Combo_Type'].str.split(pat='-').sum()).value_counts()

df2


# The idea of this exercise is to find strongest regular pokemons
# 
# Legendary pokemons are, by definition, the strongest pokemons, and are not naturally catchable (in each games, there is only One Legendary pokemon to catch in particular circumstances), therefore let's create a sub df with only regular non-legendary pokemons, in order to have less noisy data

# In[95]:


df_regular_pokemon = df_pokemon[df_pokemon['Legendary'] != True].copy()

df_regular_pokemon.drop(columns='Legendary', inplace=True)


# spliting datasets into two subdatasets : 
# - df_pokedex = all categorical values i.e. ID, name, Generation, Legendary, Type1 & Type2
# - df_pokestats = all stats : Type1 & Type2, Total, HP, Attack , Defense, Sp. Atk, Sp. Def, Speed
# 
# I want to know which Types are the strongest so I'm keeping both Type variables in both df in order to measure their impact on overall stats

# In[96]:


df_pokedex = df_regular_pokemon[['#', 'Name', 'Type 1', 'Type 2', 'Generation']]

df_pokestats = df_regular_pokemon[['#', 'Type 1', 'Type 2','Total', 'HP', 'Attack' , 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]


# **Which are the Strongest Pokemons ?**
# 
# Before doing any particular data processing, let's dive right in : which are the strongest ones ?

# In[97]:


df_regular_pokemon.nlargest(n=10, columns='Total').drop_duplicates(subset='#') 
#dropping duplicates # to avoid having duplicates Pokemons with same # (due to evoluion or X/Y Types)


# **Which are the Weakest Pokemons ?**
# 
# On the contrary, let's find out which are the weakest ones

# In[98]:


df_regular_pokemon.sort_values(by='Total').drop_duplicates(subset='#').head(10)
#dropping duplicates # to avoid having duplicates Pokemons with same # (due to evoluion or X/Y Types)


# We can already have an idea of which Types have the strongest & weakest ones through those operations

# # Part II - Data Visualization

# ## 1 - Plotting basic distributions

# One of the original assumption was that Legnedary Pokemons are way stronger than regular ones and are skewing the data - which is why we took them away from the regular dataframe.
# Just to be sure, let's check it by comparing the 'Total' feature of Legendary VS. Regular ones with a Boxplot

# In[109]:


sns.boxplot(x='Legendary', y='Total', data=df_pokemon)


# Indeed Legendary ones have in average a much higher 'Total'.
# 
# Now let's plot all 6 features to measure their distribution.

# In[105]:


#creating subplot with only 6 features top plot - i.e. dropping Total (sum of 6 features), Generation & Legendary
df_pokemon_features = df_pokemon.drop(columns=['#','Total', 'Generation', 'Legendary'])


# In[106]:


sns.boxplot(data=df_pokemon_features)


# In[112]:


#classical boxplot to visualize distribution of Total feature
sns.boxplot(data=df_pokemon['Total'])#C


# In[31]:


#distplot to visualize distribution of Total feature
sns.displot(data=df_pokemon['Total'])
#distplot deprecated - changed to displot

# In[114]:


#same distplot with Pyplot to make it interactive through hovering
ff.create_distplot([df_pokemon.Total], ['Total'], bin_size=20)


# In[115]:


# combined distplot with Pyplot of both Defense & Attack measure their distribution
ff.create_distplot([df_pokemon.Attack, df_pokemon.Defense], ['Attack', 'Defense'], bin_size=5)


# In[34]:


fig = px.histogram(df_pokemon, x="Total", 
                   hover_data=df_pokemon.columns)
fig.show()


# In[119]:


from plotly.offline import init_notebook_mode, iplot


# In[120]:


hp_distplot = ff.create_distplot([df_pokemon.HP], ['HP'], bin_size=5)
iplot(hp_distplot, filename='HP Distplot')

attack_defense_distplot = ff.create_distplot([df_pokemon.Attack, df_pokemon.Defense], ['Attack', 'Defense'], bin_size=5)
iplot(attack_defense_distplot, filename='Attack/Defense Distplot')


# In thoery each Generation are balanced with comparable stats, but is there a Generation which outperforms others ?

# In[38]:


sns.boxenplot(x='Generation', y='Total', data=df_pokemon)


# ## 2 - Comparing Types

# In[39]:


sns.boxenplot(x='Type 1', y='Total', data=df_pokemon)


# In[40]:


sns.boxenplot(x='Type 2', y='Total', data=df_pokemon)


# **Plotting Type distribution**

# In[22]:


sns.countplot(x='Type 1',
             data=df_pokemon,
             order=df_pokemon['Type 1'].value_counts().index)


# In[100]:


sns.countplot(x='Type 2',
             data=df_pokemon,
             order=df_pokemon['Type 2'].value_counts().index)


# In[24]:


# df_pokemon['Combo_Type'].str.split(pat='-').sum().value_counts()


# In[25]:


dfcombotype = pd.DataFrame(pd.Series(df_pokemon['Combo_Type'].str.split(pat='-').sum()).value_counts())

#dfcombotype.drop('None', inplace=True)

dfcombotype.reset_index(inplace=True)

dfcombotype.columns = ['type', 'count']


# In[26]:


dfcombotype


# In[27]:


fig_type = px.treemap(dfcombotype,
                     path   = ['type'],
                     values = 'count')
fig_type.show()


# **Some conclusions**
# - Most Pokemon only have 1 Type
# - Flying type is underrepresented in Type 1, but is the #1 2nd Type (i.e. many Pokemon have Flying as a complementary Type)
# - I would have assumed Normal Type was the most common Type, but in fact Water is the most common one 

# In[28]:


dual_pokemon = df_pokedex[df_pokedex['Type 2'] != 'None']


# In[29]:


sns.heatmap(dual_pokemon.groupby(['Type 1', 'Type 2']).size().unstack(),
            linecolor='white',
            annot=True)


# **Mapping Strongest & Weakest Pokemon types**

# In[45]:


# creating sub df with crossed table of two Types to measure which Type combinations have the strongest & weakest combinations
# measuring over Median of "Total" feature
type_stacked = df_pokestats.groupby(['Type 1', 'Type 2']).agg({'Total':'median'})

sns.heatmap(
            type_stacked.unstack(),
            linewidths=1,
            cmap='coolwarm')


# In[46]:


type_stacked.reset_index().sort_values('Total', ascending=False).head(10)


# **Mapping Types VS. Features**
# 
# Are there importance infuence between Types & features ? i.e. are there certain Types which outperform with particular features ?

# In[47]:


# creating new sub df focusing over Type 1 VS. 6 Features
# grouping by only Type 1 over Median for all 6 features - from .loc() HP to Speed  
# (adding 2nd type to the group by would generate a too hard to read heatmap with too many variables)

feature_stacked = df_regular_pokemon.groupby(['Type 1']).median().loc[:,'HP':'Speed']


# In[48]:


sns.heatmap(feature_stacked,
            linewidths=1,
            cmap='coolwarm'
            )


# ## 3 - Comparing 6 Features

# Let's create a Correlation matrix of all 6 features
# - The "Total" feature being the sum of all 6 features, it will be by definition strongly correlated to other features
# - it might be nonetheless to measure which feature influences the most the "Total" one

# In[42]:


df_corr = df_regular_pokemon[['Total','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']].corr()


# In[43]:


df_corr


# In[44]:


sns.heatmap(df_corr, annot=True)


# **Plotting potential correlation between 6 features**

# In[52]:


# fig, axs = plt.subplots(3,3, figsize=(20,10)) #3 by 3 subplots

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(nrows=3, ncols=3, figsize=(25,15))


sns.regplot(x='HP', y='Attack', 
              data=df_pokemon, ax=ax1)
ax1.set_title("Plot1: HP VS. Attack", fontsize =18)

sns.regplot(x='HP', y='Defense', 
              data=df_pokemon, ax=ax2,  color = 'orange')
ax2.set_title("Plot2: HP VS Defense", fontsize =18)

sns.regplot(x='HP', y='Speed', 
              data=df_pokemon, ax=ax3,  color = 'c')
ax3.set_title("Plot3: HP VS Speed", fontsize =18)

sns.regplot(x='Speed', y='Attack', 
              data=df_pokemon, ax=ax4,  color = 'green')
ax4.set_title("Plot4: Speed VS. Attack", fontsize =18)

sns.regplot(x='Speed', y='Defense', 
              data=df_pokemon, ax=ax5, color = '.255')
ax5.set_title("Plot5: Speed VS. Defense", fontsize =18)

sns.regplot(x='Speed', y='Sp. Def', 
              data=df_pokemon, ax=ax6, color = 'b')
ax6.set_title("Plot5: Speed VS. Sp. Defense", fontsize =18)

sns.regplot(x='Speed', y='Sp. Atk', 
              data=df_pokemon, ax=ax7, color = 'darkgreen')
ax7.set_title("Plot6: Speed VS. Sp. Attack", fontsize =18)

sns.regplot(x='Defense', y='Sp. Def', 
              data=df_pokemon, ax=ax8, n_boot=50, x_bins = 250, marker='^', color = 'purple')
ax8.set_title("Plot7: Defense VS. Sp. Defense", fontsize =18)

sns.regplot(x='Attack', y='Sp. Atk', 
              data=df_pokemon, ax=ax9, x_bins = 250, color = 'r')
ax9.set_title("Plot8: Attack VS. Sp. Attack", fontsize =18)

fig.tight_layout() # To understand how this works see point and link 3


# In[ ]:





# In[36]:


plt.figure(figsize=(20,10))
sns.lmplot(x='Attack', y='Defense', data=df_pokemon,
          hue='Generation',
          height=10, aspect=1)


# To finish out, le's scatter all pokemons at once with a PyPlot scatterplot, to map which are the strongests overall pokemons, in terms of Attack & Defense - with a Generation hue.
# 
# Truth be told, it is a messy plot which does not tell much - but it is a fun one - and one may hover to find out the name of each plot

# In[124]:


px.scatter(df_pokemon, x='Attack', y='Defense', size='Total', 
           width=800, height=600,
           color='Generation', hover_name='Name')


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# Guiding questions: 
# At what companies do developers get paid the most?
# How much does remote working matter to employees?
# How does coding experience affect the level of pay?
# What's the most popular method of learning to code?
# Are you more likely to get a job as a developer if you have a master's degree?

# First we install all the libraries we will be needing in this project. 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


df=pd.read_csv("survey_results_public.csv")


# In[5]:


print(df.head(100))


# In[6]:


print(df.info())


# In[7]:


#to see what our missing values are!
missing_values= df.isnull().sum()
data_types=df.dtypes


# In[8]:


missing_values


# 

# 1-At what companies do developers get paid the most?
# for this we need to clean the industry column and remove all the rows where information is missing.

# In[12]:


# Remove rows with missing 'ConvertedCompYearly' or 'Industry' data 
df_cleaned = df.dropna(subset=['ConvertedCompYearly', 'Industry'])

# Clean the 'Industry' column for consistency removing the spaces at the beginning and end basically 
df_cleaned['Industry'] = df_cleaned['Industry'].str.strip()

#calculating the avg compensation by industry we want it grouped by the industry but the avg of ConvertedCompYearly 
average_comp_by_industry_cleaned = df_cleaned.groupby('Industry')['ConvertedCompYearly'].mean().sort_values(ascending=False)

top_10_industries_cleaned = average_comp_by_industry_cleaned.head(10)

top_10_industries_cleaned


# How much does remote working matter to employees?
# 

# In[13]:


df_cleaned = df.dropna(subset=['ConvertedCompYearly','RemoteWork'])

df_cleaned['RemoteWork'] = df_cleaned['RemoteWork'].str.strip()

#Return a Series containing counts of unique values. and if normalize=True If True then the object returned will contain the relative frequencies of the unique values
remote_work_distribution = df_cleaned['RemoteWork'].value_counts(normalize=True) * 100

average_comp_by_remote_work= df_cleaned.groupby('RemoteWork')['ConvertedCompYearly'].mean().sort_values(ascending=False)

remote_work_distribution,average_comp_by_remote_work


# What's the most popular method of learning to code?

# In[17]:


learning_methods_column="LearnCode"

if learning_methods_column in df.columns:
    #seperate the multiple learning methods by semicolons and creates a list of methods for each respondent 
    all_methods= df[learning_methods_column].dropna().str.split(';')
    #all methods is a list of lists basically and we use strip() ti remove any leading or trailing spaces from each method
    flat_list= [item.strip() for sublist in all_methods for item in sublist]
    
    #counting each method frequency counter class is used to count the frequency 
    from collections import Counter
    method_counts= Counter(flat_list)
    
    #convert to a dataframe and sort it 
    method_counts_df = pd.DataFrame(method_counts.items(), columns=['Method', 'Count']).sort_values(by='Count', ascending=False)
    
    # Visualization of the top methods
    top_methods = method_counts_df.head(10)
else:
    top_methods = "Learning methods column does not exist in the dataset."

top_methods


# How does coding experience affect the level of pay?

# In[18]:


#checking if we have the columns in our dataframe that we need
experience_columns = [col for col in df.columns if 'year' in col.lower() or 'experience' in col.lower()]

#we want to directly use YearsCoding if it exists if not we will go back to our first step 
experience_column_name = 'YearsCoding' if 'YearsCoding' in experience_columns else experience_columns[0] if experience_columns else None

#This line is a general approach to cleaning the experience data. It attempts to extract numerical values from the experience column, converting it to float for numerical analysis. 
df_cleaned[experience_column_name] = df_cleaned[experience_column_name].astype(str).str.extract('(\d+)').astype(float)

#dropping missing values 
df_experience_cleaned = df_cleaned.dropna(subset=[experience_column_name, 'ConvertedCompYearly'])

#getting the avg and sorting the value 
average_comp_by_experience = df_experience_cleaned.groupby(experience_column_name)['ConvertedCompYearly'].mean().sort_values()


# In[21]:


average_comp_by_experience.plot(kind='bar', figsize=(10, 6), title="Average Compensation by Coding Experience")


# Are you more likely to get a job as a developer if you have a master's degree?

# In[27]:


education_column = 'EdLevel'
employment_column = 'Employment'

# Clean and standardize the education level data
df[education_column] = df[education_column].str.strip().str.lower()

#rows with masters degree
masters_degree = df[df[education_column].str.contains("master's", na=False)]

no_masters_degree = df[~df[education_column].str.contains("master's|doctorate", na=False)]


#avg of employment with and without a masters degree
employed_masters= masters_degree[employment_column].str.contains('Employed', na=False).mean()
employed_no_masters = no_masters_degree[employment_column].str.contains('Employed', na=False).mean()

results = {
    "With Master's Degree": employed_masters,
    "Without Master's Degree": employed_no_masters
}

results


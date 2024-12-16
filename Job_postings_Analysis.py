#!/usr/bin/env python
# coding: utf-8

# # Naukri.com Job Posting Analysis

# ## **Introduction**

# ### The aim of this project is to analyze job postings data to uncover key hiring trends in the job market. This includes analyzing:
# ### 1. **Top hiring companies** across various roles.
# ### 2.  **Geographic locations** with the highest job opportunities.
# ### 3. **Experience and salary** trends for different roles.
# ### 4. **Common responsibilities** and skills required for popular roles.
# 
# ### The analysis is helpful for job seekers and industry analysts to understand current trends, optimize job searches, and identify roles in demand.
# 

# ### Importing Necessary Libraries

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ### Loading the data

# In[2]:


df = pd.read_csv("jobs.csv")


# In[3]:


df


# ### Exploring the Data and Cleaning

# In[4]:


df.describe()


# In[5]:


df.info()


# In[6]:


df.isnull().sum()


# In[7]:


df['job_id'].drop_duplicates()


# In[8]:


df.drop_duplicates(subset='job_id', inplace=True)


# In[9]:


df


# In[10]:


df['company']


# In[11]:


df = df.dropna()


# In[52]:


df


# ### Preparing data for analysis 

# In[14]:


df['reviews'] = df['reviews'].str.extract('(\d+)').astype('int')


# In[15]:


df


# In[16]:


all_resposibilities = df['resposibilities'].str.lower().str.split(",").explode()


# In[17]:


all_resposibilities.value_counts().sort_values(ascending = False)


# In[18]:


df['resposibilities'] = df['resposibilities'].str.lower().str.split(",")
df = df.explode('resposibilities').reset_index(drop=True)


# In[19]:


df


# In[20]:


df['location'] = df['location'].str.lower().str.split(",")
df = df.explode('location').reset_index(drop=True)


# In[21]:


df


# In[22]:


df = df.drop(columns = ["job_link","company_link"])


# In[23]:


df


# In[24]:


df[['min_exp', 'max_exp']] = df['experience'].str.split('-', expand=True)
df['min_exp'] = df['min_exp'].astype(int)  # Convert to integer
df['max_exp'] = df['max_exp'].str.extract('(\d+)').astype(int)


# In[25]:


df


# ### Writing Functions so that user is able to find jobs according to his prefrences

# ### These will help the job seeker to filter out jobs based on **job role**, **location** and **experience** making it easy for them to find their ideal Job

# In[26]:


def filtered_jobs_posts(candidate_exp,df):
    filtered_jobs = df[
        (df['min_exp'] <= candidate_exp) & (df['max_exp'] >= candidate_exp)
    ]
    return filtered_jobs

candidate_exp = int(input("Your Experience ="))
matching_jobs = filtered_jobs_posts(candidate_exp, df)

# Display matching jobs
print(matching_jobs)


# In[64]:


matching_jobs


# In[27]:


def filtered_posts(candidate_skills,df):
    filtered_jobss = df[
        (df['resposibilities'].str.lower() == candidate_skills)
    ]
    return filtered_jobss

candidate_skills = str(input("input skill ="))
matched_jobs = filtered_posts(candidate_skills, df)

# Display matching jobs
print(matched_jobs)


# In[62]:


matched_jobs


# In[29]:


def filtered_jobs(role,df):
    filtered_jobs_ = df[
        (df['job_role'].str.lower() == role )
    ]
    return filtered_jobs_

role = str(input("Role You are Seeking ="))
matches = filtered_jobs(role, df)

# Display matching jobs
print(matches)


# In[63]:


matches


# In[ ]:





# ### Visualisations

# In[30]:


df['job_role'].value_counts().head(10).plot(kind = 'bar')


# ## Top Job Roles demanded in the market
# ### Most number of Companies are looking to hire Java Developers followed by Business development executive and manager

# In[31]:


top_companies = df['company'].value_counts().head(10)


# In[32]:


top_companies = top_companies.reset_index()
top_companies.columns = ['company', 'count']  # Rename columns for clarity

# Plot using seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='count', y='company', data=top_companies, palette='viridis')
plt.title('Top 10 Companies by Job Postings')
plt.xlabel('Number of Job Postings')
plt.ylabel('Company')
plt.show()


# ### **Top 10 Companies Hiring**
# ### Here, I identify the top 10 companies based on the number of job postings. This helps job seekers focus on organizations actively hiring.
# 
# ### The bar chart shows the companies with the most postings.
# 
# #### **Insights:**
# ### - **Accenture** has the highest number of job postings followed by ** Wintax Solutions** and **IBM**.
# ### - The majority of job postings are concentrated among a few companies.
# 

# In[33]:


top_locations = df['location'].value_counts().head(10)


# In[34]:


top_locations


# In[35]:


top_locations = top_locations.reset_index()
top_locations.columns = ['location', 'count']

# Strip leading and trailing spaces from the location column
top_locations['location'] = top_locations['location'].str.strip()

# Now rename the columns correctly
top_locations.columns = ['location', 'count']

# Drop the extra index column if it exists
top_locations = top_locations.drop(columns=['index'], errors='ignore')

# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(x='location', y='count', data=top_locations)
plt.title("Highest Number of Postings Based on Location")
plt.xlabel("Location")
plt.ylabel("Posting Count")
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.show()


# ## **Top Locations for Job Postings**
# ### In this section, I analyze the locations with the most job opportunities.
# 
# ### The bar chart highlights cities where job postings are concentrated, helping job seekers identify geographic job hubs.
# 

# ## **Insights:**
# ### - **Bangalore**  is the top city with the highest job postings.
# ### - These top 10 cities act as major job markets, particularly for roles in technology and business sectors.
# 

# In[49]:


top_review = df.groupby('company')['reviews'].count().sort_values(ascending = False).head(10)


# In[50]:


top_review


# In[51]:


plt.figure(figsize=(12, 6))
sns.barplot(x=top_review.index, y=top_review.values, palette='viridis')
plt.title('Top 10 Companies Based on Reviews')
plt.xlabel('Company')
plt.ylabel('Review Count')
plt.xticks(rotation=45)
plt.show()


# ## **Top Locations for Job Postings**
# ### In this section, I analyze the companies with the most reviews.
# 
# ### The bar chart highlights companies with most number reviews, helping job seekers identify positives and negatives of the company they want to join.
# 

# ## **Insights:**
# ### - **Accenture**, **Wintax Solutions** and **IBM**  hold the top 3 Based on Reviews
# ### - These reviews showcases these companies have huge employee counts compared to others
# 

# In[52]:


top_companies_df = df[df['company'].isin(top_review.index)]

# Step 3: Calculate average rating for each of the top 10 companies
top_companies_ratings = (
    top_companies_df.groupby('company')['rating']
    .mean()
    .reindex(top_review.index)  # Ensure the order matches top 10 companies
)

# Step 4: Plot the ratings
plt.figure(figsize=(12, 6))
sns.barplot(x=top_companies_ratings.index, y=top_companies_ratings.values, palette='viridis')
plt.title("Average Ratings of Top 10 Companies Based on Reviews")
plt.xlabel("Company")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()


# ## **Average Rating ** 

# In[ ]:





# # **Conclusion**
# ## This analysis of job postings highlights key trends in the job market:
# ### 1. **Top Companies**: The majority of postings are from a few organizations.
# ### 2. **Top Locations**: Bangalore and Hyderabad dominate the job market.
# ### 3. **Experience Trends**: Most roles require 2-5 years of experience.
# ### 4. **Responsibilities**: Understanding common tasks helps candidates prepare better for applications.
# 
# 
# ### This project provides actionable insights for job seekers and industry analysts looking to understand job market trends.
# 
# 

# In[ ]:





# In[ ]:





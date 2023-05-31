import pandas as pd 
import streamlit

def jobcat_level(df):
    
    job_cat=df['job_category'].unique().tolist()
    job_cat.sort()
    job_cat.insert(0,'Overall')
    career_level=df['career_level'].unique().tolist()
    career_level.sort()
    career_level.insert(0,'Overall')
   

    return job_cat,career_level
   

def filter_jobs(job_cat, career, keyword, df):
    if job_cat == 'Overall' and career == 'Overall':
        temp_df = df.copy()
    elif job_cat == 'Overall' and df.career_level.isin(career).any():
        temp_df = df[df.career_level.isin(career)]
    elif df.job_category.isin(job_cat).any() and career == 'Overall':
        temp_df = df[df.job_category.isin(job_cat)]
    elif df.job_category.isin(job_cat).any() and df.career_level.isin(career).any():
        temp_df = df[df.job_category.isin(job_cat) & df.career_level.isin(career)]
    else:
        temp_df = df.copy()

    filtered = temp_df.loc[temp_df['Title'].str.contains(keyword, case=False, regex=True),
                           ['Job ID', 'Title', 'agency', 'Salary', 'Post Until', 'job_category', 'career_level']]

    return filtered





    # if job_cat=='Overall' and career_level=='Overall':
    #     temp_df=df

    # if job_cat=='Overall' and career_level!='Overall':
    #     temp_df=df[(df.career_level.isin(career_level))]


    # if job_cat!='Overall' and career_level=='Overall':
    #     temp_df=df[df['job_category'].isin(job_cat)]

    # if job_cat!='Overall' and career_level!='Overall':
    #     temp_df = df[(df['job_category'].isin(job_cat)) & (df.career_level.isin(career_level))]

   

import pandas as pd 
import streamlit



#will help to print when keyword 
#df.loc[df['shield'] > 6, ['max_speed']]

#trying to merge the function into the filter function 
# def kewyord_process(keyword,df):
#     #df=jobs.preprocess()
#     df=df.loc[df['Title'].str.contains(keyword, case=False, regex=True), ['Job ID','Title','Salary','Post Until']]
#     return df


def jobcat_level(df):
    #df=jobs.preprocess()
    job_cat=df['job_category'].unique().tolist()
    job_cat.sort()
    job_cat.insert(0,'Overall')
    career_level=df['career_level'].unique().tolist()
    career_level.sort()
    career_level.insert(0,'Overall')
    return job_cat,career_level


# function for results of filtering job search 

def filter_jobs(job_cat, career_level,keyword,df):

    if job_cat=='Overall' and career_level=='Overall':
        temp_df=df
    if job_cat=='Overall' and career_level!='Overall':
        temp_df=df[(df['career_level']==career_level)]
    
    if job_cat!='Overall' and career_level=='Overall':
        temp_df=df[df['job_category']==job_cat]
            
    if job_cat!='Overall' and career_level!='Overall':
        temp_df=df[(df['job_category']==job_cat) & (df['career_level']==career_level)] 


    filtered_jobs=temp_df.loc[df['Title'].str.contains(keyword, case=False, regex=True), ['Job ID','Title','Salary','Post Until','job_category','career_level']]

    return filtered_jobs


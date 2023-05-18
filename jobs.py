import pandas as pd 


#data cleaning and checking for nulls to handle later 
def preprocess(df):

    df['minimum_qual_requirements']=df['minimum_qual_requirements'].fillna(' ')
    df['work_location_1']=df['work_location_1'].fillna(' ')
    df['salary']='$'+df['salary_range_from']+'-$'+df['salary_range_to']+'/'+df['salary_frequency']
    df=df.rename({'job_id':'Job ID','business_title':'Title','salary':'Salary','post_until':'Post Until'}, axis=1)
    df['Post Until']=df['Post Until'].fillna('Not Provided')
    df= df.drop_duplicates(subset='Job ID',keep='first')

    return df 



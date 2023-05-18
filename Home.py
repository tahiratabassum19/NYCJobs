import streamlit as st
import pandas as pd
import helper
import jobs
import requests
import time

#import numpy as np

# api token find out then 
API_KEY ='76ee7p4cmyfe0bd14jv02m310'
#build the url with endpoint+apptoken+filter
#API documentation will help here and doc has the link of instruction page
#headers= #could build the app token this way too.
#i might need to use api token as api key not working bookmarked article 
# endpoint='https://data.cityofnewyork.us/resource/kpav-sd4t.json'
# url= f"{endpoint}?$$app_token={API_KEY}"

#$select=job_id, agency, number_of_positions,business_title,civil_service_title,job_category,career_level, salary_range_from , salary_range_to ,salary_frequency, work_location, job_description, minimum_qual_requirements, preferred_skills, posting_date,  posting_updated, work_location,  post_until
#url="https://data.cityofnewyork.us/resource/kpav-sd4t.json?$$app_token=VqqaMeCXwluae4iAUkvGyheal&$limit=50000"
url = "https://data.cityofnewyork.us/resource/kpav-sd4t.json?$$app_token=VqqaMeCXwluae4iAUkvGyheal&$select=job_id,agency,number_of_positions,business_title,civil_service_title,job_category,career_level,salary_range_from,salary_range_to,salary_frequency,work_location,job_description,minimum_qual_requirements,work_location_1,posting_date,post_until&$limit=50000"

response=requests.get(url).json()
#print(response[0])
# date coming as datetime must fix it
df = pd.DataFrame(response)
cleaned_df=jobs.preprocess(df)


st.set_page_config(page_title="Job Search",page_icon='🔎', layout="wide")
def add_bg_from_url():

    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url("https://i.pinimg.com/736x/6e/32/87/6e32878542a4a6b86e640204d951fbff--blue-wallpapers-blue-backgrounds.jpg");
        background-attachment: fixed;
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
   
    )
add_bg_from_url() 





# hide_st_style= """
#     <style>
#     header {visibility: hidden;}
#     footer {visibility:hidden;}
#     </>style
# """
#st.markdown(hide_st_style, unsafe_allow_html=True)
st.title("NYC Job Search")

job_cat,career_level=helper.jobcat_level(cleaned_df)

st.sidebar.header("Filter Search")
selected_jobcat=st.sidebar.selectbox("Select Job Category",job_cat)

selected_career_level=st.sidebar.selectbox("Select Career Level",career_level)

st.sidebar.title("About")
st.sidebar.info(
    """
    This app is maintained by Tahira Tabassum :female-technologist: . You can follow me on 
        [LinkedIn](https://www.linkedin.com/in/tahira-tabassum/) |[GitHub](https://github.com/tahiratabassum19)


    Source Code: <https://github.com/tahiratabassum19/NYCJobs.git>


    Dataset Used: [NYC Jobs](https://data.cityofnewyork.us/City-Government/NYC-Jobs/kpav-sd4t)



""")


col1,col2=st.columns([3,1])
with col1:
    #can give diff font n all here
    #st.markdown('<p>Keyword/Job Title </p>,unsafe_allow_html=True')
    keyword_input=st.text_input("Keyword/Job Title", key="Keyword")



with col2:
    st.write("Click")
    search_button=st.button("search")
if search_button:
    #st.write("You entered"+keyword_input)
    st.header("Job Results")
    #st.table(helper.kewyord_process(keyword_input,df))
    st.table(helper.filter_jobs(selected_jobcat,selected_career_level,keyword_input,cleaned_df))




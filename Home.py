import streamlit as st
import pandas as pd
import helper
import jobs
import requests
from PIL import Image
import time


API_TOKEN=st.secrets["auth_token"]

# API Calling 
url = f"https://data.cityofnewyork.us/resource/kpav-sd4t.json?$$app_token={API_TOKEN}&$select=job_id,agency,number_of_positions,business_title,civil_service_title,job_category,career_level,salary_range_from,salary_range_to,salary_frequency,work_location,job_description,minimum_qual_requirements,work_location_1,posting_date,post_until&$limit=50000"

response=requests.get(url).json()
df = pd.DataFrame(response)
cleaned_df=jobs.preprocess(df)


st.set_page_config(page_title="Job Search",page_icon='🔎',layout="wide")


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


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pangolin&display=swap');
    .nyc {
    font-family: 'Pangolin', sans-serif;
     
    font-size:60px !important;
    color: #0B2FA0;
    font-weight: bold;

        }
    </style>
    """, unsafe_allow_html=True)
st.markdown(f'<p class="nyc">NYC Jobs and Career Opportunities</p>', unsafe_allow_html=True)
#st.markdown("----")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Ubuntu&display=swap');
    .ny {
    font-family: 'Ubuntu', sans-serif;
     
    font-size:25px !important;
    color: #5676DA;
    font-weight: bold;

        }
    </style>
    """, unsafe_allow_html=True)
st.markdown(f'<p class="ny">Please Click The Search Button To See The Results. To Apply For Any Position-Please Visit NYC Jobs Original <a href="https://www.nyc.gov/jobs/index.page">Career Page</a> and Search By Job ID. </p>', unsafe_allow_html=True)


st.title("Search Jobs")

job_cat,career_level=helper.jobcat_level(cleaned_df)

st.sidebar.header("Filter Search")

selected_jobcat=st.sidebar.multiselect("Select Job Category",job_cat)

selected_career_level=st.sidebar.multiselect("Select Career Level",career_level)


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
    #st.markdown('<p>Keyword/Job Title </p>,unsafe_allow_html=True')
    keyword_input=st.text_input("**Keyword/Job Title**", key="Keyword")



with col2:
    st.write("Click")
    search_button=st.button("Search")
if search_button:
    st.header("Job Results")
    filtered_result=helper.filter_jobs(selected_jobcat,selected_career_level,keyword_input,cleaned_df)
    st.dataframe(filtered_result)




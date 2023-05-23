import streamlit as st
import pandas as pd 
import numpy as np 
import seaborn as sns
import plotly.express as px
import plotly as plt
import plotly.graph_objects as go
import Home
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import PyPDF2
import re

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


selection=st.sidebar.radio("Select an Option",("Job Dashboard","Resume WordCloud"))

if selection=="Job Dashboard":

    df=Home.cleaned_df
    st.title(":bar_chart: Job Dashboard")
    st.markdown('##')
    container=st.container()
    col1, col2=container.columns(2)

    with col1:
        df['number_of_positions'] = df['number_of_positions'].astype(float)

        career = df.groupby('career_level')['number_of_positions'].sum().reset_index()

        car = career.rename(columns={'career_level': 'Level', 'number_of_positions': 'Count'})
        fig = px.pie(car, values='Count',names='Level',hover_name='Count', color_discrete_sequence=["#3372CD","#BB0A04","#9884E9"])

        fig.update_layout(
        showlegend=True,
        width=500,    
        height=300,   
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=30, b=20, t=20),  
        font=dict(color='black', size=15)
        )
        st.markdown("""
        <style>
        .e {
            font-size:20px !important;
            font-family:Sans-serif;
            font-weight: bold;
            color: black
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<p class="e">Job Count By Experience Level</p>', unsafe_allow_html=True)
        st.write(fig)
    with col2:
        st.markdown("""
        <style>
        .e {
            font-size:20px !important;
            font-family:Sans-serif;
            font-weight: Bold;
            color: black
            }
        </style>
        """, unsafe_allow_html=True)
        df['number_of_positions'] = df['number_of_positions'].astype(float)
        sum_position = (df['number_of_positions']).sum()

        st.markdown('<p class="e">Total Open Positions</p>', unsafe_allow_html=True)
        values=[sum_position]
        labels=['Total Positions']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=['#12168A']),textinfo='value')])
        fig.update_layout(
        showlegend=False,
        width=400,   
        height=300,   
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=30, b=20, t=20), 
        font=dict(color='black', size=50)
    )
    
        st.plotly_chart(fig)





    #line chart 

    ## def filteringjobcat for two purpose two dropdown filter one for line chart and one for bar chart 
    def filtering_job_cat(df,instance):
        job_cat=Home.job_cat

        st.markdown('<span style="font-size: 20px;color: black;"><b>Please Specify a Job Category</b></span>', unsafe_allow_html=True)
        j_cat=st.multiselect(f"{instance}",job_cat, 'Overall')
        if 'Overall' in j_cat:
            df_filtered=df
        else:
            df_filtered = df[df['job_category'].isin(j_cat)]
        return df_filtered
    
    def date_process(df):
        #line_chart_date = df.copy()
        line_chart_date=filtering_job_cat(df, "Line Chart")
        line_chart_date['posting_date'] = pd.to_datetime(line_chart_date['posting_date'])
        line_chart_date['month_year'] = line_chart_date['posting_date'].dt.strftime('%m/%Y')
        jobs_per_month=line_chart_date.groupby('month_year')['number_of_positions'].sum().reset_index()

        jobs_per_month = jobs_per_month.rename(columns={'month_year': 'Month Year', 'number_of_positions': 'Job Count'})
        jobs_per_month['Month Year'] = pd.to_datetime(jobs_per_month['Month Year'], format='%m/%Y')
        jobs_per_month = jobs_per_month.sort_values('Month Year')
        return jobs_per_month


    def line_chart(jobs_per_month):

        st.markdown("""
        <style>
        .f {
        font-size:30px !important;
        font-family:Sans-serif;
        font-weight: Bold;
        color: #1A0556
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<p class="f">Monthly Job Posted</p>', unsafe_allow_html=True)
        fig = px.line(jobs_per_month, x='Month Year', y='Job Count',color_discrete_sequence=px.colors.qualitative.Set1,  
                labels={'Month Year':'<b><span style="color: blue;">Monthly</span></b>', 'Job Count': '<b><span style="color: blue;">Number of Jobs</span></b>'}, 
                )
        fig.update_layout(
        xaxis=dict(title_font=dict(size=20),
                tickfont=dict(size=20),
                )
        ,
        yaxis=dict
        (
        title_font=dict(size=20),
        tickfont=dict(size=20),
        )
        )
        fig.update_traces(mode='lines+markers', hovertemplate=None) 
       

        #fig.update_xaxes(showline=True,gridcolor='#1B1E66')
        fig.update_yaxes(showline=True,gridcolor='#8E8FAB')

        fig.update_layout(
            hoverlabel=dict(
            bgcolor="#F13557",
            font_size=20,
            font_family="Rockwell")
         )
        
        fig.update_layout(hovermode='x unified') 
        fig.update_layout(width=800,height=500,transition_duration=300, autosize=True,plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(255,255,255,255)') 


        st.plotly_chart(fig)



    jobs_per_month=date_process(df)

    # calling the function to create the line chart 
    line_chart(jobs_per_month)

    
    #calling job filter function for bar chart 

    filtered=filtering_job_cat(df,"Bar Chart")

    agency_bar= filtered.groupby('agency')['number_of_positions'].sum().reset_index()

    fig_3=px.bar(agency_bar, x='agency',y='number_of_positions',color='agency')

    fig_3.update_layout(
        width=1000,
        height=600,
        xaxis_tickangle=-45, 
        showlegend=False,
        margin=dict(l=100, r=50, t=50, b=170), 

        xaxis=dict(
            title='<b>Agency</b>',title_font=dict(size=14),
                tickfont=dict(size=10),
                )
        ,
        yaxis=dict
            (       
            title='<b>Number of Positions</b>',
            title_font=dict(size=14),
            tickfont=dict(size=20),
            )
    )


    st.plotly_chart(fig_3)
# when radio button resume cloud selected 
# WordCloud for resume 

if selection =="Resume WordCloud":
    def generate_word_cloud(text):
        

        wordcloud = WordCloud(
            width=900,
            height=700,
            max_words=120,
            colormap='seismic',  
            background_color='white',
            min_font_size=12,
            max_font_size=50,
            prefer_horizontal=1,
            relative_scaling=0,  
            margin=2,
            random_state=42
        ).generate(text)

        fig=plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(fig)

    def process_pdf(file):
        pdf_reader = PyPDF2.PdfReader(file)
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        # Removing email format 
        resume_text = re.sub(r'\b([A-Z][a-z]+)\b|\S+@\S+', '', resume_text)

        return resume_text

    def main():
        st.title("Resume Word Cloud")
        uploaded_file = st.file_uploader("Upload Your Resume Here In PDF Format", type="pdf")

        if uploaded_file is not None:
            resume_text = process_pdf(uploaded_file)
            st.subheader("Word Cloud")
            generate_word_cloud(resume_text)

    if __name__ == "__main__":
        main()

st.sidebar.title("More")
st.sidebar.info(
    """
    This app is maintained by Tahira Tabassum :female-technologist: . You can follow me on 
        [LinkedIn](https://www.linkedin.com/in/tahira-tabassum/) |[GitHub](https://github.com/tahiratabassum19)


    Source Code: <https://github.com/tahiratabassum19/NYCJobs.git>


    Dataset Used: [NYC Jobs](https://data.cityofnewyork.us/City-Government/NYC-Jobs/kpav-sd4t)



""")
st.sidebar.image("side.jpeg",use_column_width=True)
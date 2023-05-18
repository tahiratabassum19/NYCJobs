import streamlit as st
import pandas as pd 
import numpy as np 
import seaborn as sns
import plotly.express as px
import plotly as plt
import plotly.graph_objects as go
import Home

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



df=Home.cleaned_df
st.title(":bar_chart: Job Dashboard")
st.markdown('##')


# col_1,col_2,col_3=st.columns(3)

# with col_1:
#     st.markdown("""
#     <style>
#     .d {
#         font-size:20px !important;
#         color:  royalblue
#         font-weight: bold;
#         }
#     </style>
#     """, unsafe_allow_html=True)
#     st.markdown('<p class="d">Total Open Positions by level </p>', unsafe_allow_html=True)
#     sum_position = sum(int(val) for val in df['number_of_positions'])
#     st.markdown("""
#     <style>
#     .sum {
#         font-size:15px !important;
#         color:  royalblue
#         font-weight: bold;
#         }
#     </style>
#     """, unsafe_allow_html=True)
#     st.markdown(f'<p class="sum">{sum_position}</p>', unsafe_allow_html=True)

# with col_2:
#     st.markdown("""
#     <style>
#     .d {
#         font-size:20px !important;
#         color:  royalblue
#         font-weight: bold;
#         }
#     </style>
#     """, unsafe_allow_html=True)
#     st.markdown('<p class="d">Filter By Level</p>', unsafe_allow_html=True)
#     st.selectbox("",Home.career_level)

# with col_3:
#     st.markdown("""
#     <style>
#     .d {
#         font-size:20px !important;
#         color:  royalblue
#         font-weight: bold;
#         }
#     </style>cd p
#     """, unsafe_allow_html=True)
#     st.markdown('<p class="d">Total Open Positions By Level</p>', unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#     .sum {
#         font-size:15px !important;
#         color:  royalblue
#         font-weight: bold;
#         }
#     </style>
#     """, unsafe_allow_html=True)
#     st.markdown(f'<p class="sum">{sum_position}</p>', unsafe_allow_html=True)


col1, col2=st.columns(2)

with col1:
    df['number_of_positions'] = df['number_of_positions'].astype(float)

    career = df.groupby('career_level')['number_of_positions'].sum().reset_index()

    car = career.rename(columns={'career_level': 'Level', 'number_of_positions': 'Count'})
    fig = px.pie(car, values='Count',names='Level',hover_name='Count', color_discrete_sequence=["#ee6c4d","red","black"])
    fig.update_layout(showlegend=False,margin=dict(l=1,r=1,b=1,t=1),width=170,height=170, paper_bgcolor= "rgba(0,0,0,0)",font=dict(color='white',size=10))


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
    #sum_position = sum(int(val) for val in df['number_of_positions'])

    st.markdown('<p class="e">Total Open Positions</p>', unsafe_allow_html=True)
    values=[sum_position]
    labels=['Total Positions']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=['#CE1E41']),textinfo='value')])
    fig.update_layout(showlegend=False,margin=dict(l=1,r=1,b=1,t=1),width=170,height=170,paper_bgcolor= "rgba(0,0,0,0)",font=dict(color='#080002',size=20))
    
    st.plotly_chart(fig)

#line chart 

line_chart_date = df.copy()
line_chart_date['posting_date'] = pd.to_datetime(line_chart_date['posting_date'])
line_chart_date['month_year'] = line_chart_date['posting_date'].dt.strftime('%m/%Y')
jobs_per_month=line_chart_date.groupby('month_year')['number_of_positions'].sum().reset_index()

jobs_per_month = jobs_per_month.rename(columns={'month_year': 'Month Year', 'number_of_positions': 'Job Count'})
# Convert 'Month Year' to a pandas datetime column to sort
jobs_per_month['Month Year'] = pd.to_datetime(jobs_per_month['Month Year'], format='%m/%Y')
jobs_per_month = jobs_per_month.sort_values('Month Year')

st.markdown("""
    <style>
    .f {
        font-size:20px !important;
        font-family:Sans-serif;
        font-weight: Bold;
        text-align: Center;
        color: black
        }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<p class="f">Monthly Job Posted</p>', unsafe_allow_html=True)
fig = px.line(jobs_per_month, x='Month Year', y='Job Count',color_discrete_sequence=px.colors.qualitative.Set1,  # Set color palette
              labels={'Month Year':'Monthly','Job Count': 'Number of Jobs'}, 
              )
fig.update_traces(mode='lines+markers', hovertemplate=None) 

fig.update_xaxes(showline=True,gridcolor='#DE8E7D')
fig.update_yaxes(showline=True,gridcolor='#DE8E7D')


fig.update_layout(hovermode='x unified') 
fig.update_layout(width=700,height=400,transition_duration=500, autosize=True,plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0.1)') 
st.write(fig)
#255, 96, 67, 0.8)

df['Work Location']=df['work_location'].fillna(df['work_location'])

#x=df['career_level','job_category','number_of_positions']
#x.pivot
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# df['number_of_positions'] = df['number_of_positions'].astype(np.int64)

# x=df.drop_duplicates(['career_level','number_of_positions'])

# fig,ax=plt.subplots(figsize=(30,10))
# table=x.pivot_table(index='career_level',values='number_of_positions',aggfunc=).fillna(0)
# table = table.astype(np.int64)

# ax=sns.heatmap(table.astype(int),annot=True,fmt='d',cmap="Blues")
# st.pyplot(fig)
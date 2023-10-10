import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("Scraping By Job Title")

job_titles = ['None', 'Chief Information Security Officer', 'Office Manager', 'Policy Officer', 'Internal Communications Officer']

option = st.selectbox('Select job titles to scrap',job_titles)

if option != 'None':
    site = 'linkedin.com'
    staff = option
    location = 'Westchester NY'
    location = "+".join(location.split())
    staff = "+".join(staff.split())
    url = "https://www.google.com/search?&q=site%3A"+site+"%2Fin+%2B+"+location+"+%2B+%22"+staff
    # scraping parameters
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    response=requests.get(url,headers=headers)
    page = BeautifulSoup(response.text,'html.parser')
    people = []
    profiles = []
    if page:
        elements = page.findAll("div", attrs={"class": "MjjYud"})
        for p in elements:
            title = p.find('h3')
            profile = p.find('a')

            if title:
                people.append(title.text)
            if profile:
                profiles.append(profile['href'])
        jobTitles = [option]*len(people)
        df_scraped = pd.DataFrame(list(zip(jobTitles, people, profiles)), columns = ['Title', 'Person', 'LinkedIn Profile'])
        st.dataframe(df_scraped)
        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        filename="_".join(option.split())+".csv"
        csv = convert_df(df_scraped)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=filename,
            mime='text/csv',
        )

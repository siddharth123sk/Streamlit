#importing necessary packages
import yfinance as yf
import streamlit as st
from datetime import datetime
import pandas as pd
import base64
from io import BytesIO

#using xlsxwriter engine to output the data in CSV
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

#getting the table data for major holders of the company, the data will by default be saved by the name 'major_holders.csv'
def get_table_download_link_major_holders(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="major_holders.xlsx">Download CSV file</a>' # decode b'abc' => abc

#getting the table data for institutional holders of the company, the data will by default be saved by the name 'institutional_holders.csv'
def get_table_download_link_institutional_holders(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="institutional_holders.xlsx">Download CSV file</a>' # decode b'abc' => abc

#getting the table data for recommendations of the company, the data will by default be saved by the name 'recommendations.csv'
def get_table_download_link_recommendations(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="recommendations.xlsx">Download CSV file</a>' # decode b'abc' => abc



#header image
st.image('./header.png')


#introduction of the app
st.write("""
## Simple Stock Info App

Shown are the company and stocks details!

""")

#drop down menu to select different companies, currently it supports the top 11 companies which are being viewed the most on Yahoo Finance
company = st.selectbox('Which company would you like to view?', ('TESLA', 'GOOGLE', 'APPLE', 'MICROSOFT', 'AMAZON', 'FACEBOOK', 'JPMORGAN CHASE & CO','WALMART', 'THE WALT DISNEY COMPANY', 'BANK OF AMERICA CORPORATION', 'NETFLIX'))

#getting the user selected company and assigning the option variable the ticker name of yfinance to retreive data
if (company == 'TESLA'):
    option = 'TSLA'
if (company == 'GOOGLE'):
    option = 'GOOGL'
if (company == 'APPLE'):
    option = 'AAPL'
if (company == 'MICROSOFT'):
    option = 'MSFT'
if (company == 'AMAZON'):
    option = 'AMZN'
if (company == 'FACEBOOK'):
    option = 'FB'
if (company == 'JPMORGAN CHASE & CO'):
    option = 'JPM'
if (company == 'WALMART'):
    option = 'WMT'
if (company == 'THE WALT DISNEY COMPANY'):
    option = 'DIS'
if (company == 'BANK OF AMERICA CORPORATION'):
    option = 'BAC'
if (company == 'NETFLIX'):
    option = 'NFLX'

#printing the user selected company name
st.write('Showing data for ', company)

#st.write('Please wait...Retrieving data now...')

#assigning the user input to the tickerSymbol variable
tickerSymbol = option

#getting the ticker data
tickerData = yf.Ticker(tickerSymbol)

#creating a variable called end to store current data
end = datetime.today().strftime('%Y-%m-%d')
#print(end)

#getting the date range for stock data, it is 31st May 2010 to the present data
tickerDf = tickerData.history(period='1d', start='2010-5-31', end=end)

#printing data
st.write(tickerData.info)
st.line_chart(tickerData.history(period= "max"))
st.write(tickerData.actions)
st.write(tickerData.splits)

st.write(tickerData.major_holders)
#making the download CSV button
df = tickerData.major_holders
st.markdown(get_table_download_link_major_holders(df), unsafe_allow_html=True)

st.write(tickerData.institutional_holders)
#making the download CSV button
df = tickerData.institutional_holders
st.markdown(get_table_download_link_institutional_holders(df), unsafe_allow_html=True)

st.write(tickerData.sustainability)

st.write(tickerData.recommendations)
#making the download CSV button
df = tickerData.recommendations
st.markdown(get_table_download_link_recommendations(df), unsafe_allow_html=True)

st.write(tickerData.calendar)
st.write(tickerData.isin)
st.write(tickerData.options)

st.line_chart(tickerDf.Open)
st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
st.line_chart(tickerDf.High)

st.write('\n')
st.write('\n')
st.write('\n')

st.write("""
#### Made by Siddharth """)
# st.markdown(
#     """<a href="https://www.siddharthsah.com/">siddharthsah.com</a>""", unsafe_allow_html=True,
# )
link = '[siddharthsah.com](http://www.siddharthsah.com/)'
st.markdown(link, unsafe_allow_html=True)
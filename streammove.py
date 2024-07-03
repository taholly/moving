import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# دریافت داده‌ها
url = 'https://raw.githubusercontent.com/taholly/moving/main/Mreports.xlsx'
response = requests.get(url)

if response.status_code == 200:
    file = BytesIO(response.content)
    try:
        # بارگذاری داده‌ها به DataFrame
        Mrepo = pd.read_excel(file, engine='openpyxl', index_col="نماد")
        st.write("Dataframe loaded successfully:")
        st.write(Mrepo.head())  # نمایش چند ردیف اول
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
else:
    st.error(f"Failed to retrieve file: {response.status_code}")

# توابع کمکی
def Moving(dfkol , nemad, mnum):
    dfkol = dfkol.T.ffill().bfill()
    df = dfkol[nemad].to_frame()
    df[f"SMA{mnum}"] = df[nemad].rolling(mnum).mean()
    return df

# تنظیم عنوان اپلیکیشن
st.title('Monthly Sale Data')

# گرفتن نام شرکت و بازه میانگین از کاربر
company_name = st.text_input('نام شرکت را وارد کنید:')
movnum = st.text_input('بازه ی میانگین را مشخص کنید:')

try:
    movnum = int(movnum)
except ValueError:
    st.error('لطفاً یک عدد صحیح وارد کنید.')

# اگر نام شرکت وارد شده باشد
if company_name:
    # دریافت داده‌های قیمتی شرکت
    if company_name in Mrepo.index:
        df = Moving(Mrepo, company_name, mnum=movnum)
        
        # رسم نمودار با استفاده از Plotly
        fig = go.Figure()
        
        # اضافه کردن داده‌های اصلی
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[company_name],
            mode='lines+markers',
            name='Company'
        ))

        # اضافه کردن میانگین متحرک
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[f"SMA{movnum}"],
            mode='lines',
            name=f'SMA {movnum}'
        ))

        # تنظیمات نمودار
        fig.update_layout(
            title="Monthly Sale Data",
            xaxis_title='Date',
            yaxis_title='Sale',
            xaxis_rangeslider_visible=True,
            template="plotly_dark"
        )

        # نمایش نمودار با Plotly در Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f'شرکت "{company_name}" در داده‌ها یافت نشد.')

st.markdown("Produced By Taha SadeghiZadeh")
st.markdown("Artin Asset Management")

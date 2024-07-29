import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import plotly.graph_objects as go

# دریافت داده‌ها
url = 'https://raw.githubusercontent.com/taholly/moving/main/Mreports.xlsx'
response = requests.get(url)

if response.status_code == 200:
    file = BytesIO(response.content)
    try:
        # بارگذاری داده‌ها به DataFrame
        Mrepo = pd.read_excel(file, engine='openpyxl', index_col="نماد")
        st.write("Dataframe loaded successfully:")
        #st.write(Mrepo.head())  # نمایش چند ردیف اول
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
else:
    st.error(f"Failed to retrieve file: {response.status_code}")

# توابع کمکی
def Moving(dfkol , nemad, mnum):
    dfkol = dfkol.T.bfill()
    df = dfkol[nemad].to_frame()
    df[f"SMA{mnum}"] = df[nemad].rolling(mnum).mean()
    return df

def calculate_percentage_difference(df):
    # محاسبه اختلاف درصدی بین آخرین مقدار و میانگین
    last_row = df.iloc[-1]
    percentage_diff = (last_row - df.mean()) / df.mean() * 100
    return percentage_diff.abs()

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
        
        # محاسبه اختلاف درصدی
        percentage_diff = calculate_percentage_difference(df)
        
        # پیدا کردن نمادهایی با بیشترین اختلاف درصدی
        top_diff_symbols = percentage_diff.sort_values(ascending=False).head(10)
        
        # نمایش پنجره با نمادهای با بیشترین اختلاف درصدی
        #st.subheader('نمادهایی با بیشترین اختلاف درصدی از میانگین:')
        #st.dataframe(top_diff_symbols)
        
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
        st.show(df)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f'شرکت "{company_name}" در داده‌ها یافت نشد.')
    
st.markdown("Produced By Taha SadeghiZadeh")
st.markdown("Artin Asset Management")

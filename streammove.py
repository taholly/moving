import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import matplotlib.pyplot as plt


url = 'https://raw.githubusercontent.com/taholly/moving/main/Mreports.xlsx'
response = requests.get(url)

if response.status_code == 200:
    file = BytesIO(response.content)
    try:
        Mrepo = pd.read_excel(file, engine='openpyxl', index_col="نماد")
        print(Mrepo.head())  # چاپ چند ردیف اول برای بررسی
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
else:
    print(f"Failed to retrieve file: {response.status_code}")


# ادامه کد...



#Mrepo = Mrepo.set_index(Mrepo['نماد'])

def farsito_finglish(text):
    mapping = {
        'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh',
        'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z',
        'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh', 'ک': 'k', 'گ': 'g', 'ل': 'l',
        'م': 'm', 'ن': 'n', 'و': 'v', 'ه': 'h', 'ی': 'i', 'ء': "'", 'آ': 'a', 'ئ': 'e', 'إ': 'e',
        'أ': 'a', 'ؤ': 'o', 'ى': 'a', 'ي': 'i'
    }
    finglish_text = ''.join([mapping.get(char, char) for char in text])
    return finglish_text

def Moving(dfkol , nemad, mnum):
    dfkol = dfkol.T.ffill().bfill()
    df = dfkol[nemad].to_frame()
    #df = df.rename(columns={nemad:nemad2})
    df[f"SMA{mnum}"] = df[nemad].rolling(mnum).mean()
    return df

# تنظیم عنوان اپلیکیشن
st.title('Monthly Sale data')

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
        m , n = df.shape
        for i in range(m): 
            for j in range(n):
                df.iloc[i,j] = int(df.iloc[i,j])
        # استایل‌دهی DataFrame - بلد کردن اعداد
        styled_df = df.style.applymap(lambda x: 'font-weight: bold; text-align: center;' if isinstance(x, (int, float,str)) else '')
        
        st.dataframe(styled_df, use_container_width=True)
        # رسم نمودار
        fig, ax = plt.subplots(figsize=(26, 10))
        ax.plot(df[company_name], label='Company')  
        ax.plot(df[f"SMA{movnum}"], label=f'SMA {movnum}' ) 
        ax.set_title("Monthly Sale Data")
        ax.set_xlabel('Date')
        ax.set_ylabel('Sale')
        ax.grid(True)
        ax.legend()
        # نمایش نمودار با Streamlit
        st.pyplot(fig)
    else:
        st.error(f'شرکت "{company_name}" در داده‌ها یافت نشد.')
st.markdown("Produce By Taha SadeghiZadeh")
st.markdown("Artin Asset Management")

#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd


# In[5]:


import matplotlib.pyplot as plt
plt.style.use('default')
#%matplotlib inline


# In[6]:


import numpy as np


# In[7]:


import streamlit as st


# In[8]:
import requests
from io import BytesIO

# URL فایل اکسل در گیت‌هاب
url = 'https://github.com/taholly/moving/tree/main/Mreports.xlsx'

# دریافت فایل اکسل
response = requests.get(url)
file = BytesIO(response.content)

# خواندن داده‌ها از فایل اکس

Mrepo = pd.read_excel(file , index_col='نماد')


# In[9]:


def farsito_finglish(text):
    # تعریف نگاشت حروف فارسی به معادل فینگلیش آنها
    mapping = {
        'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh',
        'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z',
        'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh', 'ک': 'k', 'گ': 'g', 'ل': 'l',
        'م': 'm', 'ن': 'n', 'و': 'v', 'ه': 'h', 'ی': 'i', 'ء': "'", 'آ': 'a', 'ئ': 'e', 'إ': 'e',
        'أ': 'a', 'ؤ': 'o', 'ى': 'a', 'ي': 'i'
    }
    
    # تبدیل حروف متن از فارسی به فینگلیش
    finglish_text = ''.join([mapping.get(char, char) for char in text])
    
    return finglish_text


# In[10]:


def Moving(dfkol , nemad, mnum):
    dfkol = dfkol.T.ffill().bfill()
    df = dfkol[nemad].to_frame()
    
    nemad2 = farsito_finglish(nemad)
    
    df = df.rename(columns={nemad:nemad2})
    #print(df)

    df[f"EMA{mnum}"] = df[nemad2].ewm(span=mnum).mean()
    #df[[farsito_finglish(nemad), f"EMA{mnum}"]].plot(title=farsito_finglish(nemad),
                                   #figsize=(24, 8),logy = True , grid = True , xticks = range(len(list(df.index))))    
    return df
    


# In[11]:


Moving(Mrepo,nemad="سآبیک",mnum=3)


# In[26]:


# تنظیم عنوان اپلیکیشن
st.title('نمایش داده‌های قیمتی شرکت')

# گرفتن نام شرکت از کاربر
company_name = st.text_input('نام شرکت را وارد کنید:')
movnum = st.text_input('بازه ی میانگین را مشخص کنید:')
try:
    movnum = int(movnum)
except:
    pass
# اگر نام شرکت وارد شده باشد
if company_name:
# دریافت داده‌های قیمتی شرکت
    df = Moving(Mrepo,company_name, mnum=movnum)
    df
    # نمایش داده‌ها
    #st.write(df)

    fig, ax = plt.subplots(figsize=(36,20))  # تنظیم اندازه فیگر

    ax.plot(df[farsito_finglish(company_name)])  # 'r-' به معنی خط قرمز است
    ax.plot(df[f"EMA{movnum}"] )  # 'b--' به معنی خط آبی نقطه‌چین است# رسم نمودار
    ax.legend()
    st.pyplot(fig)
    


# In[ ]:





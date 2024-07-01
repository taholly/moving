#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import requests
from io import BytesIO

# URL فایل اکسل در گیت‌هاب (URL مستقیم)
url = 'https://raw.githubusercontent.com/taholly/moving/main/Mreports.xlsx'

# دریافت فایل اکسل
response = requests.get(url)
file = BytesIO(response.content)

# خواندن داده‌ها از فایل اکسل
Mrepo = pd.read_excel(file)
Mrepo = Mrepo.set_index(Mrepo['نماد'])

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
    nemad2 = farsito_finglish(nemad)
    df = df.rename(columns={nemad:nemad2})
    df[f"EMA{mnum}"] = df[nemad2].ewm(span=mnum).mean()
    return df

# تنظیم عنوان اپلیکیشن
st.title('نمایش داده‌های قیمتی شرکت')

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
        
        # رسم نمودار
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(df[farsito_finglish(company_name)], label=f'{company_name} Price')  # 'r-' به معنی خط قرمز است
        ax.plot(df[f"EMA{movnum}"], label=f'EMA {movnum}')  # 'b--' به معنی خط آبی نقطه‌چین است
        ax.legend()
        ax.set_title(f'نمودار قیمتی {company_name}')
        ax.set_xlabel('تاریخ')
        ax.set_ylabel('قیمت')
        ax.grid(True)
        
        # نمایش نمودار با Streamlit
        st.pyplot(fig)
    else:
        st.error(f'شرکت "{company_name}" در داده‌ها یافت نشد.')

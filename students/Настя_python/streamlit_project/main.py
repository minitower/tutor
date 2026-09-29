import streamlit as st
import requests
import matplotlib.pyplot as plt
import PIL.Image as Image

request_url='http://www.7timer.info/bin/astro.php?lon=113.17&lat=23.09&ac=0&lang=en&unit=metric&output=internal&tzshift=0'

response = requests.get(request_url)


response.raise_for_status()
data = response.content

with open('data.png', 'wb') as f:
    f.write(data)

st.image('data.png', caption='Weather Forecast')
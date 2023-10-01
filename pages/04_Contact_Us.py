import streamlit as st
from PIL import Image
import json
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

logo = Image.open(r'./image/logo.png')

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_contact_us = load_lottiefile("./lottie/contact-us.json")

col3,col1, col2 = st.columns([2, 3,2])
with col3:
    st_lottie(
        lottie_contact_us,
        speed=0.7,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        height=200,
        width=None,
        key="barchart", )
st.markdown(""" <style> .font {font-size:50px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """,unsafe_allow_html=True)
st.markdown(""" <style> .font1 {font-size:28px ; font-family: 'Copper Black'; color: yellow;} </style> """,
            unsafe_allow_html=True)
st.markdown(""" <style> .font2 {font-size:22px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)
st.markdown(""" <style> .font4 {font-size:36px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """,
                unsafe_allow_html=True)

with col1:
    st.markdown('<p class="font">iTimesAlgo</p>', unsafe_allow_html=True)
    #html_temp = """<div style="background-color:darkgrey;padding:14px><h2 style="color: #FF9633;text-align:centre;">iTimesAlgo</h2></div>"""
    #st.markdown(html_temp, unsafe_allow_html=True)
    st.markdown('<p class="font1">Contact us through</p>', unsafe_allow_html=True)
    st.markdown("[TELEGRAM](https://t.me/itimesalgo/)    /      [TWITTER](https://twitter.com/itimesalgo)    /      [INSTAGRAM](https://www.instagram.com/itimesalgo/) ")
    #st.markdown("[Twitter](https://twitter.com/itimesalgo)")

with col2:  # To display brand log
    st.image(logo, width=200)

#st.title('iTimesAlgo')
#st.markdown(""" <style> .font1 {font-size:50px ; font-family: 'Copper Black'; color: seablue;} </style> """, unsafe_allow_html=True)
#st.markdown('<p class="font1">iTimesAlgo</p>', unsafe_allow_html=True)

#st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)
st.markdown("---")
st.markdown('<p class="font2">About the Creator</p>', unsafe_allow_html=True)
st.write("We @iTimes are trying to create basic DIY fundamental analysis. \n\n We shall try bringing you here bse announcements here")
st.write("We sincerely appreciates your suggestions and contribution to improvise our iTimes community.")
st.markdown("---")




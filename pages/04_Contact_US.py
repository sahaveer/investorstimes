import streamlit as st

from PIL import Image
logo = Image.open(r'./image/logo.png')

st.markdown(""" <style> .font {font-size:36px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)

col1, col2 = st.columns([0.8, 0.2])
with col1:  # To display the header text using css style
    st.markdown('<p class="font">Contact us through</p>',unsafe_allow_html=True)
    st.markdown("[telegram](https://t.me/itimesalgo/)")
    st.markdown("[Twitter](https://twitter.com/itimesalgo)")
    # st.markdown('<p class="font">Contact us through [telegram](https://t.me/itimesalgo/). </p>', unsafe_allow_html=True)

with col2:  # To display brand log
    st.image(logo, width=130)


st.write("We sincerely appreciates your suggestions and contribution to improvise our iTimes community.")

import streamlit as st
from PIL import Image

logo = Image.open(r'./image/logo.png')

#st.title('iTimes')
html_temp = """
    <div style="background-color:darkgrey;padding:14px>
    <h2 style="color: #FF9633;text-align:centre;">iTimesAlgo</h2>
    </div>
    st.markdown(html_temp, unsafe_allow_html=True)
    """
st.markdown(""" <style> .font1 {
                font-size:50px ; font-family: 'Copper Black'; color: seablue;} 
                </style> """, unsafe_allow_html=True)
st.markdown('<p class="font1">iTimesAlgo</p>', unsafe_allow_html=True)

#col1, col2 = st.columns([0.8, 0.2])
#with col1:
    #st.markdown('<p class="font1">iTimesAlgo</p>', unsafe_allow_html=True)
#with col2:  # To display brand log
    #st.image(logo, width=80)

st.markdown(""" <style> .font {font-size:22px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """, unsafe_allow_html=True)

st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)
st.markdown("---")
st.write("We @iTimes are trying to create basic DIY fundamental analysis. \n\n We shall try bringing you here bse announcements and amibroker eod data here")

st.markdown(""" <style> .font {font-size:36px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """,
                unsafe_allow_html=True)

col1, col2 = st.columns([0.8, 0.2])
with col1:  # To display the header text using css style
    st.markdown('<p class="font">Contact us through</p>', unsafe_allow_html=True)
    st.markdown("[telegram](https://t.me/itimesalgo/)")
    st.markdown("[Twitter](https://twitter.com/itimesalgo)")
    # st.markdown('<p class="font">Contact us through [telegram](https://t.me/itimesalgo/). </p>', unsafe_allow_html=True)

with col2:  # To display brand log
    st.image(logo, width=130)

st.write("We sincerely appreciates your suggestions and contribution to improvise our iTimes community.")

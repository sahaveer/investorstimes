import streamlit as st
from PIL import Image

logo = Image.open(r'./image/logo.png')
st.set_page_config(page_title="iTimesAlgo",page_icon=":bar_chart:",layout="wide")
def main():
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
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown('<p class="font1">iTimesAlgo</p>', unsafe_allow_html=True)
    with col2:  # To display brand log
        st.image(logo, width=80)

    st.markdown(""" <style> .font {
    font-size:22px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)

    st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.write("We @iTimes are trying to create basic DIY fundamental analysis. \n\n We shall try bringing you here bse announcements, news, amibroker eod data here")

if __name__ == '__main__':
    main()


#Custom CSS to remove header,footer, hamburger icon
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)

#REFERENCE :
#FLASK : https://www.datasciencelearner.com/how-to-create-a-bar-chart-from-a-dataframe-in-python/#:~:text=There%20is%20also%20another%20method%20to%20create%20a,y-axis%20values%20you%20want%20to%20draw%20the%20bar.

#Streamlit Basics : https://www.datacamp.com/tutorial/streamlit#on-windows-

# https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb#:~:text=When%20building%20data%20apps%20using%20Streamlit%2C%20sometimes%20you,displayed%20in%20the%20app%20looks%20plain%20and%20static.

#https://towardsdatascience.com/create-a-bar-chart-race-animation-app-using-streamlit-and-raceplotly-e44495249f11


#   https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/
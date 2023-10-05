# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pdfplumber
import streamlit as st
import re
import json
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import json
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

text = ""
texxt = ""

st.set_page_config(
        page_title="Concal Summariser",
        #page_icon=":hammer_and_wrench:",
        layout="wide"
    )

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_summariser = load_lottiefile("./lottie/summariser.json")

with st.sidebar:
	st_lottie(
		lottie_summariser,
		speed=0.7,
		reverse=False,
		loop=True,
		quality="low",  # medium ; high
		height=None,
		width=None,
		key="barchart", )

col1, col2 = st.columns([0.8, 0.2])
with col1:
	pdf_upload = st.file_uploader("upload Concal", type= ['pdf'])
with col2:
	avgperc = st.number_input("Context Length",1.00,2.00,1.25,0.05)

if pdf_upload is not None:
	name_file = pdf_upload.name.split('.')[0]
	col3, col4, col5 = st.columns([0.1,0.1,0.8])
	with pdfplumber.open(pdf_upload) as pdf:
		with col3:
			start_from_pageno = st.number_input("Start from", 1, len(pdf.pages), 2, 1)
		with col4 :
			till_page_no = st.number_input("Till page",2,len(pdf.pages),len(pdf.pages),1)
		with col5:
			with st.expander("Help"):
				st.write("Upload any Company CONCAL to get a concised report.")
				st.write(
					"Context Length : if 1, then you get the actual report. But increasing this number, summarises the report. The higher this number, the lesser the report. Please do note that, it reduces the content also ")
				st.write("Start from : starts analysing document from this page number")
				st.write("You have a provision to edit the concized report and then download it as a TXT file")
		for page in pdf.pages[start_from_pageno:till_page_no] :
			text += page.extract_text()

	# Tokenizing the text
	stopWords = set(stopwords.words("english"))
	pattern = '(page|Page|PAGE)\s*\d+\s*(of|OF|Of)\s*\d+'
	date_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December|january|february|march|april|may|june|july|august|september|october|november|december|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s*\d{2}\s*(\,|\s)\s*\d{4}'
	rupee_pattern = r'Rs.'
	replace_rupee = 'Rs'
	moderator_pattern = r'(Thank you|Please go ahead.|Moderator | Thank you very much.)'
	replace = ''
	texxt = re.sub(pattern, replace, text)
	texxt = re.sub(date_pattern, replace, texxt)
	texxt = re.sub(moderator_pattern,replace, texxt)
	texxt = re.sub(rupee_pattern,replace_rupee,texxt)
	texxt = re.sub('\s{2}',' ',texxt)
	words = word_tokenize(texxt)

	# Creating a frequency table to keep the score of each word
	freqTable = dict()
	for word in words:
		word = word.lower()
		if word in stopWords:
			continue
		if word in freqTable.keys():
			freqTable[word] += 1
		else:
			freqTable[word] = 1

	# Creating a dictionary to keep the score of each sentence based on word freq
	sentences = sent_tokenize(texxt)
	sentenceValue = dict()
	for sentence in sentences:
		for word, freq in freqTable.items():
			if word in sentence.lower():
				if sentence in sentenceValue.keys():
					sentenceValue[sentence] += freq
				else:
					sentenceValue[sentence] = freq

	sumValues = 0
	for sentence in sentenceValue:    # this gives all keys of sentenceValue
		sumValues += sentenceValue[sentence]

	# Average value of a sentence from the original text
	average = int(sumValues / len(sentenceValue))

	# Storing sentences into our summary.
	summary = ''
	for sentence in sentences:
		if (sentence in sentenceValue) and (sentenceValue[sentence] > (avgperc * average)):
			summary += "\n" + sentence
	st.write("____")
	del_further = st.text_input("Delete any particular word/s")
	if del_further is not None:
		del_these = del_further.split(',')
		for each in del_these:
			summary = re.sub(each,replace, summary)
	edited_txt = st.text_area("Edit further and generate ur own file",value=summary,height=500)
	st.info('the {} words of uploaded document is concised to {} words'.format(len(text),len(edited_txt)))
	st.download_button(label = "Download as txt",data= edited_txt,file_name=name_file+'.txt')
	#split_summary = sent_tokenize(summary)
	#for each in split_summary:
		#st.write(each)


st.write("____")
st.write('made with :green_heart: to Indian Stock Investors')

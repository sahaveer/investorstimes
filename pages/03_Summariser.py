# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pdfplumber
import streamlit as st
import re

text = ""
texxt = ""
col1, col2 = st.columns([0.8, 0.2])
with col1:
	pdf_upload = st.file_uploader("upload Concal", type= ['pdf'])
with col2:
	avgperc = st.number_input("Higher the number, Lesser the context",1.00,2.00,1.20,0.05)

if pdf_upload is not None:
	with pdfplumber.open(pdf_upload) as pdf:
		for page in pdf.pages :
			text += page.extract_text()

	# Tokenizing the text
	stopWords = set(stopwords.words("english"))
	pattern = '(page|Page|PAGE)\s*\d+\s*(of|OF|Of)\s*\d+'
	date_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December|january|february|march|april|may|june|july|august|september|october|november|december|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s*\d{2}\s*(\,|\s)\s*\d{4}'
	moderator_pattern = r'(Thank you|Please go ahead. )'
	replace = ''
	texxt = re.sub(pattern, replace, text)
	texxt = re.sub(date_pattern, replace, texxt)
	texxt = re.sub(moderator_pattern,replace, texxt)
	texxt = re.sub('\s{2}',' ',texxt)
	words = word_tokenize(texxt)

	# Creating a frequency table to keep the
	# score of each word

	freqTable = dict()
	for word in words:
		word = word.lower()
		if word in stopWords:
			continue
		if word in freqTable.keys():
			freqTable[word] += 1
		else:
			freqTable[word] = 1

	# Creating a dictionary to keep the score
	# of each sentence
	sentences = sent_tokenize(texxt)
	sentenceValue = dict()
	for sentence in sentences:
		for word, freq in freqTable.items():
			if word in sentence.lower():
				if sentence in sentenceValue:
					sentenceValue[sentence] += freq
				else:
					sentenceValue[sentence] = freq

	sumValues = 0
	for sentence in sentenceValue:
		sumValues += sentenceValue[sentence]

	# Average value of a sentence from the original text
	average = int(sumValues / len(sentenceValue))

	# Storing sentences into our summary.
	summary = ''
	for sentence in sentences:
		if (sentence in sentenceValue) and (sentenceValue[sentence] > (avgperc * average)):
			summary += " " + sentence
	st.info('the {} words of uploaded document is concised to {} words'.format(len(text),len(summary)))
	st.write("____")
	st.write(summary)

st.write("____")
st.write('made with :green_heart: to Indian Stock Investors')
#Custom CSS to remove header,footer, hamburger icon
hide_st_style = """
                <style>
                MainMenu {visibility: hidden;} 
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)

# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pdfplumber
import streamlit as st

text = ""
pdf_upload = st.file_uploader("upload Concal", type= ['pdf'])

if pdf_upload is not None:
	with pdfplumber.open(pdf_upload) as pdf:
		for page in pdf.pages :
			text += page.extract_text()

	#st.info(text)
	# Tokenizing the text
	stopWords = set(stopwords.words("english"))
	words = word_tokenize(text)

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
	sentences = sent_tokenize(text)
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
		if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
			summary += " " + sentence
	st.write("--")
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

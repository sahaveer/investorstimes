# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pdfplumber
import streamlit as st
import re

text = ""
texxt = ""
col1, col2,col3 = st.columns([0.6, 0.2,0.2])
with col1:
	pdf_upload = st.file_uploader("upload Concal", type= ['pdf'])
with col2:
	avgperc = st.number_input("Higher no., Lesser context",1.00,2.00,1.25,0.05)
with col3 :
	page_no = st.number_input("start analysing from page",1,3,2,1)
if pdf_upload is not None:
	name_file = pdf_upload.name.split('.')[0]
	with pdfplumber.open(pdf_upload) as pdf:
		for page in pdf.pages[page_no:] :
			text += page.extract_text()

	# Tokenizing the text
	stopWords = set(stopwords.words("english"))
	pattern = '(page|Page|PAGE)\s*\d+\s*(of|OF|Of)\s*\d+'
	date_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December|january|february|march|april|may|june|july|august|september|october|november|december|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s*\d{2}\s*(\,|\s)\s*\d{4}'
	moderator_pattern = r'(Thank you|Please go ahead|Moderator)'
	replace = ''
	texxt = re.sub(pattern, replace, text)
	texxt = re.sub(date_pattern, replace, texxt)
	texxt = re.sub(moderator_pattern,replace, texxt)
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
			summary += " " + sentence
	st.write("____")
	edited_txt = st.text_area("Edit further and generate ur own file",value=summary,height=500)
	st.info('the {} words of uploaded document is concised to {} words'.format(len(text),len(edited_txt)))
	st.download_button(label = "Download as txt",data= edited_txt,file_name=name_file+'.txt')
	#split_summary = sent_tokenize(summary)
	#for each in split_summary:
		#st.write(each)


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

from __future__ import print_function
import random
import re
import string
import csv
import time
import argparse


inputfilename = "bin/data/writing-1.txt"
outputMatrixFilename = "bin/data/markovMatrix.csv"
outputDictionaryFilename = "bin/data/markovDict.csv"

newGenerated = "bin/data/newWords.txt"

temperature = 0.00001

parser = argparse.ArgumentParser()

parser.add_argument("--build",dest="build",action='store_true')
parser.add_argument("--generate",dest="generate",action='store_true')
parser.set_defaults(generate=False,build=False)

args = parser.parse_args()

doMatrixBuild = args.build
generateNew = args.generate



def generate_markov_data(text):
	text = text.replace("\"","")
	text = text.replace("'","")
	text = text.replace(")","")
	text = text.replace("(","")
	wordsInOrder = text.split()
	allWords = list(set(wordsInOrder))
	print("Total input words: "+str(len(wordsInOrder)))
	print("Total unique words: "+str(len(allWords)))

	print("")
	print("GENERATING...")

	w,h = len(allWords),len(allWords)
	markovMatrix = [[temperature for x in range(w)] for y in range(h)] 
	
	for before, after in zip(wordsInOrder,wordsInOrder[1:]):
		markovMatrix[allWords.index(before)][allWords.index(after)] += 1


	for rowIndex, row in enumerate(markovMatrix):
		s = sum(row)
		markovMatrix[rowIndex] = [float(i)/s for i in row]

	print("SUCCESS. Writing files to disk...")
	with open(outputMatrixFilename,'wb') as f:
		writer = csv.writer(f,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
		for row in markovMatrix:
			writer.writerow(row)
	print("Finished writing matrix to disk. Writing dictionary: ")
	with open(outputDictionaryFilename,'wb') as f:
		writer = csv.writer(f,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
		for word in allWords:
			writer.writerow([word])

def generate_new_words(matrix,words,number):
	print("GENERATING TEXT...")
	print()
	lastWordIndex = random.randint(0,len(words)-1)
	with open(newGenerated,'ab') as f:
		#for i in range(1,number):
		sentence = ""
		endSentenceChars = ".!?"
		while True:
			#First, get the row we want to get probabilities from.
			row = matrix[lastWordIndex]
			#Second, get a random float between 0.0 and 1.0 (lets get lucky!)
			num = random.random()
			#Third, keep adding each column until we surpass num. This is the one that is great.
			#SO if num is zero, we will always get the first column, and if 1.0, we get the last.
			total = 0.0
			index = -1
			while num > total:
				index += 1
				total += row[index]
			#now we have our word! so update the last word index
			lastWordIndex = index
			word = words[lastWordIndex].strip()
			sentence = sentence + word + ' '
			print(sentence + ' ' + str(num))
			if(any(c in endSentenceChars for c in word)):
				time.sleep(15)
				sentence = ""

			# f.write(words[lastWordIndex].replace("\n","")+" ")

if(doMatrixBuild):
	text = ""
	with open(inputfilename) as f:
		text = f.read()

	generate_markov_data(text)

if(generateNew):
	print("Loading words from file...")
	words = []
	with open(outputDictionaryFilename,'rb') as f:
		reader = csv.reader(f,delimiter=' ',quotechar='|')
		for word in f:
			words.append(word.replace("\n",""))
	print("Loading matrix from file...")
	matrix = []
	with open(outputMatrixFilename,'rb') as f:
		reader = csv.reader(f,delimiter=' ',quotechar='|')
		for row in f:
			newRow = []
			oldRow = row.split()
			for item in oldRow:
				newRow.append(float(item))
			matrix.append(newRow)
	generate_new_words(matrix,words,100)







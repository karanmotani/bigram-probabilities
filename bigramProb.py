import csv
import json, pickle
import sys

def readData(fileName):
	data = []
	file = open(fileName, "r")

	for word in file.read().split():
		data.append(word)

	file.close()
	return data


def createBigram(data):
	listOfBigrams = []
	bigramCounts = {}
	unigramCounts = {}
	nbyn = {}

	for i in range(len(data)):
		if i < len(data) - 1:

			listOfBigrams.append((data[i], data[i + 1]))

			if (data[i], data[i+1]) in bigramCounts:
				bigramCounts[(data[i], data[i + 1])] += 1
			else:
				bigramCounts[(data[i], data[i + 1])] = 1

		if data[i] in unigramCounts:
			unigramCounts[data[i]] += 1
		else:
			unigramCounts[data[i]] = 1

	return listOfBigrams, unigramCounts, bigramCounts


# ------------------------------ Simple Bigram Model --------------------------------


def calcBigramProb(listOfBigrams, unigramCounts, bigramCounts):

	listOfProb = {}
	for bigram in listOfBigrams:
		word1 = bigram[0]
		word2 = bigram[1]
		
		listOfProb[bigram] = (bigramCounts.get(bigram))/(unigramCounts.get(word1))

	file = open('bigramProb.txt', 'w')
	file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

	for bigrams in listOfBigrams:
		file.write(str(bigrams) + ' : ' + str(bigramCounts[bigrams])
				   + ' : ' + str(listOfProb[bigrams]) + '\n')

	file.close()

	return listOfProb


# ------------------------------- Add One Smoothing ---------------------------------


def addOneSmothing(listOfBigrams, unigramCounts, bigramCounts):

	listOfProb = {}
	cStar = {}


	for bigram in listOfBigrams:
		word1 = bigram[0]
		word2 = bigram[1]
		listOfProb[bigram] = (bigramCounts.get(bigram) + 1)/(unigramCounts.get(word1) + len(unigramCounts))
		cStar[bigram] = (bigramCounts[bigram] + 1) * unigramCounts[word1] / (unigramCounts[word1] + len(unigramCounts))

	file = open('addOneSmoothing.txt', 'w')
	file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

	for bigrams in listOfBigrams:
		file.write(str(bigrams) + ' : ' + str(bigramCounts[bigrams])
				   + ' : ' + str(listOfProb[bigrams]) + '\n')

	file.close()

	return listOfProb, cStar


# ---------------------------- Good Turing Discounting ------------------------------


def goodTuringDiscounting(listOfBigrams, bigramCounts, totalNumberOfBigrams):
	listOfProb = {}
	bucket = {}
	bucketList = []
	cStar = {}
	pStar = {}
	listOfCounts = {}
	i = 1

	for bigram in bigramCounts.items():
		key = bigram[0]
		value = bigram[1]
		
		if not value in bucket:
			bucket[value] = 1
		else:
			bucket[value] += 1	

	# Sorted Bucket
	bucketList = sorted(bucket.items() , key=lambda t : t[0])
	zeroOccurenceProb = bucketList[0][1] / totalNumberOfBigrams
	lastItem = bucketList[len(bucketList)-1][0]

	for x in range(1, lastItem):
		if x not in bucket:
			bucket[x] = 0

	bucketList = sorted(bucket.items() , key=lambda t : t[0])
	lenBucketList = len(bucketList)

	for k, v in bucketList:

		if i < lenBucketList-1:
			if v == 0:
				cStar[k] = 0
				pStar[k] = 0

			else:
				cStar[k] = (i+1) * bucketList[i][1] / v
				pStar[k] = cStar[k] / totalNumberOfBigrams

		else:
			cStar[k] = 0
			pStar[k] = 0

		i += 1


	for bigram in listOfBigrams:
		listOfProb[bigram] = pStar.get(bigramCounts[bigram])
		listOfCounts[bigram] = cStar.get(bigramCounts[bigram])



	file = open('goodTuringDiscounting.txt', 'w')
	file.write('Bigram' + '\t\t\t' + 'Count' + '\t' + 'Probability' + '\n')

	for bigrams in listOfBigrams:
		file.write(str(bigrams) + ' : ' + str(bigramCounts[bigrams])
				   + ' : ' + str(listOfProb[bigrams]) + '\n')

	file.close()

	return listOfProb, zeroOccurenceProb, listOfCounts


if __name__ == '__main__':

	fileName = 'HW2_F17_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Unix.txt'
	data = readData(fileName)
	listOfBigrams, unigramCounts, bigramCounts = createBigram(data)
	bigramProb = calcBigramProb(listOfBigrams, unigramCounts, bigramCounts)
	bigramAddOne, addOneCstar = addOneSmothing(listOfBigrams, unigramCounts, bigramCounts)
	bigramGoodTuring, zeroOccurenceProb, goodTuringCstar = goodTuringDiscounting(listOfBigrams, bigramCounts, len(listOfBigrams))


	# ------------------------------------- Testing --------------------------------------

	input = sys.argv[1]
	# input = 'My name is Hardik'
	inputList = []
	output1 = open('bigramProb-OUTPUT.txt', 'w')
	output2 = open('addOneSmoothing-OUTPUT.txt', 'w')
	output3 = open('goodTuringDiscounting-OUTPUT.txt', 'w')
	outputProb1 = 1
	outputProb2 = 1
	outputProb3 = 1

	for i in range(len(input.split())-1):
		inputList.append((input.split()[i], input.split()[i+1]))

	print (inputList)


	# ------------------------------ Simple Bigram Model --------------------------------


	output1.write('Bigram\t\t\t\t' + 'Count\t\t\t\t' + 'Probability\n\n')
	for i in range(len(inputList)):
		if inputList[i] in bigramProb:
			output1.write(str(inputList[i]) + '\t\t' + str(bigramCounts[inputList[i]]) + '\t\t' + str(bigramProb[inputList[i]]) + '\n')
			outputProb1 *= bigramProb[inputList[i]]
		else:
			output1.write(str(inputList[i]) + '\t\t\t' + str(0) + '\t\t\t' + str(0) + '\n')
			outputProb1 *= 0

	output1.write('\n' + 'Probablility = ' + str(outputProb1))
	print ('Bigram Model: ', outputProb1)

	# ------------------------------- Add One Smoothing ---------------------------------


	output2.write('Bigram\t\t\t\t' + 'Count\t\t\t\t' + 'Probability\n\n')
	for i in range(len(inputList)):
		if inputList[i] in bigramAddOne:
			output2.write(str(inputList[i]) + '\t\t' + str(addOneCstar[inputList[i]]) + '\t\t' + str(bigramAddOne[inputList[i]]) + '\n')
			outputProb2 *= bigramAddOne[inputList[i]]
		else:
			if inputList[i][0] not in unigramCounts:
				unigramCounts[inputList[i][0]] = 1
			prob = (1) / (unigramCounts[inputList[i][0]] + len(unigramCounts))
			addOneCStar = 1 * unigramCounts[inputList[i][0]] / (unigramCounts[inputList[i][0]] + len(unigramCounts))
			outputProb2 *= prob
			output2.write(str(inputList[i]) + '\t' + str(addOneCStar) + '\t' + str(prob) + '\n')

	output2.write('\n' + 'Probablility = ' + str(outputProb2))
	print ('Add One: ', outputProb2)


	# ---------------------------- Good Turing Discounting ------------------------------


	output3.write('Bigram\t\t\t\t' + 'Count\t\t\t\t' + 'Probability\n\n')
	for i in range(len(inputList)):
		if inputList[i] in bigramGoodTuring:
			output3.write(str(inputList[i]) + '\t\t' + str(goodTuringCstar[inputList[i]]) + '\t\t' + str(bigramGoodTuring[inputList[i]]) + '\n')
			outputProb3 *= bigramGoodTuring[inputList[i]]
		else:
			output3.write(str(inputList[i]) + '\t\t\t' + str(0) + '\t\t\t' + str(zeroOccurenceProb) + '\n')
			outputProb3 *= zeroOccurenceProb

	output3.write('\n' + 'Probablility = ' + str(outputProb3))
	print ('Good Turing: ' , outputProb3)
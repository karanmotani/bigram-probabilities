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
	i = 0

	for i in range(len(data)):
		if i < len(data) - 1:
			bigramCounts[(data[i], data[i+1])] = 0
		unigramCounts[data[i]] = 0	
	
	for i in range(len(data)):
		if i < len(data) - 1:
			listOfBigrams.append((data[i], data[i+1]))
			bigramCounts[(data[i], data[i+1])] += 1
		unigramCounts[data[i]] += 1

	return listOfBigrams, unigramCounts, bigramCounts


def calcBigramProb(listOfBigrams, unigramCounts, bigramCounts):

	listOfProb = {}
	for bigram in listOfBigrams:
		word1 = bigram[0]
		word2 = bigram[1]
		
		listOfProb[bigram] = (bigramCounts.get(bigram))/(unigramCounts.get(word1))
	'''
	Sorted
	sortedListOfProb = sorted(listOfProb.items() , key=lambda t : t[1] ,  reverse=True)
	for k,v in sortedListOfProb:
		print(k , " : " , v)
	'''

	file = open('bigramProb.txt', 'w')

	for k, v in listOfProb.items():
		file.write(str(k) + ' : ' + str(v) + '\n')

	file.close()

	return listOfProb


def addOneSmothing(listOfBigrams, unigramCounts, bigramCounts):

	listOfProb = {}

	for bigram in listOfBigrams:
		
		word1 = bigram[0]
		word2 = bigram[1]
		
		listOfProb[bigram] = (bigramCounts.get(bigram) + 1)/(unigramCounts.get(word1) + len(unigramCounts))

	file = open('addOneSmoothing.txt', 'w')

	for k, v in listOfProb.items():
		file.write(str(k) + ' : ' + str(v) + '\n')

	file.close()

	return listOfProb


def goodTuringDiscounting(listOfBigrams, bigramCounts, totalNumberOfBigrams):

	listOfProb = {}
	bucket = {}
	bucketList = []
	cStar = {}
	pStar = {}
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

	lenBucketList = len(bucketList)

	for k, v in bucketList:

		if i < lenBucketList:
			
			temp = (i+1) * bucketList[i][1] / v
			if(temp < v):
				cStar[k] = (i+1) * bucketList[i][1] / v
				pStar[k] = cStar[k] / totalNumberOfBigrams
			
			else:
				cStar[k] = v
				pStar[k] = cStar[k] / totalNumberOfBigrams
			
			i += 1

	for bigram in listOfBigrams:
		listOfProb[bigram] = pStar.get(bigramCounts[bigram])

	file = open('goodTuringDiscounting.txt', 'w')
	
	for k, v in listOfProb.items():
		file.write(str(k) + ' : ' + str(v) + '\n')

	file.close()

	return listOfProb


if __name__ == '__main__':
	
	fileName = sys.argv[1]
	# fileName = 'HW2_F17_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Unix.txt'
	data = readData(fileName)

	listOfBigrams, unigramCounts, bigramCounts = createBigram(data)

	bigramProb = calcBigramProb(listOfBigrams, unigramCounts, bigramCounts)

	bigramProbAddOne = addOneSmothing(listOfBigrams, unigramCounts, bigramCounts)

	bigramGoodTuring = goodTuringDiscounting(listOfBigrams, bigramCounts, len(listOfBigrams))
	

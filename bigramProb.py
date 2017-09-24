import json, pickle

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
	i = 0
	for bigram in listOfBigrams:
		word1 = bigram[0]
		word2 = bigram[1]
		
		listOfProb[(word1, word2)] = (bigramCounts.get(bigram))/(unigramCounts.get(word1))
	'''
	Sorted
	sortedListOfProb = sorted(listOfProb.items() , key=lambda t : t[1] ,  reverse=True)
	for k,v in sortedListOfProb:
		print(k , " : " , v)
	'''
	
	# file = open('bigramProb.txt', 'w')
	# json.dump((listOfProb), file)
	# file.close()

	with open('bigramProb.txt', 'wb') as file:
		pickle.dump(listOfProb, file)

	return listOfProb


def addOneSmothing(listOfBigrams, unigramCounts, bigramCounts):

	listOfProb = {}

	for bigram in listOfBigrams:
		
		word1 = bigram[0]
		word2 = bigram[1]
		
		listOfProb[bigram] = (bigramCounts.get(bigram) + 1)/(unigramCounts.get(word1) + len(unigramCounts))

	# file = open('bigramProb.txt', 'w')
	# json.dump((listOfProb), file)
	# file.close()

	with open('addOneSmoothingProb.txt', 'wb') as file:
		pickle.dump(listOfProb, file)

	return listOfProb


if __name__ == '__main__':
	
	fileName = 'HW2_F17_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Unix.txt'
	data = readData(fileName)

	listOfBigrams, unigramCounts, bigramCounts = createBigram(data)

	bigramProb = calcBigramProb(listOfBigrams, unigramCounts, bigramCounts)

	bigramProbAddOne = addOneSmothing(listOfBigrams, unigramCounts, bigramCounts)

	# bigramGoodTuring = goodTuringDiscounting(listOfBigrams, unigramCounts, bigramCounts)


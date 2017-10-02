File to run: 
--> bigramProb.py

Minimum Python version to run the file: 3.5


--------------------------------------------------------------------------------------


HOW TO RUN:

--> On the command line interface, type the file name along with the python extension, 
	followed by the input string.
	Example: bigramProb.py "Input Test String"


--------------------------------------------------------------------------------------


OUTPUT:

--> The command line will display the input sentence probabilities for the 3 model, i.e.
	Bigram model without smoothing
	Bigram model with Add one smoothing
	Bigram model with Good Turing discounting

--> 6 files will be generated upon running the program.
	1 intermediate output file and 1 output file for each of the model
	
	=>  The intermediate output files are:

		bigramProb.txt - contains the Bigram, counts and probabilities of the bigrams 
						in the corpus for bigram model without smoothing

		addOneSmoothing.txt - contains the Bigram, counts and probabilities of the 
							bigrams in the corpus for bigram model with 
							Add one smoothing

		goodTuringDiscounting.txt - contains the Bigram, counts and probabilities of 
									the bigrams in the corpus for bigram model 
									with Good Turing Discounting


	=>  The output files are:

		bigramProb-OUTPUT.txt - contains the Bigram, their counts & probabilities, and 
								final probability of the sentence for bigram model 
								without smoothing

		addOneSmoothing-OUTPUT.txt - contains the Bigram, their counts & probabilities, 
									and final probability of the sentence for bigram model 
									with Add one smoothing

		goodTuringDiscounting-OUTPUT.txt - contains the Bigram, their counts & probabilities, 
											and final probability of the sentence for 
											bigram model with Good Turing Discounting


================================================================================================

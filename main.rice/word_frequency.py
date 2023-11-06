#This file defines the method that will count the frequency of words that appear in the cleaned transcript

import preprocessing;

def word_frequency(cleaned_list):
    """
    Counts the frequencies of the words that appear in the cleaned transcript.

    Inputs: 

    cleaned_list – A list representing the cleaned transcript

    Outputs:

    A list of tuples where the first element in the tuple are the words that appear in the cleaned transcript and the second element in 
    the tuple is the frequency with which they appear in cleaned transcript
    """


    frequency_output = {}


    for word in cleaned_list:
        
        if(word in frequency_output.keys()):
            frequency_output[word] += 1

        else:
            frequency_output[word] = 1

    
    # Sort the dictionary items by frequency in descending order
    sorted_items = sorted(frequency_output.items(), key=lambda item: item[1], reverse=True)
    return sorted_items



#Example Usage:
# transcript = preprocessing.pdf_to_final('main.rice/files/FOMC_2000_Meeting_Transcript.pdf', 'main.rice/files/sample_pre_process.txt', 'main.rice/files/sample_post_process.txt')
# print(word_frequency(transcript))
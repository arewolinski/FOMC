# This file is an automated way of finding the chairman's decision for the years of 1989 - 1998. I am using the heuristic of 
# Mr. Bernard speaking for the time right before voting happens as the decision since he always reads 
# the passages from the bluebook about the specific alternative selected before a roll call vote is cast.

import preprocessing
import rollcall

def chairmans_decision(path_to_pdf, txt_pre_process):
    """
    This function determines the chairman's recommendation for a specific FOMC transcript for the time period between 1989 - 1998.
    It uses the heuristic of Mr. Bernard speaking right before roll call in order to capture the chairman's recommendation.

    Inputs:
    path_to_pdf - A String representing a valid path to a pdf file of a FOMC transcript for the years between 1989 - 1998
    txt_pre_process - A String representing a valid path to a txt file where the contents of pdf will be processed to

    Outputs:
    A string representing the paragraph in the text which is the chairman's recommendation
    """

    preprocessing.pdf_to_txt(path_to_pdf, txt_pre_process)

    transcript_list = preprocessing.process_txt(txt_pre_process)

    output_string = ""

    word_idx = 0

    #Again, we are using a cool_down variable when we find an instance of voting that requires us to be 200 words past when 
    #voting first happened in order to have another vote
    cool_down = 0

    #We never need a variable for the specific that we are looking at so underbar is short-hand for indicating we don't need it 
    for _ in transcript_list:

        if((rollcall.yes_no_count_last_30(word_idx, transcript_list)) > 7 and cool_down > 200):
            print("An instance of voting happened")

            #Adding the parsed transcript as well as a couple new lines for spacing purposes in case 
            #clean_voting_parse is triggered again since multiple voting decisions were made
            output_string += clean_recommendation_parse(word_idx, transcript_list) + "\n" + "\n"

            cool_down = 0

        word_idx += 1

        cool_down += 1


    return output_string

    
def clean_recommendation_parse(word_idx, transcript_list):
        """
        Outputs the paragraph from Mr. Bernard about the Chairman's recommendation right before voting happens.

        Inputs: 
        word_idx - An int representing the specific index within transcript_list where yes_no_count_last_30 was greater than 7 
        instances of "yes" and "no". This will usually give an index for the word in the middle of the voting.

        transcript_list - A list where each index is a String where the indices in order make up the entire FOMC transcript

        Output:
        A String representing the chairman's recommendation
        """

        output = ""

        #Making a bigger interval since sometimes there will be a lot said between Mr. Bernard's reading from the 
        #BlueBook and the roll call vote 
        lower_bound_idx = word_idx - 1000

        if (lower_bound_idx < 0):
            return "error: need to adjust algorithm to slice at a greater index"

        intermediate_parse = transcript_list[lower_bound_idx : word_idx]


        previous_word = ""

        #The index at which Mr. Bernard starts his recount of the recommendation
        start_speech_idx = -1

        #The index at which Mr. Bernard ends his recount of the recommendation
        end_speech_idx = -1

        #The current index starts at the lower bound index but gets incremented within the for loop in order to follow the iteration
        current_idx = lower_bound_idx

        #This iteration will go through and mark the index at which Mr. Bernard appears right before voting 
        # (making sure that he talks for more than 50 words since these could be trivial comments in this case)
        for word in intermediate_parse:

            #The not statement filters out the case where Mr. Bernard is called for voting
            if (previous_word == "BERNARD" and word != "Chairman" and check_length_of_speech(current_idx, transcript_list)):

                start_speech_idx = current_idx
                end_speech_idx = find_end_speech_index(start_speech_idx, transcript_list)
            
            current_idx += 1
            previous_word = word

        if(start_speech_idx == -1 and end_speech_idx == -1):
             return "error: this is a check for debugging purposes"

        optimal_slice = transcript_list[start_speech_idx : (end_speech_idx + 1)]

        #Taking optimal_slice, which is a list of strings, and turning it back into its paragraph form as a string
        for word in optimal_slice:
            output += word + " "

        return output


def check_length_of_speech(bernard_idx, transcript_list):
        """
        Checks that Mr. Bernard speaks for more than 30 words in order to qualify as him giving his recommendation.
        I use this heuristic since he sometimes says a sentence or two between his recommendation and him calling the vote,
        but these are usually short sentences that can be weeded out by word count.

        Inputs:
        bernard_idx - An int representing the index at which Mr. Bernard is saying his first word (the index right after
        BERNARD) 

        transcript_list - A list of Strings where the concatenated strings yield an FOMC transcript from 1989 - 1998
        """

        bernard_count = 0

        #Starting word is at the bernard_idx (which is the first word Mr. Bernard says)
        current_word = transcript_list[bernard_idx]

        break_word_list = ["CHAIRMAN", "VICE", "MR", "MS", "MRS"]

        #Iterating until we hit a word in break_word_list, which indicates when a new speaker starts
        while (current_word not in break_word_list):

            bernard_count += 1
            current_word = transcript_list[bernard_idx + bernard_count]

        if (bernard_count > 30):
            return True
        else:
            return False
        

def find_end_speech_index(start_speech_index, transcript_list):
        """
        This function finds the end index anytime Mr. Bernard is speaking by looking at when the next instance of Mr, Ms, Mrs,
        Chairman, or Vice appears since these words all indicate when someone is speaking. 

        Inputs:

        start_speech_index - An int representing the index at which Mr. Bernard is starting to speak
        transcript_list - A list of strings where the concatenated strings yield an FOMC transcript

        Outputs:
        An int representing the index at which Mr. Bernard is done speaking
        """

        #Originally set the end index to the start index (we will be incrememnting end_idx and we
        #need it to start at the index representing the beginning of Mr. Bernard's speech)
        end_idx = start_speech_index

        #Again, same break words as the previous function
        break_word_list = ["CHAIRMAN", "VICE", "MR", "MS", "MRS"]

        #This variable, current_word, represents the current word we are analyzing within Mr. Bernard's speech 
        current_word = transcript_list[start_speech_index]

        #We go until we hit a break word found in break_word_list which indicates that Mr. Bernard is done speaking
        while (current_word not in break_word_list):

            end_idx += 1
            current_word = transcript_list[end_idx]

        return end_idx    



#Example Usage:
print(chairmans_decision('main.rice/files/Transcripts Raw pdf/8_1993_transcript.pdf', 'main.rice/files/sample_pre_process.txt'))   



































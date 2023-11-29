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
    for word in transcript_list:

        if(rollcall.yes_no_count_last_30(word_idx, transcript_list)) > 7:

            #Adding the parsed transcript as well as a couple new lines for spacing purposes in case 
            #clean_voting_parse is triggered again since multiple voting decisions were made
            output_string += clean_voting_parse(word_idx, transcript_list) + "\n" + "\n"



        word_idx += 1

    
    def clean_voting_parse(word_idx, transcript_list):
        """
        """






















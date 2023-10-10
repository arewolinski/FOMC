#This file is for determining the results of the roll call 

import preprocessing


def results_of_roll_call(path_to_pdf, txt_pre_process):
    """
    This function determines the result of "calling the roll" within the transcript. Essentially,
    it determines who voted yes or no on the agenda. Outputs the paragraph of text that is within the 
    roll call voting as a String.

    Inputs: 

    path_to_pdf - A valid path to a PDF file that contains FOMC transcript data
    txt_pre_process - A valid path to a txt file where the PDF contents will be processed to

    Returns: A string that is the paragraph resulted from the roll call voting.
    """
    print("instance 1")
    preprocessing.pdf_to_txt(path_to_pdf, txt_pre_process)
    print("instance 2")
    transcript_list = preprocessing.process_txt(txt_pre_process)

    output_string = "empty"

    #Need to be after the start point and before the end point in order to record in output_string
    after_start_point = False
    before_end_point = True

    #Variables for keeping track of previous words 
    last_word = ""
    two_ago_word = ""


    for word in transcript_list:

        #Checking if "Call the roll" was said in order to check if we have reached the roll call point yet
        if(two_ago_word == "Call" and last_word == "the" and word == "roll"):
            print("instance 3")
            after_start_point = True
        
        #Checks if we pass the roll call portion in which case we are not before the end point anymore
        if(after_start_point and word == "CHAIRMAN"):
            print("instance 4")
            before_end_point = False

        #If we are after the start point and before the end point, we want to add everything to output_string
        if(after_start_point and before_end_point):
            output_string += word

        #Creating copies of the strings so we don't run into reference issues
        two_ago_word = last_word[:]
        last_word = word[:]
    
    return output_string

#Example usage:
path_to_pdf = 'main.rice/files/FOMC_2000_Meeting_Transcript.pdf'
txt_pre_process = 'main.rice/files/sample_pre_process.txt'
print(results_of_roll_call(path_to_pdf, txt_pre_process))
        










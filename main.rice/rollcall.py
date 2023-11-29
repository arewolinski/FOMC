#This file is for determining the results of the roll call 

import preprocessing


def roll_call(path_to_pdf, txt_pre_process):
    """
    This function determines the result of roll call on voting items. It does so by determining if 
    more than 7 "Yes" or "No" quotes have been said in the last 30 words, which is the indication I am
    using to determine if voting is taking place. Using other indications such as "Call the roll." are not reliable
    or consistent throughout transcript data. Relies on two helper methods – one to count the instances
    of "Yes" and "No" and one to clean the data once we have identified the general area where the voting takes place.
    

    Inputs:

    path_to_pdf - A String which represents a valid path to a pdf file containing a FOMC transcript
    txt_pre_process - A String representing a valid path to a txt file where the contents of pdf will be processed to

    Outputs: 

    A String representing the chunk of the transcript that encapsulates the voting process 
    """


    preprocessing.pdf_to_txt(path_to_pdf, txt_pre_process)

    transcript_list = preprocessing.process_txt(txt_pre_process)

    output_string = ""

    #Cool down variable ensures that the same voting process is not output 30 times as we traverse through the transcript
    #one word at a time, causing yes_no_count_last_30 to be greater than 7 multiple times for the same voting process
    cool_down = 0

    

    for word_count in range(len(transcript_list)):

        if(yes_no_count_last_30(word_count, transcript_list) > 7):

            #I create a 50 word cool down, meaning that two votes cannot take place within 50 words of each other
            if(cool_down > 50):
                output_string += clean_voting_parse(word_count, transcript_list) + "\n" + "\n"
                cool_down = 0
            
        cool_down += 1
    


    if(not output_string == ""):
        return output_string
    

    return "error: voting not found"




def yes_no_count_last_30(word_count, transcript_list):
    """
    Counts instances of the words "Yes" and "No" in the last 30 words. Slices the existing transcript
    list 30 words before word_count.

    Inputs:

    word_count - An int representing about what index the voting occurs (specifically, when yes_no_count_last_30 > 7)
    transcript_list - A list of Strings, where each inner String is a word within the FOMC transcript

    Outputs:

    yes_no_count - An int representing the number of "Yes" and "No" that have appeared in the last num words
    """

    start_idx = 0
    yes_no_count = 0

    #Have to check our lower bound so that we don't slice out of bounds
    if (word_count > 30):

        start_idx = word_count - 30


    #Slice to get the appropriate sub list that encompasses the last 30 words
    parsed_transcript_list = transcript_list[start_idx : word_count + 1]


    for word in parsed_transcript_list:

        #I include capitalized and uncapitalized instances of yes and no to be thorough
        if (word == "Yes" or word == "No" or word == "yes" or word == "no"):

            yes_no_count += 1

    

    return yes_no_count


def clean_voting_parse(word_count, transcript_list):
    """
    Reduces a general area where voting happens to an exact record of voting that excludes any 
    surrounding text that occurs around the voting. I create a large boundary (50 words before yes_no_count triggers
    and 20 words after) so that we do not miss any of the voting within our portion of the transcript. Checks for the words
    "Chairman" and "Yes" in order to start copying the Strings over to output_string and stops copying the Strings over when
    CHAIRMAN appears (the chairman always speaks right after voting has finished).

    Inputs:

    word_count - An int representing about what index the voting occurs (specifically, when yes_no_count_last_30 > 7)
    transcript_list - A list of Strings, where each inner String is a word within the FOMC transcript

    Outputs:

    output_string - A string that is the paragraph resulted from the roll call voting.


    """


    output_string = ""

    start_idx = 0

    #Creating lower boundary (giving 50 words to be safe)
    if (word_count > 50):
        start_idx = word_count - 50


    #Creating upper boundary (giving 20 words to be safe)
    if (len(transcript_list) - word_count > 20):
        word_count += 20

    parsed_transcript_list = transcript_list[start_idx : word_count]


    #Need to be after the start point and before the end point in order to record in output_string
    after_start_point = False
    before_end_point = True

    #These keep track of the last two words
    two_ago_word = ""
    last_word = ""


    #Looping through our parsed transcript which has some extraneous words on either side of the voting in order to refine output_string
    for word in parsed_transcript_list:


        #One example that trigger this boolean is "Chairman Volcker Yes" (name of the chairman changes from transcript to transcript)
        if((not after_start_point) and two_ago_word == "Chairman" and (word == "Yes" or word == "yes" or word == "no" or word == "No")):
            after_start_point = True
            output_string += two_ago_word + " " + last_word + " "


        #We end when the chairman speaks again, marked by the instance of "CHAIRMAN"
        if(after_start_point and word == "CHAIRMAN"):
            before_end_point = False

        #If in our interval of voting, we want to copy the transcript over to output_string
        if(after_start_point and before_end_point):

            if(word == "Yes" or word == "yes" or word == "No" or word == "no"):
                output_string += word + "\n"
            else:
                output_string += word + " "
        

        #Update these relative variables
        two_ago_word = last_word[:]
        last_word = word[:]

        

    return output_string


#Example usage:
# path_to_pdf = 'main.rice/files/Transcripts Raw pdf/1_1989_transcript.pdf'
# txt_pre_process = 'main.rice/files/sample_pre_process.txt'
# print(roll_call(path_to_pdf, txt_pre_process))


#Example usage in bulk:
# for num in range(10):
#     path_to_pdf = f'main.rice/files/Transcripts Raw pdf/1_199{num}_transcript.pdf'
#     txt_pre_process = 'main.rice/files/sample_pre_process.txt'
#     print(roll_call(path_to_pdf, txt_pre_process))
















        










#This is the file where all of the pre-processing for the transcripts will be done. Will add more files
#and update structure as necessary. Refer to API for a more thorough explanation of what everything does


import pdfplumber
import spacy


def pdf_to_txt(path_to_pdf, path_to_txt):
    """
    Takes in a String representing a path to a pdf file and a String representing a path to a txt file, writing the contents 
    of the PDF file to the txt file. If the txt file is not empty, this function will essentially remove everything that was 
    previously in the file and write over it with the new content found in the PDF.

    Inputs: 
    path_to_pdf - A String representing the path to a PDF file (the FOMC meeting transcripts in our case)
    path_to_txt - A String representing the path to a TXt file 

    Returns: Nothing; this function is void.

    """


    try:
        text = ""

        #Utilizing pdfplumber library which is more accurate than PyPDF2 library
        with pdfplumber.open(path_to_pdf) as pdf:
            for page in pdf.pages:
                text += page.extract_text()

        
        with open(path_to_txt, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
    
        #Useful print statements for debugging
        print(f"PDF file '{path_to_pdf}' successfully converted to '{path_to_txt}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage:
pdf_to_txt('main.rice/files/FOMC_2000_Meeting_Transcript.pdf', 'main.rice/files/sample_pre_process.txt')


def process_txt(path_to_txt):
    """
    Takes in a txt file path and returns a list of Strings which represents the words after they have been split 
    at spaces. Note that the way that we are splitting the words already gets rid of the spaces in the words for us.

    Inputs: 

    text_file_path - A String representing a path to a txt file.

    Returns: A list of Strings representing the words within the txt file after they have been split at spaces.

    """


    try:
        words_without_spaces = []

        #debugging purpose
        #line_check = 0 

        # Open the text file for reading line by line
        with open(path_to_txt, 'r') as file:
            for line in file:

                # Splits the line into a list of strings separated by spaces
                words = line.split()

                for word in words:

                    #debugging purpose
                    #line_check += 1 
                    words_without_spaces.append(word)

                    #debuggin purpose
                    #print(f"Processed word: {word} & line: {line_check}") 


        return words_without_spaces
    except FileNotFoundError:
        print(f"File not found: {path_to_txt}")
        return []

# Example usage:
# result = process_txt("main.rice/files/sample_pre_process.txt")
# print(result)

def remove_punctuation(transcript_list, punctuation):
    """
    Takes in a list of Strings representing the FOMC transcript split at spaces and removes all punctuation in the variable
    named punctuation from the Strings within transcript_list.

    Inputs:

    transcript_list - A list of strings where each string represents a word within the FOMC transcript
    punctuation - A tuple of strings where each string represents a punctuation mark we want removed from the transcript

    Returns: A list of strings free of punctuation

    """

    new_transcript_list = []

    for word in transcript_list:
        intermediate_word = ''
        for character in word:
            if character not in punctuation:
                intermediate_word += character

        
        if len(intermediate_word) > 0:
            new_transcript_list.append(intermediate_word)

    
    return new_transcript_list


# Example usage:
# transcript_list = process_txt("main.rice/files/sample.txt")
# punctuation = (".", ",","!","/","?")
# print(remove_punctuation(transcript_list, punctuation))

def remove_preliminary_text(transcript_list):
    """
    Removes preliminary text, which is all text before the converstaion between members starts, by removing all text that
    appears before the word CHAIRMAN appears in the transcript. In all of the transcripts I have looked at, the meaningful conversation
    starts when the CHAIRMAN first speaks. Thus, we can remove all text from the transcript before the first instance of this word.

    Inputs: 

    transcript_list - A list of strings where each string represents a word within the FOMC transcript

    Returns: A transcript_list that is free from preliminary procedures 
    """
    can_start = False
    new_transcript_list = []

    for word in transcript_list:

        if (word == "CHAIRMAN"):
            can_start = True

        if can_start:
            new_transcript_list.append(word)


    return new_transcript_list

# Example usage:
# transcript_list = process_txt("main.rice/files/sample_pre_process.txt")
# print(remove_preliminary_text(transcript_list))


def convert_all_words_to_lowercase(transcript_list):
    """
    Converts all the words within transcript_list EXCEPT for words that are all caps since these all caps words are acryonyms
    that don't make sense lower case or are referencing who is speaking which is fine to be kept all caps

    Inputs:
    transcript_list - A list of strings where each individual string represents a word within the FOMC transcript

    Returns: A list of strings that are lowercased except if the word is all caps
    """

    new_transcript_list = []

    for word in transcript_list:
        if(not word.isupper()):
            new_transcript_list.append(word.lower())
        else:
            new_transcript_list.append(word)

    return new_transcript_list


# Example usage:
# transcript_list = process_txt("main.rice/files/sample_pre_process.txt")
# print(convert_all_words_to_lowercase(transcript_list))

def remove_stopwords(transcript_list, stopwords):
    """
    Removes all words within stopwords from the transcript_list

    Inputs: 
    
    transcript_list - A list of strings representing the words within the FOMC transcripts
    stopwords - A tuple of strings representing the stopwords we want removed form the transcript

    Returns - The transcript_list free from stopwords

    """

    new_transcript_list = []

    for word in transcript_list:
        if(word not in stopwords):
            new_transcript_list.append(word)


    return new_transcript_list

# Example usage:
# transcript_list = process_txt("main.rice/files/sample_pre_process.txt")
# stopwords = ("of", "the", "and", "a")
# print(remove_stopwords(transcript_list, stopwords))

def root_cutter(transcript_list):
    """
    Note: Need to discuss this function since I have tried several different libraries and none of them
    operate very well.

    Takes the transcript list and converts all tenses of the same word to the same root word 
    (e.g. “prefers” and “preferential” both become “prefer”). I utilize the spaCy library which reduces words
    down to their original tense. Note that sometimes the word changes as a result of the lemmantization process
    that spaCy incorporates (e.g. better --> good). 

    Inputs:

    transcript_list - A list of strings where each inner string represents a word within the FOMC transcript

    Returns: A transcript_list that has all similar words cut down to the same common word.
    """

    # Initialize the spaCy English language model
    nlp = spacy.load("en_core_web_sm")

    stemmed_transcript = []

    # Apply spaCy stemming to each word in the transcript_list
    for word in transcript_list:
        doc = nlp(word)
        for token in doc:
            stemmed_transcript.append(token.lemma_)

    return stemmed_transcript



# Example usage:
# transcript_list = process_txt("main.rice/files/sample_pre_process.txt")
# print(transcript_list)
# transcript_list2 = remove_punctuation(transcript_list, (",", "."))
# print(root_cutter(transcript_list2))




def create_txt(transcript_list, output_file):
    """
    Takes a list of Strings and outputs a txt file where there is a space between each 
    String in transcript_list. Essentially, if you were to call create_txt(process_txt(txt_file))
    the output would be equivalent to the original input (just the spacing would not be the same). 
    """

    try:
        # Open the output file in write mode
        with open(output_file, 'w') as file:
            # Join the strings in the list with spaces and write them to the file
            file.write(' '.join(transcript_list))
        print(f'Successfully wrote the strings to {output_file}')
    except Exception as e:
        print(f'Error: {e}')

# Example usage:
# transcript_list = process_txt("main.rice/files/sample_pre_process.txt")
# output_file = "main.rice/files/sample_post_process.txt"
# create_txt(transcript_list, output_file)






def pdf_to_final(pdf_file_path, txt_pre_process, txt_post_process):

    """
    Takes in a PDF file path and uses all of the above functions to turn this PDF file path into a completely pre-processed transcript.

    Inputs: A String representing the pdfFilePath

    Outputs: A list of Strings that represents the entirely pre-processed transcript
    """

    punctuation = [".", ",", "!", "@", "?", "/", "$", "#", "%", "&", "*", "(", ")","<", ">","[", "]", "{", "}", "+", "=", "-", "`", "~"]
    stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him",
                 "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
                 "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
                 "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                 "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
                 "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
                 "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some",
                 "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "can", "will", "just", "should", "now"]


    pdf_to_txt(pdf_file_path, txt_pre_process)
    transcript_list = process_txt(txt_pre_process)
    transcript_list = remove_punctuation(transcript_list, punctuation)
    transcript_list = remove_preliminary_text(transcript_list)
    transcript_list = convert_all_words_to_lowercase(transcript_list)
    transcript_list = remove_stopwords(transcript_list, stopwords)
    #transcript_list = root_cutter(transcript_list)
    create_txt(transcript_list, txt_post_process)

    return transcript_list

# Example usage:
# print(pdf_to_final('main.rice/files/FOMC_2000_Meeting_Transcript.pdf', 'main.rice/files/sample_pre_process.txt', 'main.rice/files/sample_post_process.txt'))







    
    
    









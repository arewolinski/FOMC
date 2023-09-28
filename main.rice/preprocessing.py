#This is the file where all of the pre-processing for the transcripts will be done. Will add more files
#and update structure as necessary. Refer to API for a more thorough explanation of what everything does


import PyPDF2

def pdf_to_text(path_to_pdf, path_to_txt):
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
        pdf_reader = PyPDF2.PdfReader(path_to_pdf)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        with open(path_to_txt, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
    
        print(f"PDF file '{path_to_pdf}' successfully converted to '{path_to_txt}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage:
#pdf_to_text('main.rice/files/FOMC_2000_Meeting_Transcript.pdf', 'main.rice/files/sample.txt')


def load_transcripts(textFilePath):

    """
    Takes in a txt file path and returns a list of Strings which represents the words after they have been split 
    at spaces. Notes that this function does not get rid of the spaces; that is for a later function

    Inputs: 

    """
    pass


def pdf_to_final(pdfFilePath):

    """
    Takes in a PDF file path and uses all of the above functions to turn this PDF file path into a completely pre-processed transcript.

    Inputs: A String representing the pdfFilePath

    Outputs: A list of Strings that represents the entirely pre-processed transcript
    """
    pass









#main program code goes here
from pypdf import PdfReader
import summarize

# Replace PDF name with desired document
file = "64292321.pdf"
reader = PdfReader(file)
number_of_pages = len(reader.pages)

final_summary = ["Multi-Point inspection complete"]
pdf_text = []
new_text = []
red = []
yellow = []
x = ""

# Grab all the text from the pdf
for page_num in range(number_of_pages):
    page = reader.pages[page_num]
    text = page.extract_text()
    pdf_text.append(text)

# split up pdf text to new lines
for text in pdf_text:
    string = text.split("\n")
    for line in string:
        new_text.append(line)

# Split up text between red and yellow
for line in new_text:
    if line == "Requires Immediate Attention":
        x = "red"
        continue
    elif line == "May Require Future Attention":
        x = "yellow"
        continue
    elif line == "Full Inspection Results":
        break
    if x == "red":
        red.append(line)
    elif x == "yellow":
        yellow.append(line)



# Print the extracted text (or process it further)
for text in final_summary:
    #print(text)
    pass

summarize.summarized(red, yellow)
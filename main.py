#main program code goes here
from pypdf import PdfReader
import functions_page
import sys

# Replace PDF name with desired document
print("Which RO would you like to summarize?")
inp = input(">> ")
file = inp + ".pdf"
try:
    reader = PdfReader(file)
except:
    print("File does not exist")
    sys.exit()


red, yellow = functions_page.get_file(reader)
final_summary = functions_page.summarized(red, yellow)
functions_page.get_brakes()
functions_page.get_tires()
final_summary.append("No other issues at this time\n")


# Print the extracted text (or process it further)
for text in final_summary:
    print(text)
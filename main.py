#main program code goes here
import functions_page

# Replace PDF name with desired document
print("Which RO would you like to summarize?")
inp = input(">> ")
file = inp + ".pdf"


functions_page.get_file(file)
final_summary = functions_page.summarized(red, yellow)
functions_page.get_brakes()
functions_page.get_tires()
final_summary.append("No other issues at this time\n")


# Print the extracted text (or process it further)
for text in final_summary:
    print(text)
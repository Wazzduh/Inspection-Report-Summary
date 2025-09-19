import functools
from pypdf import PdfReader
import sys

final_summary = []
pdf_text = []
new_text = []
red = []
yellow = []
characters = ["-", "(", ")", "|"]
brake_measurements = ["1mm", "2mm", "3mm", "4mm", "5mm", "6mm", "7mm", "8mm"]
tire_measurements = ["1/32", "2/32", "3/32", "4/32", "5/32", "6/32", "7/32", "8/32", "9/32", "10/32"]
headers = ["Engine Oil Level & Condition/Leaks", "Cabin Air Filter", "Engine Air Filter", "Engine Air Filter Cabin Air Filter", 
            "Front Brake Pads/Rotors", "Rear Brake Pads/Rotors", "Windshield Wiper/Washer Operation", "Brake Fluid Level & Condition/Leaks", "Battery", "Front Lights", "Rear Lights",
            "Instruments and Gauges/Warning Lights", "Seat Belt Inspection", "Heating & AC / Performance / Hoses /", "Brake Pedal Operation", "Parking Brake Operation", 
            "Electrical Inspection (Horns, Signals,", "Glass/Power Window Operation", "Mirror Operation-Side/Auto-Dimming", "Door Latches/Power Lock Operation", 
            "Master Cylinder/Brake Lines", "Transmission Fluid Level &", "Accessory Drive Belts", "Socks/Struts and Suspension", "Steering System / Rack / Pump / Lines", 
            "Exhaust System (Leaks, Damage,", "Transmission / Linkages / Clutch (if", "Engine / Transmission Mounts", "Front/Rear Tires", "Full Inspection Results"]


def get_file(reader):
    x = ""
    number_of_pages = len(reader.pages)

    for page_num in range(number_of_pages):
        page = reader.pages[page_num]
        text = page.extract_text()
        pdf_text.append(text)

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
    return red, yellow
    

def summarized(red, yellow):
    final = ["\nMulti-Point Inspection complete"]
    i = 0

    # Finalize red items
    for i in range(len(red)):
        if len(red) < 1:
            break
        line = red[i]
        if red[i] in headers:
            if line == "Engine Oil Level & Condition/Leaks":
                for word in red[i+1].split(" "):
                    word = word.lower()
                    if word == "leak":
                        final.append("Oil leak from engine")
                        break
                else:
                    try:
                        if red[i+2] not in headers:
                            final.append(convert_line(red[i+1] + " " + red[i+2]))
                            break
                    except: 
                        final.append(convert_line(red[i+1]))
                        break
            elif line == "Cabin Air Filter":
                final.append("Cabin filter in the red")
            elif line == "Engine Air Filter":
                final.append("Engine air filter in the red")
            elif line == "Engine Air Filter Cabin Air Filter":
                final.append("Both air filters in the red")
            elif line == "Front Brake Pads/Rotors":
                measurement = ""
                for word in red[i+1].split(" "):
                    if word in brake_measurements:
                        measurement = word
                        break
                final.append(f"Front brakes @ {measurement}")
            elif line == "Rear Brake Pads/Rotors":
                for word in red[i+1].split(" "):
                    if word in brake_measurements:
                        measurement = word
                        break
                final.append(f"Rear brakes @ {measurement}")
            elif line == "Battery":
                final.append("Battery tested bad")
            elif line == "Front Lights":
                try:
                    if red[i+2] not in headers:
                        final.append(convert_line(red[i+1] + " " + red[i+2]))
                except: 
                    final.append(convert_line(red[i+1]))
            elif line == "Rear Lights":
                try:
                    if red[i+2] not in headers:
                        final.append(convert_line(red[i+1] + " " + red[i+2]))
                except: 
                    final.append(convert_line(red[i+1]))
            elif line == "Windshield Wiper/Washer Operation":
                final.append(convert_line(red[i+1]))
            elif line == "Brake Fluid Level & Condition/Leaks":
                final.append("Brake fluid discolored. Recommend brake flush")
            elif line == "Front/Rear Tires":
                try:
                    if red[i+2] not in headers:
                        final.append("Tires: " + convert_line(red[i+1] + " " + convert_line(red[i+2])))
                except: 
                    final.append("Tires: " + convert_line(red[i+1]))
            else:
                try:
                    if red[i+2] not in headers:
                        final.append(convert_line(red[i+1] + " " + red[i+2]))
                except: 
                    final.append(convert_line(red[i+1]))

        i += 1


    
    # Finalize red items
    for i in range(len(yellow)):
        if len(yellow) < 1:
            break
        line = yellow[i]
        if line in headers:
            if line == "Engine Oil Level & Condition/Leaks":
                for word in yellow[i+1].split(" "):
                    word = word.lower()
                    if word == "seep":
                        final.append("Oil seep from engine")
                        break
                    else:
                        try:
                            if yellow[i+2] not in headers:
                                final.append(convert_line(yellow[i+1] + " " + yellow[i+2]))
                        except: 
                            final.append(convert_line(yellow[i+1]))
            elif line == "Cabin Air Filter":
                final.append("Cabin filter in the yellow")
            elif line == "Engine Air Filter":
                final.append("Engine air filter in the yellow")
            elif line == "Engine Air Filter Cabin Air Filter":
                final.append("Both air filters in the yellow")
            elif line == "Front Brake Pads/Rotors":
                measurement = ""
                for word in yellow[i+1].split(" "):
                    if word in brake_measurements:
                        measurement = word
                        break
                final.append(f"Front brakes @ {measurement}")
            elif line == "Rear Brake Pads/Rotors":
                for word in yellow[i+1].split(" "):
                    if word in brake_measurements:
                        measurement = word
                        break
                final.append(f"Rear brakes @ {measurement}")
            elif line == "Battery":
                final.append("Battery needs recharge and retest")
            elif line == "Front Lights":
                try:
                    if yellow[i+2] not in headers:
                        final.append(convert_line(yellow[i+1] + " " + yellow[i+2]))
                except: 
                    final.append(convert_line(yellow[i+1]))
            elif line == "Rear Lights":
                try:
                    if yellow[i+2] not in headers:
                        final.append(convert_line(yellow[i+1] + " " + yellow[i+2]))
                except: 
                    final.append(convert_line(yellow[i+1]))
            elif line == "Windshield Wiper/Washer Operation":
                final.append(convert_line(yellow[i+1]))
            elif line == "Brake Fluid Level & Condition/Leaks":
                final.append("Brake fluid slightly discolored")
            elif line == "Front/Rear Tires":
                try:
                    if yellow[i+2] not in headers:
                        final.append("Tires: " + convert_line(yellow[i+1] + " " + convert_line(yellow[i+2])))
                except: 
                    final.append("Tires: " + convert_line(yellow[i+1]))
            else:
                try:
                    if yellow[i+2] not in headers:
                        final.append(convert_line(yellow[i+1] + " " + yellow[i+2]))
                except: 
                    final.append(convert_line(yellow[i+1]))
        i += 1
    
    return final
            
def convert_line(line):
    line = line.split(" ")
    if len(line) > 0 and line[0] == "Notes:":
        return " ".join(line[1:])
    return " ".join(line)

def get_brakes():
    for i in range(len(new_text)):
        if new_text[i] == "Front Brake Pads/Rotors":
            measurement = ""
            for word in new_text[i+1].split(" "):
                if word in brake_measurements:
                    measurement = word
                    break
            if f"Front brakes @ {measurement}" not in final_summary:
                final_summary.append(f"Front brakes @ {measurement}")
        elif new_text[i] == "Rear Brake Pads/Rotors":
            for word in new_text[i+1].split(" "):
                if word in brake_measurements:
                    measurement = word
                    break
            if f"Rear brakes @ {measurement}" not in final_summary:
                final_summary.append(f"Rear brakes @ {measurement}")
        i += 1


def get_tires():
    for i in range(len(new_text)):
        if new_text[i] == "Front/Rear Tires":
            try:
                if new_text[i+2] not in headers:
                    keyword = "Tires: " + convert_line(new_text[i+1] + " " + convert_line(new_text[i+2]))
            except: 
                keyword = "Tires: " + convert_line(new_text[i+1])
            if keyword not in final_summary:
                final_summary.append("Tires: " + convert_line(new_text[i+1]))
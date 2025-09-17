

def summarized(red, yellow):
    final = ["Multi-Point Inspection complete"]
    for line in red:
        line = line.split(" ")
        for word in line:
            word = word.lower()
            if word == "rear":
                print(" ".join(line))
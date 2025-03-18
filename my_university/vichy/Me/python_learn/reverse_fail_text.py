with open("C:\\Users\\79125\\Downloads\\dataset_24465_4.txt", "r") as inp, open(
    "revers_text.txt", "w"
) as out:
    text = []
    for line in inp:
        line = line.strip()
        text.append(line)
    for x in text[::-1]:
        out.write(x + "\n")

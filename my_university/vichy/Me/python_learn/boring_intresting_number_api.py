import requests

with open("C:\\Users\\79125\\Downloads\\dataset_24476_3.txt", "r") as inp, open(
    "int_bor_numb.txt", "w"
) as out:
    for line in inp:
        number = line.strip()
        template = "http://numbersapi.com/{}/math?json"
        res = requests.get(template.format(number))
        data = res.json()
        if data["found"]:
            out.write("Interesting\n")
        else:
            out.write("Boring\n")

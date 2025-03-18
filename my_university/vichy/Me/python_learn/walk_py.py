import os.path

with open("walking.txt", "w") as out:
    for address, dirs, files in os.walk("D:\\Programming_C++\\vichy\\Me\\main"):
        for name in files:
            if name[-3::] == ".py":
                out.write(address[28::] + "\n")
                break

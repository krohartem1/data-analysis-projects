import simplecrypt

with open("C:\\Users\\79125\\Downloads\\encrypted (1).bin", "rb") as inp:
    encrypted = inp.read()
    with open("C:\\Users\\79125\\Downloads\\passwords (1).txt", "r") as password:
        for line in password:
            line = line.strip()
            try:
                print(simplecrypt.decrypt(line, encrypted))
                break
            except simplecrypt.DecryptionException:
                print("No no no")

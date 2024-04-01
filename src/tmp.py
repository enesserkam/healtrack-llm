import json

sentence = "Hello, HPC world!/n"

with open('example.txt', 'w') as file:
    file.write(sentence)

print("Sentence written to example.txt")
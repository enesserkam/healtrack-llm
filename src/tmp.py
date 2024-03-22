import json

sentence = "Hello, HPC world!"

with open('example.txt', 'w') as file:
    file.write(sentence)

print("Sentence written to example.txt")
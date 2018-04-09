from random import randint as randint


FILE = "BD_pytan/przyklad_pytania.csv"
SEPARATOR = "@"

f = open(FILE, 'r')
questions = [l.strip().split(SEPARATOR) for l in f]

print(questions[randint(0, len(questions) - 1)])
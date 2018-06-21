import sys
import random

def replace_all(string, repl, *args):
	strlen = len(string)
	for i in reversed(range(strlen)):
		if string[i] in args:
			string = string[:i] + repl + string[i+1:]
	return string

def without(string, i):
	return string[:i] + string[i+1:]

def condense(string, char):
	i = 0
	while i < len(string) - 1:
		if string[i] == char:
			while string[i+1] == char:
				string = without(string, i+1)
		i += 1
	return string

def split_into_words(source):
	source = replace_all(source, ' ', '\n', '\t')
	source = condense(source, ' ')
	source = source.strip(' ')
	return source.split(' ')

def get_occurrences(word, words):
	occur = {}
	for i in range(len(words) - 1):
		if words[i] != word:
			continue
		if words[i+1] not in occur:
			occur[words[i+1]] = 1
		else:
			occur[words[i+1]] += 1
	return occur

def largest_pair(dictionary):
	largest = None
	for item in dictionary.items():
		if largest == None:
			largest = item
		else:
			if item[1] > largest[1]:
				largest = item
	return largest

def generate_chain(words):
	chain = {}
	for i, word in enumerate(words):
		if word in chain:
			continue
		occurrences = get_occurrences(word, words)
		if occurrences == None:
			continue
		max_prob = sum([x[1] for x in occurrences.items()])
		probabilities = []
		for key in occurrences:
			probabilities.append((key, occurrences[key] / max_prob))
		probabilities = sorted(probabilities, key=lambda tup: tup[1])
		chain[word] = probabilities
	return chain

def weighted_choice(ls):
	return random.choices([tup[0] for tup in ls], weights=[tup[1] for tup in ls])[0]

def generate_text(chain, seed, max_length):
	text = seed
	length = 0
	while seed in chain and length <= max_length:
		next_word = weighted_choice(chain[seed])
		text = text + ' ' + next_word
		seed = next_word
		length += 1
	return text

def load_chain(filename):
	try:
		with open(filename, "r") as f:
			source = f.read()
	except FileNotFoundError:
		print("That file does not exist")
		return
	words = split_into_words(source)
	chain = generate_chain(words)
	print("Loaded {0}...".format(filename))
	return chain
	
def sanitize(string):
	string = string.lower()
	string = string.strip(' ')
	string = string.strip('\t')
	string = string.strip('\n')
	string = string.split(' ')[0]
	return string

def interact(chains):
	while True:
		inp = input("$ ")
		inp = sanitize(inp)
		if   (inp == 'quit'):
			break
		elif (inp == 'generate'):
			chain_name = input("Chain? ")
			if (chain_name not in chains):
				print("Not a chain")
				continue
			
			seed = input("Seed Word? ")
			if (seed not in chains[chain_name]):
				print("Not in chain")
				continue
			
			max_words = input("Maximum Words? ")
			
			print(generate_text(chains[chain_name], seed, int(max_words)))
		elif (inp == 'load'):
			filename = input("Filename? ")
			chain = load_chain(filename)
			if (chain != None):
				chains[filename] = chain
		elif (inp == 'list'):
			[print(k) for k in chains]
		elif (inp == 'help'):
			print("""\
  quit:     Quit the application
  generate: Generate text from a chain
  load:     Load a chain from a text file
  list:     List currently loaded chains
  help:     Display this dialogue""")
		else:
			print("{0} is not a valid command. Try typing help.".format(inp))
	
def main():
	chains = {}
	for filename in sys.argv[1:]:
		chains[filename] = load_chain(filename)
	interact(chains)

if __name__ == "__main__":
	main()

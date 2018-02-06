w = [ "a",  "b",  "ba", "bca", "bda", "bdca" ]

def find_next_chain(word, words):
    chains = set()
    for i in range(len(word)):
        current_word = word[:i] + word[i+1:]
        if current_word in words:
            chains.add(current_word)
    return chains


def max_chain(word, words):
    current_chain = find_next_chain(word, words)
    chain_length = 1
    
    while len(current_chain) != 0:
        chain_length = chain_length + 1
        next = set()
        for j in list(current_chain):
            next = next.union(find_next_chain(j, words))
        current_chain = next

    return chain_length

def get_max_chain(words):
    chain_lengths = []
    for i in words:
        chain_lengths.append(max_chain(i, words))
    return max(chain_lengths)

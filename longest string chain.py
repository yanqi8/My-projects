w = [ "a",  "b",  "ba", "bca", "bda", "bdca" ]

# mine version
def find_next_chain(word, words):
# for any string, find the descendants if any
    chains = set()
    for i in range(len(word)):
        current_word = word[:i] + word[i+1:]
        if current_word in words:
            chains.add(current_word)
    return chains


def max_chain(word, words):
# for any string, compute the length of longest chain
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
# get the max number of chain length for all elements in words
    chain_lengths = []
    for i in words:
        chain_lengths.append(max_chain(i, words))
    return max(chain_lengths)





# quicker version
def longest(word_set, cache, word):
    if word not in cache:
        ret = 1
        for i in xrange(len(word)):
            w = word[:i] + word[i+1:]
            if w and w in word_set:
                cnt = longest(word_set, cache, w)
                ret = max(ret, 1 + cnt)

        cache[word] = ret

    return cache[word]


def longestChain(words):
    cache = {}
    word_set = set(words)
    gmax = 0
    for word in words:
        gmax = max(gmax, longest(word_set, cache, word))

    return gmax










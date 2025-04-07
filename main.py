# This is a sample Python script.
import itertools
import json
import numpy as np
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def filter_words(words, guess, pattern):

    # Filtering mask for valid words based on feedback pattern
    filter = np.ones(len(words), dtype=bool)

    # filter words with grey letters
    for i, l in enumerate(guess):
        if pattern[i] == 1:
            if l not in guess[:i]:
                filter &= np.all(words != l,axis=1)
    # filter yellow
    for i, l in enumerate(guess):
        if pattern[i] == 2:

            filter &= np.any(((words == l) & (words[:, i] != l)[:, None]),axis=1)

    # fitler green
    for i, l in enumerate(guess):
        if pattern[i] == 3:

            filter &= (words[:, i] == l)

    return words[filter]


def generate_feedback(guess, secret):
    # 1 - gray, 2 - yellow, 3 - green
    l = len(guess)
    feedback = np.ones(l, dtype=int)  # Start with all gray (1)
    guess_used = np.zeros(l, dtype=bool)
    secret_used = np.zeros(l, dtype=bool)

    # generate greens
    for i in range(l):
        if guess[i] == secret[i]:
            guess_used[i] = True
            secret_used[i] = True
            feedback[i] = 3  # Green feedback

    # generate yellows
    for i in range(l):
        if feedback[i] == 3:  # Skip already matched greens
            continue
        for j in range(l):
            if guess[i] == secret[j] and not guess_used[i] and not secret_used[j]:
                guess_used[i] = True
                secret_used[j] = True
                feedback[i] = 2  # Yellow feedback
                break

    return tuple(feedback)

if __name__ == '__main__':
    '''
    # calculating entropy for all the words
    num = [1, 2, 3]  # 1: gray, 2: yellow, 3: green
    # generating all possible outcomes of: letter not present 1, 2 letter present but in wrong place, 3 - letter present and in good place
    outcomes = np.array(list(itertools.product(num, repeat=5)))

    # calculating probabilities for each word

    f = open("words.json")
    data = json.load(f)
    f.close()

    all_words = data["words"]
    all_words_arr = np.array([[ord(c) for c in word] for word in all_words], dtype=int)
    E_entropy = {}

    for i, guess in enumerate(all_words_arr):
        print(str(i)+"/"+str(len(all_words)))
        # Collect all feedback patterns
        feedbacks = np.zeros((len(all_words_arr), 5), dtype=int)

        for j, secret in enumerate(all_words_arr):
            feedbacks[j] = generate_feedback(guess, secret)

        # Get unique feedback patterns and counts
        unique_patterns, counts = np.unique(feedbacks, axis=0, return_counts=True)

        # Calculate probabilities and entropy
        probs = counts / len(all_words_arr)
        entropy = -np.sum(probs * np.log2(probs))  # Correct entropy formula
        E_entropy[all_words[i]] = float(entropy)

    with open("entropy.json", "x") as f:
        json.dump(E_entropy, f)
    '''

    # gettin entropy of first words from file (calculated beforehand to minimize time)
    # Load the pre-calculated entropy from the JSON file
    with open("entropy.json") as f:
        entropy = json.load(f)

    # Sort entropy values in descending order
    sorted_entropy = sorted(entropy.items(), key=lambda x: x[1], reverse=True)
    sorted_entropy = dict(sorted_entropy)

    isSecret = False
    while not isSecret:
        # Show 10 best words based on entropy
        for w in itertools.islice(sorted_entropy.items(), 10):
            print(f"#{w[0]}: {w[1]}")

        guess = input("Guess: ")

        # Get letter pattern (gray, yellow, green)
        print("# 1: gray, 2: yellow, 3: green")
        pattern = np.array([int(c) for c in input("letter pattern: ")])

        # Convert guess to ord array
        guess_arr = np.array([ord(c) for c in guess], dtype=int)

        # Calculate feedbacks for all remaining words
        all_words = list(sorted_entropy.keys())
        all_words_arr = np.array([[ord(c) for c in word] for word in all_words], dtype=int)
        feedbacks = np.zeros((len(all_words_arr), 5), dtype=int)
        for i, secret in enumerate(all_words_arr):
            feedbacks[i] = generate_feedback(guess_arr, secret)

        # Get unique feedback patterns and their counts
        unique_patterns, count = np.unique(feedbacks, axis=0, return_counts=True)
        guess_ind = np.where(np.all(unique_patterns == pattern, axis=1))[0]
        prob = count[guess_ind] / len(all_words_arr)
        guess_entropy = -np.log2(prob)  # Calculate entropy of the guess
        print(f"{guess} entropy is {guess_entropy}")
        valid_words = filter_words(all_words_arr, guess_arr, pattern)
        valid_words_str = ["".join(chr(c) for c in word) for word in valid_words]
        print(f"Valid words left: {len(valid_words)}")

        # Recalculate entropy for remaining valid words
        E_entropy = {}
        for i, guess in enumerate(valid_words):
            print(f"{i}/{len(valid_words)}")
            feedbacks = np.zeros((len(valid_words), 5), dtype=int)
            for j, secret in enumerate(valid_words):
                feedbacks[j] = generate_feedback(guess, secret)

            unique_patterns, counts = np.unique(feedbacks, axis=0, return_counts=True)
            probs = counts / len(all_words_arr)
            entropy_val = -np.sum(probs * np.log2(probs))  # Correct entropy formula
            E_entropy[valid_words_str[i]] = float(entropy_val)

        # Update sorted entropy list
        sorted_entropy = sorted(E_entropy.items(), key=lambda x: x[1], reverse=True)
        sorted_entropy = dict(sorted_entropy)







# See PyCharm help at https://www.jetbrains.com/help/pycharm/

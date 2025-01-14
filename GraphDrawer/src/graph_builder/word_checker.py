
class WordChecker:

    @staticmethod
    def are_one_letter_apart(word1, word2):
        if abs(len(word1) - len(word2)) > 1:
            return False

        if len(word1) == len(word2):
            differences = sum(1 for a, b in zip(word1, word2) if a != b)
            return differences == 1

        if len(word1) > len(word2):
            word1, word2 = word2, word1

        for i in range(len(word2)):
            if word2[:i] + word2[i+1:] == word1:
                return True
        return False

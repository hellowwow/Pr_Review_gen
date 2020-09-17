import numpy as np
str = ['1', '1', '2', '2', '3']

class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []
        self.length = 0
    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = self.length + 1
            self.length += 1
        return self.word2idx[word]
    def __len__(self):
        return len(self.length)
    def onehot_encoded(self, word):
        vec = np.zeros(self.length)
        vec[self.word2idx[word] - 1] = 1
        return vec

def test():
    Onehot = Dictionary()
    str = "the action scenes were top notch in this movie."
    for tok in str.split():
        Onehot.add_word(tok)
    print(Onehot.word2idx)
    print(Onehot.onehot_encoded('movie.'))

if __name__ == '__main__':
    test()
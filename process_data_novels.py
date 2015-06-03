import numpy as np
import cPickle
from collections import defaultdict
import sys, re
import pandas as pd
import argparse
import time

def load_data(filename, genre):
    docs = []
    vocab = defaultdict(float)
    c = 0
    for line in read_lines(open(filename, 'r')):
        print 'processing %s' % c
        c += 1
        line = line.strip()
        splitted = line.split()
        name = splitted[0]
        did, gid, fold, label = name.split("_")
        if genre == 0 or int(gid) == genre:
            sentences = ' '.join(str(s) for s in splitted[1:])
            num_words = len(splitted[1:])
            words = set(splitted[1:])
            for word in words:
                word = '%s_%s_%s' % (word, did, gid)
                vocab[word] += 1
            datum  = {"y":int(label),
                      "text": sentences,
                      "id": did,
                      "gid": gid, 
                      "num_words": num_words,
                      "split": int(fold)}
            docs.append(datum)
    return docs, vocab

def read_lines(f):
    for ii,line in enumerate(f):
        yield line

    
def get_W(filename, vocab, split, t, k):
    """
    Get word matrix. W[i] is the vector for word indexed by i
    """
    vocab_size = len(vocab)
    W = np.zeros(shape=(vocab_size+1, k))
    W[0] = np.zeros(k)
    word2idx = {}
    j = 1
    i = 0
    counter = 0
    for line in read_lines(open(filename, 'r')):
        if i == 0:
            i = 1
            continue
        print 'processing %s' % counter
        counter += 1
        line = line.split()
        sentence = line[0]
        if sentence in vocab:
            if not split:
                W[j] = np.array(line[1:]).astype(np.float32)
            else:
                if t == 'sent':
                    W[j] = np.array(line[k+1:]).astype(np.float32)
                elif t == 'syn':
                    W[j] = np.array(line[1:k+1]).astype(np.float32)
            word2idx[sentence] = j
            j += 1
    return W, word2idx

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', required=True) # doc as sentences (probably the syntax based one)
    parser.add_argument('-e', '--embeddings', required=True) # sentence embeddings (or syntax one)
    parser.add_argument('-o', '--output', required=True) # pickle output
    parser.add_argument('-s', '--split', required=False, type=bool, default=False)
    parser.add_argument('-t', '--type', required=False, default='sent')
    parser.add_argument('-k', '--k', required=False, type=int, default=200)
    parser.add_argument('-g', '--genre', required=False, type=int, default=0)
    args = parser.parse_args()

    if args.split:
        assert args.type == 'sent' or args.type == 'syn'

    print "loading data..."        
    docs, vocab = load_data(args.input, args.genre)
    max_l = np.max(pd.DataFrame(docs)["num_words"])
    print "data loaded"
    print "number of sentences: " + str(len(docs))
    print "vocab size: " + str(len(vocab))
    print "max sentence length: " + str(max_l)

    W, word2idx = get_W(args.embeddings, vocab, args.split, args.type, args.k)
    print "W shape %s" % str(W.shape)
    print "dumping pickle"
    start = time.time()
    cPickle.dump([docs, W, word2idx, vocab, max_l], open(args.output, "wb"))
    print 'dump took %s' % (time.time() - start)

    print "dataset created"

if __name__=="__main__":
    main()    

    

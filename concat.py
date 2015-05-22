#!/usr/bin/python
from __future__ import division
import argparse
import time
import numpy as np
from collections import defaultdict
from operator import itemgetter
import re

def read_lines(f):
  for ii,line in enumerate(f):
    yield line

def read_embeddings(filename, prefix, name):
  dictionary = {}
  c = 0
  i = 0
  for line in read_lines(open(filename, 'r')):
    if i == 0:
      i = 1
      continue
    print 'processing %s %d' % (name, c)
    c += 1
    l = line.split()
    if l[0].startswith(prefix):
      dictionary[l[0]] = l[1:]
  return dictionary    

def main():
  parser = argparse.ArgumentParser(description='TODO')
  parser.add_argument('-i1', '--sentence_file', required=True) # sentence
  parser.add_argument('-i2', '--syntax_file', required=True) # syntax
  parser.add_argument('-e1', '--sentence_embedding_file', required=True) # sentence embedding file
  parser.add_argument('-e2', '--syntax_embedding_file', required=True) # syntax embedding file
  parser.add_argument('-oe', '--output_embedding_file', required=True) # output embedding file
  parser.add_argument('-of', '--output_vocab_file', required=True) # output file with new vocabs
  args = parser.parse_args()

  syntaxs = defaultdict(list)
  for line in open(args.syntax_file).read().splitlines():
    doc = line.split()
    did, gid, fid, label = doc[0].split("_")
    rest = doc[1:]
    syntaxs[(did, gid, fid, label)] = rest

  novels = defaultdict(list)
  for line in open(args.sentence_file).read().splitlines():
    doc = line.split()
    _, did, gid, fid, label = doc[0].split("_")
    rest = doc[1:]
    novels[(did, gid, fid, label)] = rest

  assert len(syntaxs) == len(novels)

  novels_embeddings = read_embeddings(args.sentence_embedding_file, 'SENT', 'emb')
  print 'size of novels embedding %s' % len(novels_embeddings)
  syntax_embeddings = read_embeddings(args.syntax_embedding_file, 'SYN', 'syn')
  print 'size of syntax embedding %s' % len(syntax_embeddings)


  oe = open(args.output_embedding_file, 'w')
  of = open(args.output_vocab_file, 'w')
  c = 0
  for key in syntaxs:
    print 'last processing %s' % c
    c += 1
    s_array = syntaxs[key]
    print s_array
    n_array = novels[key]
    print n_array
    assert len(s_array) == len(n_array)
    doc_id = '%s_%s_%s_%s' % (key[0], key[1], key[2], key[3])
    elems = [doc_id]
    for s, n in zip(s_array, n_array):
      se = syntax_embeddings[s]
      print se
      ne = novels_embeddings[n]
      print ne
      emb = se.extend(ne)
      print emb
      exit()
      sentence_nr = n.split("_")[-1]
      new_s = s.replace("SYN", "")
      new_id = '%s_%s' % (new_s, sentence_nr)
      emb_as_str = " ".join(str(e) for e in emb)
      oe.write('%s %s\n' % (new_id, emb_as_str))
      elems.append(new_id)
    elems_as_str = " ".join(str(e) for e in elems)
    of.write('%s\n' % elems_as_str)

  oe.close()
  of.close()

if __name__ == '__main__':
  main()

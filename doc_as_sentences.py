#!/usr/bin/python
from __future__ import division
import argparse
import time
import numpy as np
from collections import defaultdict
from gensim.models import word2vec
from gensim import matutils
from operator import itemgetter
import re


def main():
  parser = argparse.ArgumentParser(description='TODO')
  parser.add_argument('-i', '--input_file', required=True)
  parser.add_argument('-o', '--output_file', required=True)
  args = parser.parse_args()

  documents = defaultdict(list)
  p = re.compile(ur'^SENT_(\d+)_(\d)_(\d)_(\d)_(\d+)$')
  for line in open(args.input_file).read().splitlines():
    sentence = line.split()[0]
    search_obj = re.search(p, sentence)
    if search_obj:
      did = search_obj.group(1)
      gid = search_obj.group(2)
      fid = search_obj.group(3)
      label = search_obj.group(4)
      sentence_nr = search_obj.group(5)
      value = 'SENT_%s_%s_%s_%s_%s' % (did, gid, fid, label, sentence_nr)
      documents[(did, gid, fid, label)].append(value)

  print 'documents length: %s' % len(documents)

  of = open(args.output_file, 'w')
  for key in documents:
    sentences_as_str = ' '.join(str(e) for e in documents[key])
    of.write('DOC_%s_%s_%s_%s %s\n' % (key[0], key[1], key[2], key[3], sentences_as_str))
  of.close()

if __name__ == '__main__':
  main()


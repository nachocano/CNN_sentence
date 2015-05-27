#!/usr/bin/python
import argparse

def main():
  parser = argparse.ArgumentParser(description='TODO')
  parser.add_argument('-i', '--sent_syn_file', required=True) # sentence & syntax file
  parser.add_argument('-t', '--threshold', required=True, type=int) # sentence & syntax file
  args = parser.parse_args()

  for line in open(args.sent_syn_file).read().splitlines():
    doc = line.split()
    rest = doc[1:]
    if len(rest) > args.threshold:
      rest = doc[1:args.threshold+1]
    rest_as_str = " ".join(str(e) for e in rest)
    print '%s %s' % (doc[0], rest_as_str)
    
if __name__ == '__main__':
  main()

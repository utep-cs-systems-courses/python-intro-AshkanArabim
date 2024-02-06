import os
import re
import argparse


# this will handle all the complexity of counting words in a file
class FileParser:
    def __init__(self, sourcepath: str):
        self._buffer = ""
        self._fd = os.open(sourcepath, os.O_RDONLY)
        self._buffer_idx = 0
    
    def _loadbuffer(self, n=100):
        self._buffer = os.read(self._fd, n)
        self._buffer_idx = 0
        return len(self._buffer)  # num of chars actually read

    def _readchar(self):
        l = len(self._buffer)
        if l == 0 or self._buffer_idx == l:
            self._loadbuffer()
        if len(self._buffer) == 0:
            return -1  # nothing left to read!
        self._buffer_idx += 1
        return chr(self._buffer[self._buffer_idx - 1])

    def _readword(self):
        word = ""
        while True:
            ch = self._readchar()
            # print(ch)  # debug
            if ch == -1: return -1
            if re.match(r"[a-zA-Z]", ch) == None: # note: import
                return word  # return word if non-alphabet char found
            word += ch
    
    def get_next_word(self):
        return self._readword()
    
    
if __name__ == "__main__":
    # parse arguments
    argparser = argparse.ArgumentParser(
        prog="wc-py",
        description="python implementation of unix `wc`",
    )
    argparser.add_argument("input_file")
    argparser.add_argument("output_file")
    args = argparser.parse_args()
    
    # initialize FileParser using the input file path
    parser = FileParser(args.input_file)
    
    # count all words, until none exists
    word_counts = {}
    while(True):
        word = parser.get_next_word()
        if word == -1: break  # break if no more words left
        if word == "": continue
        print(word) # debug
        word_counts[word] = word_counts.get(word, 0) + 1
        
    # print words and counts to output file
    output_file = os.open(args.output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o777)
    for word in sorted(word_counts.keys()):
        buffer = f"{word}: {word_counts[word]}\n"
        
        while len(buffer):
            bc = os.write(output_file, buffer.encode())
            buffer = buffer[bc:]

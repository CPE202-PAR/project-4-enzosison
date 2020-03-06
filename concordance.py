from hash_quad import *
import string

class Concordance:

    def __init__(self):
        self.stop_table = None          # hash table for stop words
        self.concordance_table = None   # hash table for concordance
        self.load_stop_table("stop_words.txt")

    def load_stop_table(self, filename):
        """ Read stop words from input file (filename) and insert each word as a key into the stop words hash table.
        Starting size of hash table should be 191: self.stop_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        self.stop_table = HashTable(191)
        f = open(filename)
        for word in f:
            word_split = word.rstrip()
            self.stop_table.insert(word_split, 0)   #the insert function needs to take in a value so I just inserted 0 for each key

    def load_concordance_table(self, filename):
        """ Read words from input text file (filename) and insert them into the concordance hash table, 
        after processing for punctuation, numbers and filtering out words that are in the stop words hash table.
        Do not include duplicate line numbers (word appearing on same line more than once, just one entry for that line)
        Starting size of hash table should be 191: self.concordance_table = HashTable(191)
        Process of adding new line numbers for a word (key) in the concordance:
            If word is in table, get current value (list of line numbers), append new line number, insert (key, value)
            If word is not in table, insert (key, value), where value is a Python List with the line number
        If file does not exist, raise FileNotFoundError"""
        self.concordance_table = HashTable(191)
        linecounter = 0
        try:
            f = open(filename)
        except:
            raise FileNotFoundError
        for line in f:
            linecounter += 1
            line = self.string_prep(line)
            split_line = line.split()           #there's currently no check against stop words, punctuation, and numbers
            for word in split_line:
            #add another if statement here, that checks for bad inputs first
                if self.concordance_table.get_value(word) and not self.stop_check(word):      #if the word already exists in our table
                    new_value = self.concordance_table.get_value(word)
                    if linecounter not in new_value:            #insert new line number as long as it's not a repeat
                        new_value = new_value + [linecounter]
                        self.concordance_table.insert(word, new_value)
                else:                                           #if it's a whole new word
                    self.concordance_table.insert(word, [linecounter])

    def string_prep(self, line):
        for i in line:
            if i == "-":
                x = line.replace("-"," ")
            translator = str.maketrans('', '', string.punctuation)
            return line.translate(translator).lower()

    def check_num(self, word):
        return str.replace('.','','1').isdigit()

    def stop_check(self, word):
        return not self.stop_table.in_table(word) and not self.check_num(word)

    def write_concordance(self, filename):
        """ Write the concordance entries to the output file(filename)
        See sample output files for format."""
        word_list = []
        d = open(filename, "w+")
        for word in self.concordance_table.hash_table:
            if word:
                word_list.append(word)
        sorted_list = sorted(word_list)
        for index, entry in enumerate(sorted_list):
            word = entry.key
            value_list = entry.value     #value list is currently ints  -> convert to strings -> join strings
            line_string = " ".join([str(i) for i in value_list])
            d.write(word + ": " + line_string)
            if index != len(sorted_list) - 1:
                d.write("\n")








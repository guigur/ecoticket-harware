# -*- coding: utf-8 -*-
import re

class Parser():

    cleaned = []
    parsed = []

    # Call this function in EcoticketClass.py
    def parseFile(self, filename, conf_values):
        # Clean file and keep only articles and prices in cleaned[]
        self.cleanFile(filename, conf_values[3], conf_values[4])
        # Parse cleaned[] and put results in parsed[]
        total = self.doParsing(conf_values[5])
        # Create and fill file
        self.makeFile(filename)
        return total

    def cleanFile(self, filename, j, eof):
        i = 0
        f = open(filename, 'r')
        line = f.readline()

        while line:
            if (line.rstrip('\n') == eof.rstrip('\n')):
                break
            elif (i > int(j)):
                self.cleaned.append(line)
            line = f.readline()
            i += 1
        f.close()

    def doParsing(self, delimiters):
        i = 0
        j = 1
        self.parsed.append("----\n")
        for line in self.cleaned:
            if (line == '\n'):
                i += 1
            if (line != '\n' and i == 0):
                m = re.match("\d[x]\w+", line)
                if m:
                    h = re.compile(delimiters)
                    splitted = h.split(line)
                    number = splitted[0].rstrip('\n')
                    article = splitted[1].rstrip('\n')
                    self.parsed.append(number + ' X ' + article + '____')
                else:
                    h = re.compile(delimiters)
                    splitted = h.split(line)
                    article = splitted[0].rstrip('\n')
                    self.parsed.append('1 X ' + article + '____')
            if (line != '\n' and i == 1):
                price = line
                price = price.replace('€', '')
                price = price.replace(',', '.')
                self.parsed[j] += price
                j+=1
            if (line != '\n' and i == 2):
                total = line
                total = total.replace('€', '')
                total = total.replace(',', '.')
                self.parsed.append("TOTAL____" + total)
                self.parsed.append("----\n")
                break
        return total

    def makeFile(self, filename):
        file = open(filename, 'w')
        file.writelines(self.parsed)
        file.close()
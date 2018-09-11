import re
import io
class LexicalUnit:
    oprel=["==","<>","<",">","<=",">="]

    signe=["+","-"]
    opmul=["*","/","div","mod","and"]
    opaffect=["="]
    key_word=["prog","var",":","int","func","porc",";","if","then","else","while","do","not","(",")","}","{","or",","]

    def __init__(self):
        self.units={a:"oprel" for a in LexicalUnit.oprel}
        self.units.update({a:"signe" for a in LexicalUnit.signe})
        self.units.update({a: "opmul" for a in LexicalUnit.opmul})
        self.units.update({a: "opaffect" for a in LexicalUnit.opaffect})
        self.units.update({a: a for a in LexicalUnit.key_word})
        self.nbPattern=re.compile("^[0-9]*$")
        self.wordPattern=re.compile("^[a-z][a-zA-Z0-9_]*$")
        self.WordPattern = re.compile("^[A-Z][a-zA-Z0-9_]*$")
        self.nonSpaced=["==","<>","<",">","<=",">=","+","-","*","/","=",":",";","(",")","}","{",","]

    def identify(self,word):
        if(word in self.units):
            return (self.units[word],word)
        if(self.nbPattern.match(word)):
            return ("nb",word)
        if(self.wordPattern.match(word)):
            return ("id",word)
        if (self.WordPattern.match(word)):
            return ("Id", word)
        print("this is not a valid lexical element {}".format(word))
        return ("Error","NO")


class LexicalAnalyser:
    def __init__(self,f):
        self.lexicalUnit=LexicalUnit()
        self.input=f.read()
        self.deleteComment()
        for unit in self.lexicalUnit.nonSpaced:
            self.input =self.input.replace(unit," "+unit+" ")
        self.input=" ".join(self.input.split())
        for unit in self.lexicalUnit.nonSpaced:
            if(len(unit)==2):
                self.input = self.input.replace(unit[0]+" "+unit[1], unit)

    def analyse(self):
        for unit in self.input.split():
            yield self.lexicalUnit.identify(unit)
        yield ("$","")

    def deleteComment(self):
        pass



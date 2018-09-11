from collections import Counter

from lexicalAnalyser import LexicalAnalyser

axiome="programmes"

class Grammar:

    def __init__(self):
        self.grammar=self.read_grammar()
        self.grammar=self.immediate_recursive(self.grammar)
        self.grammar=self.factorisation(self.grammar)
        self.atom_type()
        self.first={}
        for non_terminal in self.non_terminals:
            self.find_first(non_terminal)

        self.follow = {}
        self.follow[axiome]={"$"}
        for non_terminal in self.non_terminals:
            self.find_follow(non_terminal)


        self.parsing_table()

    def read_grammar(self):
        grammar={}
        with open("grammar","r") as f:
            for line in f:
                line= line.strip('\n').split(" = ")
                if(len(line)>1):
                    grammar[line[0]]=line[1].split(" | ")

        for key,val in grammar.items():
            for i in range(len(val)):
                val[i] = val[i].split(" ")

        return grammar


    def atom_type(self):
        self.terminals =set()
        self.non_terminals=set()
        for val in self.grammar.values():
            for rule in val:
                for atom in rule:
                    if(atom not in self.grammar):
                        self.terminals.add(atom)

        for atom in self.grammar:
            self.non_terminals.add(atom)

    def find_first(self,atom):
        if atom in self.terminals:
            return {atom}
        if atom in self.first:
            return self.first[atom]
        self.first[atom]=set()
        for rule in self.grammar[atom]:
            for i in range(len(rule)):
                s=self.find_first(rule[i])
                self.first[atom]|=s-{"epsilon"}
                if "epsilon" not in s:
                    break
                if( i==len(rule)-1):
                    self.first[atom] |= {"epsilon"}
        return self.first[atom]

    def find_follow(self,atom):
        if atom in self.follow:
            return self.follow[atom]
        self.follow[atom]=set()

        for key,rules in self.grammar.items():
            for rule in rules:
                for i in range(len(rule)):
                    if rule[i]==atom:
                        j=i+1
                        curFollow=None
                        for j in range(i+1,len(rule)):
                            curFollow=self.find_first(rule[j])
                            self.follow[atom] |= (curFollow - {"epsilon"})
                            if "epsilon" not in curFollow:
                                break

                        if(curFollow is None or "epsilon" in curFollow):
                            curFollow=self.find_follow(key)
                            self.follow[atom] |= curFollow

        return self.follow[atom]

    def rule_first(self,rule):
        first=set()
        for i in range(len(rule)):
            s = self.find_first(rule[i])
            first |= s - {"epsilon"}
            if "epsilon" not in s:
                break
            if (i == len(rule) - 1):
                first |= {"epsilon"}

        return first

    def parsing_table(self):
        self.table={}
        for key,rules in self.grammar.items():
            assert key not in self.table
            self.table[key]={}
            for rule in rules:
                first=self.rule_first(rule)
                for atom in (first- {"epsilon"}):
                    assert atom not in self.table[key]
                    self.table[key][atom]=rule
                if "epsilon" in first:
                    for atom in self.find_follow(key):
                        assert atom not in self.table[key]
                        self.table[key][atom] = rule


    @staticmethod
    def immediate_recursive(tmp_grammar):
        grammar={}
        for key,rules in tmp_grammar.items():

            atoms=list(zip(*rules))[0]

            if key in atoms:
                old_rules = []
                new_rules = [["epsilon"]]
                new_non_terminal=key+"_1"
                for rule in rules:
                    if(rule[0]==key):
                        new_rules.append(rule[1:]+[new_non_terminal])
                    else:
                        old_rules.append(rule+[new_non_terminal])

                grammar[key]=old_rules
                grammar[new_non_terminal]=new_rules
            else:
                grammar[key]=rules

        return grammar
    @staticmethod
    def factorisation(tmp_grammar):
        grammar = {}
        for key,rules in tmp_grammar.items():

            atoms=list(zip(*rules))[0]

            factor=None
            for cur, occu in Counter(atoms).items():
                if occu>1:
                    factor=cur

            if (factor is None):
                grammar[key]=rules
                continue

            new_rules = []
            new_non_terminal=key+"_'"
            old_rules = [[factor]+[new_non_terminal]]
            for rule in rules:
                if (factor==rule[0]):
                    if len(rule[1:])==0:
                        new_rules.append(["epsilon"])
                    else:
                        new_rules.append(rule[1:])
                else:
                    old_rules.append(rule)

            grammar[key] = old_rules
            grammar[new_non_terminal] = new_rules

        return  grammar


grammar=Grammar()


file=open("file.c","r")
lexical=LexicalAnalyser(file)

stack=["$",axiome]

units=lexical.analyse()
unit= next(units)



while True:
    if stack[-1]=="epsilon":
        stack.pop()
    elif (stack[-1] in grammar.non_terminals):
        X = stack.pop()
        if (unit[0] in grammar.table[X]):
            stack += list(reversed(grammar.table[X][unit[0]]))
        else:
            print("error expected {} found {}".format(X,unit[1]))
            break
    elif stack[-1]=="$":
        if unit[0]=="$":
            print("accepter")
            break
        else:
            print("error in the end of the programme")
            error=unit[1]
            for a in units:
                error+=" "+a[1]
            print("error begin in {}".format(error))
            break
    elif(stack[-1]==unit[0]):
        stack.pop()
        unit=next(units)
    else:
        print("expected {}".format(stack[-1]))
        break

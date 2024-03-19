# https://chat.openai.com/g/g-aSTwVKYNF-coder-s-teacher/c/d2ea6917-f765-4faf-992b-06379c39bc33
import re

class Predicate:
    def __init__(self, name, arguments, negated=False):
        self.name = name      
        self.arguments = arguments
        self.negated = negated
    def print_predicate(self):
        print("name: ", self.name)
        print("argument list: ", self.arguments)
        print("Negated or not: ", self.negated)
    
class Clause:
    def __init__(self, predicates):
        self.predicates = predicates # It is a LIST of predicate above

    def print_clause(self):
        num = len(self.predicates)
        for i in range(num):
            print("Predicate", i+1, ":")
            self.predicates[i].print_predicate()
            print("-------------------")
    
    def print_user_view(self):
        # TODO
        return []

def parse_predicate(predicate_str):
    """Parses a single predicate string into a Predicate object."""
    predicate_str = predicate_str.strip()
    negated = predicate_str.startswith("¬")
    if negated:
        predicate_str = predicate_str[1:]  # Remove negation symbol

    name_end_index = predicate_str.find("(")
    name = predicate_str[:name_end_index]
    arguments_str = predicate_str[name_end_index+1:-1]  # Exclude parentheses
    arguments = arguments_str.split(", ") if ", " in arguments_str else [arguments_str]

    return Predicate(name, arguments, negated)

def remove_outer_parentheses(input):
    if input.startswith("(") and input.endswith(")"):
        return input[1:-1]
    return input

def split_on_outer_comma(input_text):
    return re.split(r',(?![^()]*\))', input_text)

def parse_input(input_text):
    """input text and turns into clause object: (¬C(y), ¬L(y, rain)) """
    # Return a clause
    input_text = remove_outer_parentheses(input_text) #  ¬C(y), ¬L(y, rain)
    predicates_str = split_on_outer_comma(input_text) #  [¬C(y), ¬L(y, rain)]
    
    predicates = [parse_predicate(predicate_str) for predicate_str in predicates_str]
    return Clause(predicates)




def unify(predicates1, predicates2):
    # Input 2 predicates
    # Output a substitution if successful unified
    pass

def resolve(clause1, clause2):
    # Input 2 clauses
    # Output a new clause if successful
    pass
def MGB(KB):
    # find 1 compatible replace rule. If so, return true, else return false
    # The same predicate, with different value
    # ITS A TREE!

def resolution_algorithm(KB):
    # Main loop here
    goal_test = False
    while True:
        # find 2 same 
        goal_test = not MGB(KB)
        


def main():
    clauses_num = int(input())
    KB = []
    for i in range(clauses_num):
        input_text = input()
        KB.append(parse_input(input_text))
    for clause in KB:
        clause.print_clause()
    # Turn all the input string to clauses object, and each clauses is consisted of predicates.

def test1():
    test = parse_input("(¬C(y), ¬L(y, rain))")
    test.print_clause()

main()
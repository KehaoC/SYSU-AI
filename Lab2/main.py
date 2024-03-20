# https://chat.openai.com/g/g-aSTwVKYNF-coder-s-teacher/c/d2ea6917-f765-4faf-992b-06379c39bc33
import re

class Predicate:
    def __init__(self, name, arguments, negated=False):
        self.name = name      
        self.arguments = arguments
        self.negated = negated
    def print_predicate(self):
        # print("name: ", self.name)
        # print("argument list: ", self.arguments)
        # print("Negated or not: ", self.negated)
        output = ""
        if self.negated:
            output += "¬"
        output += self.name + "("
        for argument in self.arguments:
            output += argument
            if argument is not self.arguments[-1]:
                output += ", "
        output += ")"
        return output
    
class Clause:
    def __init__(self, predicates):
        self.predicates = predicates # It is a LIST of predicate above

    def print_clauses(self, direct = True):
        if len(self.predicates) == 1:
            if direct is not False:
                print(self.predicates[0].print_predicate())
            return 
        output = "( "
        for predicate in self.predicates:
            output += predicate.print_predicate()
            if predicate is not self.predicates[-1]:
                output += ", "
        output += " )"
        if direct is not False:
            print(output)
        return output
            
            


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

def int_to_char(n, lower_case=True):
    if lower_case:
        return chr(n + 97)  # 返回小写字母
    else:
        return chr(n + 65)  # 返回大写字母

def resolve(KB, clause1, clause2, predicate1, predicate2):
    # Input 2 clauses
    # Output a new clause if successful
    index1 = ""
    index2 = ""
    for i in range(len(KB)):
        if KB[i] is clause1:
            index1 += str(i+1)
            for j in range(len(clause1.predicates)):
                if clause1.predicates[j] is predicate1:
                    index1 += int_to_char(j)
        if KB[i] is clause2:
            index2 += str(i+1)
            for j in range(len(clause2.predicates)):
                if clause2.predicates[j] is predicate2:
                    index2 += int_to_char(j)
    dic = {}
    for i in range(len(predicate1.arguments)):
        dic[predicate1.arguments[i]] = predicate2.arguments[i]
    clause1.predicates.remove(predicate1)
    clause2.predicates.remove(predicate2)
    for predicate in clause2.predicates:
        clause1.predicates.append(predicate)
    for predicate in clause1.predicates:
        for key,value in dic.items():
            predicate.arguments = [key if arg == value else arg for arg in predicate.arguments]
    KB.remove(clause2)
    
    for clause in KB:
        if len(clause.predicates) == 0:
            KB.remove(clause)

    info = "R[" + index1 + "," + index2 + "]"
    for key, value in dic.items():
        info += ("(" + key + "=" + value + ")")
    info += " => " + str(clause1.print_clauses(direct = False))
    print(info)


def is_match(predicate1, predicate2):
    return predicate1.name == predicate2.name and predicate1.negated != predicate2.negated

def find_clause2(clause1, KB):
    for predicate1 in clause1.predicates:
        for clause2 in KB:
            for predicate2 in clause2.predicates:
                if is_match(predicate1, predicate2):
                    resolve(KB, clause1, clause2, predicate1, predicate2)
                    return True
    return False

def debug_info(KB):
    print("\n----------Debug Info------------")
    print("Number of clause in KB: ", len(KB))
    count = 1
    for clause in KB:
        print("Clause:", count,"\t",sep="",end="")
        count = count+1
        clause.print_clauses()
    print("---------------------------------\n")

def resolution_algorithm(KB):
    # Main loop here
    goal_test = False
    while True:
        for clause1 in KB:
            goal_test = find_clause2(clause1, KB)
            if goal_test == True:
                debug_info(KB)
                break
        if goal_test is False:
            break
            

        


def main():
    clauses_num = int(input())
    KB = []
    for i in range(clauses_num):
        input_text = input()
        KB.append(parse_input(input_text))
    for clause in KB:
        clause.print_clause()
    # Turn all the input string to clauses object, and each clauses is consisted of predicates.

if __name__ == "__main__":
    main()


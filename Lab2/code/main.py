import re
import copy

class Predicate:
    def __init__(self, name, arguments, negated=False):
        self.name = name      
        self.arguments = arguments
        self.negated = negated
    def print_predicate(self):
        """Print the predicate in a readable format."""
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
    def deepcopy(self):
        """Create a deep copy of the Predicate instance."""
        return Predicate(copy.deepcopy(self.name),
                         copy.deepcopy(self.arguments),
                         copy.deepcopy(self.negated))
    def __eq__(self, __value: object) -> bool:
        if self.name == __value.name and self.arguments == __value.arguments and self.negated == __value.negated:
            return True
        return False
    
class Clause:
    def __init__(self, predicates = []):
        self.predicates = predicates # It is a LIST of predicate above

    def print_clause(self, direct = True):
        """Print the clause in a readable format. If direct is False, return the string instead of printing it."""
        if len(self.predicates) == 1:
            if direct is not False:
                print(self.predicates[0].print_predicate())
            return 
        output = "("
        for predicate in self.predicates:
            output += predicate.print_predicate()
            if predicate is not self.predicates[-1]:
                output += ", "
        output += ")"
        if direct is not False:
            print(output)
        return output
    def deepcopy(self):
        predicates = [predicate.deepcopy() for predicate in self.predicates]
        return Clause(predicates)
    def __eq__(self, other):
        if len(self.predicates) != len(other.predicates):
            return False
        for predicate in self.predicates:
            if predicate not in other.predicates:
                return False
        return True
            
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
    """Splits a string on commas that are not inside parentheses."""
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

def resolve(clause1, clause2, predicate1, predicate2, replace):
    new_clause = Clause([])
    for predicate in clause1.predicates:
        if predicate != predicate1:
            new_clause.predicates.append(predicate.deepcopy())
    for predicate in clause2.predicates:
        if predicate != predicate2:
            new_clause.predicates.append(predicate.deepcopy())

    for key, value in replace.items():
        for predicate in new_clause.predicates:
            for i in range(len(predicate.arguments)):
                if predicate.arguments[i] == key:
                    predicate.arguments[i] = value
    # TODO去重
    while True:
        find = False
        for i in range(len(new_clause.predicates)):
            for j in range(i+1, len(new_clause.predicates)):
                if new_clause.predicates[i] == new_clause.predicates[j]:
                    del new_clause.predicates[j]
                    find = True
                    break
            break
        if find == False:
            break
    return new_clause

def MGU(predicate1, predicate2):
    dic = {} # x = aa key is x, value is aa, 
    for argument1, argument2 in zip(predicate1.arguments, predicate2.arguments):
        if len(argument1) == 1 and len(argument2) == 1:
            dic[argument1] = argument2
        elif len(argument1) == 1 and len(argument2) != 1: 
            dic[argument1] = argument2
        elif len(argument1) != 1 and len(argument2) == 1:
            dic[argument2] = argument1
        elif len(argument1) != 1 and len(argument2) != 1 and argument1 != argument2:
            return False
    return dic

def is_match(predicate1, predicate2):
    if predicate1.name == predicate2.name and predicate1.negated != predicate2.negated:
        for argument1, argument2 in zip(predicate1.arguments, predicate2.arguments):
            if len(argument1) != 1 and len(argument2) != 1 and argument1 != argument2:
                return False
        return True
    return False
def debug_info(KB):
    print("\n----------Debug Info------------")
    print("Number of clause in KB: ", len(KB))
    count = 1
    for clause in KB:
        print("Clause:", count,"\t",sep="",end="")
        count = count+1
        clause.print_clause()
    print("---------------------------------\n")

def display_info(new_clause, replace, signal):
    # [2a, 5a](bb:x) => (¬Green(aa), Green(bb))
    info = "[" + signal + "]"
    for key, value in replace.items():
        info += "(" + key + "=" + value + ")"
    info += " => "
    print(info, end="")
    new_clause.print_clause()
def resolution_algorithm(KB, debug = False): #TODO 为什么过了一个循环之后，A(tony)就变成负的了
    visited = []
    goal_test = False
    while True:
        if goal_test ==True:
            break
        # 1. Select two clauses to resolve
        find = False
        for i in range(len(KB)):
            for j in range(i+1, len(KB)):
                clause1 = KB[i]
                clause2 = KB[j]
                for index1, predicate1 in enumerate(clause1.predicates):
                    for index2, predicate2 in enumerate(clause2.predicates):
                        signal = str(i+1) + int_to_char(index1) +", " +str(j+1) + int_to_char(index2)
                        if is_match(predicate1, predicate2) and signal not in visited:
                            replace = MGU(predicate1, predicate2)
                            if replace != False:
                                visited.append(signal)
                                find = True
                                new_clause = resolve(clause1, clause2, predicate1, predicate2, replace)
                                if debug:
                                    debug_info(KB)
                                display_info(new_clause, replace, signal)
                                if len(new_clause.predicates) == 0:
                                    goal_test = True
                                    break
                                # KB.append(new_clause)
                                if new_clause not in KB:
                                    KB.append(new_clause)
                            if find == True:
                                break
                        if find == True:
                            break
                    if find == True:
                        break
                if find == True:
                    break
            if find == True:
                break
        if find == False:
            break
    if goal_test == True:
        print("\nSo SATISFY\n")
    else:
        print("\nSO NOT SATISFY\n")
            
        

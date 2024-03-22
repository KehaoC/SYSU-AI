import re

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
    
class Clause:
    def __init__(self, predicates):
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

def resolve(KB, clause1, clause2, predicate1, predicate2, visited):
    # Input 2 clauses
    # Output a new clause if successful
    index1 = ""
    index2 = ""
    for i, c in enumerate(KB):
        if c is clause1:
            index1 += str(i+1)
            for j, p in enumerate(clause1.predicates):
                if p is predicate1:
                    index1 += int_to_char(j)
        if c is clause2:
            index2 += str(i+1)
            for j, p in enumerate(clause2.predicates):
                if p is predicate2:
                    index2 += int_to_char(j)
    dic = {}
    replacable = True
    for i in range(len(predicate1.arguments)):
        if len(predicate1.arguments[i]) != 1 and len(predicate2.arguments[i]) != 1:
            replacable = False
            break
        if len(predicate1.arguments[i]) == 1:
            dic[predicate1.arguments[i]] = predicate2.arguments[i]
        else:
            dic[predicate2.arguments[i]] = predicate1.arguments[i]

    signal = (index1, index2)
    if not replacable or signal in visited:
        return
    else:
        visited.append(signal)
        new_clause = Clause(clause1.predicates + clause2.predicates)
        new_clause.predicates.remove(predicate1)
        new_clause.predicates.remove(predicate2)
        KB.append(new_clause)
        for predicate in new_clause.predicates:
            for key, value in dic.items():
                predicate.arguments = [value if arg == key else arg for arg in predicate.arguments]
    info = f"R[{index1},{index2}]"
    for key, value in dic.items():
        info += f"({key}={value})"
    info += f" => {new_clause.print_clause(direct=False)}"
    print(info)
    # clause1.predicates.remove(predicate1)
    # clause2.predicates.remove(predicate2)
    # clause1.predicates.extend(clause2.predicates)
    # for predicate in clause1.predicates:
    #     for key, value in dic.items():
    #         predicate.arguments = [key if arg == value else arg for arg in predicate.arguments]
    # KB.remove(clause2)
    
    # # KB = [c for c in KB if len(c.predicates) > 0]
    # for clause in KB:
    #     if clause.predicates == []:
    #         KB.remove(clause)

    # info = f"R[{index1},{index2}]"
    # for key, value in dic.items():
    #     info += f"({key}={value})"
    # info += f" => {clause1.print_clause(direct=False)}"
    # print(info)


def is_match(predicate1, predicate2):
    return predicate1.name == predicate2.name and predicate1.negated != predicate2.negated

def find_clause2(clause1, KB, visited):
    for predicate1 in clause1.predicates:
        for clause2 in KB:
            for predicate2 in clause2.predicates:
                if is_match(predicate1, predicate2):
                    resolve(KB, clause1, clause2, predicate1, predicate2, visited)
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

def resolution_algorithm(KB, debug = False):
    # Main loop here
    goal_test = False
    visited = []
    while True:
        for clause1 in KB:
            goal_test = find_clause2(clause1, KB, visited) # TODO Find the same all the time
            if goal_test == True:
                if debug:
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


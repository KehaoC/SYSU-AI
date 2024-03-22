import main as logic
def test1():
    """test the input and output. Finish the data transforming."""
    test = logic.parse_input("(¬C(y), ¬L(y, rain))")
    print(test.print_clause())

def test2():
    """test in dataset1"""
    input_text1 = """
11
A(tony)
A(mike)
A(john)
L(tony, rain)
L(tony, snow)
(¬A(x), S(x), C(x))
(¬C(y), ¬L(y, rain))
(L(z, snow), ¬S(z))
(¬L(tony, u), ¬L(mike, u))
(L(tony, v), L(mike, v))
(¬A(w), ¬C(w), S(w))
""" 
    
    input_text2 = """
5
On(aa, bb)
On(bb, cc)
Green(aa)
¬Green(cc)
(¬On(x, y), ¬Green(x), Green(y))
"""

    input_text = input_text1.strip().split("\n")[1:]
    print("Input data: ",input_text, sep="\n")

    KB = []
    for input in input_text:
        KB.append(logic.parse_input(input)) 
    
    print("\nData loading...\n")
    print("Clause number: ", len(KB))
    for clause in KB:
        clause.print_clause()
    
    print("\nLoad finished, processing...\n")
    logic.resolution_algorithm(KB, debug = True)

    print("Excaution is finished, quitting...")



import main as logic

def test_deepcopy():
    """Test the deepcopy method of the Predicate class."""
    # Create a Predicate object
    predicate = logic.Predicate("A", ["x", "y"], True)

    # Perform a deep copy of the Predicate object
    print(predicate.print_predicate())
    copied_predicate = predicate.clone()
    copied_predicate.arguments[0] = "z"
    print(predicate.print_predicate())
    print(copied_predicate.print_predicate())

#test_deepcopy()
test2()
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

    input_text = input_text2.strip().split("\n")[1:]
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

    print("\nProcessing ends and below is the result.")
    print("Here is your knowledge in the end:")
    print("Number of clauses in KB: ", len(KB),"\n")
    count = 1
    for clause in KB:
        print("Clause:", count,"\t",sep="",end="")
        count = count+1
        clause.print_clause()

    if len(KB) != 0:
        print("\nSo SATISFY\n")
    else:
        print("\nSO NOT SATISFY\n")
    
    print("Excaution is finished, quitting...")

test2()
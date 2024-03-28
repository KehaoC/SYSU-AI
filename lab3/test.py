import main as test

def test1():
    node = test.initialState()
    print(node.state)
    print("Initialization finished...")
    isTarget = test.goalTest(node.state)
    print(f'Found target:{isTarget}')
    print("Finding '0' ...")
    index = test.getIndex(state=node.state)
    print(index)

    print(test.heuristic_normal(node.state))

test1()
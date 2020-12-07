import treelib as tl

from utils import uid, join, absorb, collapse

def test_join():
    t1, t2 = get_test_trees()

    t3 = join(t1, t2)

    print("T1, T2 Joined:")
    print(t3)

def test_absorb():
    t1, t2 = get_test_trees()

    t3 = absorb(t1, t2)

    print("T2 Absorbed into T1:")
    print(t3)

def test_collapse():
    t1, t2 = get_test_trees()

    t3 = collapse(t1, t2)

    print("T1, T2 Collapsed:")
    print(t3)

def get_test_trees():
    t1 = tl.Tree()
    r1 = uid()
    t1.create_node(tag=-1, identifier=r1)
    t1.create_node(identifier=1, parent=r1)
    t1.create_node(identifier=2, parent=r1)

    t2 = tl.Tree()
    r2 = uid()
    t2.create_node(tag=-1, identifier=r2)
    t2.create_node(identifier=3, parent=r2)
    t2.create_node(identifier=4, parent=r2)
    t2.create_node(identifier=5, parent=r2)

    print("T1:")
    print(t1)

    print("T2:")
    print(t2)

    return t1, t2

if __name__ == '__main__':
    test_join()
    test_absorb()
    test_collapse()

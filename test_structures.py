import CustomDataStructures.CustomArray as Ca
import CustomDataStructures.CustomLinkedList as Cl
import CustomDataStructures.CustomHashTable as Ch
import CustomDataStructures.SQDQ as Sq
import CustomDataStructures.CustomBST as Cb


def run_tests():
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"  PASS  {name}")
        else:
            failed += 1
            print(f"  FAIL  {name}")

    def raises(exc, fn):
        try:
            fn()
        except exc:
            return True
        except Exception:
            return False
        return False

    print("\nRunning self-tests ...")

    # Array
    a = Ca.Array(3)
    check("Array: starts empty, search on empty = -1", len(a) == 0 and a.search(1) == -1)
    check("Array: delete from empty raises", raises(IndexError, lambda: a.delete_at(0)))
    a.append(1)
    a.append(3)
    a.insert(1, 2)
    check("Array: insert in the middle keeps order", a.to_list() == [1, 2, 3])
    check("Array: append when full raises", raises(OverflowError, lambda: a.append(4)))
    check("Array: insert when full raises", raises(OverflowError, lambda: a.insert(0, 9)))
    check("Array: delete at start shifts left", a.delete_at(0) == 1 and a.to_list() == [2, 3])
    check("Array: search found / missing", a.search(3) == 1 and a.search(99) == -1)
    check("Array: bad index raises", raises(IndexError, lambda: a.get(5)))

    # Dynamic array
    d = Ca.DynamicArray(2)
    for i in range(100):
        d.append(i)
    check("DynamicArray: grows past initial capacity", len(d) == 100 and d.capacity >= 100 and d.resizes > 0)
    check("DynamicArray: order preserved after resizes", d.to_list() == list(range(100)))
    d.insert(0, -1)
    check("DynamicArray: insert at start after growth", d.get(0) == -1 and d.get(1) == 0 and len(d) == 101)
    for _ in range(95):
        d.delete_at(len(d) - 1)
    check("DynamicArray: shrinks after many deletes", d.capacity < 128)
    check("DynamicArray: data intact after shrink", d.to_list() == [-1, 0, 1, 2, 3, 4])
    check("DynamicArray: delete from empty raises", raises(IndexError, lambda: Ca.DynamicArray().delete_at(0)))

    # Singly linked list
    s = Cl.SinglyLinkedList()
    check("SLL: delete_first / delete_last on empty raise",
          raises(IndexError, s.delete_first) and raises(IndexError, s.delete_last))
    s.append(2)
    s.prepend(1)
    s.append(3)
    check("SLL: prepend/append order", s.to_list() == [1, 2, 3])
    check("SLL: delete_last", s.delete_last() == 3 and s.to_list() == [1, 2])
    s.append(3)
    check("SLL: delete middle value", s.delete_value(2) and s.to_list() == [1, 3])
    check("SLL: delete head value", s.delete_value(1) and s.to_list() == [3])
    check("SLL: delete missing value returns False", not s.delete_value(42))
    check("SLL: delete last of single element", s.delete_last() == 3 and len(s) == 0 and s.head is None)
    s.append(5)
    check("SLL: search found / missing", s.search(5) == 0 and s.search(9) == -1)

    # Doubly linked list
    dl = Cl.DoublyLinkedList()
    for v in (1, 2, 3):
        dl.append(v)
    dl.prepend(0)
    check("DLL: forward and backward order",
          dl.to_list() == [0, 1, 2, 3] and dl.to_list_reverse() == [3, 2, 1, 0])
    check("DLL: delete_last updates tail", dl.delete_last() == 3 and dl.tail.value == 2)
    check("DLL: delete_first updates head", dl.delete_first() == 0 and dl.head.prev is None
          and dl.to_list() == [1, 2])
    check("DLL: delete middle/head value keeps links", dl.delete_value(1) and dl.head is dl.tail
          and dl.to_list() == [2])
    check("DLL: delete last remaining element empties list",
          dl.delete_value(2) and dl.head is None and dl.tail is None and len(dl) == 0)
    check("DLL: delete on empty raises",
          raises(IndexError, dl.delete_first) and raises(IndexError, dl.delete_last))

    # Stack, Queue, Deque
    st = Sq.Stack()
    for v in (1, 2, 3):
        st.push(v)
    check("Stack: LIFO order", st.pop() == 3 and st.peek() == 2 and len(st) == 2)
    st.pop()
    st.pop()
    check("Stack: pop on empty raises", raises(IndexError, st.pop))
    q = Sq.Queue()
    q.enqueue(1)
    q.enqueue(2)
    check("Queue: FIFO order", q.dequeue() == 1 and q.peek() == 2)
    q.dequeue()
    check("Queue: dequeue on empty raises", raises(IndexError, q.dequeue))
    dq = Sq.Deque()
    dq.add_back(2)
    dq.add_front(1)
    dq.add_back(3)
    check("Deque: both ends", dq.to_list() == [1, 2, 3] and dq.remove_front() == 1
          and dq.remove_back() == 3 and dq.peek_front() == 2 and dq.peek_back() == 2)
    dq.remove_back()
    check("Deque: remove on empty raises", raises(IndexError, dq.remove_front))

    # Hash table
    h = Ch.HashTable(capacity=1, max_load=1e9)
    for i in range(10):
        h.put(i, i * i)
    check("HashTable: collisions all stored (one chain)",
          all(h.get(i) == i * i for i in range(10)) and h.stats()["longest chain"] == 10)
    h.put(3, "x")
    check("HashTable: put on existing key updates", h.get(3) == "x" and len(h) == 10)
    check("HashTable: delete from middle of chain", h.delete(5) and not h.contains(5) and len(h) == 9)
    check("HashTable: delete missing returns False", not h.delete(12345))
    h2 = Ch.HashTable()
    for i in range(1000):
        h2.put(i, i)
        h2.put(f"k{i}", i)
    check("HashTable: resize keeps every key (int and str)",
          all(h2.get(i) == i and h2.get(f"k{i}") == i for i in range(1000))
          and h2.resizes > 0 and len(h2) == 2000)
    h2.put(-7, "neg")
    check("HashTable: negative key and default value", h2.get(-7) == "neg" and h2.get("nope", "d") == "d")

    # BST
    t = Cb.BST()
    for k in (50, 30, 70, 20, 40, 60, 80):
        t.insert(k)
    check("BST: in-order is sorted", t.inorder() == [20, 30, 40, 50, 60, 70, 80] and len(t) == 7)
    check("BST: duplicate rejected", not t.insert(50) and len(t) == 7)
    check("BST: search found / missing", t.search(60) and not t.search(65))
    check("BST: delete leaf", t.delete(20) and t.inorder() == [30, 40, 50, 60, 70, 80])
    t.insert(65)
    check("BST: delete node with one child", t.delete(60) and t.inorder() == [30, 40, 50, 65, 70, 80])
    check("BST: delete root with two children",
          t.delete(50) and t.root.key == 65 and t.inorder() == [30, 40, 65, 70, 80])
    check("BST: delete missing returns False", not t.delete(999))
    for k in (30, 40, 65, 70, 80):
        t.delete(k)
    check("BST: deleting everything empties the tree",
          t.root is None and len(t) == 0 and not t.delete(1) and t.height() == 0)
    t2 = Cb.BST()
    for i in range(1, 201):
        t2.insert(i)
    check("BST: sorted insertion makes a chain (height = n)", t2.height() == 200)
    check("BST: search deep in the chain", t2.search(200))
    check("BST: delete root of a chain", t2.delete(1) and t2.root.key == 2 and t2.height() == 199)

    print(f"\n  {passed} passed, {failed} failed")


if __name__ == "__main__":
    run_tests()
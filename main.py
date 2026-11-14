import CustomDataStructures.CustomArray as Ca
import CustomDataStructures.CustomLinkedList as Cl
import CustomDataStructures.CustomHashTable as Ch
import CustomDataStructures.SQDQ as Sq
import CustomDataStructures.CustomBST as Cb
from test_structures import run_tests

import itertools
import random
import time

SIZES = [100, 1000, 10000]
SENTINEL = -5   # value never stored, used for "not found" searches


# ---------- helpers ----------
def measure(op, undo=None, max_reps=200, budget=0.25):
    total_ns, reps = 0, 0
    while reps < max_reps:
        t0 = time.perf_counter_ns()
        op()
        total_ns += time.perf_counter_ns() - t0
        reps += 1
        if undo:
            undo()
        if total_ns / 1e9 > budget and reps >= 5:
            break
    return total_ns / reps / 1000.0


def fmt(v):
    return "-" if v is None else f"{v:,.2f}"


def print_table(title, n, results, cols):
    name_w, col_w = 36, 22
    print(f"\n=== {title} | n = {n:,} | times in microseconds ===")
    header = "Operation".ljust(name_w) + "".join(c.rjust(col_w) for c in cols) + "Fastest".rjust(col_w)
    print(header)
    print("-" * len(header))
    for op, row in results.items():
        present = {c: row[c] for c in cols if row.get(c) is not None}
        fastest = min(present, key=present.get) if len(present) > 1 else "-"
        print(op.ljust(name_w)
              + "".join(fmt(row.get(c)).rjust(col_w) for c in cols)
              + fastest.rjust(col_w))


# ---------- option 1: arrays and linked lists ----------
def build_seq(name, n):
    if name in ("Array", "Dynamic Array"):
        s = Ca.Array(n + 10) if name == "Array" else Ca.DynamicArray()
        t = time.perf_counter()
        for i in range(n):
            s.append(i)
        return s, (time.perf_counter() - t) * 1e6
    if name == "Singly Linked List":
        s = Cl.SinglyLinkedList()
        for i in range(n):
            s.prepend(i)   # prepend is O(1), append would make the build O(n^2)
        return s, None
    s = Cl.DoublyLinkedList()
    for i in range(n):
        s.append(i)
    return s, None


def seq_ops(s, name):
    """operation name -> (timed function, undo function)"""
    if name in ("Array", "Dynamic Array"):
        return {
            "Insert at start": (lambda: s.insert(0, -1), lambda: s.delete_at(0)),
            "Insert at end": (lambda: s.append(-1), lambda: s.delete_at(s.size - 1)),
            "Delete at start": (lambda: s.delete_at(0), lambda: s.insert(0, -1)),
            "Delete at end": (lambda: s.delete_at(s.size - 1), lambda: s.append(-1)),
            "Search (not found)": (lambda: s.search(SENTINEL), None),
        }
    return {
        "Insert at start": (lambda: s.prepend(-1), s.delete_first),
        "Insert at end": (lambda: s.append(-1), s.delete_last),
        "Delete at start": (s.delete_first, lambda: s.prepend(-1)),
        "Delete at end": (s.delete_last, lambda: s.append(-1)),
        "Search (not found)": (lambda: s.search(SENTINEL), None),
    }


def benchmark_arrays_and_lists():
    names = ["Array", "Dynamic Array", "Singly Linked List", "Doubly Linked List"]
    for n in SIZES:
        print(f"\nRunning n = {n:,} ...")
        results = {}
        for name in names:
            s, build_us = build_seq(name, n)
            if build_us is not None:
                results.setdefault("Build by appending n (total)", {})[name] = build_us
            for op, (do, undo) in seq_ops(s, name).items():
                results.setdefault(op, {})[name] = measure(do, undo)
        print_table("Array vs Dynamic Array vs Linked Lists", n, results, names)


# ---------- option 2: stack, queue, deque ----------
def benchmark_stack_queue_deque():
    cols = ["Stack", "Queue", "Deque"]
    for n in SIZES:
        print(f"\nRunning n = {n:,} ...")
        stack, queue, deque = Sq.Stack(), Sq.Queue(), Sq.Deque()
        for i in range(n):
            stack.push(i)
            queue.enqueue(i)
            deque.add_back(i)

        results = {
            "Add (push/enqueue/add_back)": {
                "Stack": measure(lambda: stack.push(-1), stack.pop),
                "Queue": measure(lambda: queue.enqueue(-1), queue.dequeue),
                "Deque": measure(lambda: deque.add_back(-1), deque.remove_back),
            },
            "Remove (pop/dequeue/remove_front)": {
                "Stack": measure(stack.pop, lambda: stack.push(-1)),
                "Queue": measure(queue.dequeue, lambda: queue.enqueue(-1)),
                "Deque": measure(deque.remove_front, lambda: deque.add_front(-1)),
            },
            "Add at front (Deque only)": {
                "Deque": measure(lambda: deque.add_front(-1), deque.remove_front),
            },
            "Remove at back (Deque only)": {
                "Deque": measure(deque.remove_back, lambda: deque.add_back(-1)),
            },
        }
        print_table("Stack vs Queue vs Deque", n, results, cols)


def undo_redo_app():
    text = ""
    undo, redo = Sq.Stack(), Sq.Stack()
    while True:
        print(f'\nText: "{text}"')
        print("1. Type text")
        print("2. Undo")
        print("3. Redo")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            undo.push(text)              # save the old text so it can be undone
            text += input("Text to add: ")
            redo = Sq.Stack()            # a new edit clears the redo history
        elif choice == "2":
            if undo.is_empty():
                print("Nothing to undo.")
            else:
                redo.push(text)
                text = undo.pop()
        elif choice == "3":
            if redo.is_empty():
                print("Nothing to redo.")
            else:
                undo.push(text)
                text = redo.pop()
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def print_queue_app():
    queue = Sq.Queue()
    job_number = 0
    while True:
        print(f"\nJobs waiting: {queue.to_list()}")
        print("1. Add print job")
        print("2. Print next job")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            job_number += 1
            queue.enqueue(f"job #{job_number}")   # new jobs go to the back
        elif choice == "2":
            if queue.is_empty():
                print("No jobs waiting.")
            else:
                print("Printed", queue.dequeue())  # oldest job leaves first
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def history_app():
    history = Sq.Deque()
    limit = 5
    while True:
        print(f"\nRecent pages (oldest -> newest): {history.to_list()}")
        print("1. Visit page")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            if len(history) == limit:
                print("History full, removed:", history.remove_front())  # drop oldest
            history.add_back(input("Page name: "))
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def sqdq_menu():
    while True:
        print("\n--- SQDQ menu ---")
        print("1. Undo / Redo (Stack)")
        print("2. Print jobs (Queue)")
        print("3. Recent history, last 5 pages (Deque)")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            undo_redo_app()
        elif choice == "2":
            print_queue_app()
        elif choice == "3":
            history_app()
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def stack_queue_deque_menu():
    while True:
        print("\n--- Stack, Queue, Deque ---")
        print("1. Show benchmarks (Stack vs Queue vs Deque)")
        print("2. Go to SQDQ menu (mini apps)")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            benchmark_stack_queue_deque()
        elif choice == "2":
            sqdq_menu()
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


# ---------- option 3: hash table ----------
def test_hash_table():
    print("\n[HASH TABLE DEMO] 5 buckets, auto-resize off, so collisions show up as chains")
    table = Ch.HashTable(capacity=5, max_load=5.0)
    words = ["apple", "banana", "cherry", "date", "elder", "fig",
             "grape", "honey", "iris", "jam", "kiwi", "lemon"]
    for i, w in enumerate(words):
        table.put(w, i)
    table.show()
    print("  stats:", table.stats())
    print("  get('cherry') ->", table.get("cherry"))
    print("  delete('cherry') ->", table.delete("cherry"), "| contains('cherry') ->", table.contains("cherry"))
    print("  delete('missing') ->", table.delete("missing"))
    table.put("apple", 999)
    print("  put('apple', 999) -> get('apple') =", table.get("apple"))

    cols = ["Hash Table", "Array (linear)"]
    for n in SIZES:
        print(f"\nRunning n = {n:,} ...")
        keys = random.sample(range(n * 20), n)
        absent = n * 20 + 7
        ht = Ch.HashTable()
        t = time.perf_counter()
        for k in keys:
            ht.put(k, k)
        build_h = (time.perf_counter() - t) * 1e6
        arr = Ca.DynamicArray()
        t = time.perf_counter()
        for k in keys:
            arr.append(k)
        build_a = (time.perf_counter() - t) * 1e6

        probe = random.sample(keys, min(500, n))
        next_get = itertools.cycle(probe).__next__
        next_arr = itertools.cycle(probe).__next__
        next_del = itertools.cycle(probe).__next__
        cur = [0]

        def do_delete():
            cur[0] = next_del()
            ht.delete(cur[0])

        results = {
            "Build n keys (total)": {cols[0]: build_h, cols[1]: build_a},
            "Insert new key": {cols[0]: measure(lambda: ht.put(absent, 1), lambda: ht.delete(absent))},
            "Search (existing key)": {
                cols[0]: measure(lambda: ht.get(next_get())),
                cols[1]: measure(lambda: arr.search(next_arr())),
            },
            "Search (not found)": {
                cols[0]: measure(lambda: ht.contains(absent)),
                cols[1]: measure(lambda: arr.search(absent)),
            },
            "Delete (existing key)": {cols[0]: measure(do_delete, lambda: ht.put(cur[0], cur[0]))},
        }
        print_table("Hash Table vs linear search", n, results, cols)
        print("  Table stats:", ht.stats())


# ---------- option 4: BST ----------
def show_tree(tree):
    if tree.root is None:
        print("  (empty tree)")
    else:
        tree.display()


def test_bst():
    print("\n[BST DEMO] insert, search, delete")
    t = Cb.BST()
    for k in (50, 30, 70, 20, 40, 60, 80):
        t.insert(k)
    print("  in-order:", t.inorder(), "| height:", t.height())
    show_tree(t)
    print("  search(60) ->", t.search(60), "| search(65) ->", t.search(65))
    print("  insert(50) duplicate ->", t.insert(50))
    print("  delete(20) leaf ->", t.delete(20), t.inorder())
    print("  delete(30) one child ->", t.delete(30), t.inorder())
    print("  delete(50) root, two children ->", t.delete(50), t.inorder())
    print("  delete(999) missing ->", t.delete(999))

    print("\n[SORTED INPUT DEMO] inserting 1..10 in order")
    chain = Cb.BST()
    for k in range(1, 11):
        chain.insert(k)
    show_tree(chain)
    print("  height =", chain.height())

    # sorted insertion is O(n^2), so n = 10,000 takes a couple of seconds
    cols = ["BST (random)", "BST (sorted)"]
    for n in SIZES:
        print(f"\nRunning n = {n:,} ...")
        keys = random.sample(range(n * 10), n)
        orders = {cols[0]: keys, cols[1]: sorted(keys)}
        results = {"Build n keys (total)": {}, "Search (existing key)": {}, "Delete (existing key)": {}}
        heights = {}
        for name, seq in orders.items():
            tree = Cb.BST()
            t0 = time.perf_counter()
            for k in seq:
                tree.insert(k)
            results["Build n keys (total)"][name] = (time.perf_counter() - t0) * 1e6
            heights[name] = tree.height()

            probe = random.sample(keys, min(300, n))
            next_search = itertools.cycle(probe).__next__
            next_del = itertools.cycle(probe).__next__
            cur = [0]

            def do_delete():
                cur[0] = next_del()
                tree.delete(cur[0])

            results["Search (existing key)"][name] = measure(lambda: tree.search(next_search()))
            results["Delete (existing key)"][name] = measure(do_delete, lambda: tree.insert(cur[0]))
        print_table("BST: random vs sorted insertion", n, results, cols)
        print(f"  Tree height: random = {heights[cols[0]]}, sorted = {heights[cols[1]]}, "
              f"best possible = {n.bit_length()}")


# ---------- main menu ----------
def main():
    while True:
        print("\n=== DATA STRUCTURES LAB CONSOLE APP ===")
        print("1. Run Performance Benchmarks (Arrays & Linked Lists)")
        print("2. Stack, Queue, Deque")
        print("3. Test Custom Hash Table (Chaining Collision Resolution)")
        print("4. Test Binary Search Tree (Operations & Sorted Input Impact)")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            benchmark_arrays_and_lists()
        elif choice == "2":
            stack_queue_deque_menu()
        elif choice == "3":
            test_hash_table()
        elif choice == "4":
            test_bst()
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Invalid choice, enter a number from 1 to 5.")


if __name__ == "__main__":
    try:
        print("--- Running Automated Library Tests ---")
        run_tests()
        print("\n--- Starting Console App ---")
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
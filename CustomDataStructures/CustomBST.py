class BSTNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
            self.size = 1
            return True
        cur = self.root
        while True:
            if key == cur.key:
                return False
            if key < cur.key:
                if cur.left is None:
                    cur.left = BSTNode(key)
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = BSTNode(key)
                    break
                cur = cur.right
        self.size += 1
        return True

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def delete(self, key):
        parent, cur = None, self.root
        while cur and cur.key != key:
            parent = cur
            cur = cur.left if key < cur.key else cur.right
        if cur is None:
            return False
        if cur.left and cur.right:
            succ_parent, succ = cur, cur.right
            while succ.left:
                succ_parent, succ = succ, succ.left
            cur.key = succ.key
            parent, cur = succ_parent, succ
        child = cur.left if cur.left else cur.right
        if parent is None:
            self.root = child
        elif parent.left is cur:
            parent.left = child
        else:
            parent.right = child
        self.size -= 1
        return True

    def height(self):
        if self.root is None:
            return 0
        best = 0
        stack = [(self.root, 1)]
        while stack:
            node, d = stack.pop()
            if d > best:
                best = d
            if node.left:
                stack.append((node.left, d + 1))
            if node.right:
                stack.append((node.right, d + 1))
        return best

    def inorder(self):
        out, stack, cur = [], [], self.root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            out.append(cur.key)
            cur = cur.right
        return out

    def display(self):

        def rec(node, depth):
            if node is None:
                return
            rec(node.right, depth + 1)
            print("      " * depth + str(node.key))
            rec(node.left, depth + 1)

        rec(self.root, 0)
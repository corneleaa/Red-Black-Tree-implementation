RED = True
BLACK = False

class Node:
    def __init__(self, key, value, color=RED):
        self.key = key
        self.value = value
        self.color = color
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.root = None

    def is_red(self, node):
        return node is not None and node.color == RED

    def rotate_left(self, h):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x

    def rotate_right(self, h):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        return x

    def flip_colors(self, h):
        h.color = RED
        h.left.color = BLACK
        h.right.color = BLACK

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)
        self.root.color = BLACK

    def _insert(self, h, key, value):
        if h is None:
            return Node(key, value)

        if key < h.key:
            h.left = self._insert(h.left, key, value)
        elif key > h.key:
            h.right = self._insert(h.right, key, value)
        else:
            h.value += value

        if self.is_red(h.right) and not self.is_red(h.left):
            h = self.rotate_left(h)
        if self.is_red(h.left) and self.is_red(h.left.left):
            h = self.rotate_right(h)
        if self.is_red(h.left) and self.is_red(h.right):
            self.flip_colors(h)

        return h

    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node is None:
            return
        self._in_order(node.right, result)
        result.append((node.key, node.value))
        self._in_order(node.left, result)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        return None

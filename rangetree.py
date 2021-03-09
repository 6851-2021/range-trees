import collections
from typing import List, Tuple
from abc import ABC

Point = Tuple[float, ...]

def augment_nodes(node):
    dict_key = 'subtree_size'
    subtree_nodes = 'subtree_nodes'
    coord = 'coord'
    
    if node is None:
        return False
    
    if not node.left and not node.right:
        node.value[dict_key] = 1
        node.value[subtree_nodes] = [node.value[coord]]
        return
    
    augment_nodes(node.left)
    augment_nodes(node.right)
    
    if node.left:
        left_subtree = node.left.value[dict_key]
        left_nodes = node.left.value[subtree_nodes]
    else:
        left_subtree = 0
        left_nodes = []
    if node.right:
        right_subtree = node.right.value[dict_key]
        right_nodes = node.right.value[subtree_nodes]
    else:
        right_subtree = 0
        right_nodes = []
    
    node.value[dict_key] = left_subtree + right_subtree + 1
    node.value[subtree_nodes] = left_nodes + [node.value[coord]] + right_nodes
    return node

def traverse(node):
    if not node:
        yield None
    if node.left:
        yield from traverse(node.left)
    yield node
    if node.right:
        yield from traverse(node.right)

class LeafTree(ABC):
    @property
    @abstractmethod
    def is_internal(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

    @property
    @abstractmethod
    def key(self):
        pass

    @property
    @abstractmethod
    def min(self):
        pass

    @property
    @abstractmethod
    def max(self):
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @classmethod
    def create(cls, points):
        # make sure points are sorted by the x coordinate

        if len(points) == 1: 
            return LeafTreeLeaf(points[0])
            
        elif len(points) == 2:
            left_leaf = LeafTreeLeaf(points[0])
            right_leaf = LeafTreeLeaf(points[1])
            return LeafTreeBranch(left_leaf, right_leaf)

        left = construct_1D_tree(points[:len(points)//2])
        right = construct_1D_tree(points[len(points)//2:])
        
        return LeafTreeBranch(left, right)

            
    def range_query(self, start, end):
        # First phase, traverse until PRED(start)/SUCC(end) diverge
        if self.key < start:
            


class LeafTreeBranch(LeafTree):
    def __init__(self, left, right, data=None):
        self.size = left.size + right.size
        self.key = left.max
        self.min = left.min
        self.max = right.max
        self.left = left
        self.right = right
        self.is_internal = True
        self.data = data

    def __repr__(self):
        return f"Branch({self.left}, {self.right})"

class LeafTreeLeaf(LeafTree):
    is_internal = False
    
    def __init__(self, key, data=None):
        self.size = 1
        self.key = key
        self.min = key
        self.max = key
        self.data = data

    def __repr__(self):
        return f"Leaf({self.key})"

"""
class StaticVanillaRangeTree:
    def __init__(self, points: List[Point]):
        
        assert len(points) > 0
        tree_1D = LeafTree(points)
        for 
        
    def print_tree(self, root):
        for node in traverse(root):
            print('key:', node.key)
            print('val:', node.value)
        print("-------------------")
    
    def construct_tree(self, points):
        assert len(points) > 0
        
        dim = len(points[0])
        
        if dim == 1:
            pass
        else:
            tree = AVL()
            for point in points:
                x, rest = point[0], point[1:]
                tree.insert(x, {'coord': point})
            augment_nodes(tree._root)

            self.print_tree(tree._root)

            for node in traverse(tree._root):
                subtree_nodes = [coord[1:] for coord in node.value['subtree_nodes']]
                recursive_range_tree = StaticVanillaRangeTree(subtree_nodes)
                node.value['sub_range_tree'] = recursive_range_tree
                self.print_tree(recursive_range_tree.tree._root)
            return tree
"""
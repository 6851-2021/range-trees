from bintrees import AVLTree as AVL
import collections
from typing import List, Tuple

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

class StaticVanillaRangeTree:
    def __init__(self, points: List[Point]):
        
        assert len(points) > 0

        self.tree = self.construct_tree(points)
        
    def print_tree(self, root):
        for node in traverse(root):
            print('key:', node.key)
            print('val:', node.value)
        print("-------------------")
    
    def construct_tree(self, points):
        assert len(points) > 0
        
        dim = len(points[0])
        
        if dim == 1:
            tree = AVL()
            for point in points:
                x, rest = point[0], point[1:]
                tree.insert(x, {'coord': point})
            augment_nodes(tree._root)
            return tree
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

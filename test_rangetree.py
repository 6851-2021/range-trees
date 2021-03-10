import unittest
from rangetree import TreeNode

class TestRangeTree(unittest.TestCase):

    def test_pred(self):
        for num in [2, 4, 10, 17, 127]:
            tree = TreeNode.create_from_sorted_list(range(0, num * 2, 2))
            self.assertIsNone(tree.pred(0))
            for k in range(1, num * 2 + 2, 2):
                pred = tree.pred(k).key
                self.assertEqual(pred, max(v for v in range(0, num * 2, 2) if v < k))

    def test_traverse(self):
        tree = TreeNode.create_from_sorted_list(range(23))
        self.assertEqual([node.key for node in tree.traverse_leaves()], list(range(23)))

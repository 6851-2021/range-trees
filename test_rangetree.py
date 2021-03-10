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

    def test_range_query(self):
        for num in [2, 4, 10, 17, 127]:
            tree_range = range(0, num * 2, 2)
            tree = TreeNode.create_from_sorted_list(tree_range)
            for start in range(-1, num*2 + 1):
                for end in range(start, num*2 + 2):
                    expected_keys = [key for key in tree_range if start <= key <= end]
                    expected_count = len(expected_keys)
                    top_nodes = list(tree.range_query(start, end))
                    actual_count = sum((st.size for st in top_nodes), start=0)
                    all_keys = [d.key for st in top_nodes for d in st.traverse_leaves()]
                    self.assertEqual(expected_count, actual_count)
                    self.assertEqual(all_keys, [key for key in tree_range if start <= key <= end])

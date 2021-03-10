from __future__ import annotations

from dataclasses import dataclass, InitVar, field
from typing import Optional, Generic, TypeVar, Any, List, Tuple, Sequence, Iterator

K = TypeVar("K")
V = TypeVar("V")


@dataclass(frozen=True)
class TreeNode(Generic[K, V]):
    is_leaf: bool = True
    size: int = 1
    _key: InitVar[Optional[K]] = None
    left: Optional[TreeNode] = None
    right: Optional[TreeNode] = None
    value: Optional[V] = None
    key: K = field(init=False)
    min: K = field(init=False)
    max: K = field(init=False)

    def __post_init__(self, _key: Optional[K]):
        if _key is not None:
            object.__setattr__(self, 'key', _key)
            object.__setattr__(self, 'min', self.key)
            object.__setattr__(self, 'max', self.key)
        else:
            assert not self.is_leaf
            object.__setattr__(self, 'key', self.left.max)
            object.__setattr__(self, 'min', self.left.min)
            object.__setattr__(self, 'max', self.right.max)

    def __repr__(self):
        if self.is_leaf:
            return f"Leaf({self.key})"
        else:
            return f"Node({self.left}, {self.right})"

    @classmethod
    def create_leaf(cls, key, value=None) -> TreeNode[K]:
        return cls(_key=key, value=value)

    @classmethod
    def create_internal(cls, left: TreeNode, right: TreeNode, value=None) -> TreeNode[K]:
        return cls(is_leaf=False, left=left, right=right, value=value, size=left.size + right.size)

    @classmethod
    def create_from_sorted_list(cls, keys: Sequence[K], values: Optional[Sequence[V]] = None) -> TreeNode[K]:
        assert keys
        if values is not None:
            assert len(values) == len(keys)
        else:
            values = [None] * len(keys)
        nodes: List[TreeNode[K]] = [cls.create_leaf(k, v) for k, v in zip(keys, values)]
        while len(nodes) > 1:
            new_nodes = [TreeNode.create_internal(nodes[i], nodes[i + 1]) for i in range(0, len(nodes) - 1, 2)]
            if len(nodes) % 2 != 0:
                new_nodes.append(nodes[-1])
            nodes = new_nodes
        return nodes[0]

    def search(self, key: K, *, path: Optional[List] = None) -> Optional[TreeNode[K]]:
        if path is not None:
            path.append(self)

        if self.is_leaf:
            if self.key == key:
                return self
            else:
                return None

        if key <= self.key:
            return self.left.search(key, path=path)
        else:
            return self.right.search(key, path=path)

    def pred(self, key: K, *, path: Optional[List] = None) -> Optional[TreeNode[K]]:
        if path is not None:
            path.append(self)
        if self.is_leaf:
            if key > self.key:
                return self
            else:
                return None

        if key > self.right.max:
            return self.right.max_node(path=path)
        if key > self.right.min:
            assert not self.right.is_leaf  # cannot be leaf, as self.right.min != self.right.max
            return self.right.pred(key, path=path)
        if key > self.left.max:
            return self.left.max_node(path=path)
        else:
            return self.left.pred(key, path=path)

    def succ(self, key: K, *, path: Optional[List] = None) -> Optional[TreeNode[K]]:
        if path is not None:
            path.append(self)
        if self.is_leaf:
            if key < self.key:
                return self
            else:
                return None
        if key < self.left.min:
            return self.left.min_node(path=path)
        if key < self.left.max:
            assert not self.left.is_leaf
            return self.left.succ(key, path=path)
        if key < self.right.min:
            return self.right.min_node(path=path)
        else:
            return self.right.succ(key, path=path)

    def max_node(self, *, path: Optional[List] = None) -> TreeNode[K]:
        if path is not None:
            path.append(self)

        if self.is_leaf:
            return self
        return self.right.max_node(path=path)

    def min_node(self, *, path: Optional[List] = None) -> TreeNode[K]:
        if path is not None:
            path.append(self)

        if self.is_leaf:
            return self
        return self.left.min_node(path=path)

    def range_query(self, start: K, end: K) -> Sequence[TreeNode[K, V]]:
        pred_path = []
        succ_path = []
        pred_result = self.pred(start, path=pred_path)
        succ_result = self.succ(end, path=succ_path)
        if pred_result is None and succ_result is None:
            return [self]  # The entire tree is within the range; this handles the one element case as well
        split_idx = None  # Last index where pred_path is equal to succ_path
        for split_idx, (pred_node, succ_node) in enumerate(zip(pred_path[1:], succ_path[1:]), start=0):
            if pred_node is not succ_node:
                break
        pred_top_trees = []
        if pred_path[-1].key >= start:
            pred_top_trees.append(pred_path[-1])
        for i in range(len(pred_path) - 1, split_idx):
            if pred_path[i - 1].left is pred_path[i]:
                pred_top_trees.append(pred_path[i].right)
        succ_top_trees = []
        for i in range(split_idx, len(succ_path) - 1):
            if succ_path[i].right is succ_path[i + 1]:
                succ_top_trees.append(succ_path[i].left)
        return pred_top_trees + succ_top_trees

    def traverse(self) -> Iterator[TreeNode[K, V]]:
        if self.is_leaf:
            yield self
        else:
            yield from self.left.traverse()
            yield from self.right.traverse()



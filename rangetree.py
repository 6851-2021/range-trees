import collections
from typing import List, Tuple
from sbbst import sbbst as SBBST

Point = Tuple[float, ...]


class StaticVanillaRangeTree:
    def __init__(self, points: List[Point], dim: int = 0):
        """Recursively construct a range tree on k-dimensional data."""
        assert len(points[0]) >= 1
        #assert len(points[0]) == dim
        if dim == 1:
            return SBBST([point[0] for point in points])
        first_coords = [point[dim - 1] for point in points]
        tree = SBBST(first_coords)

        
        # for point in points:
        #     #fix this; needs to insert all the nodes in the subtree
        #     tree.insert(StaticVanillaRangeTree(points, dim - 1), point[dim - 1])

    def query(self, p1: Point, p2: Point) -> List[Point]:
        """Returns points in the k-dimensional box formed by p1 and p2."""
        # TODO: Return a generator instead of a list so that we only
        # read points we need.
        pass


if __name__ == '__main__':
    pass
class BinaryHeap:
    def __init__(self):
        self.heap = []
        self.position_map = {}

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position_map[self.heap[i][1]], self.position_map[self.heap[j][1]] = \
            self.position_map[self.heap[j][1]], self.position_map[self.heap[i][1]]

    def push(self, item):
        self.heap.append(item)
        self.position_map[item[1]] = len(self.heap) - 1
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            item = self.heap.pop()
            del self.position_map[item[1]]
            return item

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.position_map[self.heap[0][1]] = 0
        del self.position_map[root[1]]
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        while index > 0:
            parent_index = self.parent(index)
            if self.heap[index][0] < self.heap[parent_index][0]:
                self.swap(index, parent_index)
                index = parent_index
            else:
                break

    def _heapify_down(self, index):
        size = len(self.heap)
        while True:
            left = self.left_child(index)
            right = self.right_child(index)
            smallest = index

            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == index:
                break

            self.swap(index, smallest)
            index = smallest

    def update(self, item):
        if item[1] not in self.position_map:
            return

        index = self.position_map[item[1]]
        self.heap[index] = item

        parent_index = self.parent(index)
        if index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self._heapify_up(index)
        else:
            self._heapify_down(index)


    def peek(self):
        return self.heap[0] if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def __str__(self):
        return str(self.heap)


# Example Usage
if __name__ == "__main__":
    heap = BinaryHeap()
    heap.push((3, "C"))
    heap.push((1, "A"))
    heap.push((2, "B"))
    heap.push((4, "D"))

class BinaryHeap:
    def __init__(self):
        """Initialize an empty binary heap"""
        self.heap = []

    def parent(self, index):
        """Return the index of the parent of the node at index"""
        return (index - 1) // 2

    def left_child(self, index):
        """Return the index of the left child of the node at index"""
        return 2 * index + 1

    def right_child(self, index):
        """Return the index of the right child of the node at index"""
        return 2 * index + 2

    def swap(self, i, j):
        """Swap two elements in the heap"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def push(self, item):
        """
        Insert a new item into the heap.
        item: (priority, value) where priority is used for sorting.
        """
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        """Remove and return the item with the smallest priority"""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        """Move the node at index up to maintain heap property"""
        while index > 0:
            parent_index = self.parent(index)
            if self.heap[index][0] < self.heap[parent_index][0]:  # Compare priorities
                self.swap(index, parent_index)
                index = parent_index
            else:
                break

    def _heapify_down(self, index):
        """Move the node at index down to maintain heap property"""
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

    def update(self, item, new_priority):
        """Update the priority of an existing item and re-heapify."""
        if item not in self.position_map:
            raise KeyError("Item not found in heap.")

        index = self.position_map[item]
        self.heap[index] = (new_priority, item[1]) # Update the item at the correct index.

        # Decide whether to heapify up or down
        parent_index = self.parent(index)
        if index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self._heapify_up(index)
        else:
            self._heapify_down(index)

    def peek(self):
        """Return the item with the smallest priority without removing it"""
        return self.heap[0] if self.heap else None

    def is_empty(self):
        """Check if the heap is empty"""
        return len(self.heap) == 0

    def size(self):
        """Return the number of elements in the heap"""
        return len(self.heap)

    def __str__(self):
        """Return a string representation of the heap"""
        return str(self.heap)


# Example Usage
if __name__ == "__main__":
    heap = BinaryHeap()
    heap.push((3, "C"))
    heap.push((1, "A"))
    heap.push((2, "B"))
    heap.push((4, "D"))

    print("Heap after insertions:", heap)

    print("Extracted:", heap.pop())  # Should return (1, "A")
    print("Extracted:", heap.pop())  # Should return (2, "B")
    print("Heap after extractions:", heap)

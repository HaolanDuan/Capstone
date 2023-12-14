import os

class BinaryHeap:
    def __init__(self, maxn, comp):
        self.heap = []
        self.heap_idx = [-1] * (maxn + 10)
        self.comp = comp

    def left(self, parent):
        l = 2 * parent + 1
        if l < len(self.heap):
            return l
        else:
            return -1

    def right(self, parent):
        r = 2 * parent + 2
        if r < len(self.heap):
            return r
        else:
            return -1

    def parent(self, child):
        p = (child - 1) // 2
        if child == 0:
            return -1
        else:
            return p

    def heapswap(self, x, y):
        self.heap_idx[self.heap[x][1]], self.heap_idx[self.heap[y][1]] = self.heap_idx[self.heap[y][1]], self.heap_idx[self.heap[x][1]]
        self.heap[x], self.heap[y] = self.heap[y], self.heap[x]

    def heapifyup(self, in_):
        while True:
            pin = self.parent(in_)

            if in_ >= 0 and pin >= 0 and self.comp(self.heap[in_][0], self.heap[pin][0]):
                self.heapswap(in_, pin)
                in_ = pin
            else:
                break

    def heapifydown(self, in_):
        while True:
            child = self.left(in_)
            child1 = self.right(in_)

            if child >= 0 and child1 >= 0 and self.comp(self.heap[child1][0], self.heap[child][0]):
                child = child1

            if child > 0 and self.comp(self.heap[child][0], self.heap[in_][0]):
                self.heapswap(in_, child)
                in_ = child
            else:
                break

    def as_map(self):
        rtn = {}
        for item in self.heap:
            rtn[item[1]] = item[0]
        return rtn

    def get_elements(self):
        return self.heap

    def get_value(self, idx):
        return self.heap[self.heap_idx[idx]][0]

    def insert(self, index, element):
        self.heap_idx[index] = len(self.heap)
        self.heap.append((element, index))
        self.heapifyup(len(self.heap) - 1)

    def delete_top(self):
        if len(self.heap) == 0:
            print("Heap is Empty")
            return
        self.heapswap(0, len(self.heap) - 1)
        self.heap_idx[self.heap[-1][1]] = -1
        self.heap.pop()
        self.heapifydown(0)

    def modify(self, index, newvalue):
        idx = self.heap_idx[index]
        if self.comp(newvalue, self.heap[idx][0]):
            self.heap[idx] = (newvalue, self.heap[idx][1])
            self.heapifyup(idx)
        else:
            self.heap[idx] = (newvalue, self.heap[idx][1])
            self.heapifydown(idx)

    def extract_top(self):
        return self.heap[0]

    def display(self):
        print("Heap -->  ", end="")
        for p in self.heap:
            print(p[0], end=" ")
        print()

    def size(self):
        return len(self.heap)

    def clear(self):
        while self.size():
            self.delete_top()

    def has_idx(self, idx):
        return self.heap_idx[idx] != -1

    def verify(self):
        for child in range(len(self.heap)):
            p = self.parent(child)
            if p >= 0:
                assert not self.comp(self.heap[child][0], self.heap[p][0])



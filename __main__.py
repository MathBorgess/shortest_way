import pandas as pd
import time
import random

data = pd.read_csv('Airports2.csv')[
    ["Origin_airport", "Destination_airport", "Distance"]]

data_vertex = pd.concat(
    [data["Origin_airport"], data["Destination_airport"]], axis=0).unique()

data_dict = {}

for i in range(len(data_vertex)):
    data_dict[data_vertex[i]] = i

data["Origin_airport"] = data["Origin_airport"].map(data_dict)
data["Destination_airport"] = data["Destination_airport"].map(data_dict)

graph_matrix = len(data_vertex)*[len(data_vertex)*[0]]

for i in range(len(data)):
    graph_matrix[data["Origin_airport"][i]
                 ][data["Destination_airport"][i]] = data["Distance"][i]


def dijkstra_linear(graph, start):
    n = len(graph)
    distance = [float('inf')]*n
    distance[start] = 0
    visited = [False]*n
    antecessor = [-1]*n

    vertex = start
    for _ in range(n):
        visited[vertex] = True

        for j in range(n):
            if graph[vertex][j] != 0 and distance[j] > distance[vertex]+graph[vertex][j]:
                distance[j] = distance[vertex]+graph[vertex][j]
                antecessor[j] = vertex

        less = float('inf')
        for j in range(n):
            if not visited[j] and distance[j] < less:
                vertex = j
                less = distance[j]

    return antecessor


class Element():
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Heap():
    def __init__(self, length):
        self.array_ = length*[0]
        self.size_ = length

    def insert(self, elem):
        self.size_ += 1
        idx = self.size_ - 1
        self.array_[idx] = elem

        while idx != 0 and self.array_[self.parent(idx)].value > self.array_[idx].value:
            self.switch(self.array_, self.parent(idx), idx)
            idx = self.parent(idx)

    def critical(self):
        temp = self.array_[0]
        self.array_[0] = self.array_[self.size_-1]
        self.size_ -= 1
        self.min_heapify(0)
        return temp

    def parent(self, idx):
        return idx // 2

    def left(self, idx):
        return (idx * 2) + 1

    def right(self, idx):
        return (idx * 2) + 2

    def switch(self, array, elem1, elem2):
        aux = array[elem1]
        array[elem1] = array[elem2]
        array[elem2] = aux

    def min_heapify(self, idx):

        if not idx < 0:

            left_idx = self.left(idx)
            right_idx = self.right(idx)

            if left_idx <= self.size_ - 1 and self.array_[left_idx].value < self.array_[idx].value:

                smallest = left_idx
            else:
                smallest = idx

            if right_idx <= self.size_ - 1 and self.array_[right_idx].value < self.array_[smallest].value:

                smallest = right_idx

            if smallest != idx:
                self.switch(self.array_, idx, smallest)
                self.min_heapify(smallest)

    def search(self, key):
        for i in range(self.size_):
            if self.array_[i].key == key:
                return i
        return -1

    def build_min_heap(self):
        for idx in range((self.size_//2), -1, -1):
            self.min_heapify(idx - 1)


def dijkstra_heap(graph, start):
    n = len(graph)
    distance = [float('inf')]*n
    distance[start] = 0
    antecessor = [-1]*n
    visited = [False]*n

    heap = Heap(n)
    heap.array_ = [Element(i, distance[i]) for i in range(n)]
    heap.build_min_heap()

    while heap.size_ != 0:
        u = heap.critical()
        visited[u] = True

        for v in range(n):
            if graph[u][v] != 0 and not visited[v] and distance[v] > distance[u]+graph[u][v]:
                distance[v] = distance[u]+graph[u][v]
                antecessor[v] = u
                heap.array_[heap.search(v)] = Element(v, distance[v])
                heap.build_min_heap()

    return antecessor


def belman_ford(graph, start):
    n = len(graph)
    distance = [float('inf')]*n
    distance[start] = 0
    antecessor = [-1]*n

    for i in range(n):
        for j in range(n):
            if graph[i][j] != 0 and distance[j] > distance[i]+graph[i][j]:
                distance[j] = distance[i]+graph[i][j]
                antecessor[j] = i

    return antecessor


examples = [[random.randint(0, len(
    data_vertex)-1), random.randint(0, len(data_vertex)-1)] for _ in range(1000)]

print("START")
start = time.time()
for example in examples:
    ant = dijkstra_linear(graph_matrix, example[0])
end = time.time()
print("Dijkstra Linear: ", end-start)
start = time.time()
for example in examples:
    ant2 = dijkstra_heap(graph_matrix, example[0])
end = time.time()
print("Dijkstra Heap: ", end-start)
print(ant == ant2)
start = time.time()
for example in examples:
    ant3 = belman_ford(graph_matrix, example[0])
end = time.time()
print("Belman Ford: ", end-start)
print(ant2 == ant3)

print(ant == ant2 and ant2 == ant3)

import heapq

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]
        # Create a list of lists to represent the graph

    def add_edge(self, src, dest, weight):
        self.graph[src].append((dest, weight))
        self.graph[dest].append((src, weight))
        # each unit is a pair(to, weight)

    def dijkstra(self, src, target):
        distances = [float('inf')] * self.V
        distances[src] = 0 # src to itself is 0
        predecessors = [-1] * self.V  # to record pre node
        pq = [(0, src)] # priority queue

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            if current_vertex == target:
                break
            if current_distance > distances[current_vertex]:
                continue   
            for neighbor, weight in self.graph[current_vertex]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance 
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))
        
        path, current = [], target
        while current != -1:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return path, distances[target]

def main():
    m, n = map(int, input().split())
    graph = Graph(m)

    for _ in range(n):
        u, v, w = input().split()
        graph.add_edge(int(u), int(v), int(w))
    
    try:
        while True:
            src, dest = map(int, input().split())
            path, length = graph.dijkstra(src, dest)
            print(f"Min path: {' -> '.join(map(str, path))}, length: {length}")
    except EOFError:
        pass
if __name__ == "__main__":
    main()

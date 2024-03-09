import heapq

class Graph():
    def __init__(self, vertices):
        self.vertices = vertices
        self.adj = [[] for _ in range(vertices)]
        self.name_to_index = {}
        self.index_to_name = {}

    def addVertex(self, name):
        if name not in self.name_to_index:
            index = len(self.name_to_index)
            self.name_to_index[name] = index
            self.index_to_name[index] = name
    
    def addEdge(self, nodeA, nodeB, weight):
        if nodeA not in self.name_to_index:
            self.addVertex(nodeA)
        if nodeB not in self.name_to_index:
            self.addVertex(nodeB)
        indexA = self.name_to_index[nodeA]
        indexB = self.name_to_index[nodeB]
        self.adj[indexA].append((indexB, weight))
        self.adj[indexB].append((indexA, weight))

    def dijkstra(self, src, target):
        distances = [float('inf')] * self.vertices
        distances[src] = 0
        pre = [-1] * self.vertices
        pq = [(0, src)]

        while pq:
            currentDistance, currentNode = heapq.heappop(pq)
            if currentNode == target:
                break
            if currentDistance > distances[currentNode]:
                continue

            for neighbor, weight in self.adj[currentNode]:
                if weight+currentDistance < distances[neighbor]:
                    distances[neighbor] = weight + currentDistance
                    heapq.heappush(pq, (distances[neighbor], neighbor))
                    pre[neighbor] = currentNode 
        
        path, current = [], target
        while current != -1:
            path.append(current)
            current = pre[current]
        path.reverse()

        return path, distances[target]
        
def main():
    vertices, edges = map(int, input().split())
    graph = Graph(vertices)

    for i in range(edges):
        fromNode, toNode, weight =input().split()
        weight = int(weight)
        graph.addEdge(fromNode, toNode, weight)
    
    src, dest = input().split()
    src_index = graph.name_to_index[src]
    dest_index = graph.name_to_index[dest]
    path, length = graph.dijkstra(src_index , dest_index)
    path_names = [graph.index_to_name[node] for node in path]
    print(f"Minpath: {' -> '.join(path_names)}, length = {length}")

if __name__ == "__main__":
    main()
                    

import heapq

class Graph():
    def __init__(self, vertices):
        self.vertices = vertices
        self.adj = [[] for _ in range(vertices)]
    
    def addEdge(self, nodeA, nodeB, weight):
        self.adj[nodeA].append((nodeB, weight))
        self.adj[nodeB].append((nodeA, weight))

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

    for i in range(vertices):
        fromNode, toNode, weight = map(int,(input().split()))
        graph.addEdge(fromNode, toNode, weight)
    
    src, dest = map(int, input().split())
    path, length = graph.dijkstra(src, dest)
    print(f"Minpath: {' -> '.join(map(str,path))}, length = {length}")

if __name__ == "__main__":
    main()
                    

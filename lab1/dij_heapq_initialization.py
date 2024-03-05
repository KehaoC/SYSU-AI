import heapq

class Node:
	def __init__(self, v, distance):
		self.v = v
		self.distance = distance
	
	def __ls__(self, other):
		return self.distance < other.distance # which means "less than"

def dijkstra(v, adj, start):
	visited = [False] * v # create a false list with num = v
	map = {} 			  # create a map which contains the minist distance
	queue = []            # queue is a priority queue

	map[start] = Node(start, 0) #start to start = 0
	heapq.heappush(queue, Node(start,0)) # add node-start to queue

	while queue:
		currentNode = heapq.heappop(queue) # pop the minist node in queue to process
		currentVer = currentNode.v		   # 
		distance = current.distance
		visited[v] = True

		neighborList = adj[currentVer]
		for neighbor in neighborList:
			if neighbor[0] not in map:
				map[neighbor[0]] = Node(currentVer, distance + neighbor[1]
			else:
				sn = map[neighbor[0]]
				if distance + neighbor[1] < sn.distance:
					sn.v = v
					sn.distance = distance + neighbor[1]
				heapq.heappush(queue, Node(neighbor[0], distance + neighbor[1])
	result = [0] * v
	for i in range(v):
		result[i] = map[i].distance
	
	return result

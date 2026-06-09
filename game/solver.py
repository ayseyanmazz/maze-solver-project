from collections import deque

class BFSVisualizer:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.start = (1, 1)
        self.end = (self.rows - 2, self.cols - 2)
        self.reset()

    def reset(self):
        self.queue = deque([self.start])
        self.visited = {self.start}
        self.parent = {self.start: None}
        self.current = self.start
        self.finished = False
        self.path_found = False
        self.shortest_path = []
        self.path_index = 0
        self.animating_path = False

    def get_open_neighbors(self, cell):
        r, c = cell
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.matrix[nr][nc] == 0:
                    neighbors.append((nr, nc))
        return neighbors

    def build_path(self):
        current = self.end
        path = []
        while current is not None:
            path.append(current)
            current = self.parent.get(current)
        path.reverse()
        return path

    def step(self):
        if self.finished:
            return

        if len(self.queue) == 0:
            self.finished = True
            return

        self.current = self.queue.popleft()

        if self.current == self.end:
            self.shortest_path = self.build_path()
            self.path_found = True
            self.animating_path = True
            self.finished = True
            return

        neighbors = self.get_open_neighbors(self.current)
        for neighbor in neighbors:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.parent[neighbor] = self.current
                self.queue.append(neighbor)

    def update_path_animation(self):
        if not self.animating_path:
            return

        if self.path_index < len(self.shortest_path):
            # Kırmızı çizginin hızını buradan ayarlıyoruz. 
            # 1 yerine örneğin 4 adım birden atlarsak çizgi çok daha hızlı çizilir.
            self.path_index += 4 
            
            # İndeksin listenin sonunu aşmasını engelliyoruz
            if self.path_index > len(self.shortest_path):
                self.path_index = len(self.shortest_path)
        else:
            # Animasyon tamamen bittiğinde animasyon bayrağını kapatıyoruz
            self.animating_path = False
            
    def get_visible_path(self):
        return self.shortest_path[:self.path_index]

    def get_queue_size(self):
        return len(self.queue)

    def get_visited_count(self):
        return len(self.visited)

    def get_path_length(self):
        return len(self.shortest_path)
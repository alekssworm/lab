import pygame
import random

WIN_WIDTH, WIN_HEIGHT = 800, 600
CELL_SIZE = 20
ROWS, COLS = WIN_HEIGHT // CELL_SIZE, WIN_WIDTH // CELL_SIZE


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


def generate_maze(width, height):
    maze = [[0] * width for _ in range(height)]
    
    def create_maze(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 0:
                maze[y][x] |= 1 << directions.index((dx, dy))
                maze[ny][nx] |= 1 << directions.index((-dx, -dy))
                create_maze(nx, ny)
    
    create_maze(random.randint(0, width - 1), random.randint(0, height - 1))
    return maze


def solve_maze(maze):
    visited = [[False] * len(maze[0]) for _ in range(len(maze))]
    path = []
    
    def dfs(x, y):
        if x < 0 or x >= len(maze[0]) or y < 0 or y >= len(maze) or visited[y][x]:
            return False
        if x == len(maze[0]) - 1 and y == len(maze) - 1:
            path.append((x, y))
            return True
        
        visited[y][x] = True
        if maze[y][x] & 1 and dfs(x + 1, y):
            path.append((x, y))
            return True
        if maze[y][x] & 2 and dfs(x - 1, y):
            path.append((x, y))
            return True
        if maze[y][x] & 4 and dfs(x, y + 1):
            path.append((x, y))
            return True
        if maze[y][x] & 8 and dfs(x, y - 1):
            path.append((x, y))
            return True
        
        visited[y][x] = False
        return False
    
    dfs(0, 0)
    return path[::-1]


def draw_maze(screen, maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] & 1:
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, y * CELL_SIZE))
            if maze[y][x] & 2:
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE, (y + 1) * CELL_SIZE))
            if maze[y][x] & 4:
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE, (y + 1) * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
            if maze[y][x] & 8:
                pygame.draw.line(screen, WHITE, ((x + 1) * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
                

def draw_path(screen, path):
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        pygame.draw.line(screen, BLUE, (x1 * CELL_SIZE + CELL_SIZE // 2, y1 * CELL_SIZE + CELL_SIZE // 2),
                         (x2 * CELL_SIZE + CELL_SIZE // 2, y2 * CELL_SIZE + CELL_SIZE // 2), 4)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Maze Generator and Solver")
    clock = pygame.time.Clock()
    
    maze = generate_maze(COLS, ROWS)
    path = solve_maze(maze)
    
    running = True
    while running:
        screen.fill(BLACK)
        
        draw_maze(screen, maze)
        draw_path(screen, path)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()



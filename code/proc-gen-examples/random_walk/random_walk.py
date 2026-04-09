import numpy as np
import matplotlib.pyplot as plt
import random

def random_walk_image(grid_size=100, steps=1000):
    grid = np.zeros((grid_size, grid_size))

    x, y = grid_size // 2, grid_size // 2

    directions = [(0,1), (0,-1), (1,0), (-1,0)]

    for _ in range(steps):
        dx, dy = random.choice(directions)

        x = (x + dx) % grid_size
        y = (y + dy) % grid_size

        grid[y, x] += 1

    grid = grid / grid.max() if grid.max() > 0 else grid

    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='terrain')
    plt.axis('off')

    filename = f"random_walk_{grid_size}x{grid_size}_{steps}steps.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()

    print(f"Saved: {filename}")


# Example usage:
if __name__ == "__main__":
    random_walk_image(grid_size=10, steps=10000)
    random_walk_image(grid_size=100, steps=100000)
    random_walk_image(grid_size=200, steps=100000)
    random_walk_image(grid_size=300, steps=1000000)
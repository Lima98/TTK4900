import matplotlib.pyplot as plt
import random

def random_walk_lines(grid_size=100, steps=1000):
    # Start in the middle
    x, y = grid_size // 2, grid_size // 2

    # Store path
    path_x = [x]
    path_y = [y]

    directions = [(0,1), (0,-1), (1,0), (-1,0)]

    def move(x, y, dx, dy):
        x = (x + dx) % grid_size
        y = (y + dy) % grid_size

        return x, y

    path_x = [x]
    path_y = [y]

    for _ in range(steps):
        dx, dy = random.choice(directions)

        new_x = (x + dx) % grid_size
        new_y = (y + dy) % grid_size

        # Detect wrap (big jump)
        if abs(new_x - x) > 1 or abs(new_y - y) > 1:
            # Break the line
            path_x.append(None)
            path_y.append(None)

        x, y = new_x, new_y

        path_x.append(x)
        path_y.append(y)

    # Plot
    plt.figure(figsize=(6, 6), facecolor='white')
    plt.plot(path_x, path_y, color='black', linewidth=0.5)

    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')

    filename = f"random_walk_lines_{grid_size}x{grid_size}_{steps}steps.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0, facecolor='white')
    plt.close()

    print(f"Saved: {filename}")


# Example usage
if __name__ == "__main__":
    random_walk_lines(grid_size=50, steps=500)
    random_walk_lines(grid_size=100, steps=100000)
    random_walk_lines(grid_size=1000, steps=1000000)
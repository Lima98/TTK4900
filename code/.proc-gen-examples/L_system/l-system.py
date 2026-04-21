import matplotlib.pyplot as plt
import numpy as np
from math import pi

iterations = 7

# --- L-system generator ---
def generate_lsystem(axiom, rules, iterations):
    current = axiom
    for _ in range(iterations):
        current = "".join(rules.get(c, c) for c in current)
    return current

# --- Drawing function ---
def draw_lsystem(instructions, angle, step, initial_angle=90):
    x, y = 0, 0
    direction = np.radians(initial_angle)  # FIX: start pointing up
    stack = []

    points_x = [x]
    points_y = [y]

    for cmd in instructions:
        if cmd in ["F", "G"]:  # support both symbols
            x += step * np.cos(direction)
            y += step * np.sin(direction)
            points_x.append(x)
            points_y.append(y)
        elif cmd == "+":
            direction -= np.radians(angle)
        elif cmd == "-":
            direction += np.radians(angle)
        elif cmd == "[":
            stack.append((x, y, direction))
        elif cmd == "]":
            x, y, direction = stack.pop()
            points_x.append(x)
            points_y.append(y)

    return points_x, points_y

# --- Save function ---
def save_plot(x, y, filename):
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, linewidth=0.8)
    plt.axis("equal")
    plt.axis("off")
    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

# --- Examples ---

examples = {
    "sierpinski": {
        "axiom": "F-G-G",
        "rules": {
            "F": "F-G+F+G-F",
            "G": "GG"
        },
        "angle": 120,
        "iterations": iterations,
        "step": 1,
        "initial_angle": 0,
        "filename": "sierpinski.png"
    },

    "plant": {
        "axiom": "X",
        "rules": {
            "X": "F+[[X]-X]-F[-FX]+X",
            "F": "FF"
        },
        "angle": 25,
        "iterations": iterations,
        "step": 1,
        "initial_angle": 90,
        "filename": "plant.png"
    },

    "arrowhead": {
        "axiom": "F",
        "rules": {
            "F": "G-F-G",
            "G": "F+G+F"
        },
        "angle": 60,
        "iterations": iterations,
        "step": 1,
        "initial_angle": 180,
        "filename": "arrowhead.png"
    },

    "bush": {
        "axiom": "F",
        "rules": {
            "F": "FF+[+F-F-F]-[-F+F+F]",
        },
        "angle": 22.5,
        "iterations": iterations,
        "step": 1,
        "initial_angle": 90,
        "filename": "bush.png"
    },

    "chain": {
        "axiom": "F",
        "rules": {
            "F": "FXF",
            "X": "[-F+F+F]+F-F-F+"
        },
        "angle": 60,
        "iterations": iterations,
        "step": 1,
        "initial_angle": 0,
        "filename": "chain.png"
    }

}


# --- Run all examples ---
for name, ex in examples.items():
    instructions = generate_lsystem(
        ex["axiom"],
        ex["rules"],
        ex["iterations"]
    )

    x, y = draw_lsystem(
        instructions,
        ex["angle"],
        ex["step"],
        ex["initial_angle"]
    )

    save_plot(x, y, ex["filename"])
    print(f"Saved {ex['filename']}")
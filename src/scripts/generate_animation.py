"""
A simple script to create a GIF animation of the supermarket simulation.
The code reads from the saved csv file (named: "supermarket_abm_simulation.csv" in the main.py).
"""

import os
from pathlib import Path
import imageio
import matplotlib.pyplot as plt
import pandas as pd

animation_dir = Path("./animation/")
if not os.path.exists("./animation/"):
    animation_dir.mkdir()

agent_df = pd.read_csv("../supermarket_abm_simulation.csv", index_col=0)

colormap = {"Healthy": "green", "Infected": "red", "Risky": "orange", "Exposed": "purple"}


def generate_plot_save(step):
    step_df = agent_df.query("step == @step")
    fig = plt.figure(figsize=(8, 4), dpi=144)
    ax = plt.subplot(111)

    # extent = (0, shelves.shape[1], shelves.shape[0], 0)
    # plt.imshow(shelves, interpolation='nearest', cmap=plt.cm.Reds, extent=extent)

    for state in step_df["state"].unique():
        state_step_df = step_df.query("state == @state")
        plt.scatter(
            state_step_df["y"], state_step_df["x"], c=colormap[state], label=state, s=2
        )

    plt.xlim([0, 25])
    plt.ylim([0, 35])

    #  Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)
    plt.savefig(animation_dir / f"{str(step).zfill(3)}.png")
    plt.close()


for s in range(agent_df.step.values.max()):
    generate_plot_save(s)

image_list = Path("./animation/").glob("*.png")

with imageio.get_writer("supermarket_abm_animation.gif", mode="I") as writer:
    for filename in image_list:
        image = imageio.imread(filename)
        writer.append_data(image)

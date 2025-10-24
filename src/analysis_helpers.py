import numpy as np
import matplotlib.pyplot as plt


def side_by_side_bar_plot(
        x_vals, 
        y_vals_left,
        y_vals_right,
        bar_width=0.35,
        title=None,
        x_axis_label=None,
        y_axis_label=None,
        y_vals_left_legend_label=None,
        y_vals_right_legend_label=None,
):
    """Creates a side-by-side bar plot.

    Args:
        x_vals (Iterable[str, int or float]): The x values to be plotted.
        y_vals_left (Iterable[int or float]): The heights of the left set of bars.
        y_vals_right (Iterable[int or float]): The heights of the right set of bars.
        bar_width (int or float): Width of a singular bar.
        title (str): The title of the plot.
        x_axis_label (str): Label for the x-axis.
        y_axis_label (str): Label for the y-axis.
        y_vals_left_legend_label (str): Legend label for y_vals_left.
        y_vals_right_legend_label (str): Legend label for y_vals_right.
    """
    # X-axis positions for the categories
    x_positions = np.arange(len(x_vals))

    # Plot
    bars_left = plt.bar(x_positions - bar_width/2, y_vals_left, bar_width, label=y_vals_left_legend_label)
    bars_right = plt.bar(x_positions + bar_width/2, y_vals_right, bar_width, label=y_vals_right_legend_label)

    # Adding value labels to the bars
    plt.bar_label(bars_left, padding=1)
    plt.bar_label(bars_right, padding=1)

    # Adding labels and title
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.title(title)
    plt.xticks(x_positions, x_vals) # Set x-axis tick labels
    
    # Only show legend if at least one legend label is provided
    if y_vals_left_legend_label or y_vals_right_legend_label:
            plt.legend()
    
    plt.tight_layout()
    plt.show()
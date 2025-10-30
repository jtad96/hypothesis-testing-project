import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def distribution_plots(
        sample_a, 
        sample_b,
        sample_a_label,
        sample_b_label,
        title,
        x_axis_label,
        figsize=(12, 5),
        bar_width=0.35,
        gap=0,
        include_bar_value_labels=True,
        bar_label_font_size=7
):
    """Creates two side-by-side bar plots given two sample populations with categorical data. One showing counts, and the other showing percentages.

    Args:
        sample_a (Iterable): The first sample population to be plotted.
        sample_b (Iterable): The second sample population to be plotted.
        sample_a_label (str): The label for the first sample population. Will be used to denote sample_a in the legend.
        sample_b_label (str): The label for the second sample population. Will be used to denote sample_b in the legend.
        title (str): The super-title for the figure containing both plots.
        x_axis_label (str): The x-axis label for both plots. Should be a description of what both samples contain.
        figsize (tuple[str, str]): The size of the figure containing both plots.
        bar_width (int or float): Width of a singular bar.
        gap (int or float): Gap between side-by-side bars. Default is 0.
        include_bar_value_labels (bool): Whether or not to include value labels for each bar. Default is False.
        bar_label_font_size (int): Font size of bar labels. Only relevant if include_bar_value_labels is True.
    """
    
    value_counts = get_value_counts(sample_a, sample_b)
    categories = value_counts["category"]
    bar_values_left = value_counts["count_x"]
    bar_values_right = value_counts["count_y"]

    fig, ax = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle(title)
    
    # Barplot of counts
    side_by_side_bar_plot(
        categories, 
        bar_values_left,
        bar_values_right,
        ax=ax[0],
        bar_width=bar_width,
        gap=gap,
        include_bar_value_labels=include_bar_value_labels,
        bar_label_font_size=bar_label_font_size,
        title="Count",
        x_axis_label=x_axis_label,
        y_axis_label="Count",
        y_vals_left_legend_label=sample_a_label,
        y_vals_right_legend_label=sample_b_label,
    )

    # Barplot of percentages
    bar_values_left = round(value_counts["proportion_x"] * 100, 1)
    bar_values_right = round(value_counts["proportion_y"] * 100, 1)

    side_by_side_bar_plot(
        categories, 
        bar_values_left,
        bar_values_right,
        ax=ax[1],
        bar_width=bar_width,
        gap=gap,
        include_bar_value_labels=include_bar_value_labels,
        bar_label_font_size=bar_label_font_size,
        title="Percentage",
        x_axis_label=x_axis_label,
        y_axis_label="Percentage",
        y_vals_left_legend_label=sample_a_label,
        y_vals_right_legend_label=sample_b_label,
)


def get_value_counts(sample_a, sample_b):
    """Creates a dataframe of value counts for two sample populations
    Args:
        sample_a (pandas.Series): The first sample.
        sample_b (pandas.Series): The second sample.
    Returns:
        df_sample_counts (pandas.DataFrame): The dataframe containing value counts and percentages for each sample
    """
    # Get review counts for each sample and convert to dataframe - so can be merged into singular dataframe afterwards
    sample_a_counts = pd.DataFrame(sample_a.value_counts()).reset_index(names="category")
    sample_b_counts = pd.DataFrame(sample_b.value_counts()).reset_index(names="category")

    # Create singular dataframe by outer joining samples together
    df_sample_counts = sample_a_counts.merge(sample_b_counts, on="category", how="outer")
    df_sample_counts = df_sample_counts.fillna(0)  # Fill na values that occur when one sample has values that other sample does not. Filled count should be 0.

    # Create proportion columns for both samples
    df_sample_counts["proportion_x"] = df_sample_counts.count_x / df_sample_counts.count_x.sum()
    df_sample_counts["proportion_y"] = df_sample_counts.count_y / df_sample_counts.count_y.sum()

    return df_sample_counts


def side_by_side_bar_plot(
        x_vals, 
        y_vals_left,
        y_vals_right,
        ax=None,
        bar_width=0.35,
        gap=0,
        include_bar_value_labels=False,
        bar_label_font_size=7,
        title=None,
        x_axis_label=None,
        y_axis_label=None,
        y_vals_left_legend_label=None,
        y_vals_right_legend_label=None):
    """Creates a side-by-side bar plot.

    Args:
        x_vals (Iterable[str, int or float]): The x values to be plotted.
        y_vals_left (Iterable[int or float]): The heights of the left set of bars.
        y_vals_right (Iterable[int or float]): The heights of the right set of bars.
        ax (matplotlib.axes._axes.Axes): Optional. A matplotlib axes if barplot is needed as a subplot.
        bar_width (int or float): Width of a singular bar.
        gap (int or float): Gap between side-by-side bars. Default is 0.
        include_bar_value_labels (bool): Whether or not to include value labels for each bar. Default is False.
        bar_label_font_size (int): Font size of bar labels. Only relevant if include_bar_value_labels is True.
        title (str): The title of the plot.
        x_axis_label (str): Label for the x-axis.
        y_axis_label (str): Label for the y-axis.
        y_vals_left_legend_label (str): Legend label for y_vals_left.
        y_vals_right_legend_label (str): Legend label for y_vals_right.
    """

    if ax is None:
         fig, ax = plt.subplots(1, 1)

    # X-axis positions for the categories
    x_positions = np.arange(len(x_vals))

    # Plot
    bars_left = ax.bar(x_positions - bar_width/2 - gap/2, y_vals_left, bar_width, label=y_vals_left_legend_label)
    bars_right = ax.bar(x_positions + bar_width/2 + gap/2, y_vals_right, bar_width, label=y_vals_right_legend_label)

    # Adding value labels to the bars
    if include_bar_value_labels:
        ax.bar_label(bars_left, padding=1, fontsize=bar_label_font_size)
        ax.bar_label(bars_right, padding=1, fontsize=bar_label_font_size)

    # Adding labels and title
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    ax.set_title(title)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_vals) # Set x-axis tick labels
    
    # Only show legend if at least one legend label is provided
    if y_vals_left_legend_label or y_vals_right_legend_label:
            ax.legend()
    
    #ax.tight_layout()
    #plt.show()
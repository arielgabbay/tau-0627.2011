import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches


NAME="formant_scatter"
DESCRIPTION="Given data files and corresponding TextGrid files, displays a scatter plot of formant values in the TextGrid intervals"


def get_grid_intervals(grid, step):
    intervals = []
    with open(grid, "r") as g:
        while "intervals [1]:" != g.readline().strip():
            pass
        while True:
            xmin = int(float(g.readline().split()[-1]) * 1000)
            xmax = int(float(g.readline().split()[-1]) * 1000)
            text = '"'.join(g.readline().split('"')[1:-1])
            if text != "":
                intervals.append((round(xmin / step) * step, int((xmax - xmin) / step), text))
            if not g.readline().strip().startswith("intervals ["):
                break
    return intervals


def plot(inputs, grids, axes, annotate, no_stats):
    data = {}
    axis_names = {str(i): "F%d" % i for i in range(1, 6)}
    axis_names.update({"t": "time", "d": "duration", "n": ""})
    fig, plts = plt.subplots(1 if no_stats else 2)
    if no_stats:
        plt1 = plts
    else:
        plt1, plt2 = plts
        tbl_data = []
    plt1.set(xlabel=axis_names[axes[0]])
    plt1.set(ylabel=axis_names[axes[1]])
    plt1.set_title("Scatter")
    for csv, grid in zip(inputs, grids):
        df = pd.read_csv(csv)
        step = df.iloc[0].end
        intervals = get_grid_intervals(grid, step)
        x = []
        y = []
        names = []
        for start, dur, text in intervals:
            for axis, dst in zip(axes, [x, y]):
                if axis == "t":
                    dst.append(round(start / 1000, 3))
                elif axis == "d":
                    dst.append(round(dur * step / 1000, 3))
                elif axis == "n":
                    dst.append(0)
                else:
                    dst.append(df["F%s_%02d" % (axis, dur)][df.start == start].values[0])
            names.append(text)
        data[csv] = (x, y, names)
    colors = cm.rainbow(np.linspace(0, 1, len(data)))
    handles = []
    for item, color in zip(data.items(), colors):
        csv, d = item
        x, y, names = d
        plt1.scatter(x, y, color=color)
        if annotate:
            for xi, yi, name in zip(*d):
                plt1.annotate(name, (xi, yi))
        if not no_stats:
            stats = []
            if axes[0] not in "tn":
                stats += [np.mean(x), np.std(x)]
            if axes[1] not in "tn":
                stats += [np.mean(y), np.std(y)]
            tbl_data.append(stats)
        handles.append(mpatches.Patch(color=color, label=csv))
    if len(inputs) > 1:
        plt.legend(handles=handles)
    if not no_stats:
        colables = []
        if axes[0] not in "tn":
            colables += [axis_names[axes[0]] + " mean", axis_names[axes[0]] + " std"]
        if axes[1] not in "tn":
            colables += [axis_names[axes[1]] + " mean", axis_names[axes[1]] + " std"]
        plt2.set_title("Statistics", y=0.75)
        plt2.axis("off")
        plt2.table(cellText=tbl_data, colLabels=colables, rowLabels=inputs, rowColours=colors, loc="center")
    plt.show()


def add_args(parser):
    parser.add_argument("input", metavar="csv grid", help="The csv and TextGrid files with the extended formant data and boundaries (can pass several pairs)", nargs="+")
    parser.add_argument("axes", help="The axes to plot. For example, t1 plots time in the horizontal axis and F1 in the vertical; options are t (time), d (duration), n (none), 1, 2, 3, 4, 5")
    parser.add_argument("-t", "--annotate", action="store_true", help="If specified, TextGrid text is added to the scatter plot")
    parser.add_argument("-s", "--no-stats", action="store_true", help="If specified, only the scatter plot is plotted")


def run(args):
    assert len(args.input) % 2 == 0, "Different number of csv/TextGrid files given"
    assert len(args.axes) == 2 and all(c in "ntd12345" for c in args.axes), "Invalid axes: %s" % args.axes
    csvs = [args.input[i] for i in range(0, len(args.input), 2)]
    grids = [args.input[i] for i in range(1, len(args.input), 2)]
    plot(csvs, grids, args.axes, args.annotate, args.no_stats)


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


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
            if g.readline().strip() != 'text = ""':
                intervals.append((xmin, int((xmax - xmin) / step)))
            if not g.readline().strip().startswith("intervals ["):
                break
    return intervals


def plot(inputs, grids, axes):
    data = {}
    axis_names = {str(i): "F%d" % i for i in range(1, 6)}
    axis_names.update({"t": "time", "d": "duration"})
    for csv, grid in zip(inputs, grids):
        df = pd.read_csv(csv)
        step = df.iloc[0].end
        intervals = get_grid_intervals(grid, step)
        x = []
        y = []
        for start, dur in intervals:
            for axis, dst in zip(axes, [x, y]):
                if axis == "t":
                    dst.append(round(start / 1000, 3))
                elif axis == "d":
                    dst.append(round(dur * step / 1000, 3))
                else:
                    dst.append(df["F%s_%02d" % (axis, dur)][df.start == start].values[0])
        data[csv] = (x, y)
    colors = cm.rainbow(np.linspace(0, 1, len(data)))
    for item, color in zip(data.items(), colors):
        csv, axes_code = item
        x, y = axes_code
        plt.scatter(x, y, color=color)
    plt.xlabel(axis_names[axes[0]])
    plt.ylabel(axis_names[axes[1]])
    plt.show()


def add_args(parser):
    parser.add_argument("input", metavar="input_csv", help="The csv file(s) with the extended formant data", nargs="+")
    parser.add_argument("grid", metavar="text_grid", help="The corresponding TextGrid files (one for each csv file given", nargs="+")
    parser.add_argument("axes", help="The axes to plot. For example, t1 plots time in the horizontal axis and F1 in the vertical; options are t (time), d (duration), 1, 2, 3, 4, 5")


def run(args):
    assert len(args.input) == len(args.grid), "Different number of csv/TextGrid files given"
    assert len(args.axes) == 2 and all(c in "td12345" for c in args.axes), "Invalid axes: %s" % args.axes
    plot(args.input, args.grid, args.axes)


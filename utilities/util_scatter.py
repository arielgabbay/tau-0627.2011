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
            text = '"'.join(g.readline().split('"')[1:-1])
            if text != "":
                intervals.append((round(xmin / step) * step, int((xmax - xmin) / step), text))
            if not g.readline().strip().startswith("intervals ["):
                break
    return intervals


def plot(inputs, grids, axes):
    data = {}
    axis_names = {str(i): "F%d" % i for i in range(1, 6)}
    axis_names.update({"t": "time", "d": "duration"})
    fig, (plt1, plt2) = plt.subplots(2)
    plt1.set(xlabel=axis_names[axes[0]])
    plt1.set(ylabel=axis_names[axes[1]])
    plt1.set_title("Scatter")
    plt2.set_title("Statistics", y=0.75)
    plt2.axis("off")
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
                else:
                    dst.append(df["F%s_%02d" % (axis, dur)][df.start == start].values[0])
            names.append(text)
        data[csv] = (x, y, names)
    colors = cm.rainbow(np.linspace(0, 1, len(data)))
    tbl_data = []
    for item, color in zip(data.items(), colors):
        csv, d = item
        x, y, names = d
        plt1.scatter(x, y, color=color)
        for xi, yi, name in zip(*d):
            plt1.annotate(name, (xi, yi))
        tbl_data.append([np.mean(x), np.std(x), np.mean(y), np.std(y)])
    colables = [axis_names[axes[0]] + " mean", axis_names[axes[0]] + " std", axis_names[axes[1]] + " mean", axis_names[axes[1]] + " std"]
    plt2.table(cellText=tbl_data, colLabels=colables, rowLabels=inputs, rowColours=colors, loc="center")
    plt.show()


def add_args(parser):
    parser.add_argument("input", metavar="csv grid", help="The csv and TextGrid files with the extended formant data and boundaries (can pass several pairs)", nargs="+")
    parser.add_argument("axes", help="The axes to plot. For example, t1 plots time in the horizontal axis and F1 in the vertical; options are t (time), d (duration), 1, 2, 3, 4, 5")


def run(args):
    assert len(args.input) % 2 == 0, "Different number of csv/TextGrid files given"
    assert len(args.axes) == 2 and all(c in "td12345" for c in args.axes), "Invalid axes: %s" % args.axes
    csvs = [args.input[i] for i in range(0, len(args.input), 2)]
    grids = [args.input[i] for i in range(1, len(args.input), 2)]
    plot(csvs, grids, args.axes)


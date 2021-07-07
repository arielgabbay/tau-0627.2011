import os
import pandas as pd


NAME="formant_filter"
DESCRIPTION="Build a TextGrid file with boundaries marking intervals with certain mean formant values"


def get_formant_range(df, min_duration, f1=None, f2=None, f3=None, f4=None, f5=None):
    step = df.iloc[0].end
    conditions = []
    for i in range(1, 6):
        fmt_range = eval("f%d" % i)
        if fmt_range is not None:
            conditions.append(df["F%d_%02d" % (i, min_duration / step)] >= fmt_range[0])
            conditions.append(df["F%d_%02d" % (i, min_duration / step)] <= fmt_range[1])
    ret_df = df
    for cond in conditions:
        ret_df = ret_df.loc[cond]
    return ret_df


def build_textgrid(filename, df, min_duration, fmt_ranges):
    step = df.iloc[0].end
    total_dur = df.iloc[-1].end
    with open(filename, 'w') as f:
        f.write('''File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0
xmax = {0}
tiers? <exists>
size = {1}
item []:'''.format(total_dur / 1000, len(fmt_ranges)))
        fmts_count = 1
        for fmt_range in fmt_ranges:
            entries = get_formant_range(df, min_duration, **fmt_range)
            locations = []
            i = 0
            while i < len(entries):
                start = i
                end = i
                i += 1
                while i < len(entries) and entries.iloc[i].start <= entries.iloc[end].start + min_duration:
                    end += 1
                    i += 1
                locations.append((entries.iloc[start].start, entries.iloc[end].start + min_duration))
            intervals = []
            prev = 0
            counter = 1
            for start, end in locations:
                intervals.append((prev, start, ""))
                intervals.append((start, end, str(counter)))
                prev = end
                counter += 1
            intervals.append((end, total_dur, ""))
            f.write('''
    item [{0}]:
        class = "IntervalTier"
        name = "AutoTier{0}"
        xmin = 0
        xmax = {1}
        intervals: size = {2}'''.format(fmts_count, total_dur / 1000, len(intervals)))
            counter = 1
            for start, end, text in intervals:
                f.write('''
        intervals [{0}]:
            xmin = {1}
            xmax = {2}
            text = "{3}"'''.format(counter, start / 1000, end / 1000, text))
                counter += 1
            fmts_count += 1


def fmt_range(arg):
    if arg is None:
        return None
    vals = arg.split("-")
    if len(vals) != 2:
        raise TypeError("Invalid formant range given: " + arg)
    return tuple(float(v) for v in vals)


def add_args(parser):
    parser.add_argument("input", metavar="input_csv", help="The csv file with the extended formant data")
    parser.add_argument("output", metavar="output_textgrid", help="The TextGrid file to build")
    parser.add_argument("duration", type=int, help="The minimal duration (in milliseconds) of segments to find")
    for i in range(1, 6):
        parser.add_argument("-f%d" % i, type=fmt_range, nargs="?", metavar="start-end", help="The range for the formant F%d; e.g. 700-740" % i)
    parser.add_argument("--overwrite", action="store_true", help="Whether to overwrite the output file if it exists")
    parser.add_argument("--formant-file", "-f", action="store", help="A csv containing formant ranges, given instead of formant arguments; each line is put in a separate tier and is of the form 700-750,,2000-2500,,")


def run(args):
    arg_range = any(getattr(args, "f%d" % i) is not None for i in range(1, 6))
    assert args.formant_file is None or not arg_range, "Both formant arguments and formant file given"
    assert args.formant_file is not None or arg_range, "No formant ranges given"
    assert args.overwrite or not os.path.exists(args.output), "%s exists" % args.output
    df = pd.read_csv(args.input)
    if arg_range:
        fmt_ranges = [{"f%d" % i: getattr(args, "f%d" % i) for i in range(1, 6)}]
    else:
        ranges = pd.read_csv(args.formant_file, names=["f%d_raw" % i for i in range(1, 6)])
        ranges = ranges.where(pd.notnull(ranges), None)
        for i in range(1, 6):
            ranges["f%d" % i] = ranges["f%d_raw" % i].apply(fmt_range)
            ranges = ranges.drop("f%d_raw" % i, axis=1)
        fmt_ranges = [dict(row) for _, row in ranges.iterrows()]
    build_textgrid(args.output, df, args.duration, fmt_ranges)


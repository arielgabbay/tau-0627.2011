import sys
import pandas as pd
import numpy as np
from io import StringIO


def extend_formant_durations(fmts, multiples=None, num_formants=5, no_partial_means=True):
    multiples = range(2, 11) if multiples is None else multiples
    for i in [m - 1 for m in multiples]:
        for formant in range(1, num_formants + 1):
            means = []
            for s in range(0, fmts.shape[0] - i):
                vals = fmts.loc[s: s + i, "F%d" % formant]
                if no_partial_means and vals.count() != i + 1:
                    means.append(np.nan)
                else:
                    means.append(vals.mean())
            fmts["F%d_%02d" % (formant, i + 1)] = pd.Series(means)


def load_raw_csv(filename):
    with open(filename, 'r') as f:
        t = f.read()
    t = t.replace("--undefined--", "")
    sio = StringIO(t)
    df = pd.read_csv(sio)
    df.start = (df.start * 1000).apply(lambda x: round(x))  # astype(int) causes some roundoff problems
    df.end = (df.end * 1000).apply(lambda x: round(x))
    return df


def main():
    assert len(sys.argv) in (2, 5), "Invalid number of arguments"
    multiples=None
    if len(sys.argv) == 5:
        try:
            start, stop, step = (int(x) for x in sys.argv[2:])
            multiples = range(start, stop + 1, step)
        except ValueError:
            print("Invalid duration multiplies: %s; format is start stop step (e.g. 1 10 1 for 1, 2, ... 10)")
    fmts = load_raw_csv(sys.argv[1])
    extend_formant_durations(fmts, multiples=multiples)
    fmts.to_csv(".".join(sys.argv[1].split(".")[:-1]) + "_extended.csv")


if __name__ == "__main__":
    main()


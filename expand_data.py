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
    return pd.read_csv(sio)


def main():
    assert len(sys.argv) == 2, "Invalid number of arguments"
    fmts = load_raw_csv(sys.argv[1])
    extend_formant_durations(fmt)


if __name__ == "__main__":
    main()


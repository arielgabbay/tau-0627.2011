# AutoPRAAT

## Prerequisites

You'll need Praat and Python 3 installed on your computer. The Python scripts require the `numpy` and `pandas` packages.

## How to use

### Step 1: extracting raw formant data from Praat

In this step, we'll run a Praat script on the sound to be analyzed which will extract the mean formants on constant intervals throughout the sounds and write them to a `csv` file that can later be analyzed. To do this:

* Open the sound from which the data is to be extracted in Praat (`Open` -> `Read from file...` or *Ctrl+O*).
* Open the script `get_formants.praat` (`Praat` -> `Open Praat script...`). A new window containing the script will open.
* If you want to change the sampling interval from the default 10 milliseconds, change the duration in the line `interval = 0.01` to the desired duration.
* If needed, change the maximal frequency (default is 5500 Hz) in the line `To Formant (burg)... 0 5 5500 0.025 50` to better suit the analyzed speaker. 5500 Hz (the default) is recommended for female speakers; 5000 for male speakers.
* In the `Praat Objects` window, select the sound from which the data is to be extracted.
* In the script window, run the script (`Run` -> `Run` or *Ctrl+R*). Choose the name and location of the `csv` file created by the script when requested. Notice that the script may take a short while to run.
* The file created by the script contains the raw data retrieved from the selected sound and can be opened in Excel, for example.

### Step 2: extending the data

Once we have the raw formant data, we can extend it to contain mean formant values over several intervals using the script `extend_data.py`. Unless specified otherwise, the script adds formant data for multiples of 1 to 10 of intervals; for example, if in step 1 we extracted mean formants for every 10 milliseconds, the script will calculate mean formants for intervals of 20, 30, 40, ..., 100 milliseconds. To specify a different set of interval multiples, pass three arguments of the form `start stop step` to the script; for example, for the default behavior shown before, pass `1 10 1`:

```
python3 extend_data.py formants.csv 1 10 1
```

Where `formants.csv` is the `csv` file generated in step 1. The script will create a new file in the same location as the input file; for example, in the case shown above, a file `formants_extended.csv` will be created.

### Step 3: building a TextGrid with formant filters

In the last step, we'll use the script `formant_filter.py` to build a Praat TextGrid file for the analyzed sound, where boundaries will be set to mark intervals where there are certain formant values. For example, to build a TextGrid where intervals of length at least 50 milliseconds long and a mean F1 value of 700 to 800 Hz are marked, run:

```
python3 formant_filter.py formants_extended.csv newTextGrid.TextGrid 50 -f1 700-800
```

This will create the TextGrid file `newTextGrid.TextGrid` with the desired data. The script refuses to overwrite existing files by default; to overwrite files, pass the `--overwrite` flag.

If you want several tiers, with each tier corresponding to a different set of formant constraints, you can pass the script a `csv` file of the following format:

```
700-800,1000-1500,,,
600-650,,2500-2800,,
```

Passing this file (using `--formant-file`) will create a TextGrid with two tiers: the first will mark intervals where F1 is in the range 700-800 Hz and F2 is in the range 1000-1500 Hz; the second will mark intervals where F1 is in the range 600-650 Hz and F3 is in the range 2500-2800 Hz. Notice that all five formant fields should be included in each line, and can be left empty if no constraints are needed.

## Demonstration

For example, using Steve Ballmer as a guest speaker repeating the word "developers" six times ([link](https://www.youtube.com/watch?v=EMldOiiG1Ko)):

![ballmer](./demo_images/ballmer.png)

We find upon inspection of the first /ɛ/ ("de**vel**opers") that its first three formants are about 847, 1527, 2735 Hz.

Extracting the formants and extending them (steps 1 and 2 above) and applying step 3 to the resulting `ballmer_extended.csv` file thus:

```
python3 formant_filter.py ballmer_extended.csv ballmer.TextGrid 50 -f1 750-900 -f2 1400-1600 -f3 2500-2800
```

Yields the following TextGrid (`ballmer.TextGrid`):

![ballmer_w_text](./demo_images/ballmer_w_text.png)

Where all six /ɛ/ phones are marked (intervals 1, 3, 5, 7, 8 and 10), with a few false-positives where background noise happens to give similar formant values in Praat (a less noisy recording would lead to fewer errors).
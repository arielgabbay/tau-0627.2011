sound$ = selected$("Sound")
select Sound 'sound$'
dur = Get total duration
To Formant (burg)... 0 5 5000 0.025 50
select Formant 'sound$'
interval = 0.01
cur = 0
filename$ = chooseWriteFile$: "Choose destination file", sound$ + "_formants.csv"
writeFileLine: "'filename$'", "start,end,F1,F2,F3,F4,F5"
repeat
	next = cur + interval
	f1 = Get mean... 1 cur next Hertz
	f2 = Get mean... 2 cur next Hertz
	f3 = Get mean... 3 cur next Hertz
	f4 = Get mean... 4 cur next Hertz
	f5 = Get mean... 5 cur next Hertz
	appendFileLine: "'filename$'", cur, ",", next, ",", f1, ",", f2, ",", f3, ",", f4, ",", f5
	cur = next
until cur > dur - interval

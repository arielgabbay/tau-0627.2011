sound$ = selected$("Sound")
select Sound 'sound$'
dur = Get total duration
To Formant (burg)... 0 5 5000 0.025 50
select Formant 'sound$'
interval = 0.1
cur = 0
writeInfoLine: "Start"
repeat
	next = cur + interval
	f2 = Get mean... 2 cur next Hertz
	appendInfoLine: cur, "-", next, ": ", f2
	cur = next
until cur > dur - interval

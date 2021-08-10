#!/bin/bash
gnuplot -persist <<EOF
set terminal x11
set grid
set xdata time
set style data points
set timefmt "%s"
set format x "%H:%M"
plot [$(date --date=yesterday +%s):][12:18] "file.log" using 1:2 lt 4
EOF

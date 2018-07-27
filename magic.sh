#!bin/bash
cd /home/jeff/Documents/TACChrono-master/results/my_output
for d in */
do
	for f in $d/*.ann
	do
		mv $f ../
	done
done

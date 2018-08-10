#!bin/bash
cd /home/jeff/Documents/track2-training_data_1/
for f in *.txt
do
	name=${f%.*}
	mkdir /home/jeff/Documents/TACChrono-master/data/my_input/$name/
	cp $f /home/jeff/Documents/TACChrono-master/data/my_input/$name/
done

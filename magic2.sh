#!bin/bash
cd /home/jeff/TAC_SRIE_2018_Task1_Training_Annotation
for f in *.txt
do
	name=${f%.*}
	mkdir /home/jeff/Documents/TACChrono-master/data/my_input/$name/
	cp $f /home/jeff/Documents/TACChrono-master/data/my_input/$name/
	cp /home/jeff/Documents/TACChrono-master/filler.dct /home/jeff/Documents/TACChrono-master/data/my_input/$name/$name.dct
done

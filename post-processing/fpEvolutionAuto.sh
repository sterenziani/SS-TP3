cd ..
./build.sh
for N in 50 100 250
do
	for SIMULATION in {1..5}
	do
		python3 generator.py $N 0.025
		java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar
		cd post-processing
		python3 animator.py
		python3 fpEvolution.py
		cd ..
	done
done
for GAPSIZE in 0.01 0.025 0.04
do
	for SIMULATION in {1..5}
	do
		python3 generator.py 100 $GAPSIZE
		java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar
		cd post-processing
		python3 animator.py
		python3 fpEvolution.py
		cd ..
	done
done
cd post-processing
python3 fpCombiner.py

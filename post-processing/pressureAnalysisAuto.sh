cd ..
./build.sh
for VELOCITY in 0.5 0.4 0.3 0.2 0.1
do
	for SIMULATION in {1..5}
	do
		python3 generator.py 100 0.02 $VELOCITY
		java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar
		cd post-processing
		python3 pressureAnalysis.py $VELOCITY $SIMULATION
		cd ..
		echo Finished with simulation $SIMULATION
	done
	echo Finished with velocity $VELOCITY
done
cd post-processing
python3 pressureAnalysisCombiner.py
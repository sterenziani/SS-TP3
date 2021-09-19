cd ..
./build.sh
for VELOCITY in 1.0 1.25 1.5 1.75 2.0
do
	for SIMULATION in {1..10}
	do
		python3 generator.py 100 0.02 $VELOCITY
		java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar
		cd post-processing
		python3 pressureAnalysis.py $VELOCITY $SIMULATION
		cd ..
	done
done
cd post-processing
python3 pressureAnalysisCombiner.py
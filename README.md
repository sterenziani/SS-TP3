# SS TP3

## Para ejecutar:
```
./build.sh
java -jar bin/SS-TP3-1.0-SNAPSHOT-jar-with-dependencies.jar
```

## PARA ANIMAR:
```
python3 generator.py
( Ejecutar en Java )
cd post-processing
python3 animator.py
cd ..
```

## PARA SIMULAR Y GENERAR GRÁFICOS:
```
cd post-processing
./fpEvolutionAuto.sh
python3 fpCombiner.py <-- Este último en caso de que quieras volver a graficar los datos generados por el script
```

## OVITO:
```
Abrir animation/output0
Configurarlo como: x, y, vx, vy, radius, color
A la derecha, donde dice "Add modification...", elegir "Combine datasets"
Abajo aparece la ventanita para importar un dataset. Abrir "wall.txt"
Configurarlo como: x, y, radius
Destildar el elemento "Simulation cell"
Seleccionar output0 y en searchPattern poner "output\*"
```

## INPUT:
```
Cant de Particulas
Width Total
Height
GapSize
x	y	vx	vy	m 	r
x	y	vx	vy	m 	r
.....
```

## OUTPUT:
```
N

x	y	vx	vy	r 	m
x	y	vx	vy	r 	m
......
```
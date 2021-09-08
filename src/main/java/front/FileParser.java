package front;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.SortedSet;
import java.util.TreeSet;

import back.Particle;

public class FileParser {
	private int particleCount;
	private double gap;
	private double length;
	private double height;
	private SortedSet<Particle> particles;

	public FileParser() {
		this.particles = new TreeSet<Particle>();
	}
	
    public List<Particle> getParticles(String filePath) throws FileNotFoundException {
        List<Particle> ret = new LinkedList<>();
    	FileInputStream fis = new FileInputStream(filePath);  
        Scanner sc = new Scanner(fis);
        particleCount = sc.nextInt();
        length = sc.nextDouble();
        height = sc.nextDouble();
        gap = sc.nextDouble();
        for (int i = 0; i < particleCount; i++) {
        	double x = sc.nextDouble();
        	double y = sc.nextDouble();
        	double vx = sc.nextDouble();
        	double vy = sc.nextDouble();
        	double mass = sc.nextDouble();
        	double r = sc.nextDouble();
        	Particle p = new Particle(i, x, y, vx, vy, mass, r);    
        	particles.add(p);
        }            
        ret.addAll(particles);
		return ret;       
	}

	public double getGap() {
		return gap;
	}

	public double getHeigth() {
		return height;
	}

	public double getLength() {
		return length;
	}

	public int getN() {
		return particleCount;
	}
}
package front;
import java.util.Collection;

import back.Particle;

public class Input {
    double width;
    double height;
    double gapSize;
    Collection<Particle> particles;
    
	public Input(double width, double height, double gapSize, Collection<Particle> particles)
	{
		this.width = width;
		this.height = height;
		this.gapSize = gapSize;
		this.particles = particles;
	}

	public double getWidth() {
		return width;
	}

	public double getHeight() {
		return height;
	}

	public double getGapSize() {
		return gapSize;
	}

	public Collection<Particle> getParticles() {
		return particles;
	}
	
	public int getN() {
		return particles.size();
	}
}

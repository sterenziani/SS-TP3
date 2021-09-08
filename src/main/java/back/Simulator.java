package back;
import java.util.Collection;
import java.util.SortedSet;
import java.util.TreeSet;

public class Simulator {
	private double width;
	private double height;
	Collection<Particle> particles;
	SortedSet<Event> events;
	double current_time;
	double gapSize;

	public Simulator(Collection<Particle> particles, double width, double height, double gap) {
		this.particles = particles;
		this.events = new TreeSet<>(); 
		this.current_time = 0;
		this.height = height;
		this.width = width;
		this.gapSize = gap;
	}

	public double getTime() {
		return current_time;
	}
	
	public void nextEvent()
	{
		if(events.size() == 0)
			return;
		executeEvent(events.first());
		events.clear();
		findEvents();
	}

	public void findEvents() {
		for(Particle p : particles)
			findEventsForParticle(p);
	}
	
	private void findEventsForParticle(Particle p1)
	{
		double tx = p1.timeUntilWallCollisionX(width, height, gapSize);
		double ty = p1.timeUntilWallCollisionY(height);
		
		// If hitting a wall, add that event
		if(tx >= 0)
			events.add(new Event(null, p1, tx));
		if(ty >= 0)
			events.add(new Event(p1, null, ty));

		// Check for particle collisions
		for(Particle p2 : particles)
		{
			double tc = p1.timeUntilCollision(p2);
			if(tc >= 0)
				events.add(new Event(p1, p2, tc));
		}
	}

	private void executeEvent(Event e)
	{
		Particle a = e.getParticle1();
		Particle b = e.getParticle2();
		double new_time = e.getTime();
		if(a == null && b == null)
			return;
		if(a != null)
			a.addCollision();
		if(b != null)
			b.addCollision();
		
		moveParticles(new_time);
		current_time = current_time + new_time;
		if(a == null && b != null)
			b.bounceX();
		if(a != null && b == null)
			a.bounceY();
		if(a != null && b!= null)
			a.bounce(b);
	}

	private void moveParticles(double time)
	{
		for(Particle p : particles)
		{
			double new_x = p.getVx()*time;
			double new_y = p.getVy()*time;
			p.setX(p.getX() + new_x);
			p.setY(p.getY() + new_y);
		}
	}
}

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
	
	public double getTemperature() {
		double R = 0.0821; // This one is for when pressure is in atm
		return Math.pow(getVrms(), 2) * getMassSum() / (3*R);
	}
	
	private double getVrms()
	{
		double sum = 0;
		for(Particle p : particles)
		{
			double v2 = Math.pow(p.getVx(), 2) + Math.pow(p.getVy(), 2);
			sum += v2;
		}
		return Math.sqrt(sum/particles.size());
	}
	
	private double getMassSum()
	{
		double sum = 0;
		for(Particle p : particles)
			sum += p.getMass();
		return sum;
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
		if( hitsPartitionTip( a, b ) ) {
			if( a != null ) {
				a.bounceY();
			} else {
				b.bounceY();
			}
		} else {
			if(a == null && b != null)
				b.bounceX();
			if(a != null && b == null)
				a.bounceY();
			if(a != null && b!= null)
				a.bounce(b);
		}
	}

	private boolean hitsPartitionTip( Particle a, Particle b ) {
		double delta = 0.0000001;
		if( a != null ) {
			return a.getX() == width/2 && ( a.getY() + a.getRadius() <= (height - gapSize)/2 + delta && a.getX() + a.getRadius() >= (height - gapSize)/2 + delta) || (a.getY() + a.getRadius() <= ((height - gapSize)/2 + gapSize + delta) && a.getY() + a.getRadius() >= ((height - gapSize)/2 + gapSize - delta));
		} else {
			return b.getX() == width/2 && ( b.getY() + b.getRadius() <= (height - gapSize)/2 + delta && b.getX() + b.getRadius() >= (height - gapSize)/2 + delta) || (b.getY() + b.getRadius() <= ((height - gapSize)/2 + gapSize + delta) && b.getY() + b.getRadius() >= ((height - gapSize)/2 + gapSize - delta));
		}
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

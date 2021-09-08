package back;

public class Event implements Comparable<Event>{
	private Particle i;
	private Particle j;
	private double time;
	
	// null i -> i is a horizontal wall
	// null j -> j is a vertical wall
	public Event(Particle i, Particle j, double time)
	{
        this.i = i;
        this.j = j;
        this.time = time;  
    }

    public double getTime() {
    	return time;
    }

    public Particle getParticle1() {
    	return i;
    }

    public Particle getParticle2() {
    	return j;
    }

    @Override
    public int compareTo(Event o) {
    	return Double.compare(this.getTime(), o.getTime());
    }
}

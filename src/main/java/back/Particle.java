package back;

public class Particle implements Comparable<Particle>{
    private int id;
    private double x;
    private double y;
    private double radius;
    private double mass;
    private double vx;
    private double vy;
    static double trajectory;
    private int collisionCounter;

    public Particle(int id, double x, double y, double vx, double vy, double mass, double radius)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.mass = mass;
        this.vx = vx;
        this.vy = vy;
        this.collisionCounter = 0;
    }

    private boolean passesGap(double width, double height, double gap)
    {
    	if( (vx > 0 && x > width/2) || (vx < 0 && x < width/2) )
    		return true;
    	// Moving right, could make it
    	if(vx > 0 && x < width/2 && y > (height/2 - gap/2) && y < (height/2 + gap/2))
    	{
    		double Xf = width/2;
    		double dt = (Xf - x) / vx;
    		double Yf = y + vy*dt;
    		return (Yf > (height/2 - gap/2) && Yf < (height/2 + gap/2));
    	}
    	// Moving left, could make it
    	if(vx < 0 && x > width/2 && y > (height/2 - gap/2) && y < (height/2 + gap/2))
    	{
    		double Xf = width/2;
    		double dt = (Xf - x) / vx;
    		double Yf = y + vy*dt;
    		return (Yf > (height/2 - gap/2) && Yf < (height/2 + gap/2));
    	}
    	return false;
    }
    
    public double timeUntilWallCollisionX(double width, double height, double gap)
    {
        if(vx > 0)
        {
        	// If passes through gap or is on right side
            if(x >= width/2 || passesGap(width, height, gap))
                return ((width - radius - x) / vx); 	// Hit right wall
            else
                return ((width/2 - radius - x) / vx); 	// Hit middle wall, left side
        }
        if(vx < 0)
        {
        	// If passes through gap or is on left side
            if(x < width/2 || passesGap(width, height, gap))
                return ((radius - x) / vx);				// Hit left wall
            else
                return ((width/2 + radius - x) / vx);	// Hit middle wall, right side
        }
        return -1;
    }
    
    public double timeUntilWallCollisionY(double height)
    {
        if(vy > 0)
            return ((height - radius - y) / vy);	// Hit top wall
        if(vy < 0)
            return ((radius - y) / vy);				// Hit bottom wall
        return -1;
    }

    public double timeUntilCollision(Particle b)
    {
    	if (id == b.getId())
    		return -1;
        double radiusSum = radius + b.getRadius();
        double diffX = b.getX() - x;
        double diffY = b.getY() - y;
        double diffVx = b.getVx() - vx;
        double diffVy = b.getVy() - vy;
        double diffVR = (diffVx*diffX) + (diffVy*diffY);
    	double d = Math.pow(diffVR, 2) - (Math.pow(diffVx, 2) + Math.pow(diffVy, 2)) * ((Math.pow(diffX, 2) + Math.pow(diffY, 2)) - Math.pow(radiusSum, 2));
        if(diffVR >= 0 || d < 0)
            return -1;
        return -(diffVR + Math.sqrt(d)) / (Math.pow(diffVx, 2) + Math.pow(diffVy, 2));
    }    
    
    public void bounceX() {
        this.vx = -vx;
    }

    public void bounceY() {
        this.vy = -vy;
    }

    public void bounce(Particle b)
    {
        double radiusSum = radius + b.getRadius();
        double massSum = mass + b.getMass();
        double diffX = b.getX() - x;
        double diffY = b.getY() - y;
        double diffVx = b.getVx() - vx;
        double diffVy = b.getVy() - vy;
        double diffVR = (diffVx*diffX) + (diffVy*diffY);

        double jValue = (2 * mass * b.getMass() * diffVR) / (radiusSum * massSum);
    	double jX = (jValue * diffX) / radiusSum;
    	double jY = (jValue * diffY) / radiusSum;

        vx = vx + jX/mass;
        vy = vy + jY/mass;
        b.setVx(b.getVx() - jX/b.getMass());
        b.setVy(b.getVy() - jY/b.getMass());
    }

    public int getId() {
        return id;
    }

    public double getVx() {
        return vx;
    }

    public double getVy() {
        return vy;
    }
    
    public double getRadius() {
        return radius;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double getMass() {
        return mass;
    }

    public int getCollisionCounter() {
        return collisionCounter;
    }

    public void addCollision() {
    	collisionCounter++;
    }

    public void setX(double x){
        this.x = x;
    }

    public void setY(double y){
        this.y = y;
    }

    public void setVx(double vx){
        this.vx = vx;
    }

    public void setVy(double vy){
        this.vy = vy;
    }

    @Override
	public int compareTo(Particle j) {
        double dx  = j.x - this.x;
        double dy  = j.y - this.y;
		if (Math.sqrt(dx*dx + dy*dy) <= (this.radius*2)) {			
			return 0;
		}
		return this.id - j.id;
	}
}

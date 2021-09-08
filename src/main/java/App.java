import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import java.util.Collection;
import back.Particle;
import back.Simulator;
import front.Input;
import front.Output;
import front.Parser;

public class App {
	
	private static double STABILITY_MARGIN = 0.05;
	private static int STABILITY_TIMESTAMPS = 5;
	
	public static void main(String[] args) throws IOException
	{
		Input input = Parser.ParseInputFile("input.txt");
		Collection<Particle> particles = input.getParticles();
		Output.resetFolder(Output.OUTPUT_DIR);
		Output.createWallFile(input);
		double rightSidePercentage = 0;
		int stable_timestamps = 0;
		
		Simulator simulator = new Simulator(particles, input.getWidth(), input.getHeight(), input.getGapSize());
		simulator.findEvents();
		while(stable_timestamps < STABILITY_TIMESTAMPS)
		{
			Output.outputToFile(particles, simulator.getTime());
			simulator.nextEvent();
			rightSidePercentage = getRightSidePercentage(particles, input);
			if(rightSidePercentage > (0.5 - STABILITY_MARGIN) && rightSidePercentage < (0.5 + STABILITY_MARGIN))
				stable_timestamps++;
			else
				stable_timestamps = 0;
		}
		System.out.println("Finished!");	
	}
	
	public static void writeParticlesToFile(Collection<Particle> particles, int n, double time) throws UnsupportedEncodingException, FileNotFoundException, IOException
	{	
		try (Writer writer = new BufferedWriter(new OutputStreamWriter( new FileOutputStream("output/output_t=" +time + ".txt"), "utf-8")))
		{
			writer.write(String.valueOf(n) + "\n\n");
			for(Particle p: particles)
			{
				writer.write(String.valueOf(p.getX()) + " " + String.valueOf(p.getY()) + " " 
					+ String.valueOf(p.getVx()) + " " + String.valueOf(p.getVy()) 
					+ " " + String.valueOf(p.getRadius()) + " " + String.valueOf(p.getMass()) + "\n");
			}
		}		    	
	}
	
	
	public static double getRightSidePercentage(Collection<Particle> particles, Input input) {
		int rightSideParticles = 0;
		for(Particle p: particles)
		{
			if(p.getX() >= input.getWidth()/2)
				rightSideParticles++;
		}
		return ((double)rightSideParticles)/input.getN();
	}
}

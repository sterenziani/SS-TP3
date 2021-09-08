package front;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.Collection;
import back.Particle;

public class Output {
	public static String OUTPUT_DIR = "output";
	
	public static void outputToFile(Collection<Particle> particles, double t)
	{
		outputToFile(particles, t, "output/output_t=" +t + ".txt");
	}
	
    public static void outputToFile(Collection<Particle> particles, double t, String outputFileName)
    {
    	File file = new File(outputFileName);
		try
		{
			if(file.createNewFile())
			{
				FileWriter writer = new FileWriter(outputFileName, true);
				writer.write(particles.size() +"\n\n");
				writer.close();
			}
		}
		catch (IOException e)
		{
			e.printStackTrace();
			return;
		}
        try (FileWriter writer = new FileWriter(outputFileName, true))
        {
			for(Particle p: particles)
				writer.write(p.getX() +"\t" + p.getY() +"\t" +p.getVx() +"\t" +p.getVy() +"\t" +p.getRadius() +"\t" +p.getMass() +"\n");
        	writer.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
    
    public static void resetFolder(String folderName)
    {
    	File folder = new File(folderName);
        File[] files = folder.listFiles();
        if(files!=null)
        {
            for(File f: files)
                f.delete();
        }
        folder.delete();
        folder.mkdir();        
    }
    
    public static void createWallFile(Input input) throws IOException
    {
    	String filename = "wall.txt";
    	StringBuilder s = new StringBuilder();
    	File file = new File(filename);
        file.delete();
        file.createNewFile();
        try (FileWriter writer = new FileWriter(filename, true))
        {
        	int lines = 0;
        	double radius = 0.0005;
        	DecimalFormat df = new DecimalFormat("#.#");
        	df.setMaximumFractionDigits(5);
        	
			// Vertical walls
        	for(double y=0; y < input.getHeight(); y += radius)
        	{
        		s.append("0.00" +"\t" +df.format(y) +"\t"  +df.format(radius) +"\n");
        		if(y < (input.getHeight()-input.getGapSize())/2 || y > (input.getHeight()+input.getGapSize())/2)
        		{
        			lines++;
        			s.append(df.format(input.getWidth()/2) +"\t" +df.format(y) +"\t" +df.format(radius) +"\n");
        		}
        		s.append(df.format(input.getWidth()) +"\t" +df.format(y) +"\t"  +df.format(radius) +"\n");
        		lines += 2;
        	}
        	
        	// Horizontal walls
        	for(double x=0; x < input.getWidth(); x += radius)
        	{
        		s.append(df.format(x) +"\t" +"0.00" +"\t" +df.format(radius) +"\n");
        		s.append(df.format(x) +"\t" +df.format(input.getHeight()) +"\t" +df.format(radius) +"\n");
        		lines += 2;
        	}
        	writer.write(lines +"\n\n");
        	writer.write(s.toString());
        	writer.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
}

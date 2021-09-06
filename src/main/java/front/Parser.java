package front;
import java.io.FileReader;
import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class Parser {
	private final static Integer DEFAULT_SEED = (int) (Math.random() * Integer.MAX_VALUE);
	
	@SuppressWarnings("unchecked")
    public static Input ParseJSON(String filename)
    {
		Integer seed;
		
    	JSONParser parser = new JSONParser();
		try
		{
			Object obj = parser.parse(new FileReader(filename));
			JSONObject json = (JSONObject) obj;
			seed = ((Long) json.getOrDefault("seed", DEFAULT_SEED)).intValue();
			return new Input();
		}
		catch (Exception e)
		{
			e.printStackTrace();
			return null;
		}
    }
}

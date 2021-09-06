import java.util.*;

import back.*;
import front.Input;
import front.Output;
import front.Parser;

public class App {

	public static void main(String[] args) throws Exception
	{
		Input input = Parser.ParseJSON("input.json");
		Output.resetFolder(Output.OUTPUT_DIR);
		System.out.println("Implement me!");
	}
}

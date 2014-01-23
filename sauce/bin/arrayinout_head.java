import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;


public class Class {

	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		List<Integer> list = new ArrayList<Integer>();
		while (scanner.hasNextInt())
			list.add(scanner.nextInt());
		scanner.close();
		int[] array = new int[list.size()];
		for (int i = 0; i < list.size(); ++i) {
			array[i] = list.get(i);
		}
		array = run(array);
		for (int i: array) {
			System.out.println(i);
		}
	}

	public static int[] run(int[] array) {

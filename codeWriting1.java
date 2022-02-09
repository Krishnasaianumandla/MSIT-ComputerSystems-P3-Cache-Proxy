import java.util.ArrayList;
import java.util.Scanner;

public class Solution {
	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);

		int num_caches = Integer.parseInt(scanner.nextLine());
		String[] caches_capacities = scanner.nextLine().split(" ");

		Cache[] caches_list = new Cache[num_caches];
		for (int i = 0; i < caches_capacities.length; i++) {
			int size = Integer.parseInt(caches_capacities[i]);
			caches_list[i] = new Cache(size);
		}
		while (true) {
			String input = scanner.nextLine();
			if (input.contains("RANGE")) {
				processRange(input, caches_list);
			} else if (input.contains("ADDR")) {
				processAddr(input, caches_list);
			} else if (input.contains("STAT")) {
				processStat(caches_list);
			} else if (input.contains("END")) {
				break;
			}
		}
		scanner.close();
	}

	private static void processRange(String input, Cache[] caches_list) {
		String[] data = input.split(" ");
		int b = Integer.parseInt(data[1]);
		int y = Integer.parseInt(data[2]);
		int n = Integer.parseInt(data[3]);
		for (int k = 0; k < n; k++) {
			int data_reference = b + (y * k);
			addDataReference(data_reference, caches_list);
		}
	}

	private static void processAddr(String input, Cache[] caches_list) {
		String[] data = input.split(" ");
		int data_reference = Integer.parseInt(data[1]);
		addDataReference(data_reference, caches_list);
	}

	private static void processStat(Cache[] caches_list) {
		for (int i = 0; i < caches_list.length; i++) {
			if (i < caches_list.length - 1){
				System.out.print(caches_list[i].getMiss());
				System.out.print(" ");
			} else {
				System.out.println(caches_list[i].getMiss());
			}
			caches_list[i].resetMiss();
		}
	}

	private static void addDataReference(int data_reference, Cache[] caches_list) {
		for (Cache cache : caches_list) {
			cache.check(data_reference);
		}
	}
}

class Cache {
	int miss;
	int cache_size;
	ArrayList<Integer> cache_list;

	public Cache(int cache_size) {
		this.miss = 0;
		this.cache_size = cache_size;
		this.cache_list = new ArrayList<>();
	}

	public void check(Integer data) {
		if (cache_list.contains(data)) {
			cache_list.remove(data);
			cache_list.add(data);
		} else {
			miss++;
			cache_list.add(data);
			if (cache_list.size() > cache_size) {
				cache_list.remove(0);
			}
		}
	}

	public int getMiss() {
		return miss;
	}

	public void resetMiss() {
		this.miss = 0;
	}
}
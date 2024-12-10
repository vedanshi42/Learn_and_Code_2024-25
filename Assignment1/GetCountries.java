import java.util.*;

public class GetCountries {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter country code (e.g. IN, US, NZ): ");
        String countryCode = scanner.nextLine().toUpperCase();

        List<String> adjacentCountries = AdjacentCountryData.findAdjacentCountries(countryCode);

        if (adjacentCountries != null) {
            Collections.sort(adjacentCountries);
            System.out.println(adjacentCountries);
        } else {
            System.out.println("Country code not available.");
        }
    }
}
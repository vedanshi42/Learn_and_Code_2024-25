import java.util.*;

public class GetCountries {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter country code: ");
        String countryCode = scanner.nextLine().toUpperCase();

        List<String> adjacentCountries = findAdjacentCountries(countryCode);

        if (adjacentCountries != null) {
            Collections.sort(adjacentCountries);
            System.out.println(adjacentCountries);
        } else {
            System.out.println("Country code not found.");
        }
    }

    public static List<String> findAdjacentCountries(String countryCode) {
        Map<String, List<String>> countries = new HashMap<>();
        countries.put("IN", Arrays.asList("Pakistan", "China", "Nepal", "Bhutan", "Bangladesh", "Myanmar", "Afghanistan", "Maldives", "Sri Lanka"));
        countries.put("US", Arrays.asList("Canada", "Mexico"));
        countries.put("NZ", Arrays.asList("Australia"));
        countries.put("GB", Arrays.asList("Ireland", "France", "Netherlands"));
        countries.put("FR", Arrays.asList("Belgium", "Luxembourg", "Switzerland", "Spain", "Italy", "Germany", "Monaco", "Brazil", "Andorra", "Suriname"));

        return countries.get(countryCode);
    }
}

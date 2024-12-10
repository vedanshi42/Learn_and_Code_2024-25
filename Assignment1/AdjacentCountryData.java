import java.util.*;

    public class AdjacentCountryData {
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


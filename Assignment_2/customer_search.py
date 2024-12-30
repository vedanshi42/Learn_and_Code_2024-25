import json
import csv


class CustomerSearch:

    def __init__(self, customers_data_json):
        with open(customers_data_json, 'r') as customers:
            self.customers = json.load(customers)

    def search_customers(self, by_field_name, value_to_search):
        customers_found = [customer for customer in self.customers if value_to_search.lower() in customer[by_field_name].lower()]

        for current_index in range(len(customers_found)):
            min_element_index = current_index

            for next_index in range(current_index + 1, len(customers_found)):
                if customers_found[next_index]['CustomerID'] < customers_found[min_element_index]['CustomerID']:
                    min_element_index = next_index

            customers_found[current_index], customers_found[min_element_index] = customers_found[min_element_index], customers_found[current_index]

        return customers_found

    def search_by_country(self, country):
        return self.search_customers('Country', country)

    def search_by_company_name(self, company_name):
        return self.search_customers('CompanyName', company_name)

    def search_by_contact(self, contact_name):
        return self.search_customers('ContactName', contact_name)


class Export_data:

    def __init__(self, customer_search_data):
        self.customers = customer_search_data.customers

    def export_to_csv(self):
        with open('customers_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            column_names = ['CustomerID', 'CompanyName', 'ContactName', 'Country']
            writer.writerow(column_names)
            for customer in self.customers:
                writer.writerow([customer['CustomerID'], customer['CompanyName'], customer['ContactName'], customer['Country']])
        print("Data exported to 'customers_data.csv'")


if __name__ == "__main__":
    search = CustomerSearch('customers.json')

    country_results = search.search_by_country('USA')
    print(country_results)

    company_results = search.search_by_company_name('CorpKit')
    print(company_results)

    contact_results = search.search_by_contact('Niharika Singh')
    print(contact_results)

    export = Export_data(search)
    export.export_to_csv()

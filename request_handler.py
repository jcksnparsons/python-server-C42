from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animals_with_query_strings
from locations import get_all_locations, get_single_location, create_location, delete_location, update_location
from employees import get_all_employees, get_single_employee, create_employee, delete_employee, update_employee, get_employees_by_location
from customers import get_all_customers, get_single_customer, delete_customer, update_customer, get_customer_by_email
from models import Animal, Location, Employee, Customer

# Here's a class. It inherits from another class.


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:

            # Splits the resource string to get data resource name and query parameters
            params = resource.split("?")
            resource_string = params[0]
            # Makes a list of all the query parameters, even if it's a list of one
            queries_list = params[1].split("&")

            return_dict = {}

            query_dict = {}

            for query in queries_list:
                # Splits the query into a list where the 1st element is a key and the 2nd element is a value
                deconstructed_query = query.split("=")

                # Creates a key on the above dictionary and assigns it a value, both coming from the deconstructed query
                query_dict[deconstructed_query[0]] = deconstructed_query[1]

            # Returns a tuple where the first element is a string describing the data resource that we will be querying and the second element is a dictionary that contains key value pairs based on the query parameters in the URL
            return_dict["resource"] = resource_string
            return_dict["query_dict"] = query_dict
            return return_dict

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return_dict = {}
            return_dict['resource'] = resource

            if id is not None:
                return_dict['id'] = id

            return return_dict

    # Here's a class function

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        parsed = self.parse_url(self.path)

        if parsed['resource'] == "animals":

            if 'query_dict' in parsed:
                response = f"{get_animals_with_query_strings(parsed['query_dict'])}"

            elif 'id' in parsed:
                response = f"{get_single_animal(parsed['id'])}"

            else:
                response = f"{get_all_animals()}"

        # if parsed[1] is None:
        #     resource = parsed[0]

        #     if resource == "animals":
        #         response = f"{get_all_animals()}"

        #     elif resource == "locations":
        #         response = f"{get_all_locations()}"

        #     elif resource == "employees":
        #         response = f"{get_all_employees()}"

        #     elif resource == "customers":
        #         response = f"{get_all_customers()}"

        # elif type(parsed[1]) is int:
        #     (resource, id) = parsed

        #     if resource == "animals":
        #         response = f"{get_single_animal(id)}"

        #     elif resource == "locations":
        #         response = f"{get_single_location(id)}"

        #     elif resource == "employees":
        #         response = f"{get_single_employee(id)}"

        #     elif resource == "customers":
        #         response = f"{get_single_customer(id)}"

        # elif type(parsed[1]) is dict:
        #     (resource, query_dict) = parsed

        #     if resource == "animals":
        #         response = get_animals_with_query_strings(query_dict)

        #     elif resource == "employees":
        #         response = f"{get_employees_by_location(value)}"

        #     elif resource == "customers":
        #         response = f"{get_customer_by_email(value)}"

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_resource = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_resource = create_animal(post_body)

        elif resource == "locations":
            new_resource = create_location(post_body)

        elif resource == "employees":
            new_resource = create_employee(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_resource}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)

        if resource == "locations":
            update_location(id, post_body)

        if resource == "employees":
            update_employee(id, post_body)

        if resource == "customers":
            update_customer(id, post_body)

    # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        elif resource == "customers":
            delete_customer(id)

        elif resource == "employees":
            delete_employee(id)

        elif resource == "locations":
            delete_location(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()

from http.server import BaseHTTPRequestHandler, HTTPServer
from views import *
import json
from urllib.parse import urlparse, parse_qs

class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)
    
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function
    def _set_headers(self, status):
       
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        parsed_search = self.path.split('/')
        search_value = parsed_search[-1] 

        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()

            if resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()
            if resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()
            if resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()
            if resource == "search":
                if search_value is not None:
                    response = search(search_value)
                else:
                    response = get_all_animals()
        
        else: # There is a ? in the path, run the query param functions
                (resource, query) = parsed

                if query.get('email') and resource == 'customers':
                    response = get_customer_by_email(query['email'][0])
                if query.get("location_id") and resource == 'animals':
                    response = get_animal_by_location_id(query['location_id'][0])
                if query.get("status") and resource == 'animals':
                    response = get_animal_by_status(query['status'][0])
                if query.get("location_id") and resource == 'employees':
                    response = get_employee_by_location_id(query['location_id'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_animal = None
        
        if resource == "animals":
            new_animal = create_animal(post_body)
            self.wfile.write(json.dumps(new_animal).encode())
        
        if resource == "locations":
            new_location = create_location(post_body)
            self.wfile.write(json.dumps(new_location).encode())
            
        if resource == 'employees':
            new_employee = create_employee(post_body)
            self.wfile.write(json.dumps(new_employee).encode())
            
        if resource == 'customers':
            new_customer = create_customer(post_body)
            self.wfile.write(json.dumps(new_customer).encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)
        
        success = False
        
        if resource == "animals":
            success = update_animal(id, post_body)
        if resource == "locations":
            update_location(id, post_body)
        if resource == "employees":
            update_employee(id, post_body)
        if resource == 'customers':
            update_customer(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            delete_animal(id)
        
        if resource == 'customers':
            delete_customer(id)
            
        if resource == 'locations':
            delete_location(id)
            
        if resource == 'employees':
            delete_employee(id)
        
        self.wfile.write("".encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()

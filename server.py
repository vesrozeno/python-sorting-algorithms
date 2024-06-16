from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Define alguns algoritmos de ordenação
def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers

def quick_sort(numbers):
    if len(numbers) <= 1:
        return numbers
    pivot = numbers[len(numbers) // 2]
    left = [x for x in numbers if x < pivot]
    middle = [x for x in numbers if x == pivot]
    right = [x for x in numbers if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the data
        content_length = int(self.headers['Content-Length'])
        
        # Read the data
        post_data = self.rfile.read(content_length)
        
        # Parse the data (assuming it's urlencoded)
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        # Get the numbers to be sorted
        numbers = parsed_data.get('numbers')
        if numbers:
            # Convert the numbers from strings to integers
            numbers = list(map(int, numbers[0].split(',')))
        
        # Get the sorting algorithm from the headers
        sorting_algorithm = self.headers.get('Sorting-Algorithm')
        
        if sorting_algorithm == 'bubble_sort':
            sorted_numbers = bubble_sort(numbers)
        elif sorting_algorithm == 'quick_sort':
            sorted_numbers = quick_sort(numbers)
        else:
            sorted_numbers = 'Invalid sorting algorithm specified'
        
        # Process the data (print it in this example)
        print(f'Received numbers: {numbers}')
        print(f'Sorted numbers: {sorted_numbers}')
        
        # Respond to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        response = f'Sorted numbers: {sorted_numbers}'.encode('utf-8')
        self.wfile.write(response)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

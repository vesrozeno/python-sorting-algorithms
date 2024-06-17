from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import random
import json

# Define função geradora de números aleatórios
def generate_data(size):
    return [random.randint(0, size) for _ in range(size)]

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

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = key
            j -= 1
        arr[j + 1] = key
    return arr

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'healthy'}
            self.wfile.write(str(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/sort':
            try:
                # Get the length of the data
                content_length = int(self.headers['Content-Length'])
                
                # Read the data
                post_data = self.rfile.read(content_length)
                
                # Parse the data (assuming it's urlencoded)
                parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                
                # Get the numbers to be sorted
                numbers = int(parsed_data.get('numbers')[0])
                
                # Generate random numbers 
                data = generate_data(numbers)
                
                # Get the sorting algorithm from the headers
                sorting_algorithm = self.headers.get('Sorting-Algorithm')
                
                if sorting_algorithm == 'bubble_sort':
                    sorted_numbers = bubble_sort(data)
                elif sorting_algorithm == 'quick_sort':
                    sorted_numbers = quick_sort(data)
                elif sorting_algorithm == 'insertion_sort':
                    sorted_numbers = insertion_sort(data)
                elif sorting_algorithm == 'selection_sort':
                    sorted_numbers = selection_sort(data)
                elif sorting_algorithm == 'merge_sort':
                    sorted_numbers = merge_sort(data)
                else:
                    sorted_numbers = 'Invalid sorting algorithm specified'
                
                # Respond to the client
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {
                    'sorted_numbers': sorted_numbers,
                    'algorithm': sorting_algorithm
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Internal server error: {str(e)}".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

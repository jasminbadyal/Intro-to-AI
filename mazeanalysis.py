import csv

def analyze_maze_results(file_path):
    results = {}
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            method = row[0]
            expanded_cells = int(row[1])
            runtime = float(row[2])
            
            if method not in results:
                results[method] = {'expanded_cells': [], 'runtime': []}
            
            results[method]['expanded_cells'].append(expanded_cells)
            results[method]['runtime'].append(runtime)
    
    for method, data in results.items():
        avg_expanded_cells = sum(data['expanded_cells']) / len(data['expanded_cells'])
        avg_runtime = sum(data['runtime']) / len(data['runtime'])
        print(f"Method: {method}")
        print(f"Average Expanded Cells: {avg_expanded_cells}")
        print(f"Average Runtime: {avg_runtime}\n")

if __name__ == "__main__":
    analyze_maze_results('maze_results.txt')
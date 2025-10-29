from pathFinder import analyze_coordinate_pairs, detailed_route_analysis, generate_statistics
import csv
import random
import math

def export_coordinate_analysis_to_csv(filename="coordinate_analysis.csv"):
    from pathFinder import mapping, get_optimal_path_with_constraints, get_path, calculate_hops, calculate_coverage
    all_coords = list(mapping.keys())
    random.seed(42)
    pairs = []
    
    for i in range(50):
        start = random.choice(all_coords)
        end = random.choice(all_coords)

        while start == end:
            end = random.choice(all_coords)
        pairs.append((start, end))
    

    csv_data = []
    max_hops_options = [0, 1, 2, 3, 4]
    
    for i, (start, end) in enumerate(pairs):
        pair_name = f"P{i+1:02d}"
        

        def calculate_distance(coord1, coord2):
            return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
        
        direct_distance = calculate_distance(start, end)
        

        best_route = None
        best_hops = None
        min_max_hops = None
        
        for max_hops in max_hops_options:
            try:
                result = get_optimal_path_with_constraints(
                    starts=list(start), 
                    ends=list(end), 
                    max_hops=max_hops
                )
                
                if result["status"] == "success":
                    if best_route is None:
                        best_route = result["route"]
                        best_hops = result["hops"]
                        min_max_hops = max_hops
                    break
            except Exception as e:
                continue
        

        if best_route is None:
            try:
                best_route = get_path(list(start), list(end))
                if best_route != "Not Possible" and best_route != "No Solution Found!":
                    best_hops = calculate_hops(best_route, start, end)
                    min_max_hops = "No Limit"
                else:
                    best_hops = "N/A"
                    min_max_hops = "N/A"
            except Exception as e:
                best_hops = "Error"
                min_max_hops = "Error"
        

        def calculate_coverage_local(route, all_coordinates):
            if not route or route == "Not Possible" or route == "No Solution Found!":
                return 0
            
            route_stops = set()
            for coord in route:
                route_stops.add(tuple(coord))
            
            total_stops = len(all_coordinates)
            covered_stops = len(route_stops)
            
            return (covered_stops / total_stops) * 100
        
        coverage = calculate_coverage_local(best_route, all_coords)
        

        csv_row = {
            'Name': pair_name,
            'Start_X': start[0],
            'Start_Y': start[1],
            'End_X': end[0],
            'End_Y': end[1],
            'Distance': round(direct_distance, 6),
            'Hops': best_hops if best_hops != "N/A" else "N/A",
            'Max_Hops': min_max_hops if min_max_hops != "N/A" else "N/A",
            'Coverage_Percent': round(coverage, 2),
            'Start_Ward': mapping.get(start, 'Unknown'),
            'End_Ward': mapping.get(end, 'Unknown'),
            'Route_Type': 'Intra_Ward' if mapping.get(start) == mapping.get(end) else 'Inter_Ward'
        }
        csv_data.append(csv_row)
    

    fieldnames = ['Name', 'Start_X', 'Start_Y', 'End_X', 'End_Y', 'Distance', 'Hops', 'Max_Hops', 'Coverage_Percent', 'Start_Ward', 'End_Ward', 'Route_Type']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ Coordinate analysis exported to {filename}")
    return csv_data

def export_all_to_csv():
    """
    Export all analyses to CSV files.
    """
    print("🚌 Exporting Bus Route Analysis to CSV Files")
    print("=" * 60)
    

    print("\n1. Exporting coordinate pairs analysis...")
    coord_data = export_coordinate_analysis_to_csv("coordinate_analysis.csv")

if __name__ == "__main__":
    export_all_to_csv()
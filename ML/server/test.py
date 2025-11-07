from pathFinder import analyze_coordinate_pairs, detailed_route_analysis, generate_statistics
import csv
import random
import math

def export_coordinate_analysis_to_csv(filename="coordinate_analysis.csv"):
    from pathFinder import mapping, get_optimal_path_with_constraints, get_path, calculate_hops, calculate_coverage, BUS_STOP_MAPPING, find_nearest_bus_stop, get_standard_and_min_hop_routes
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
    # max_hops_options = [0, 1, 2, 3, 4]
    
    for i, (start, end) in enumerate(pairs):
        pair_name = f"P{i+1:02d}"
        

        # def calculate_distance(coord1, coord2):
        #     return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
        
        # direct_distance = calculate_distance(start, end)
        

        # best_route = None
        # best_hops = None
        # min_max_hops = None
        
        # for max_hops in max_hops_options:
        #     try:
        #         result = get_optimal_path_with_constraints(
        #             starts=list(start), 
        #             ends=list(end), 
        #             max_hops=max_hops
        #         )
                
        #         if result["status"] == "success":
        #             if best_route is None:
        #                 best_route = result["route"]
        #                 best_hops = result["hops"]
        #                 min_max_hops = max_hops
        #             break
        #     except Exception as e:
        #         continue
        

        # if best_route is None:
        #     try:
        #         best_route = get_path(list(start), list(end))
        #         if best_route != "Not Possible" and best_route != "No Solution Found!":
        #             best_hops = calculate_hops(best_route, start, end)
        #             min_max_hops = "No Limit"
        #         else:
        #             best_hops = "N/A"
        #             min_max_hops = "N/A"
        #     except Exception as e:
        #         best_hops = "Error"
        #         min_max_hops = "Error"
        

        # def calculate_coverage_local(route, all_coordinates):
        #     if not route or route == "Not Possible" or route == "No Solution Found!":
        #         return 0
            
        #     route_stops = set()
        #     for coord in route:
        #         route_stops.add(tuple(coord))
            
        #     total_stops = len(all_coordinates)
        #     covered_stops = len(route_stops)
            
        #     return (covered_stops / total_stops) * 100
        
        # coverage = calculate_coverage_local(best_route, all_coords)
        
        #Get bus stop names
        start_bus_stop = find_nearest_bus_stop(start, BUS_STOP_MAPPING)        
        end_bus_stop = find_nearest_bus_stop(end, BUS_STOP_MAPPING)
        
        # Get both standard and minimum hop routes
        routes = get_standard_and_min_hop_routes(start, end)
        
        csv_row = {
            'Name': pair_name,
            'Start_Bus_Stop_Name': start_bus_stop,
            'End_Bus_Stop_Name': end_bus_stop,
            'Start_X': start[0],
            'Start_Y': start[1],
            'End_X': end[0],
            'End_Y': end[1],
            'Standard_Route_Distance': round(routes['standard_route']['distance'], 6),
            'Standard_Route_Hops': routes['standard_route']['hops'],
            'Min_Hop_Route_Distance': round(routes['min_hop_route']['distance'], 6),
            'Min_Hop_Route_Hops': routes['min_hop_route']['hops'],
            'Standard_Route_Feasible': routes['standard_route']['feasible'],
            'Min_Hop_Route_Feasible': routes['min_hop_route']['feasible'],
            # 'Max_Hops': min_max_hops if min_max_hops != "N/A" else "N/A",
            # 'Coverage_Percent': round(coverage, 2),
            'Start_Ward': mapping.get(start, 'Unknown'),
            'End_Ward': mapping.get(end, 'Unknown'),
            'Route_Type': 'Intra_Ward' if mapping.get(start) == mapping.get(end) else 'Inter_Ward'
        }
        csv_data.append(csv_row)
    

    fieldnames = [
        'Name', 'Start_Bus_Stop_Name', 'End_Bus_Stop_Name', 'Start_X', 'Start_Y', 'End_X', 'End_Y',
        'Standard_Route_Distance', 'Standard_Route_Hops', 'Min_Hop_Route_Distance', 'Min_Hop_Route_Hops',
        'Standard_Route_Feasible', 'Min_Hop_Route_Feasible', 
        'Max_Hops', 'Coverage_Percent', 'Start_Ward', 'End_Ward', 'Route_Type'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ Coordinate analysis exported to {filename}")
    return csv_data
    
def export_detailed_analysis_to_csv(filename="detailed_analysis.csv"):
    """
    Export detailed analysis similar to the existing detailed_analysis.csv but with bus stop names
    """
    from pathFinder import mapping, BUS_STOP_MAPPING, find_nearest_bus_stop, get_route_with_alternatives, calculate_coverage
    
    all_coords = list(mapping.keys())
    random.seed(42)
    
    # Generate 10 pairs like in your existing detailed_analysis.csv  
    pairs = []
    pair_ids = ['D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10']
    
    for i in range(10):
        start = random.choice(all_coords)
        end = random.choice(all_coords)
        pairs.append((start, end))
    
    csv_data = []
    hop_options = [0, 1, 2, 3]
    
    for i, (start, end) in enumerate(pairs):
        pair_id = pair_ids[i]
        
        # Get bus stop names
        start_bus_stop = find_nearest_bus_stop(start, BUS_STOP_MAPPING)
        end_bus_stop = find_nearest_bus_stop(end, BUS_STOP_MAPPING)
        
        start_ward = mapping.get(start, 'Unknown')
        end_ward = mapping.get(end, 'Unknown')
        route_type = f"intra_ward_{start_ward}" if start_ward == end_ward else f"inter_ward_{start_ward}_to_{end_ward}"
        
        # Test each hop option
        for hop_option in hop_options:
            try:
                alternatives = get_route_with_alternatives(list(start), list(end), [hop_option])
                
                hop_key = f"{hop_option}_hops"
                if hop_key in alternatives['alternatives'] and alternatives['alternatives'][hop_key]['feasible']:
                    details = alternatives['alternatives'][hop_key]
                    coverage = calculate_coverage(details['route'], all_coords)
                    
                    csv_row = {
                        'Pair_ID': pair_id,
                        'Start_Bus_Stop_Name': start_bus_stop,
                        'End_Bus_Stop_Name': end_bus_stop,
                        'Start_X': start[0],
                        'Start_Y': start[1],
                        'End_X': end[0], 
                        'End_Y': end[1],
                        'Start_Ward': start_ward,
                        'End_Ward': end_ward,
                        'Route_Type': route_type,
                        'Hop_Option': hop_key,
                        'Feasible': True,
                        'Actual_Hops': details['actual_hops'],
                        'Route_Length': len(details['route']) if details['route'] else 0,
                        'Coverage_Percent': round(coverage, 2),
                        'Reason': 'Success'
                    }
                else:
                    csv_row = {
                        'Pair_ID': pair_id,
                        'Start_Bus_Stop_Name': start_bus_stop,
                        'End_Bus_Stop_Name': end_bus_stop, 
                        'Start_X': start[0],
                        'Start_Y': start[1],
                        'End_X': end[0],
                        'End_Y': end[1],
                        'Start_Ward': start_ward,
                        'End_Ward': end_ward,
                        'Route_Type': route_type,
                        'Hop_Option': hop_key,
                        'Feasible': False,
                        'Actual_Hops': 'N/A',
                        'Route_Length': 0,
                        'Coverage_Percent': 0,
                        'Reason': 'No route found within specified constraints'
                    }
                
                csv_data.append(csv_row)
                
            except Exception as e:
                csv_row = {
                    'Pair_ID': pair_id,
                    'Start_Bus_Stop_Name': start_bus_stop,
                    'End_Bus_Stop_Name': end_bus_stop,
                    'Start_X': start[0],
                    'Start_Y': start[1], 
                    'End_X': end[0],
                    'End_Y': end[1],
                    'Start_Ward': start_ward,
                    'End_Ward': end_ward,
                    'Route_Type': route_type,
                    'Hop_Option': f"{hop_option}_hops",
                    'Feasible': False,
                    'Actual_Hops': 'N/A',
                    'Route_Length': 0,
                    'Coverage_Percent': 0,
                    'Reason': 'No route found within specified constraints'
                }
                csv_data.append(csv_row)
    
    fieldnames = [
        'Pair_ID', 'Start_Bus_Stop_Name', 'End_Bus_Stop_Name', 'Start_X', 'Start_Y', 'End_X', 'End_Y',
        'Start_Ward', 'End_Ward', 'Route_Type', 'Hop_Option', 'Feasible', 'Actual_Hops', 
        'Route_Length', 'Coverage_Percent', 'Reason'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ Detailed analysis exported to {filename}")
    return csv_data

def export_all_to_csv():
    """
    Export all analyses to CSV files.
    """
    print("🚌 Exporting Bus Route Analysis to CSV Files")
    print("=" * 60)
    

    print("\n1. Exporting coordinate pairs analysis...")
    coord_data = export_coordinate_analysis_to_csv("coordinate_analysis.csv")
    
    print("\n2. Exporting detailed analysis...")
    detailed_data = export_detailed_analysis_to_csv("detailed_analysis.csv")
    
    print(f"\n All exports completed successfully.")

if __name__ == "__main__":
    export_all_to_csv()
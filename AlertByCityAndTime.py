import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Static array of city names
cities = ["כרמיאל", "עכו", "חיפה", "נהריה", "גילון", "קריית ביאליק", "קריית מוצקין", "עין המפרץ"]

# Path to JSON file
json_file_path = r"C:\Users\ittayeya\Downloads\Telegram Desktop\ChatExport_2024-11-10\result.json"
input_folder = os.path.dirname(json_file_path)  # Detect folder from the input file path
output_file_path = os.path.join(input_folder, "output.txt")  # Output file in the same folder

# Function to extract cities from a message
def extract_cities(message, cities):
    found_cities = []
    for city in cities:
        if city in message:
            found_cities.append(city)
    return found_cities

# Function to calculate the rounded hour based on the half-hour rule
def get_half_hour_rounded_hour(message_time):
    hour = message_time.hour
    minute = message_time.minute
    if minute >= 30:
        hour = (hour + 1) % 24
    return hour

# Function to process JSON file and group messages by cities and half-hour rounded hour
def process_json(json_file_path, cities):
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    city_mapping = {city: {hour: {"count": 0, "messages": []} for hour in range(24)} for city in cities}

    for item in data.get('messages', []):
        message_text = str(item.get('text', '')) + str(item.get('text_entities', ''))
        try:
            message_time = datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S')
            rounded_hour = get_half_hour_rounded_hour(message_time)
        except (ValueError, KeyError):
            continue

        cities_in_message = extract_cities(message_text, cities)
        for city in cities_in_message:
            city_mapping[city][rounded_hour]["messages"].append({
                'message': message_text,
                'time': message_time.strftime('%Y-%m-%d %H:%M:%S')
            })
            city_mapping[city][rounded_hour]["count"] += 1

    return city_mapping

# Function to write and print the output grouped by city and half-hour rounded hour with message counts
def write_and_print_output(output_file_path, city_mapping):
    with open(output_file_path, "w", encoding="utf-8") as file:
        for city, hours in city_mapping.items():
            file.write(f"City: {city}\n")
            for hour, data in hours.items():
                if data["count"] > 0:
                    file.write(f"  Hour {hour} (Count: {data['count']}):\n")
                    for message in data["messages"]:
                        file.write(f"    Time: {message['time']}\n")
                        file.write(f"    Message: {message['message']}\n\n")

# Function to plot bar graphs of hourly message counts for each city
def plot_city_message_counts(city_mapping, input_folder):
    for city, hours in city_mapping.items():
        hours_list = list(range(24))
        counts = [hours[hour]["count"] for hour in hours_list]

        plt.figure(figsize=(10, 6))
        plt.bar(hours_list, counts, color='skyblue')
        plt.xlabel('Hour of Day')
        plt.ylabel('Message Count')
        plt.title(f'Hourly Message Count for {city[::-1]}')
        plt.xticks(hours_list)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plot_file_path = os.path.join(input_folder, f"{city}_hourly_counts.png")
        plt.savefig(plot_file_path)
        print(f"Bar graph saved for {city} at {plot_file_path}")
        
        plt.close()

# Main processing
city_mapping = process_json(json_file_path, cities)
write_and_print_output(output_file_path, city_mapping)
plot_city_message_counts(city_mapping, input_folder)

print(f"Output written to {output_file_path}")

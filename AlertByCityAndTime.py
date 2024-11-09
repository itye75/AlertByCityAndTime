import json
from datetime import datetime
import matplotlib.pyplot as plt

# Static array of city names
cities = ["כרמיאל", "עכו", "חיפה", "נהריה", "גילון", "קריית ביאליק","קריית מוצקין"]

# Paths to files
json_file_path = r"D:\Downloads\Telegram Desktop\ChatExport_2024-11-09\result.json"
output_file_path = r"D:\Downloads\Telegram Desktop\ChatExport_2024-11-09\output.txt"

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
    # If minutes are 30 or more, round up to the next hour
    if minute >= 30:
        hour = (hour + 1) % 24  # Ensure the hour wraps around correctly at midnight
    return hour

# Function to process JSON file and group messages by cities and half-hour rounded hour
def process_json(json_file_path, cities):
    # Open and load the JSON file
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Initialize a dictionary to hold city mappings with 24-hour sub-groups
    city_mapping = {city: {hour: {"count": 0, "messages": []} for hour in range(24)} for city in cities}

    for item in data['messages']:
        # Extract the message text from 'text' and 'text_entities'
        message_text = ''
        message_text += str(item.get('text', '')) + str(item.get('text_entities', ''))

        # Parse the date and calculate the rounded hour for half-hour grouping
        try:
            message_time = datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S')
            rounded_hour = get_half_hour_rounded_hour(message_time)
        except (ValueError, KeyError):
            continue  # Skip this message if date parsing fails

        # Find all cities mentioned in the message
        cities_in_message = extract_cities(message_text, cities)

        for city in cities_in_message:
            # Add the message to the corresponding half-hour group for each relevant city
            city_mapping[city][rounded_hour]["messages"].append({
                'message': message_text,
                'time': message_time.strftime('%Y-%m-%d %H:%M:%S')
            })
            # Increment the count for that rounded hour
            city_mapping[city][rounded_hour]["count"] += 1

    return city_mapping

# Function to write and print the output grouped by city and half-hour rounded hour with message counts
def write_and_print_output(output_file_path, city_mapping):
    with open(output_file_path, "w", encoding="utf-8") as file:
        for city, hours in city_mapping.items():
            print(f"City: {city}")
            file.write(f"City: {city}\n")
            for hour, data in hours.items():
                if data["count"] > 0:  # Only write if there are messages for this hour
                    print(f"  Hour {hour} (Count: {data['count']}):")
                    file.write(f"  Hour {hour} (Count: {data['count']}):\n")
                    for message in data["messages"]:
                        # Print message details to console
                        print(f"    Time: {message['time']}")
                        print(f"    Message: {message['message']}\n")
                        # Write message details to the output file
                        file.write(f"    Time: {message['time']}\n")
                        file.write(f"    Message: {message['message']}\n\n")

# Function to plot bar graphs of hourly message counts for each city
def plot_city_message_counts(city_mapping):
    for city, hours in city_mapping.items():
        # Extract the hourly counts for the current city
        hours_list = list(range(24))
        counts = [hours[hour]["count"] for hour in hours_list]

        # Plot the bar graph
        plt.figure(figsize=(10, 6))
        plt.bar(hours_list, counts, color='skyblue')
        plt.xlabel('Hour of Day')
        plt.ylabel('Message Count')
        plt.title(f'Hourly Message Count for {city[::-1]}')
        plt.xticks(hours_list)  # Set x-axis to show each hour
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save the plot to a file without displaying it
        plot_file_path = f"D:/Downloads/Telegram Desktop/ChatExport_2024-11-09/{city}_hourly_counts.png"
        plt.savefig(plot_file_path)
        print(f"Bar graph saved for {city} at {plot_file_path}")
        
        # Close the plot to avoid memory issues if many plots are generated
        plt.close()


# Main processing
city_mapping = process_json(json_file_path, cities)
write_and_print_output(output_file_path, city_mapping)
plot_city_message_counts(city_mapping)

print(f"Output written to {output_file_path}")

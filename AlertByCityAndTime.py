import json
from datetime import datetime

# Static array of city names
cities = ["כרמיאל", "עכו", "חיפה", "נהריה", "גילון"]

# Path to the JSON file
json_file_path = r"D:\Downloads\Telegram Desktop\ChatExport_2024-11-09\result.json"
output_file_path = r"D:\Downloads\Telegram Desktop\ChatExport_2024-11-09\output.txt"

# Function to extract cities from a message
def extract_city(message, cities):
    for city in cities:
        if city in message:
            return city
    return None

# Function to process JSON file
def process_json(json_file_path, cities):
    # Open and load the JSON file
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    print("Data loaded:")
    print(data)  # Debugging: Print the structure of the loaded JSON

    city_mapping = {}

    # Check if data is a list
    if isinstance(data, list):
        for item in data:
            # Check if 'messages' exists in the current item
            if isinstance(item, dict) and 'messages' in item:
                for message_item in item['messages']:
                    # Extract the message text from 'text' and 'text_entities'
                    message_text = ''
                    if isinstance(message_item['text'], list):
                        # Combine the text from the array into a single string
                        for part in message_item['text']:
                            # Check if the part is a dictionary and has 'text' field
                            if isinstance(part, dict) and 'text' in part:
                                message_text += part['text']
                            else:
                                message_text += str(part)  # Handle non-dict parts as strings
                    else:
                        message_text += message_item['text']

                    # Include 'text_entities' in the message
                    for entity in message_item['text_entities']:
                        if 'text' in entity:
                            message_text += entity['text']

                    # Extract the date and convert it to a readable format
                    try:
                        message_time = datetime.strptime(message_item['date'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        message_time = 'Invalid Date'

                    # Find the city in the message
                    city = extract_city(message_text, cities)

                    if city:
                        if city not in city_mapping:
                            city_mapping[city] = []
                        city_mapping[city].append({
                            'message': message_text,
                            'time': message_time
                        })
    else:
        print("Error: The JSON data is not in the expected list format.")
    
    return city_mapping

# Function to write and print the output
def write_and_print_output(output_file_path, city_mapping):
    with open(output_file_path, "w", encoding="utf-8") as file:
        for city, messages in city_mapping.items():
            # Print to console
            print(f"City: {city}")
            file.write(f"City: {city}\n")
            for message in messages:
                # Print message details to console
                print(f"  Time: {message['time']}")
                print(f"  Message: {message['message']}\n")
                # Write message details to the output file
                file.write(f"  Time: {message['time']}\n")
                file.write(f"  Message: {message['message']}\n\n")

# Main processing
city_mapping = process_json(json_file_path, cities)

# If there were no errors, print and write the output
if city_mapping:
    write_and_print_output(output_file_path, city_mapping)
    print(f"Output written to {output_file_path}")
else:
    print("No valid city messages found or JSON format issue.")

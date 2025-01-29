import csv
import LLM_Gemini
import random
import os
import LLM_Mistral
from tqdm import tqdm

output_file_path = "assets/Reviews_annotated.csv"
def load_data():
    # Path to CSV file
    csv_file_path = 'assets/Reviews.csv'

    # Dictionary to store data
    data_dict = {}

    # Open CSV file and read content
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)  # Use DictReader to read lines as dictionaries
        for row in csv_reader:
            # Extract Id and Text
            id_key = row['Id']
            text_value = row['Text']
            # Store in dictionary
            data_dict[id_key] = text_value

    return data_dict



GeneralPrompt_1 = """
    You are an AI that analyzes Amaxon reviews. Your task is to provide an annotation for the review text and score it between 1 (negative review of the product) and 5 (positive review of the product).

    The output you will provide shall be only in the form id:
    id: "{review_id}", score: x

    Do not provide any other output or remarks.

    Here a list of text:    
"""

GeneralPrompt_2 = """
    You are an AI that analyzes Amaxon reviews. Your task is to provide an annotation for the review text and score it between 1 (negative review of the product) and 5 (positive review of the product).
    1 corresponds to really bad review, 2 to bad, 3 to average, 4 to good and 5 to really good.
    The output you will provide shall be only in the form id:
    id: "{review_id}", score: x

    Do not provide any other output or remarks.

    Here a list of text:    
"""

def process_response(response, llm_name, combined_dict):
    """
    Process the response from the LLM and update the combined dictionary with the review ID and score.

    Args:
        response (str): The response text from the LLM.
        llm_name (str): The name of the LLM that generated the response.
        combined_dict (dict): The dictionary to update with the review ID and score.

    Returns:
        None
    """
    for line in response.splitlines():
        if line.startswith("id:"):
            try:
                parts = line.split(", ")
                review_id = parts[0].split(": ")[1].strip('"')
                score = parts[1].split(": ")[1]
                if review_id in combined_dict:
                    combined_dict[review_id].append((llm_name, score))
                else:
                    combined_dict[review_id] = [(llm_name, score)]
            except IndexError:
                print(f"Index error while processing the line: {line}")

# Remove the output file from disk if it already exists
output_file_path = "assets/Reviews_annotated.csv"
if os.path.exists(output_file_path):
    os.remove(output_file_path)

data_dict = load_data()

# Print the random reviews
number_of_review_parsed = 0
stringToParse = ""
cycle = 0

for review_id, review_text in tqdm(data_dict.items(), desc="Processing reviews"):
    stringToParse += f"id: {review_id}, text: {review_text}\n"
    number_of_review_parsed += 1
    if number_of_review_parsed == 100:

        combined_dict = {}
        resp = LLM_Gemini.get_gemini_response(GeneralPrompt_1 + stringToParse)
        process_response(resp, "Gemini_1", combined_dict)
        resp = LLM_Mistral.get_mistral_response(GeneralPrompt_1 + stringToParse)
        process_response(resp, "Mistral_1", combined_dict)
        resp = LLM_Gemini.get_gemini_response(GeneralPrompt_2 + stringToParse)
        process_response(resp, "Gemini_2", combined_dict)
        resp = LLM_Mistral.get_mistral_response(GeneralPrompt_2 + stringToParse)
        process_response(resp, "Mistral_2", combined_dict)
        file_exists = os.path.isfile("assets/Reviews_annotated.csv")

        with open("assets/Reviews_annotated.csv", 'a', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            if not file_exists:
                csv_writer.writerow(['review_id', 'LLM', 'score'])  # Write header if file does not exist
            for review_id, llm_scores in combined_dict.items():
                row = [review_id]
                for llm_name, score in llm_scores:
                    row.append(llm_name)
                    row.append(score)
                csv_writer.writerow(row)
        number_of_review_parsed = 0
        stringToParse = ""



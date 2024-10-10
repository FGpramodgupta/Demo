import json

# Function to generate labeled data for Azure CLU model from the capital call samples
def create_labeled_data(samples):
    labeled_data = {"utterances": []}
    
    for sample in samples:
        # Extract parts of the sample for labeling
        text = (f"In anticipation of upcoming investments and expenses, {sample[0]} is calling capital in an amount totaling "
                f"{sample[1]} ({sample[2]} of committed capital). The funds will be used to support new and follow-on investments "
                f"({sample[3]}), management fees ({sample[4]}), and {sample[5]}. Following this capital call, {sample[6]} of committed capital "
                "has been called.")
        
        # Labeled data structure
        labeled_utterance = {
            "text": text,
            "intent": "CapitalCall",
            "entities": [
                {"category": "FundName", "offset": 53, "length": len(sample[0]), "text": sample[0]},
                {"category": "Amount", "offset": text.index(sample[1]), "length": len(sample[1]), "text": sample[1]},
                {"category": "CommittedCapitalPercentage", "offset": text.index(sample[2]), "length": len(sample[2]), "text": sample[2]},
                {"category": "InvestmentsPercentage", "offset": text.index(sample[3]), "length": len(sample[3]), "text": sample[3]},
                {"category": "ManagementFeesPercentage", "offset": text.index(sample[4]), "length": len(sample[4]), "text": sample[4]},
                {"category": "OtherCosts", "offset": text.index(sample[5]), "length": len(sample[5]), "text": sample[5]},
                {"category": "TotalCommittedCapital", "offset": text.index(sample[6]), "length": len(sample[6]), "text": sample[6]}
            ]
        }
        
        labeled_data["utterances"].append(labeled_utterance)
    
    return labeled_data

# Create labeled data for the 100 samples
labeled_data = create_labeled_data(capital_call_samples_with_fund)

# Define the JSON file path
json_file_path = "/mnt/data/capital_call_labeled_data.json"

# Write to JSON
with open(json_file_path, mode="w") as file:
    json.dump(labeled_data, file, indent=4)

json_file_path  # Return the file path for download

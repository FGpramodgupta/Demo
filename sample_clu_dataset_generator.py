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



# Updated function to include random distribution from Expense, Capital_Contribution, and Management_Fee lists

# Define the lists
expense = [
    'Establishment Cost', 'Operational cost', 'Placement fee', 'Start-up cost',
    'Syndication Costs', 'Tax withholding', 'Transaction Cost', 'Working Capital', 'Working Capital Reserve'
]

capital_contribution = [
    'Blocker Loan Call', 'Bridge Financing', 'Call for waived amount', 'Capital call', 'Catch Up Capital',
    'Contributions Investments', 'Contributions (all forms)', 'Drawdown', 'Follow-on investment', 'Invested Capital',
    'Investment', 'Loan Discount', 'Takedown', 'Transaction Cost related to Shares'
]

management_fee = [
    'Blocker Related Fees', 'Call for ISDA', 'Commission', 'General partner allocation',
    'General Partners\' Share', 'Management fee', 'Priority profit share (Carried Interest)',
    'Contributions - Management Fees'
]

# Function to generate a capital call description with varying fund names and random distributions
def generate_capital_call_with_distributions():
    fund = random.choice(fund_names)
    amount = round(random.uniform(25, 35) * 1e6, 0)
    committed_capital_percent = round(random.uniform(9.0, 11.0), 2)
    investment_percent = round(random.uniform(95.0, 97.0), 2)
    management_fee_percent = round(random.uniform(2.0, 4.0), 2)
    other_costs_percent = round(100 - investment_percent - management_fee_percent, 2)
    other_costs_desc = random.choice(["reserve for expenses", "call for ISDA", "other expenses"])

    # Select random items from each list
    random_expense = random.sample(expense, k=random.randint(1, 3))
    random_capital_contribution = random.sample(capital_contribution, k=random.randint(1, 3))
    random_management_fee = random.sample(management_fee, k=random.randint(1, 2))

    total_committed_capital = round(random.uniform(75.0, 85.0), 2)
    
    # Combine all the details into one description
    return (f"In anticipation of upcoming investments and expenses, {fund} is calling capital in an amount totaling ${amount:,.0f} "
            f"({committed_capital_percent}% of committed capital). The funds will be used to support new and follow-on investments "
            f"({investment_percent}%), management fees ({management_fee_percent}%), and {other_costs_desc} ({other_costs_percent}%). "
            f"Following this capital call, {total_committed_capital}% of committed capital has been called.\n\n"
            f"Expense categories: {', '.join(random_expense)}.\n"
            f"Capital Contributions: {', '.join(random_capital_contribution)}.\n"
            f"Management Fees: {', '.join(random_management_fee)}.\n")

# Generate 100 samples with distributions
capital_call_samples_with_distributions = [generate_capital_call_with_distributions() for _ in range(100)]

# Combine all samples into a single text
capital_call_paragraph_with_distributions = "\n\n".join(capital_call_samples_with_distributions)

capital_call_paragraph_with_distributions[:1000]  # Display a portion of the generated text


#sample expense sharing algorithm that allows you to choose method of splitting and adding custom splits.

def input_validation(num_members, incomes, expenses, split_mode, custom_percentages):
    if num_members <= 0:
        raise ValueError("Number of earning members must be greater than zero.")
    
    if len(incomes) != num_members or any(income <= 0 for income in incomes):
        raise ValueError("Incomes must be provided for all members and must be greater than zero.")
    
    if expenses <= 0:
        raise ValueError("Total shared expenses must be greater than zero.")
    
    if split_mode not in ["equal", "equity", "custom"]:
        raise ValueError("Invalid split mode. Choose 'equal', 'equity', or 'custom'.")
    
    if split_mode == "custom":
        if len(custom_percentages) != num_members or sum(custom_percentages) != 100 or any(p <= 0 for p in custom_percentages):
            raise ValueError("Custom percentages must be provided for all members, must sum to 100, and must be greater than zero.")
    
def calculate_contributions(num_members, incomes, expenses, split_mode, custom_percentages=None):
    input_validation(num_members, incomes, expenses, split_mode, custom_percentages)
    
    contributions = [0] * num_members
    
    if split_mode == "equal":
        equal_share = expenses / num_members
        contributions = [equal_share] * num_members
    
    elif split_mode == "equity":
        total_income = sum(incomes)
        contributions = [(income / total_income) * expenses for income in incomes]
    
    elif split_mode == "custom":
        contributions = [(percentage / 100) * expenses for percentage in custom_percentages]
    
    return contributions

def display_contributions(members, contributions):
    print("Shared Expense Contributions:")
    for member, contribution in zip(members, contributions):
        print(f"{member}: ${contribution:.2f}")

num_members = int(input("Enter the number of earning members: "))
members = [input(f"Enter the name of member {i+1}: ") for i in range(num_members)]
incomes = [float(input(f"Enter the monthly income of {member}: ")) for member in members]
expenses = float(input("Enter the total shared expenses for the month: "))
split_mode = input("Enter the split mode (equal/equity/custom): ").strip().lower()

custom_percentages = None
if split_mode == "custom":
    custom_percentages = [float(input(f"Enter the custom percentage for {member} (out of 100): ")) for member in members]

contributions = calculate_contributions(num_members, incomes, expenses, split_mode, custom_percentages)

display_contributions(members, contributions)

#Code for one stop insurance company
#Student Name: Dylan Finlay

import json
import time

# Constants File
CONST_FILE = 'Const.dat'

# Load constants
def load_constants(file_path):
    constants = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                constants[key] = float(value) if '.' in value else int(value)
        print(f"Constants loaded successfully: {constants}")
    except Exception as e:
        print(f"Error reading constants file: {e}")
        raise
    return constants

# Function to display a blinking message
def blinking_message(message, duration=2, interval=0.5):
    end_time = time.time() + duration
    while time.time() < end_time:
        print(message, end='\r')
        time.sleep(interval)
        print(' ' * len(message), end='\r')
        time.sleep(interval)
    print(message)

# Function to save policy data
def save_policy_data(policy_data):
    try:
        with open('policies.json', 'a') as file:
            json.dump(policy_data, file)
            file.write('\n')
        blinking_message("Policy data has been saved.", duration=3)
    except Exception as e:
        print(f"Error saving policy data: {e}")

# Function to validate province
def validate_province(province):
    valid_provinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
    return province.upper() in valid_provinces

# Function to validate payment method
def validate_payment_method(payment_method):
    valid_methods = ['FULL', 'MONTHLY', 'DOWN PAY']
    return payment_method.upper() in valid_methods

# Function to calculate insurance premium
def calculate_premium(constants, num_cars, extra_liability, glass_coverage, loaner_car):
    try:
        basic_premium = constants['basic_premium']
        discount_per_additional_car = constants['discount_per_additional_car']
        extra_liability_cost = constants['extra_liability_cost']
        glass_coverage_cost = constants['glass_coverage_cost']
        loaner_car_cost = constants['loaner_car_cost']
        
        base_premium = basic_premium + (num_cars - 1) * basic_premium * (1 - discount_per_additional_car)
        extra_costs = num_cars * (extra_liability * extra_liability_cost + glass_coverage * glass_coverage_cost + loaner_car * loaner_car_cost)
        
        total_premium = base_premium + extra_costs
        return total_premium, extra_costs
    except KeyError as e:
        print(f"Error calculating premium: missing constant {e}")
        raise

# Main function
def main():
    try:
        constants = load_constants(CONST_FILE)
        print(f"Loaded constants: {constants}")  # Debugging line to check constants
    except Exception as e:
        print(f"Error loading constants: {e}")
        return
    
    while True:
        # Input customer details
        first_name = input("Enter customer's first name: ").title()
        last_name = input("Enter customer's last name: ").title()
        address = input("Enter customer's address: ")
        city = input("Enter customer's city: ").title()
        province = input("Enter customer's province: ").upper()
        while not validate_province(province):
            print("Invalid province. Please enter again.")
            province = input("Enter customer's province: ").upper()
        postal_code = input("Enter customer's postal code: ")
        phone_number = input("Enter customer's phone number: ")
        
        # Insurance details
        num_cars = int(input("Enter number of cars being insured: "))
        extra_liability = input("Extra liability coverage (Y/N): ").upper() == 'Y'
        glass_coverage = input("Glass coverage (Y/N): ").upper() == 'Y'
        loaner_car = input("Loaner car (Y/N): ").upper() == 'Y'
        payment_method = input("Payment method (Full/Monthly/Down Pay): ").upper()
        while not validate_payment_method(payment_method):
            print("Invalid payment method. Please enter again.")
            payment_method = input("Payment method (Full/Monthly/Down Pay): ").upper()
        
        down_payment = 0
        if payment_method == 'DOWN PAY':
            down_payment = float(input("Enter down payment amount: "))
        
        # Claims
        claims = []
        while True:
            claim_number = input("Enter claim number (or 'done' to finish): ")
            if claim_number.lower() == 'done':
                break
            claim_date = input("Enter claim date (YYYY-MM-DD): ")
            claim_amount = float(input("Enter claim amount: "))
            claims.append({"claim_number": claim_number, "claim_date": claim_date, "claim_amount": claim_amount})
        
        # Calculate premium
        try:
            total_premium, extra_costs = calculate_premium(constants, num_cars, extra_liability, glass_coverage, loaner_car)
        except KeyError as e:
            print(f"Error calculating premium: missing constant {e}")
            return
        
        hst = total_premium * constants['hst_rate']
        total_cost = total_premium + hst
        
        if payment_method == 'FULL':
            monthly_payment = 0
        else:
            total_cost += constants['processing_fee']
            if down_payment > 0:
                total_cost -= down_payment
            monthly_payment = total_cost / 8
        
        # Display receipt
        print("\n----- Insurance Receipt -----")
        print(f"Policy Number: {constants['next_policy_number']}")
        print(f"Customer: {first_name} {last_name}")
        print(f"Address: {address}, {city}, {province}, {postal_code}")
        print(f"Phone: {phone_number}")
        print(f"Number of Cars: {num_cars}")
        print(f"Extra Liability: {'Yes' if extra_liability else 'No'}")
        print(f"Glass Coverage: {'Yes' if glass_coverage else 'No'}")
        print(f"Loaner Car: {'Yes' if loaner_car else 'No'}")
        print(f"Payment Method: {payment_method.title()}")
        if payment_method == 'DOWN PAY':
            print(f"Down Payment: ${down_payment:.2f}")
        print(f"Total Premium (before tax): ${total_premium:.2f}")
        print(f"HST: ${hst:.2f}")
        print(f"Total Cost: ${total_cost:.2f}")
        if monthly_payment > 0:
            print(f"Monthly Payment: ${monthly_payment:.2f}")
        print("\nPrevious Claims:")
        print("Claim #    Claim Date    Amount")
        for claim in claims:
            print(f"{claim['claim_number']}    {claim['claim_date']}    ${claim['claim_amount']:.2f}")
        
        # Save policy data
        policy_data = {
            "policy_number": constants['next_policy_number'],
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "province": province,
            "postal_code": postal_code,
            "phone_number": phone_number,
            "num_cars": num_cars,
            "extra_liability": extra_liability,
            "glass_coverage": glass_coverage,
            "loaner_car": loaner_car,
            "payment_method": payment_method,
            "down_payment": down_payment,
            "total_premium": total_premium,
            "hst": hst,
            "total_cost": total_cost,
            "monthly_payment": monthly_payment,
            "claims": claims
        }
        try:
            save_policy_data(policy_data)
        except Exception as e:
            print(f"Error saving policy data: {e}")
            return
        
        # Increment policy number
        constants['next_policy_number'] += 1
        
        # Update Const.dat file
        try:
            with open(CONST_FILE, 'w') as file:
                for key, value in constants.items():
                    file.write(f"{key}={value}\n")
        except Exception as e:
            print(f"Error updating constants file: {e}")
            return
        
        # Ask if user wants to enter another customer
        another = input("Do you want to enter another customer? (Y/N): ").upper()
        if another != 'Y':
            break

if __name__ == "__main__":
    main()

# Mortgage Payment Calculator using classes for FINE3300
# Assignment 2 - Loan Amortization and Payment Schedule
# This program builds on Assignment 1 and adds:
# - Term input from the user
# - Payment schedule generation using Pandas
# - Excel export (with 6 worksheets)
# - Graphing of loan balance decline using Matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# MortgagePayment class definition
class MortgagePayment:
    # Constructor to initialize quoted rate and amortization period
    def __init__(self, quoted_rate, amortization_years):
        self.__quoted_rate = quoted_rate / 100   # converting % rate to decimal
        self.__amortization_years = amortization_years

    # Private method: calculates present value of an annuity factor
    def __pva(self, r, n):
        return (1 - (1 + r) ** -n) / r

    # Public method: calculating all six periodic payment options
    def payments(self, principal):
        # Converting semi-annual rate to effective monthly rate
        semi_annual_rate = self.__quoted_rate / 2
        monthly_rate = (1 + semi_annual_rate) ** (1 / 6) - 1

        # Monthly payment
        n_monthly = self.__amortization_years * 12
        monthly_payment = principal * (monthly_rate / (1 - (1 + monthly_rate) ** -n_monthly))

        # Semi-monthly payment
        semi_monthly_rate = (1 + semi_annual_rate) ** (1 / 12) - 1
        n_semi_monthly = self.__amortization_years * 24
        semi_monthly_payment = principal * (semi_monthly_rate / (1 - (1 + semi_monthly_rate) ** -n_semi_monthly))

        # Bi-weekly payment
        biweekly_rate = (1 + semi_annual_rate) ** (1 / 13) - 1
        n_biweekly = self.__amortization_years * 26
        biweekly_payment = principal * (biweekly_rate / (1 - (1 + biweekly_rate) ** -n_biweekly))

        # Weekly payment
        weekly_rate = (1 + semi_annual_rate) ** (1 / 26) - 1
        n_weekly = self.__amortization_years * 52
        weekly_payment = principal * (weekly_rate / (1 - (1 + weekly_rate) ** -n_weekly))

        # Rapid options based on monthly payment
        rapid_biweekly_payment = monthly_payment / 2
        rapid_weekly_payment = monthly_payment / 4

        # Returning all payments rounded to 2 decimal places
        return (
            round(monthly_payment, 2),
            round(semi_monthly_payment, 2),
            round(biweekly_payment, 2),
            round(weekly_payment, 2),
            round(rapid_biweekly_payment, 2),
            round(rapid_weekly_payment, 2)
        )

    # New Method: builds a payment schedule for a given term and frequency
    def build_schedule(self, principal, term_years, frequency):
        semi_annual_rate = self.__quoted_rate / 2

        # Determine rate, periods, and payment based on frequency
        if frequency == "Monthly":
            f = 12
            rate = (1 + semi_annual_rate) ** (1 / 6) - 1
            payment = self.payments(principal)[0]
        elif frequency == "Semi-Monthly":
            f = 24
            rate = (1 + semi_annual_rate) ** (1 / 12) - 1
            payment = self.payments(principal)[1]
        elif frequency == "Bi-Weekly":
            f = 26
            rate = (1 + semi_annual_rate) ** (1 / 13) - 1
            payment = self.payments(principal)[2]
        elif frequency == "Weekly":
            f = 52
            rate = (1 + semi_annual_rate) ** (1 / 26) - 1
            payment = self.payments(principal)[3]
        elif frequency == "Rapid Bi-Weekly":
            f = 26
            rate = (1 + semi_annual_rate) ** (1 / 13) - 1
            payment = self.payments(principal)[4]
        elif frequency == "Rapid Weekly":
            f = 52
            rate = (1 + semi_annual_rate) ** (1 / 26) - 1
            payment = self.payments(principal)[5]
        else:
            raise ValueError("Invalid frequency")

        # Calculate the number of periods within the given term
        periods = int(term_years * f)

        # Initialize balance and an empty list for schedule data
        balance = principal
        rows = []

        # Loop to calculate payment breakdown for each period
        for period in range(1, periods + 1):
            start_balance = balance
            interest = start_balance * rate
            principal_paid = payment - interest
            end_balance = max(0, start_balance - principal_paid)
            rows.append([
                period,
                round(start_balance, 2),
                round(interest, 2),
                round(payment, 2),
                round(end_balance, 2)
            ])
            balance = end_balance
            if balance <= 0:
                break

        # Create a Pandas DataFrame from the schedule list
        df = pd.DataFrame(rows, columns=[
            "Period", "Starting Balance", "Interest", "Payment", "Ending Balance"
        ])

        return df


# Function to create Excel file and graph for all payment options
def create_outputs(principal, quoted_rate, amortization_years, term_years):
    # Create a MortgagePayment object
    mortgage = MortgagePayment(quoted_rate, amortization_years)

    # All six payment frequencies
    frequencies = [
        "Monthly",
        "Semi-Monthly",
        "Bi-Weekly",
        "Weekly",
        "Rapid Bi-Weekly",
        "Rapid Weekly"
    ]

    # Dictionary to hold all schedules
    schedules = {}
    for freq in frequencies:
        schedules[freq] = mortgage.build_schedule(principal, term_years, freq)

    # Saving all schedules to one Excel file with six worksheets
    with pd.ExcelWriter("LoanSchedules.xlsx") as writer:
        for freq, df in schedules.items():
            sheet_name = freq.replace(" ", "_").replace("-", "")
            df.to_excel(writer, index=False, sheet_name=sheet_name)

    # Creating a Matplotlib graph showing balance decline
    plt.figure(figsize=(10, 5))
    for freq, df in schedules.items():
        plt.plot(df["Period"], df["Ending Balance"], label=freq)

    plt.title("Loan Balance Decline by Payment Frequency")
    plt.xlabel("Period (within Term)")
    plt.ylabel("Ending Balance ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("LoanBalances.png", dpi=300)
    plt.close()

    print("Files created successfully:")
    print(" - LoanSchedules.xlsx")
    print(" - LoanBalances.png")


# Main program: getting user input and running the program
if __name__ == "__main__":
    print("WELCOME TO THE MORTGAGE PAYMENT CALCULATOR! :)")

    # Getting user inputs
    principal = float(input("Enter the mortgage principal amount: "))
    quoted_rate = float(input("Enter the quoted annual interest rate (ex. 2 for 2%): "))
    amortization_years = int(input("Enter the amortization period (in years): "))
    term_years = int(input("Enter the term of the mortgage (in years): "))

    # Creating object and displaying payment options
    mortgage = MortgagePayment(quoted_rate, amortization_years)
    payments = mortgage.payments(principal)

    print("HERE ARE YOUR MORTGAGE PAYMENT OPTIONS!:")
    print("Monthly Payment: $", payments[0])
    print("Semi-monthly Payment: $", payments[1])
    print("Bi-weekly Payment: $", payments[2])
    print("Weekly Payment: $", payments[3])
    print("Rapid Bi-weekly Payment: $", payments[4])
    print("Rapid Weekly Payment: $", payments[5])

    # Creating and saving the outputs
    create_outputs(principal, quoted_rate, amortization_years, term_years)

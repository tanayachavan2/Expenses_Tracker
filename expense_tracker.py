import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

CSV_FILE = 'expenses.csv'
FIELDS = ['Date', 'Item', 'Amount', 'Category','Payment Method']

def create_csv_if_not_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

def view_expenses():
    create_csv_if_not_exists()
    df = pd.read_csv(CSV_FILE)
    print(df)

def add_expense(Date, Item, Amount, Category, Payment_Method):
    create_csv_if_not_exists()
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({
            'Date': Date,
            'Item': Item,
            'Amount': Amount,
            'Category': Category,
            'Payment Method': Payment_Method
        })

#def view_expenses():
    #create_csv_if_not_exists()
    #df = pd.read_csv(CSV_FILE)
    #print(df)

def filter_by_category(category):
    create_csv_if_not_exists()
    df = pd.read_csv(CSV_FILE)
    filtered = df[df['Category'].str.lower() == category.lower()]
    print(filtered)

def summary():
    create_csv_if_not_exists()
    df = pd.read_csv(CSV_FILE)
    print("Expense Summary by Category:")
    print(df['Category'].value_counts())
    print("\nTotal Amount Spent: ", df['Amount'].sum())

    #ensuring amount is numeric for sum and plotting
    df["Category"] = df["Category"].str.strip().str.title() 
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_total = df[(df["Date"].dt.month == current_month) & (df["Date"].dt.year == current_year)]["Amount"].sum()
    if monthly_total > 10000:
        print(f"\n*** ALERT: Monthly budget exceeded! Total spent this month: {monthly_total} ***\n")


def main():
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Filter by Category")
        print("4. Summary")
        print("5. Show Chart")
        print("6. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            Date = datetime.now().strftime('%Y-%m-%d')
            Item = input("Enter item name: ")
            Amount = float(input("Enter amount: "))
            Payment_Method = input("Enter payment method (cash/card/UPI): ")
            Category = input("Enter category (food/travel/entertainment/other): ")

            add_expense(Date, Item, Amount, Category, Payment_Method)
            print("Expense added.")
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            category = input("Enter category to filter: ")
            filter_by_category(category)
        elif choice == '4':
            summary()
        elif choice == '5':
            create_csv_if_not_exists()
            df = pd.read_csv(CSV_FILE)
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            category_sums = df.groupby("Category")["Amount"].sum()

            plt.figure(figsize=(10,5))
            plt.bar(category_sums.index, category_sums.values, color="skyblue")
            plt.title("Expenses by Category")
            plt.xlabel("Category")
            plt.ylabel("Amount Spent")
            plt.show()

            category_sums.plot.pie(autopct='%1.1f%%', startangle=90, figsize=(6,6))
            plt.title("Spending Distribution")
            plt.ylabel("")
            plt.show()

        elif choice == '6':
            print("Exiting. Goodbye!")
            break
        else:                                               
            print("Invalid choice. Please try again.")
if __name__ == "__main__":      
    main()
    


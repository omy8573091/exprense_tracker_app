import csv
from datetime import datetime
import os
from typing import List, Dict, Optional

class PersonalExpenseTracker:
    """A comprehensive personal expense tracker with file storage"""
    
    def __init__(self):
        self.expenses: List[Dict] = []
        self.monthly_budget: float = 0.0
        self.filename = "expenses.csv"
        self._load_expenses()
    
    def _load_expenses(self) -> None:
        """Load expenses from CSV file if it exists"""
        if not os.path.exists(self.filename):
            return
            
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        # Validate and convert data
                        row['amount'] = float(row['amount'])
                        if not all(key in row for key in ['date', 'category', 'amount', 'description']):
                            continue
                        self.expenses.append(row)
                    except (ValueError, KeyError):
                        continue
        except Exception as e:
            print(f"Warning: Could not load expenses. {e}")

    def _save_expenses(self) -> bool:
        """Save expenses to CSV file"""
        try:
            with open(self.filename, 'w', newline='') as file:
                fieldnames = ['date', 'category', 'amount', 'description']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.expenses)
            return True
        except Exception as e:
            print(f"Error saving expenses: {e}")
            return False

    def _validate_date(self, date_str: str) -> bool:
        """Validate date format (DD-MM-YYYY)"""
        try:
            datetime.strptime(date_str, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def add_expense(self) -> None:
        """Add a new expense through user input"""
        print("\nAdd New Expense")
        
        # Get and validate date
        while True:
            date = input("Enter date (DD-MM-YYYY): ").strip()
            if self._validate_date(date):
                break
            print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Get category
        while True:
            category = input("Enter category (e.g., Food, Travel): ").strip()
            if category and category.isalpha():
                category = category.capitalize()
                break
            print("Category cannot be empty.")
        
        # Get amount
        while True:
            amount = input("Enter amount spent: ").strip()
            try:
                amount = float(amount)
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        # Get description
        while True:
            description = input("Enter description: ").strip()
            if description:
                break
            print("Description cannot be empty.")
        
        # Add to expenses
        self.expenses.append({
            'date': date,
            'category': category,
            'amount': amount,
            'description': description
        })
        print("Expense added successfully!")

    def view_expenses(self) -> None:
        """Display all expenses in a formatted table"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
        
        print("\nAll Expenses:")
        print("-" * 70)
        print(f"{'Date':10} | {'Category':15} | {'Amount':10} | Description")
        print("-" * 70)
        
        for expense in self.expenses:
            print(f"{expense['date']:10} | {expense['category']:15} | {expense['amount']:8.2f} | {expense['description']}")

    def set_budget(self) -> None:
        """Set or update the monthly budget"""
        while True:
            budget = input("\nEnter your monthly budget: ").strip()
            try:
                budget = float(budget)
                if budget < 0:
                    print("Budget must be positive.")
                    continue
                self.monthly_budget = budget
                print(f"Monthly budget set to {budget:.2f}")
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")

    def track_budget(self) -> None:
        """Display budget status and remaining balance"""
        if self.monthly_budget <= 0:
            print("\nPlease set your monthly budget first.")
            return
        
        total_spent = sum(expense['amount'] for expense in self.expenses)
        remaining = self.monthly_budget - total_spent
        
        print("\nBudget Summary:")
        print(f"Monthly Budget: {self.monthly_budget:.2f}")
        print(f"Total Expenses: {total_spent:.2f}")
        
        if remaining >= 0:
            print(f"Remaining Budget: {remaining:.2f}")
        else:
            print(f"⚠️ You've exceeded your budget by {abs(remaining):.2f}!")

    def show_menu(self) -> None:
        """Display the main menu"""
        print("\nPersonal Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Set Monthly Budget")
        print("4. Track Budget")
        print("5. Save & Exit")

    def run(self) -> None:
        """Run the expense tracker application"""
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.set_budget()
            elif choice == '4':
                self.track_budget()
            elif choice == '5':
                if self._save_expenses():
                    print("\nExpenses saved successfully. Goodbye!")
                else:
                    print("\nWarning: Expenses may not have saved correctly.")
                break
            else:
                print("Invalid choice. Please enter a number between 1-5.")

            input("\nPress Enter to continue...")

def main():
    """Initialize and run the expense tracker"""
    tracker = PersonalExpenseTracker()
    tracker.run()

if __name__ == "__main__":
    main()
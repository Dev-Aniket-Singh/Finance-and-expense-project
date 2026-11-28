from datetime import date, datetime, timedelta

# Activity 3: Problem decomposition - separate expense tracking module.
# Activity 6: Object modeling - Expense class with attributes and methods.
class Expense:
    def __init__(self):
        self.expense_records = []  # Stores each expense as a dictionary.
        self.monthly_thresholds = {}
        self.recurring_expenses = []
        self.id = 1

    # Activity 2: Flowchart 2 - repeat amount input until it is valid.
    def amount(self, prompt):
        while True:
            try:
                value = float(input(prompt).strip())

            except ValueError:
                print("Please enter a valid amount!")
                continue

            if 0 < value < float("inf"):
                return value
            else:
                print("Amount must be a finite number greater than zero!")

    # Activity 2: Flowchart 2 - validate date or use today.
    def valid_date(self, prompt="Enter date (DD-MM-YYYY, blank=today): "):
        while True:
            entered_date = input(prompt).strip()

            if entered_date == "":
                return date.today().strftime("%d-%m-%Y")

            try:
                correct_date = datetime.strptime(entered_date, "%d-%m-%Y")  # Converts text into a date.
                return correct_date.strftime("%d-%m-%Y")  # Converts the date back into text.
            except ValueError:
                print("Invalid date! Use DD-MM-YYYY.")

    def valid_month(self):
        while True:
            month = input("Enter month (MM-YYYY, blank=current month): ").strip()

            if month == "":
                return date.today().strftime("%m-%Y")

            try:
                correct_month = datetime.strptime(month, "%m-%Y")
                return correct_month.strftime("%m-%Y")
            except ValueError:
                print("Invalid month! Use MM-YYYY.")

    def next(self):
        expense_id = self.id
        self.id = self.id + 1
        return expense_id

    # Activity 3: Problem decomposition - filter records for a selected month.
    def records_for_month(self, month):
        records = []

        for record in self.expense_records:
            expense_month = record["date"][3:]  # Extracts MM-YYYY from DD-MM-YYYY.
            if expense_month == month:
                records.append(record)

        return records

    # Activity 1: Algorithm design - calculate total spending step by step.
    def total_amount(self, records):
        total = 0
        for record in records:
            total = total + record["amount"]
        return total

    # Activity 7: Data interpretation - group amounts and counts by category.
    def category_totals(self, records):
        totals = {}
        counts = {}

        for record in records:
            category = record["category"]
            amount = record["amount"]

            if category not in totals:
                totals[category] = 0
                counts[category] = 0

            totals[category] = totals[category] + amount
            counts[category] = counts[category] + 1

        return totals, counts

    # Activity 1: Algorithm design - collect, validate and save a daily expense.
    # Activity 2: Flowcharts 2 and 3 - input, optional recurring bill, save and check limit.
    def add(self):
        print("\n" + " ADD NEW EXPENSE ".center(70, "-"))

        expense_date = self.valid_date("Enter expense date (DD-MM-YYYY, blank=today): ")
        expense_amount = self.amount("Enter expense amount (₹): ")

        category = input("Enter category (Food, Travel, Bills, Shopping, etc.): ").strip().title()
        if category == "":
            category = "Other"

        subcategory = input("Enter sub-category: ").strip().title()
        if subcategory == "":
            subcategory = "General"

        seller = input("Enter seller: ").strip()
        if seller == "":
            seller = "Unspecified"

        description = input("Enter description: ").strip()
        if description == "":
            description = "Unspecified"

        while True:
            payment_method = input("Payment method (Cash/Card/UPI/Bank/Other): ").strip().capitalize()
            if payment_method != "":
                break
            print("Payment method cannot be empty!")

        repeat_bill = input("Is this a repeating bill? (y/n): ").strip().lower()

        record = {
            "id": self.next(),
            "date": expense_date,
            "time": datetime.now().strftime("%H:%M:%S"),
            "amount": expense_amount,
            "category": category,
            "subcategory": subcategory,
            "seller": seller,
            "description": description,
            "payment_method": payment_method
        }

        if repeat_bill == "y":
            self.add_recurring(record)

        self.expense_records.append(record)
        print(f"\nExpense #{record['id']} saved successfully!")

        self.check_threshold(expense_date[3:])

    # Activity 5: Decision tree - check the limit and display spending alerts.
    def check_threshold(self, month):
        if month not in self.monthly_thresholds:
            return

        records = self.records_for_month(month)
        total = self.total_amount(records)
        limit = self.monthly_thresholds[month]
        percentage = total / limit * 100

        if total >= limit:
            print(f"WARNING: Monthly limit for {month} reached or exceeded!")
            print(f"Limit: ₹{limit:,.2f} | Spent: ₹{total:,.2f}")
        elif total >= limit * 0.8:
            print(f"ALERT: You have used {percentage:.1f}% of your monthly limit.")
            print(f"Limit: ₹{limit:,.2f} | Spent: ₹{total:,.2f}")

    def view(self):
        selected_date = self.valid_date("Enter date to view (DD-MM-YYYY, blank=today): ")
        records = []

        for record in self.expense_records:
            if record["date"] == selected_date:
                records.append(record)

        print("\n" + f" DAILY EXPENSE REPORT — {selected_date} ".center(90, "-"))
        if len(records) == 0:
            print("No expenses recorded for this date!")
            return

        # Activity 4: Card sorting - Bubble Sort by transaction time.
        for i in range(len(records)):
            for j in range(len(records) - i - 1):
                if records[j]["time"] > records[j + 1]["time"]:
                    temp = records[j]
                    records[j] = records[j + 1]
                    records[j + 1] = temp  # Sorts by time using Bubble Sort.
        total = self.total_amount(records)

        for record in records:
            print(f"#{record['id']} | {record['time']} | ₹{record['amount']:,.2f}", end=" | ")
            print(f"{record['category']} | {record['seller']} | {record['description']} | {record['payment_method']}")

        print("-" * 90)
        print(f"Total spent: ₹{total:,.2f} | Transactions: {len(records)}")
        print("Category breakdown:")

        totals, counts = self.category_totals(records)
        for category in totals:
            amount = totals[category]
            percentage = amount / total * 100
            print(f" • {category}: ₹{amount:,.2f} ({percentage:.1f}%)")
        print("-" * 90)

    def edit_or_delete(self):
        try:
            expense_id = int(input("Enter expense ID to edit/delete: ").strip())
        except ValueError:
            print("Invalid ID!")
            return

        selected_record = None  # No matching expense has been found yet.
        for record in self.expense_records:
            if record["id"] == expense_id:
                selected_record = record
                break

        if selected_record is None:
            print("Expense ID not found!")
            return

        action = input("Choose action: [E]dit or [D]elete: ").strip().lower()

        if action == "e":
            self.edit_record(selected_record)
        elif action == "d":
            self.delete_record(selected_record)
        else:
            print("Invalid action! Enter e or d.")

    def edit_record(self, record):
        print("Press Enter to keep the previous value.")
        new_amount = input(f"Amount [{record['amount']}]: ").strip()
        if new_amount != "":
            try:
                value = float(new_amount)
            except ValueError:
                value = 0

            if 0 < value < float("inf"):
                record["amount"] = value
            else:
                print("Invalid amount. Keeping the previous value.")

        category = input(f"Category [{record['category']}]: ").strip()
        if category != "":
            record["category"] = category.title()

        subcategory = input(f"Sub-category [{record['subcategory']}]: ").strip()
        if subcategory != "":
            record["subcategory"] = subcategory.title()

        description = input(f"Description [{record['description']}]: ").strip()
        if description != "":
            record["description"] = description

        seller = input(f"Seller [{record['seller']}]: ").strip()
        if seller != "":
            record["seller"] = seller

        for recurring in self.recurring_expenses:
            if recurring["expense_id"] == record["id"]:
                recurring["amount"] = record["amount"]
                recurring["category"] = record["category"]
                recurring["description"] = record["description"]
                recurring["seller"] = record["seller"]
                break

        print("Expense updated.")
        print("-" * 90)

    def delete_record(self, record):
        for recurring in self.recurring_expenses:
            if recurring["expense_id"] == record["id"]:
                self.recurring_expenses.remove(recurring)
                print("Future recurring payments cancelled.")
                break

        self.expense_records.remove(record)
        print("Expense deleted.")
        print("-" * 90)

    def search(self):
        query = input("Search description, category, sub-category, seller or payment method: ").strip().lower()
        if query == "":
            return

        matches = []
        for record in self.expense_records:
            text = record["description"] + " " + record["category"]
            text = text + " " + record["subcategory"]
            text = text + " " + record["seller"]
            text = text + " " + record["payment_method"]
            text = text.lower()

            if query in text:
                matches.append(record)

        print("\n" + " EXPENSE SEARCH RESULTS ".center(90, "-"))
        if len(matches) == 0:
            print("No matching expenses found!")
            return

        for record in matches:
            print(f"#{record['id']} | {record['date']} | ₹{record['amount']:,.2f}", end=" | ")
            print(f"{record['category']} | {record['seller']} | {record['description']}")

        print("-" * 90)
        print("Matches found:", len(matches))
        print("-" * 90)

    # Activity 5: Decision tree - no records, no limit, limit reached, warning or safe.
    # Activity 7: Data interpretation - monthly totals and category percentages.
    def monthly_summary(self):
        month = self.valid_month()
        records = self.records_for_month(month)
        total = self.total_amount(records)

        print("\n" + f" MONTHLY EXPENSE DASHBOARD — {month} ".center(90, "-"))
        if len(records) == 0:
            print("No expenses recorded for this month!")
            print("-" * 90)
            return

        print(f"Total spending: ₹{total:,.2f}")
        print("Transactions:", len(records))

        if month in self.monthly_thresholds:
            limit = self.monthly_thresholds[month]
            print(f"Monthly spending limit: ₹{limit:,.2f}")

            if total >= limit:
                print("STATUS: LIMIT REACHED OR EXCEEDED!")
            elif total >= limit * 0.8:
                print("STATUS: WARNING! You have used at least 80% of the limit.")
            else:
                print("STATUS: SAFE. Within the monthly limit.")
        else:
            print("Threshold: Not set")

        totals, counts = self.category_totals(records)
        sorted_categories = list(totals.items())
        # Activity 4: Card sorting - Bubble Sort category totals in descending order.
        for i in range(len(sorted_categories)):
            for j in range(len(sorted_categories) - i - 1):
                if sorted_categories[j][1] < sorted_categories[j + 1][1]:
                    temp = sorted_categories[j]
                    sorted_categories[j] = sorted_categories[j + 1]
                    sorted_categories[j + 1] = temp  # Highest spending first.

        print("-" * 90)
        print("CATEGORY BREAKDOWN")
        for category, amount in sorted_categories:
            percentage = amount / total * 100
            print(f" • {category:<20} ₹{amount:>12,.2f} ({percentage:.2f}%)")
        print("-" * 90)

    # Activity 7: Data interpretation - category shares, bars and daily average.
    def analytics(self):
        if len(self.expense_records) == 0:
            print("No expense records available!")
            return

        totals, counts = self.category_totals(self.expense_records)
        total = self.total_amount(self.expense_records)

        unique_dates = set()  # A set keeps each date only once.
        for record in self.expense_records:
            unique_dates.add(record["date"])

        active_days = len(unique_dates)
        average = total / active_days
        sorted_categories = list(totals.items())
        # Activity 4: Card sorting - Bubble Sort category totals in descending order.
        for i in range(len(sorted_categories)):
            for j in range(len(sorted_categories) - i - 1):
                if sorted_categories[j][1] < sorted_categories[j + 1][1]:
                    temp = sorted_categories[j]
                    sorted_categories[j] = sorted_categories[j + 1]
                    sorted_categories[j + 1] = temp  # Highest spending first.

        print("\n" + " CATEGORY SPENDING ANALYTICS ".center(90, "-"))
        print("Category        | Count |  Total Amount  | Share   | Visual Share")
        print("-" * 90)

        for category, amount in sorted_categories:
            count = counts[category]
            percentage = amount / total * 100

            filled_blocks = int(percentage / 10)  # Each block represents 10%.
            empty_blocks = 10 - filled_blocks
            bar = "█" * filled_blocks + "░" * empty_blocks

            print(f"{category:<15} | {count:>5} | ₹{amount:>12,.2f} | {percentage:>6.1f}% | {bar}")

        print("-" * 90)
        print(f"Total lifetime spending: ₹{total:,.2f}")
        print("Total transactions:", len(self.expense_records))
        print(f"Average daily spend: ₹{average:,.2f} (across {active_days} active days)")
        print("-" * 90)

    def threshold(self):
        print("\n" + " SET MONTHLY EXPENSE THRESHOLD LIMIT ".center(90, "-"))
        month = self.valid_month()
        limit = self.amount("Enter maximum spending limit (₹): ")

        if month in self.monthly_thresholds:
            print(f"Threshold updated for {month}: ₹{limit:,.2f}")
        else:
            print(f"Threshold set for {month}: ₹{limit:,.2f}")

        self.monthly_thresholds[month] = limit
        print("-" * 90)

    # Activity 1: Algorithm design - calculate savings and savings rate.
    # Activity 5: Decision tree - classify savings as deficit, excellent or moderate.
    def calculator(self):
        print("\n" + " MONTHLY SAVINGS RATE CALCULATOR ".center(90, "-"))
        month = self.valid_month()
        records = self.records_for_month(month)
        total = self.total_amount(records)
        print(f"Total expenses for {month}: ₹{total:,.2f}")

        income = self.amount("Enter your total monthly income (₹): ")
        savings = income - total
        savings_rate = savings / income * 100  # Percentage of income saved.

        print("-" * 90)
        print(f"Monthly income: ₹{income:,.2f}")
        print(f"Monthly expenses: ₹{total:,.2f}")
        print(f"Net savings: ₹{savings:+,.2f}")
        print(f"Savings rate: {savings_rate:.2f}%")

        if savings < 0:
            print("STATUS: DEFICIT! Expenses are greater than income.")
        elif savings_rate >= 25:
            print("STATUS: EXCELLENT! Savings are at least 25% of income.")
        else:
            print("STATUS: MODERATE! Savings are below 25% of income.")
        print("-" * 90)

    # Activity 3: Problem decomposition - configure a recurring bill separately.
    def add_recurring(self, record):
        frequencies = ["Daily", "Weekly", "Monthly", "Yearly"]
        while True:
            frequency = input("How often? (Daily/Weekly/Monthly/Yearly): ").strip().capitalize()
            if frequency in frequencies:
                break
            print("Invalid frequency! Please try again.")

        skip_rule = input("Skip days/dates? (e.g. Weekends, Sundays, 25-12-2026 or None): ").strip()
        if skip_rule == "":
            skip_rule = "None"

        start_date = record["date"]
        end_date = self.read_end_date(start_date, frequency)
        next_due = self.next_occurrence(start_date, frequency)

        recurring = {
            "expense_id": record["id"],
            "description": record["description"],
            "category": record["category"],
            "amount": record["amount"],
            "seller": record["seller"],
            "frequency": frequency,
            "skip_rule": skip_rule,
            "start_date": start_date,
            "end_condition": end_date,
            "next_due": next_due
        }
        self.recurring_expenses.append(recurring)

    def read_end_date(self, start_date, frequency):
        start = datetime.strptime(start_date, "%d-%m-%Y").date()

        while True:
            entered_date = input("Recur until what date? (DD-MM-YYYY, blank=ongoing): ").strip()

            if entered_date == "":
                if frequency == "Daily":
                    end_date = self.next_occurrence(start_date, "Monthly")
                elif frequency == "Yearly":
                    end_date = self.change_month_or_year(start, 0, 10, start.day)
                    end_date = end_date.strftime("%d-%m-%Y")
                else:
                    end_date = self.next_occurrence(start_date, "Yearly")

                print("Ongoing selected. Schedule ends on:", end_date)
                return end_date

            try:
                end = datetime.strptime(entered_date, "%d-%m-%Y").date()
                if end < start:
                    print("End date cannot be before the start date!")
                else:
                    return end.strftime("%d-%m-%Y")
            except ValueError:
                print("Invalid date! Use DD-MM-YYYY.")

    def should_skip(self, due, skip_rule):
        rules = skip_rule.lower().split(",")

        for rule in rules:
            rule = rule.strip()
            if rule == "weekends" and due.weekday() >= 5:  # Saturday is 5 and Sunday is 6.
                return True
            if rule == "sundays" and due.weekday() == 6:
                return True
            if rule == due.strftime("%d-%m-%Y"):
                return True

        return False

    def days_in_month(self, year, month):
        if month == 2:
            if year % 400 == 0:
                return 29
            elif year % 100 == 0:
                return 28
            elif year % 4 == 0:
                return 29
            else:
                return 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    def change_month_or_year(self, current, months, years, original_day):
        year = current.year + years
        month = current.month + months

        if month > 12:
            month = month - 12
            year = year + 1

        day = original_day
        max_day = self.days_in_month(year, month)
        if day > max_day:
            day = max_day  # Avoids invalid dates such as 31 February.

        return date(year, month, day)

    def next_occurrence(self, due, frequency, original_day=None):
        current = datetime.strptime(due, "%d-%m-%Y").date()
        if original_day is None:
            original_day = current.day

        if frequency == "Daily":
            next_date = current + timedelta(days=1)
        elif frequency == "Weekly":
            next_date = current + timedelta(days=7)  # Moves the date one week ahead.
        elif frequency == "Monthly":
            next_date = self.change_month_or_year(current, 1, 0, original_day)
        elif frequency == "Yearly":
            next_date = self.change_month_or_year(current, 0, 1, original_day)
        else:
            raise ValueError("Invalid recurring frequency.")

        return next_date.strftime("%d-%m-%Y")

    def recurring_manager(self):
        print("\n" + " RECURRING EXPENSE MANAGER ".center(90, "─"))
        if len(self.recurring_expenses) == 0:
            print("No recurring expenses configured!")
            return

        for recurring in self.recurring_expenses:
            print(f"#{recurring['expense_id']} | {recurring['frequency']} | ₹{recurring['amount']:,.2f}")
            print(f"Category: {recurring['category']} | Description: {recurring['description']}")
            next_due = datetime.strptime(recurring["next_due"], "%d-%m-%Y").date()
            end = datetime.strptime(recurring["end_condition"], "%d-%m-%Y").date()
            if next_due > end:
                print("Next due: None (schedule completed)")
            else:
                print("Next due:", recurring["next_due"])
            print("End date:", recurring["end_condition"])
            print("-" * 90)

        choice = input("Generate due recurring expenses now? (y/n): ").strip().lower()
        if choice != "y":
            return

        entered_date = self.valid_date("Enter today's date (DD-MM-YYYY, blank=today): ")
        today = datetime.strptime(entered_date, "%d-%m-%Y").date()
        generated = 0

        for recurring in self.recurring_expenses:
            generated = generated + self.generate_due_payments(recurring, today)

        print("-" * 90)
        print(f"Successfully generated {generated} due recurring expense(s).")
        print("─" * 90)

    def generate_due_payments(self, recurring, today):
        start = datetime.strptime(recurring["start_date"], "%d-%m-%Y").date()
        end = datetime.strptime(recurring["end_condition"], "%d-%m-%Y").date()
        due = datetime.strptime(recurring["next_due"], "%d-%m-%Y").date()
        generated = 0

        while due <= today and due <= end:  # Processes only payments that are due.
            if not self.should_skip(due, recurring["skip_rule"]):
                record = {
                    "id": self.next(),
                    "date": due.strftime("%d-%m-%Y"),
                    "time": "00:00:00",
                    "amount": recurring["amount"],
                    "category": recurring["category"],
                    "subcategory": "Recurring Bill",
                    "seller": recurring["seller"],
                    "description": "[Recurring] " + recurring["description"],
                    "payment_method": "Automatic"
                }
                self.expense_records.append(record)
                generated = generated + 1

            next_date = self.next_occurrence(due.strftime("%d-%m-%Y"), recurring["frequency"], start.day)  # Keeps the original billing day.
            due = datetime.strptime(next_date, "%d-%m-%Y").date()

        recurring["next_due"] = due.strftime("%d-%m-%Y")  # Prevents duplicate payments next time.
        return generated

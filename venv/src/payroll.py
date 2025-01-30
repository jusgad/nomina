from datetime import datetime

class Payroll:
    @staticmethod
    def calculate_salary(base_salary, start_date):
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.now()
            days_worked = (end_date - start_date).days

            if days_worked < 0:
                return None, "Start date cannot be in the future!"

            # Calculate salary for the period (assuming 30 days in a month)
            salary_per_day = base_salary / 30
            total_salary = salary_per_day * days_worked
            return total_salary, None
        except Exception as e:
            return None, f"Calculation Error: {e}"
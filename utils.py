#Utility Module
#Helper functions used across the application


from datetime import date, datetime
import pandas as pd

def format_date(date_obj):
    #Format date object to string
    if date_obj is None:
        return "No deadline"
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
    return date_obj.strftime('%Y-%m-%d')

def calculate_days_remaining(due_date):
    #Calculate days remaining until deadline
    if due_date is None:
        return None
    
    if isinstance(due_date, str):
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    
    delta = due_date - date.today()
    return delta.days

def get_status_icon(status):
    #Return emoji icon for status
    icons = {
        'Completed': '✅',
        'Pending': '⏳',
        'In Progress': '🔄'
    }
    return icons.get(status, '📌')

def get_priority_icon(priority):
    #Return emoji icon for priority
    icons = {
        'High': '🔴',
        'Medium': '🟡',
        'Low': '🟢'
    }
    return icons.get(priority, '⚪')

def validate_task_title(title):
    #Validate task title
    if not title or title.strip() == "":
        return False, "Task title cannot be empty"
    if len(title) > 200:
        return False, "Task title too long (max 200 characters)"
    return True, "Valid"

def calculate_completion_rate(total, completed):
    """Calculate completion percentage"""
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)

def categorize_by_urgency(due_date, status):
    #Categorize task by urgency
    if status == 'Completed':
        return 'Completed'
    
    days = calculate_days_remaining(due_date)
    
    if days is None:
        return 'No Deadline'
    elif days < 0:
        return 'Overdue'
    elif days == 0:
        return 'Due Today'
    elif days <= 3:
        return 'Urgent'
    else:
        return 'On Track'
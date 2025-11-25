"""
Configuration Module
Contains all configuration settings and constants
"""

# Database Configuration
DB_NAME = 'tasks.db'

# Application Settings
APP_TITLE = "Task Progress Visualizer"
APP_ICON = "📊"
PAGE_LAYOUT = "wide"

# Categories
CATEGORIES = ["Work", "Personal", "Health", "Study", "Other"]

# Priority Levels
PRIORITIES = ["High", "Medium", "Low"]

# Status Options
STATUSES = ["Pending", "In Progress", "Completed"]

# Color Schemes for Visualizations
STATUS_COLORS = {
    'Completed': '#28a745',   # Green
    'Pending': '#ffc107',     # Yellow
    'In Progress': '#17a2b8'  # Blue
}

PRIORITY_COLORS = {
    'High': '#dc3545',        # Red
    'Medium': '#ffc107',      # Yellow
    'Low': '#28a745'          # Green
}

# Chart Settings
CHART_STYLE = 'seaborn'
FIGURE_SIZE = (10, 6)

# Export Settings
EXPORT_DATE_FORMAT = '%Y-%m-%d'
REPORT_HEADER = "TASK PROGRESS REPORT"
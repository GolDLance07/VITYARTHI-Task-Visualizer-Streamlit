# Report Generation Module
#for data export and report creation


import pandas as pd
from datetime import datetime
from config import REPORT_HEADER, EXPORT_DATE_FORMAT

class ReportGenerator:
    #Generates reports and exports
    
    @staticmethod
    def generate_csv(df):
        #Export tasks to CSV format
        return df.to_csv(index=False)
    
    @staticmethod
    def generate_json(df):
        #Export tasks to JSON format
        return df.to_json(orient='records', date_format='iso', indent=2)
    
    @staticmethod
    def generate_summary_report(stats, df):
        
        #Generate text summary report
        
        completion_rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        report = f"""
{REPORT_HEADER}
{'='*60}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW
--------
Total Tasks:          {stats['total']}
Completed:            {stats['completed']}
Pending:              {stats['pending']}
In Progress:          {stats['in_progress']}
Overdue:              {stats['overdue']}
Completion Rate:      {completion_rate:.1f}%

CATEGORY BREAKDOWN
------------------
"""
        
        if not df.empty:
            category_stats = df['category'].value_counts()
            for category, count in category_stats.items():
                report += f"{category:20s}: {count}\n"
            
            report += "\nPRIORITY BREAKDOWN\n"
            report += "------------------\n"
            
            priority_stats = df['priority'].value_counts()
            for priority, count in priority_stats.items():
                report += f"{priority:20s}: {count}\n"
            
            report += "\nSTATUS BREAKDOWN\n"
            report += "----------------\n"
            
            status_stats = df['status'].value_counts()
            for status, count in status_stats.items():
                report += f"{status:20s}: {count}\n"
        
        report += "\n" + "="*60 + "\n"
        report += "End of Report\n"
        
        return report
    
    @staticmethod
    def get_filename(extension):
        #Generate filename with timestamp
        timestamp = datetime.now().strftime(EXPORT_DATE_FORMAT)
        return f"tasks_{timestamp}.{extension}"
"""
Database Module - Task Management
Handles all database operations (CRUD)
"""

import sqlite3
import pandas as pd
from datetime import datetime, date
from config import DB_NAME

class TaskDatabase:
    """Database handler for task management"""
    
    def __init__(self):
        """Initialize database connection"""
        self.db_name = DB_NAME
        self.create_table()
    
    def get_connection(self):
        """Create and return database connection"""
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def create_table(self):
        """Create tasks table if not exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_task(self, title, description, category, priority, due_date):
        """
        Add new task to database
        Returns: True if successful, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO tasks (title, description, category, priority, due_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, description, category, priority, due_date))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding task: {e}")
            conn.close()
            return False
    
    def get_all_tasks(self):
        """
        Fetch all tasks
        Returns: DataFrame with all tasks
        """
        conn = self.get_connection()
        query = "SELECT * FROM tasks ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_task_by_id(self, task_id):
        """Get single task by ID"""
        conn = self.get_connection()
        query = "SELECT * FROM tasks WHERE id = ?"
        df = pd.read_sql_query(query, conn, params=(task_id,))
        conn.close()
        return df.iloc[0] if not df.empty else None
    
    def update_task_status(self, task_id, new_status):
        """
        Update task status
        Returns: True if successful
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if new_status == 'Completed':
                cursor.execute('''
                    UPDATE tasks 
                    SET status = ?, completed_at = ?
                    WHERE id = ?
                ''', (new_status, datetime.now(), task_id))
            else:
                cursor.execute('''
                    UPDATE tasks 
                    SET status = ?, completed_at = NULL
                    WHERE id = ?
                ''', (new_status, task_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            conn.close()
            return False
    
    def delete_task(self, task_id):
        """
        Delete task by ID
        Returns: True if successful
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            conn.close()
            return False
    
    def get_statistics(self):
        """
        Get task statistics
        Returns: Dictionary with stats
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        total = cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'Completed'"
        ).fetchone()[0]
        pending = cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'Pending'"
        ).fetchone()[0]
        in_progress = cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'In Progress'"
        ).fetchone()[0]
        overdue = cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE due_date < ? AND status != 'Completed'",
            (date.today(),)
        ).fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'overdue': overdue
        }
    
    def filter_tasks(self, status=None, category=None, priority=None):
        """
        Filter tasks by criteria
        Returns: Filtered DataFrame
        """
        conn = self.get_connection()
        
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if category:
            query += " AND category = ?"
            params.append(category)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
        query += " ORDER BY created_at DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
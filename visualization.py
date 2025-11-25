"""
Visualization Module
Generates charts and graphs for task analytics
"""

import matplotlib.pyplot as plt
import pandas as pd
from config import STATUS_COLORS, PRIORITY_COLORS, CHART_STYLE, FIGURE_SIZE



class TaskVisualizer:
    """Handles all visualization functions"""
    
    @staticmethod
    def create_status_pie_chart(df):
        """
        Chart 1: Pie chart showing task status distribution
        """
        if df.empty:
            return None
        
        status_counts = df['status'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        colors = [STATUS_COLORS.get(status, '#cccccc') for status in status_counts.index]
        
        wedges, texts, autotexts = ax.pie(
            status_counts.values,
            labels=status_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 11, 'weight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
        
        ax.set_title('Task Status Distribution', fontsize=14, weight='bold', pad=15)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def create_category_bar_chart(df):
        """
        Chart 2: Bar chart showing tasks by category
        """
        if df.empty:
            return None
        
        category_counts = df['category'].value_counts()
        
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        
        bars = ax.bar(
            category_counts.index,
            category_counts.values,
            color='#3498db',
            edgecolor='black'
        )
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10,
                weight='bold'
            )
        
        ax.set_xlabel('Category', fontsize=11, weight='bold')
        ax.set_ylabel('Number of Tasks', fontsize=11, weight='bold')
        ax.set_title('Tasks by Category', fontsize=14, weight='bold', pad=15)
        ax.grid(axis='y', alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def create_priority_bar_chart(df):
        """
        Chart 3: Bar chart showing tasks by priority
        """
        if df.empty:
            return None
        
        priority_order = ['High', 'Medium', 'Low']
        priority_counts = df['priority'].value_counts().reindex(priority_order, fill_value=0)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        colors = [PRIORITY_COLORS[p] for p in priority_order]
        
        bars = ax.bar(
            priority_order,
            priority_counts.values,
            color=colors,
            edgecolor='black'
        )
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=11,
                weight='bold'
            )
        
        ax.set_xlabel('Priority Level', fontsize=11, weight='bold')
        ax.set_ylabel('Number of Tasks', fontsize=11, weight='bold')
        ax.set_title('Tasks by Priority', fontsize=14, weight='bold', pad=15)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def create_completion_trend(df):
        """
        Chart 4: Line chart showing completion trend over time
        """
        if df.empty or 'completed_at' not in df.columns:
            return None
        
        completed_df = df[df['status'] == 'Completed'].copy()
        
        if completed_df.empty or completed_df['completed_at'].isna().all():
            return None
        
        completed_df['completed_date'] = pd.to_datetime(completed_df['completed_at']).dt.date
        trend = completed_df.groupby('completed_date').size().reset_index(name='count')
        
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        
        ax.plot(
            trend['completed_date'],
            trend['count'],
            marker='o',
            linewidth=2,
            markersize=8,
            color='#28a745'
        )
        
        ax.fill_between(
            trend['completed_date'],
            trend['count'],
            alpha=0.3,
            color='#28a745'
        )
        
        ax.set_xlabel('Date', fontsize=11, weight='bold')
        ax.set_ylabel('Tasks Completed', fontsize=11, weight='bold')
        ax.set_title('Completion Trend', fontsize=14, weight='bold', pad=15)
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig
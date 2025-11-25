"""
Main Application Module
Streamlit-based Task Progress Visualizer
"""

import streamlit as st
from datetime import date
import matplotlib.pyplot as plt

# Import custom modules
from database import TaskDatabase
from visualization import TaskVisualizer
from report import ReportGenerator
from config import *
from utils import *

# ============= PAGE CONFIGURATION =============
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT
)

# ============= INITIALIZE DATABASE =============
@st.cache_resource
def init_database():
    """Initialize database (cached)"""
    return TaskDatabase()

db = init_database()
visualizer = TaskVisualizer()
reporter = ReportGenerator()

# ============= CUSTOM CSS =============
st.markdown("""
<style>
    .main > div {padding-top: 2rem;}
    h1 {color: #2c3e50; text-align: center;}
    .stButton>button {width: 100%; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# ============= HEADER =============
st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("### Organize Tasks • Track Progress • Achieve Goals")
st.markdown("---")

# ============= SIDEBAR - ADD TASK =============
with st.sidebar:
    st.header("➕ Add New Task")
    #Takes Input to Add Task
    with st.form("task_form"):
        title = st.text_input("Task Title*", placeholder="Enter task name")
        description = st.text_area("Description", placeholder="Task details (optional)")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", CATEGORIES)
        with col2:
            priority = st.selectbox("Priority", PRIORITIES)
        
        due_date = st.date_input("Due Date", value=None)
        
        submitted = st.form_submit_button("Add Task", type="primary")
        
        if submitted:
            # Validate input
            is_valid, message = validate_task_title(title)
            
            if is_valid:
                success = db.add_task(
                    title.strip(),
                    description.strip(),
                    category,
                    priority,
                    due_date if due_date else None
                )
                
                if success:
                    st.success("✅ Task added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Error adding task")
            else:
                st.error(f"⚠️ {message}")
    
    st.markdown("---")
    
    # FILTERS
    st.header("🔧 Filters")
    filter_status = st.selectbox("Status", ["All"] + STATUSES)
    filter_category = st.selectbox("Category", ["All"] + CATEGORIES)
    filter_priority = st.selectbox("Priority", ["All"] + PRIORITIES)

# ============= MAIN AREA =============

# Get Statistics
stats = db.get_statistics()

# Display Metrics
st.markdown("## 📊 Dashboard")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tasks", stats['total'])
col2.metric("Completed", stats['completed'])
col3.metric("Pending", stats['pending'])
col4.metric("Overdue", stats['overdue'])

# Progress Bar
if stats['total'] > 0:
    progress = stats['completed'] / stats['total']
    st.progress(progress, text=f"Progress: {progress*100:.1f}%")

st.markdown("---")

# ============= VISUALIZATIONS =============
st.markdown("## 📈 Analytics")

tasks_df = db.get_all_tasks()

if not tasks_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = visualizer.create_status_pie_chart(tasks_df)
        if fig1:
            st.pyplot(fig1)
            plt.close()
        
        fig3 = visualizer.create_priority_bar_chart(tasks_df)
        if fig3:
            st.pyplot(fig3)
            plt.close()
    
    with col2:
        fig2 = visualizer.create_category_bar_chart(tasks_df)
        if fig2:
            st.pyplot(fig2)
            plt.close()
        
        fig4 = visualizer.create_completion_trend(tasks_df)
        if fig4:
            st.pyplot(fig4)
            plt.close()
        else:
            st.info("Complete tasks to see trends")
    
    # Export Section
    with st.expander("📥 Export Reports"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = reporter.generate_csv(tasks_df)
            st.download_button(
                "📄 CSV",
                csv,
                reporter.get_filename("csv"),
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            json_data = reporter.generate_json(tasks_df)
            st.download_button(
                "📋 JSON",
                json_data,
                reporter.get_filename("json"),
                "application/json",
                use_container_width=True
            )
        
        with col3:
            summary = reporter.generate_summary_report(stats, tasks_df)
            st.download_button(
                "📊 Report",
                summary,
                reporter.get_filename("txt"),
                "text/plain",
                use_container_width=True
            )

st.markdown("---")

# ============= TASK LIST =============
st.markdown("## 📝 Task List")

# Apply filters
filtered_df = tasks_df.copy() if not tasks_df.empty else tasks_df

if not filtered_df.empty:
    if filter_status != "All":
        filtered_df = filtered_df[filtered_df['status'] == filter_status]
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == filter_category]
    if filter_priority != "All":
        filtered_df = filtered_df[filtered_df['priority'] == filter_priority]

st.caption(f"Showing {len(filtered_df)} of {len(tasks_df)} tasks")

if filtered_df.empty:
    st.info("No tasks found. Add your first task!")
else:
    for idx, task in filtered_df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 1])
            
            with col1:
                status_icon = get_status_icon(task['status'])
                st.markdown(f"### {status_icon} {task['title']}")
                if task['description']:
                    st.caption(task['description'])
            
            with col2:
                st.write(f"**{task['category']}**")
            
            with col3:
                priority_icon = get_priority_icon(task['priority'])
                st.write(f"{priority_icon} {task['priority']}")
            
            with col4:
                if task['due_date']:
                    days = calculate_days_remaining(task['due_date'])
                    if days < 0 and task['status'] != 'Completed':
                        st.error(f"⚠️ Overdue")
                    elif days == 0:
                        st.warning("📅 Today")
                    else:
                        st.info(f"📅 {task['due_date']}")
            
            with col5:
                if task['status'] != 'Completed':
                    if st.button("✓", key=f"c_{task['id']}"):
                        db.update_task_status(task['id'], 'Completed')
                        st.rerun()
                
                if st.button("🗑️", key=f"d_{task['id']}"):
                    db.delete_task(task['id'])
                    st.rerun()
            
            st.markdown("---")

# Footer
st.markdown("---")
st.caption("Built with Python & Streamlit | Task Progress Visualizer v1.0")

import streamlit as st

SUBJECT_COL = "Subject/Skill"
RATING_COL = "Excellence Rating"
STATUS_COL = "Status"

def setup_page():
    st.set_page_config(page_title="StudyOS v13.0", page_icon="🔥", layout="wide")

def get_css():
    return """
    <style>
        /* Main Background */
        .stApp { background-color: #0d1117; }
        
        /* Text */
        h1, h2, h3 { color: #e6edf3 !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        p, label, span, div { color: #848d97; }
        
        /* --- SIDEBAR STYLING --- */
        section[data-testid="stSidebar"] { 
            background-color: #010409; 
            border-right: 1px solid #30363d; 
        }
        
        /* HIDE SIDEBAR SCROLLBARS */
        section[data-testid="stSidebar"] > div {
            scrollbar-width: none; 
            -ms-overflow-style: none;
            overflow-x: hidden;
        }
        section[data-testid="stSidebar"] > div::-webkit-scrollbar { display: none; }
        
        /* Metric */
        div[data-testid="stMetricValue"] {
            color: #39d353 !important;
            text-shadow: 0 0 10px rgba(57, 211, 83, 0.4);
            font-size: 32px !important;
            font-weight: bold;
        }
        div[data-testid="stMetricLabel"] { display: none; } 

        /* Green Accents */
        :root { --primary-color: #39d353; }
        div[data-testid="stCheckbox"] label span { border-color: #39d353 !important; }
        div[data-testid="stCheckbox"] label span[data-checked="true"] { background-color: #39d353 !important; }
        
        /* Toggle Switch */
        div[data-testid="stToggle"] label div[data-checked="true"] { background-color: #39d353 !important; }

        /* Inputs */
        div[data-testid="stSelectbox"] > div > div { background-color: #0d1117; color: #e6edf3; border: 1px solid #30363d; }
        div[data-testid="stTextInput"] > div > div { background-color: #0d1117; color: #e6edf3; border: 1px solid #30363d; }
        div[data-testid="stCheckbox"] { display: flex; justify-content: center; }

        /* --- HEATMAP CSS ENGINE --- */
        .graph-container {
            display: flex; flex-direction: column; 
            padding: 15px;
            background-color: #0d1117; 
            border: 1px solid #30363d;
            border-radius: 6px; 
            margin-bottom: 20px; 
            
            /* SCROLLING FIXES */
            overflow-x: auto;       
            overflow-y: hidden;     
            max-width: fit-content; 
            margin-left: auto;      
            margin-right: auto;
            
            /* Hide Scrollbar */
            scrollbar-width: none;  
            -ms-overflow-style: none;
            
            /* --- CURSOR FIX (New) --- */
            cursor: default;     /* Forces arrow cursor */
            user-select: none;   /* Prevents highlighting text */
            -webkit-user-select: none;
        }
        .graph-container::-webkit-scrollbar { display: none; }

        .heatmap-center-wrapper { width: max-content; margin: 0 auto; }
        
        /* YEARLY MAP STYLES */
        .months-row { 
            position: relative; height: 15px; margin-left: 30px; margin-bottom: 5px; 
            width: calc(100% - 30px); 
        }
        .month-label { position: absolute; font-size: 10px; color: #848d97; }
        
        .graph-body { display: flex; }
        .weekdays-col { 
            display: flex; flex-direction: column; justify-content: space-between; 
            width: 30px; margin-right: 5px; padding-top: 2px; height: 86px; 
            position: sticky; left: 0; background: #0d1117; z-index: 5;
        }
        .weekday-label { font-size: 9px; color: #848d97; height: 10px; line-height: 10px; }
        .squares-grid-year { display: grid; grid-template-rows: repeat(7, 10px); grid-auto-flow: column; gap: 3px; }
        
        /* MONTHLY MAP STYLES */
        .heatmap-grid-month {
            display: grid; grid-template-columns: repeat(7, 20px); gap: 3px; margin-top: 5px; justify-content: center;
        }
        .month-header {
            display: grid; grid-template-columns: repeat(7, 20px); gap: 3px; margin-bottom: 3px;
            text-align: center; font-size: 8px; font-weight: bold; justify-content: center;
        }
        .day-cell {
            width: 10px; height: 10px; border-radius: 2px;
            background-color: #161b22; transition: all 0.2s;
            cursor: pointer; /* Pointer on hover for interactivity feel */
        }
        .day-cell:hover { transform: scale(1.4); border: 1px solid #fff; z-index:10; }
        .month-cell {
            width: 20px; height: 20px; border-radius: 4px;
            display: flex; align-items: center; justify-content: center;
            font-size: 8px; color: #fff; font-weight: bold; background-color: #161b22;
            transition: all 0.2s; border: 1px solid #1f242c;
            cursor: default;
        }
        .month-cell:hover { transform: scale(1.2); border: 1px solid #fff; z-index: 5; }
    </style>
    """
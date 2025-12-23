import pandas as pd
import os
import time
import calendar
from datetime import datetime
import streamlit as st
from .config import SUBJECT_COL, RATING_COL, STATUS_COL

def get_file_path(year):
    return f"studyProgress{year}.xlsx"

def get_month_days(year, month_name):
    month_index = list(calendar.month_name).index(month_name)
    _, num_days = calendar.monthrange(year, month_index)
    return num_days

def generate_date_columns(year, month_name):
    month_index = list(calendar.month_name).index(month_name)
    num_days = get_month_days(year, month_name)
    return [f"Date {year}-{month_index:02d}-{day:02d}" for day in range(1, num_days + 1)]

def ensure_file_and_sheet_exist(year, month_name):
    filename = get_file_path(year)
    if not os.path.exists(filename):
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            pd.DataFrame().to_excel(writer, sheet_name=month_name)
    try:
        xls = pd.ExcelFile(filename)
        if month_name not in xls.sheet_names:
            cols = [SUBJECT_COL, RATING_COL, STATUS_COL] + generate_date_columns(year, month_name)
            # --- PLACEMENT DEFAULT SKILLS ---
            defaults = [
                ("DSA (LeetCode)", 0, "Active"), 
                ("React / Dev", 0, "Active"),
                ("Aptitude", 0, "Active"),
                ("CS Fundamentals", 0, "On Hold")
            ]
            data = []
            for subj, rate, stat in defaults:
                row = {SUBJECT_COL: subj, RATING_COL: rate, STATUS_COL: stat}
                for d_col in cols[3:]: row[d_col] = False
                data.append(row)
            df = pd.DataFrame(data)
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=month_name, index=False)
    except Exception as e:
        st.error(f"⚠️ Data Init Error: {e}")
        st.stop()

def load_data(year, month_name):
    ensure_file_and_sheet_exist(year, month_name)
    filename = get_file_path(year)
    df = pd.read_excel(filename, sheet_name=month_name)
    if STATUS_COL not in df.columns:
        loc_index = 2 if len(df.columns) >= 2 else 1
        df.insert(loc_index, STATUS_COL, "Active")
    return df

def save_data(df, year, month_name):
    filename = get_file_path(year)
    if STATUS_COL in df.columns: df[STATUS_COL] = df[STATUS_COL].fillna("Active")
    if RATING_COL in df.columns: df[RATING_COL] = df[RATING_COL].fillna(0)
    df = df.fillna(False)
    
    success = False
    for attempt in range(5):
        try:
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=month_name, index=False)
            success = True
            break 
        except PermissionError:
            time.sleep(0.5)
        except Exception as e:
            st.error(f"Save Error: {e}")
            return
    if not success:
        st.error("⚠️ Save Failed! Excel file is locked.")

def get_yearly_activity(year):
    filename = get_file_path(year)
    if not os.path.exists(filename): return pd.Series(dtype=int)
    xls = pd.ExcelFile(filename)
    all_dates = {}
    for sheet in xls.sheet_names:
        df = pd.read_excel(filename, sheet_name=sheet)
        date_cols = [c for c in df.columns if c.startswith("Date ")]
        for col in date_cols:
            try:
                date_str = col.replace("Date ", "")
                count = df[col].replace({'True': True, 'False': False}).fillna(False).sum()
                all_dates[date_str] = count
            except: pass
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    full_idx = pd.date_range(start=start_date, end=end_date, freq='D')
    yearly_series = pd.Series(index=full_idx, data=0)
    for date_str, count in all_dates.items():
        try:
            dt = pd.to_datetime(date_str)
            if dt in yearly_series.index: yearly_series[dt] = count
        except: pass
    return yearly_series

def calculate_global_streak(df, date_cols):
    if df.empty or not date_cols: return 0
    daily_activity = df[date_cols].replace({'True': True, 'False': False}).fillna(False).any(axis=0)
    today = datetime.now()
    today_str = f"Date {today.year}-{today.month:02d}-{today.day:02d}"
    if today_str in daily_activity.index:
        today_idx = list(daily_activity.index).index(today_str)
        relevant_days = daily_activity.iloc[:today_idx+1]
    else: relevant_days = daily_activity
    streak = 0
    values = relevant_days.values
    for val in reversed(values):
        if val: streak += 1
        else: break
    if streak == 0 and len(values) > 1:
        prev_values = values[:-1]
        prev_streak = 0
        for val in reversed(prev_values):
            if val: prev_streak += 1
            else: break
        if prev_streak > 0: streak = prev_streak
    return streak
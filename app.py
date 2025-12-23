import streamlit as st
import pandas as pd
import os
import time
import calendar
from datetime import datetime
import plotly.express as px

from modules.config import setup_page, get_css, SUBJECT_COL, RATING_COL, STATUS_COL
from modules.data_engine import (
    load_data, save_data, calculate_global_streak, 
    generate_date_columns, get_yearly_activity
)
from modules.renderer import render_yearly_heatmap, render_monthly_panel

# 1. SETUP
setup_page()
st.markdown(get_css(), unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.title("💻 StudyOS")
    st.caption("Kernel v13.0 (Modular)")
    st.divider()
    
    current_year = datetime.now().year
    years = list(range(2024, 2031))
    sel_year = st.selectbox("Year", years, index=years.index(current_year) if current_year in years else 0)
    
    current_month_index = datetime.now().month - 1
    months = list(calendar.month_name)[1:]
    sel_month = st.selectbox("Month", months, index=current_month_index if sel_year == current_year else 0)
    
    st.divider()
    with st.expander("🛠️ Manage Subjects"):
        new_subj = st.text_input("New Subject")
        if st.button("➕ Add", width="stretch"):
            if new_subj:
                try:
                    df_curr = load_data(sel_year, sel_month)
                    if new_subj not in df_curr[SUBJECT_COL].values:
                        new_row = {SUBJECT_COL: new_subj, RATING_COL: 0, STATUS_COL: "Active"}
                        for col in df_curr.columns:
                            if col not in new_row: new_row[col] = False
                        df_curr = pd.concat([df_curr, pd.DataFrame([new_row])], ignore_index=True)
                        save_data(df_curr, sel_year, sel_month)
                        st.rerun()
                except Exception as e: st.error(e)

        if st.button("🗑️ Delete", width="stretch"):
            st.warning("Delete using checkboxes in table.")
    st.divider()
    if st.button("🔴 Shut Down", width="stretch"):
        st.warning("Halting...")
        time.sleep(0.5)
        os._exit(0)

# 3. MAIN PAGE
c_title, c_streak = st.columns([3, 1])
with c_title: st.title(f"📅 {sel_month} {sel_year}")

try:
    df = load_data(sel_year, sel_month)
except:
    st.error(f"Please close **studyProgress{sel_year}.xlsx**.")
    st.stop()

# Prep
month_idx = list(calendar.month_name).index(sel_month)
today = datetime.now()
is_current = (sel_year == today.year) and (month_idx == today.month)
expected_date_cols = generate_date_columns(sel_year, sel_month)
valid_date_cols = [c for c in expected_date_cols if c in df.columns]

# Streak
global_streak = calculate_global_streak(df, valid_date_cols)
with c_streak: st.metric(label="Streak", value=f"🔥 {global_streak} Days")

# Smart Focus Toggle
show_history = st.toggle("📜 Show Full History", value=False)

if is_current and not show_history:
    today_str = f"Date {today.year}-{today.month:02d}-{today.day:02d}"
    if today_str in expected_date_cols:
        idx = expected_date_cols.index(today_str)
        start_idx = max(0, idx - 3) 
        visible_date_cols = expected_date_cols[start_idx:]
    else: visible_date_cols = expected_date_cols 
else: visible_date_cols = expected_date_cols

# 4. SPLIT LAYOUT
col_main, col_right = st.columns([4, 1])

with col_main:
    # TABLE
    column_config = {
        SUBJECT_COL: st.column_config.TextColumn("Subject", width="medium", pinned=True, disabled=True),
        RATING_COL: st.column_config.NumberColumn("Rating", format="%d ⭐", width="small", pinned=True),
        STATUS_COL: st.column_config.SelectboxColumn("Status", options=["Active", "Completed", "On Hold", "Dropped"], width="small", pinned=True, required=True)
    }
    for i, col_name in enumerate(visible_date_cols, 1):
        day_num = int(col_name.split("-")[-1])
        label = f"⭐ {day_num}" if (is_current and day_num == today.day) else f"{day_num}"
        column_config[col_name] = st.column_config.CheckboxColumn(label, width="small", default=False)

    for col in expected_date_cols:
        if col not in df.columns: df[col] = False

    display_cols = [SUBJECT_COL, RATING_COL, STATUS_COL] + visible_date_cols
    safe_cols = [c for c in display_cols if c in df.columns]

    edited_df = st.data_editor(
        df[safe_cols],
        column_config=column_config,
        width="stretch",
        hide_index=True,
        height=350,
        num_rows="fixed"
    )

    if not df[safe_cols].equals(edited_df):
        df.update(edited_df)
        try:
            save_data(df, sel_year, sel_month)
            st.rerun()
        except: st.error("⚠️ Close the Excel file to save changes!")
        
with col_right:
    if not edited_df.empty:
        html_month = render_monthly_panel(df, sel_year, sel_month)
        st.markdown(html_month, unsafe_allow_html=True)
    else:
        st.info("No data.")

# 5. DROPDOWN ANALYTICS
st.divider()
view_option = st.selectbox("📊 Additional Analytics:", ["🌍 Yearly Consistency", "🔥 Streaks", "📈 Total Study Volume"], index=0)
st.write("") 

if not df.empty:
    numeric_data = df[valid_date_cols].replace({'True': True, 'False': False}).fillna(False).astype(int)

    if view_option == "🌍 Yearly Consistency":
        yearly_series = get_yearly_activity(sel_year)
        if not yearly_series.empty:
            html_year = render_yearly_heatmap(yearly_series)
            st.markdown(html_year, unsafe_allow_html=True)
        else: st.warning("No data recorded for this year yet.")
            
    elif view_option == "🔥 Streaks":
        counts = numeric_data.sum(axis=1)
        res = pd.DataFrame({SUBJECT_COL: df[SUBJECT_COL], "Total Days": counts})
        res["Status"] = res["Total Days"].apply(lambda x: "🔥🔥🔥" if x>10 else ("🔥" if x>3 else "❄️"))
        st.dataframe(res, width="stretch", hide_index=True)
        
    elif view_option == "📈 Total Study Volume":
        counts = numeric_data.sum(axis=1)
        plot_df = pd.DataFrame({SUBJECT_COL: df[SUBJECT_COL], "Days": counts}).sort_values("Days", ascending=True)
        fig_bar = px.bar(plot_df, x="Days", y=SUBJECT_COL, orientation='h', text="Days", color="Days", color_continuous_scale=["#0e4429", "#39d353"])
        
        fig_bar.update_layout(
            plot_bgcolor='#0d1117', 
            paper_bgcolor='#0d1117', 
            font_color='#e6edf3', 
            margin=dict(t=0, l=0, r=0, b=0), 
            height=300,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        fig_bar.update_coloraxes(showscale=False)
        
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
else:
    st.info("No data available.")
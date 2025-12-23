import calendar

def get_color(count, max_val):
    if count == 0: return "#161b22"
    if max_val == 0: max_val = 1
    intensity = count / max(max_val, 1)
    if intensity <= 0.25: return "#0e4429"
    if intensity <= 0.50: return "#006d32"
    if intensity <= 0.75: return "#26a641"
    return "#39d353"

def render_yearly_heatmap(series):
    max_val = series.max()
    colors = {}
    titles = {}
    for w in range(54):
        for d in range(7):
            colors[(w, d)] = "transparent"
            titles[(w, d)] = ""
    for date, count in series.items():
        day_of_year = date.timetuple().tm_yday - 1
        start_weekday = series.index[0].weekday()
        week_idx = (day_of_year + start_weekday) // 7
        weekday_idx = date.weekday()
        if week_idx < 54:
            colors[(week_idx, weekday_idx)] = get_color(count, max_val)
            titles[(week_idx, weekday_idx)] = f"{date.strftime('%b %d')}: {count}"
    
    month_positions = {}
    for date in series.index:
        if date.day == 1:
            day_of_year = date.timetuple().tm_yday - 1
            start_weekday = series.index[0].weekday()
            week_idx = (day_of_year + start_weekday) // 7
            if date.month not in month_positions: month_positions[date.month] = week_idx
                
    month_html = '<div class="months-row">'
    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    CELL_WIDTH = 13 
    for m in range(1, 13):
        if m in month_positions:
            w_idx = month_positions[m]
            left_px = w_idx * CELL_WIDTH
            month_html += f'<div class="month-label" style="left: {left_px}px;">{month_names[m]}</div>'
    month_html += '</div>'

    grid_html = '<div class="squares-grid-year">'
    for w in range(54):
        for d in range(7):
            c = colors.get((w, d), "transparent")
            t = titles.get((w, d), "")
            vis = "hidden" if c == "transparent" else "visible"
            grid_html += f'<div class="day-cell" style="background-color: {c}; visibility: {vis};" title="{t}"></div>'
    grid_html += '</div>'

    return f"""
    <div class="graph-container">
      <div class="heatmap-center-wrapper">
        {month_html}
        <div class="graph-body">
            <div class="weekdays-col">
                <div class="weekday-label">Mon</div><div class="weekday-label"></div>
                <div class="weekday-label">Wed</div><div class="weekday-label"></div>
                <div class="weekday-label">Fri</div><div class="weekday-label"></div><div class="weekday-label"></div>
            </div>
            {grid_html}
        </div>
      </div>
    </div>
    """

def render_monthly_panel(df, year, month_name):
    date_cols = [c for c in df.columns if c.startswith("Date ")]
    daily_counts = {}
    max_val = 1
    for col in date_cols:
        d_str = col.replace("Date ", "")
        cnt = df[col].replace({'True': True, 'False': False}).fillna(False).sum()
        daily_counts[d_str] = cnt
        if cnt > max_val: max_val = cnt

    month_idx = list(calendar.month_name).index(month_name)
    cal = calendar.monthcalendar(year, month_idx)
    
    html = '<div class="graph-container" style="align-items: center; padding: 10px;">'
    html += f'<div style="color: #e6edf3; font-size: 12px; font-weight: bold; margin-bottom: 5px;">{month_name}</div>'
    html += '<div class="month-header">'
    for d in ["M","T","W","T","F","S","S"]: html += f'<div>{d}</div>'
    html += '</div>'
    html += '<div class="heatmap-grid-month">'
    for week in cal:
        for day in week:
            if day == 0: html += '<div class="month-cell" style="background-color: transparent; border: none;"></div>'
            else:
                d_str = f"{year}-{month_idx:02d}-{day:02d}"
                count = daily_counts.get(d_str, 0)
                color = get_color(count, max_val)
                html += f'<div class="month-cell" style="background-color: {color};" title="{d_str}: {count}">{day}</div>'
    html += '</div></div>'
    return html
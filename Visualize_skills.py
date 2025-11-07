import pandas as pd
from collections import Counter
import os
from math import pi

from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Category20
from bokeh.transform import cumsum
from bokeh.embed import components



def create_skills_chart(all_job_data):
    """
    MODIFIED: Takes a DataFrame and RETURNS chart components.
    """
    print("Generating Top 10 Skills chart...")
    df = all_job_data.copy()
    df = df.dropna(subset=['skills'])
    df = df[df['skills'].str.lower() != 'n/a']
    if df.empty: return None

    skill_counter = Counter()
    for skills_list in df['skills']:
        skills = [skill.strip() for skill in skills_list.split('|')]
        skill_counter.update(skills)
    if not skill_counter: return None

    top_skills = skill_counter.most_common(10)
    skills, counts = zip(*top_skills)
    source = ColumnDataSource(data={'skills': skills, 'counts': counts})

    TOOLTIPS = [("Skill", "@skills"), ("Job Count", "@counts")]
    p = figure(x_range=skills, height=350, title="Top 10 In-Demand Skills",
               tooltips=TOOLTIPS, tools="pan,wheel_zoom,box_zoom,reset")
    p.vbar(x='skills', top='counts', width=0.8, source=source, color="#53B0B2")
    p.xaxis.major_label_orientation = 0.4
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return components(p)


def create_locations_chart(all_job_data):
    """
    MODIFIED: Takes a DataFrame and RETURNS chart components.
    """
    print("Generating Top Locations chart...")
    df = all_job_data.copy()
    df = df.dropna(subset=['location'])
    df = df[df['location'].str.lower() != 'n/a']
    if df.empty: return None

    location_counter = Counter()
    for loc_string in df['location']:
        locs_comma_split = loc_string.split(',')
        for loc in locs_comma_split:
            locs_slash_split = loc.split('/')
            for final_loc in locs_slash_split:
                cleaned = final_loc.strip().lower()
                if cleaned: location_counter.update([cleaned])
    if not location_counter: return None

    top_locs_data = location_counter.most_common(7)
    loc_df = pd.DataFrame(top_locs_data, columns=['location', 'count'])
    
    total_count = sum(location_counter.values())
    top_7_count = loc_df['count'].sum()
    other_count = total_count - top_7_count
    
    if other_count > 0:
        loc_df = pd.concat([loc_df, pd.DataFrame([{'location': 'other', 'count': other_count}])], ignore_index=True)

    loc_df['angle'] = loc_df['count'] / loc_df['count'].sum() * 2 * pi
    loc_df['percentage'] = (loc_df['count'] / loc_df['count'].sum()) * 100
    loc_df['color'] = Category20[len(loc_df)]
    loc_df['label'] = loc_df['location'].str.capitalize() + " (" + loc_df['percentage'].round(1).astype(str) + "%)"
    
    source = ColumnDataSource(loc_df)
    TOOLTIPS = [("Location", "@location"), ("Count", "@count"), ("Percentage", "@percentage{0.1f}%")]

    p = figure(height=350, title="Job Locations", tooltips=TOOLTIPS,
               tools="pan,wheel_zoom,box_zoom,reset")
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='label', source=source)
    p.axis.visible = False
    p.grid.grid_line_color = None

    return components(p)


def create_experience_chart(all_job_data):
    """
    MODIFIED: Takes a DataFrame and RETURNS chart components.
    """
    print("Generating Job Experience distribution chart...")
    df = all_job_data.copy()
    df = df.dropna(subset=['experience'])
    df = df[df['experience'].str.lower() != 'n/a']
    df['min_exp_str'] = df['experience'].str.extract(r'^(\d+)')
    df = df.dropna(subset=['min_exp_str'])
    df['min_exp'] = pd.to_numeric(df['min_exp_str'])
    if df.empty: return None

    exp_counts = df['min_exp'].value_counts().sort_index()
    data = {'experience': exp_counts.index.tolist(), 'counts': exp_counts.values.tolist()}
    source = ColumnDataSource(data=data)

    TOOLTIPS = [("Min Experience", "@experience Years"), ("Job Count", "@counts")]
    p = figure(height=350, title="Job Distribution by Experience", tooltips=TOOLTIPS,
               tools="pan,wheel_zoom,box_zoom,reset")
    p.xaxis.axis_label = "Minimum Experience (Years)"
    p.yaxis.axis_label = "Number of Jobs"
    p.line(x='experience', y='counts', source=source, line_width=2, color="#D95B43")
    p.circle(x='experience', y='counts', source=source, size=8, fill_color="white", line_color="#D95B43")
    p.y_range.start = 0

    return components(p)


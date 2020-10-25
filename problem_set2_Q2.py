from bokeh.models.annotations import Legend
from bokeh.models.widgets.tables import DataCube
import numpy as np 
import pandas as pd 
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource as CDS
from bokeh.io import output_notebook
import os 

wd_lc = '/Users/llccf/OneDrive/Dokumente/3. Semester/International Trade and Tax Policy/Problem Sets/PS2/'
os.chdir(wd_lc)

#*##############################
#! FUNCTIONS
#*##############################

#first get columns that we want
def string_checker(data, check): 
    '''
    Returns names of columns in 'data' that contain 'check'.
    '''
    cols = [col for col in data.columns if check in col]
    return(cols)

def get_subset(data, columns): 
    subset = data[columns]
    subset['year'] = data['Year']
    return(subset)

def col_rename(data, split = '\n'):
    columns_new = [col.split('\n')[-1] for col in data.columns]
    data.columns = columns_new 
    return(data)

def get_subdata(raw_data, check): 
    '''
    Wrapper for the previously defined functions to generate subset in one command.
    '''
    new_cols = string_checker(raw_data, check = check)
    subset = get_subset(raw_data, new_cols)
    subset = col_rename(subset)
    return(subset)

def line_plot(data, colors, labels, x = 'year', leg_loc = 'bottom_left'): 
    p = figure(plot_width = 800, plot_height = 500)
    lines = list(data.columns)
    lines.remove('year')
    glyph_num = np.arange(0, len(lines))
    for j, i, col, lab in zip(glyph_num, lines, colors, labels): 
        p.line(data[x], data[i], line_color = col, legend_label = lab)
        if j == 0: 
            p.circle(data[x], data[i])
        elif j == 1: 
            p.diamond(data[x], data[i])
        elif j == 2: 
            p.square(data[x], data[i])
        elif j == 3: 
            p.cross(data[x], data[i])
    p.legend.location = leg_loc
    show(p)

#*##############################
#! DATA
#*##############################
raw = pd.read_csv('data/income_ineq_data.csv', sep = ';', header = 1)
cap_data = get_subdata(raw, 'capital')
lab_data = get_subdata(raw, 'labor')
total_data = get_subdata(raw, 'national')


#*##############################
#! ALVAREDO ET AL REPLICATION
#*##############################
#countries of interest 
anglo = ['United Kingdom', 'USA', 'Canada', 'Australia']
rest = ['Germany', 'France', 'Sweden', 'Japan']

#* PLOTTING SET UP
#set up colors 
colors4 = ['green', 'purple', 'red', 'blue']

#set up labels 
anglo_labels = ['UK', 'USA', 'Canada', 'Australia']
rest_labels = ['Germany', 'France', 'Sweden', 'Japan']

#! TOTAL INCOME
anglo_total = total_data[anglo + ['year']]
rest_total = total_data[rest + ['year']]

#PANEL A
line_plot(anglo_total, colors = colors4, labels = anglo_labels)
#PANEL B 
line_plot(rest_total, colors = colors4, labels = rest_labels)

#*##############################
#! OTHER REGIONS
#*##############################
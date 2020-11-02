from bokeh.io import export
from bokeh.models.annotations import LabelSet, Legend
from bokeh.models.widgets.tables import DataCube
import numpy as np 
import pandas as pd 
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource as CDS
from bokeh.models import Legend
from bokeh.io import output_notebook, export_png
from bokeh.layouts import column
import os

from pandas.io.parsers import count_empty_vals 

wd_lc = '/Users/llccf/OneDrive/Dokumente/3. Semester/International Trade and Tax Policy/Problem Sets/PS2/'
os.chdir(wd_lc)

#*##############################
#! FUNCTIONS
#*##############################
def get_missings(series): 
    '''
    get number of missings of a pandas series
    '''
    counter = sum(series.isnull())
    return(counter)

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

def plot(ys, colors, labels, title = '', y_range = None): 
    p = figure(plot_width = 800, plot_height = 500, title = title,
            toolbar_location = None, x_range = [1910, 2020], y_range = y_range)
    for i in range(len(ys)):
        p.line(x, ys[i], color = colors[i], legend_label = labels[i])
        if i == 0: 
            p.diamond(x, ys[i], color = colors[i])
        if i == 1: 
            p.square(x, ys[i], color = colors[i])
        if i == 2: 
            p.circle(x, ys[i], color = colors[i])
        if i == 3: 
            p.triangle(x, ys[i], color = colors[i])
        if i == 4: 
            p.hex(x, ys[i], color = colors[i])
    p.legend.orientation = 'horizontal'
    p.legend.location = 'top_center'
    show(p)
    return(p)

#*##############################
#! DATA
#*##############################
raw = pd.read_csv('data/income_ineq_data.csv', sep = ';', header = 1)
cap_data = get_subdata(raw, 'capital')
lab_data = get_subdata(raw, 'labor')
total_data = get_subdata(raw, 'national')
#only keep observation after 1910 
total_data = total_data[total_data['year'] >= 1910]

#*##############################
#! ALVAREDO ET AL REPLICATION
#*##############################
#* set up x-axis values once 
x = total_data['year'].tolist()

#countries of interest 
anglo = ['United Kingdom', 'USA', 'Canada', 'Australia']
rest = ['Germany', 'France', 'Sweden', 'Japan']
#set up colors 
colors6 = ['b8336a', '56e39f', '1f487e', 'ffa69e', '280000', 'dac4f7']
colors6 = ['#' + col for col in colors6]
colors6 = ['red', 'green', 'purple', 'blue', 'orange']
#set up labels 
anglo_labels = ['UK', 'USA', 'Canada', 'Australia']
rest_labels = ['Germany', 'France', 'Sweden', 'Japan']

#get data for respective panels
ys_A = [total_data[i] for i in anglo]
ys_B = [total_data[i] for i in rest]
#plot
output_notebook()
pA = plot(ys_A, colors = colors6, labels = anglo_labels, title = '')
pB = plot(ys_B, colors = colors6, labels = rest_labels, title = '', y_range = [0, 0.25])
#show as column layout
show(column(pA, pB))
#export both panels
export_png(pA, filename = 'Output/AlvaredoReplicaPanelA.png')
export_png(pB, filename = 'Output/AlvaredoReplicaPanelB.png')

#*##############################
#! OTHER REGIONS
#*##############################

#may be interesting to look at China and neihboring countries 
#to see what opening up led to 
new_region = ['Brazil', 'Argentina', 'Chile', 'Colombia']
new_region = ['Russia and Ukraine', 'China', 'Korea', 'India']

new_data = total_data[new_region + ['year']]
new_data = new_data[new_data['year'] >= 1910]
ys_C = [new_data[i] for i in new_region]

#! Which countries have the lowest amount of missings? 
total_data = total_data.drop('null', axis = 1)
total_data = total_data[total_data['year'] >= 1910]
missings_dict = {i: get_missings(total_data[i]) for i in total_data.columns}
sorted_missings = sorted(missings_dict.items(), key = lambda x: x[1], reverse = False)

#russain fedration has relatively little missings but no consecutive observations...
least_missings = ['South Africa', 'India', 'Singapore', 'Russian Federation', 'China']
ys = [total_data[i] for i in least_missings]
pD = plot(ys, colors = colors6, labels = least_missings)

#! Countries we should use in b) 
new_region = ['Japan', 'India', 'China', 'Singapore', 'Korea']
ys_C = [total_data[i] for i in new_region]
pC = plot(ys_C, colors6, new_region)
export_png(pC, filename = 'Output/newregions.png')
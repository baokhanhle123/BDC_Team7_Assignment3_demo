import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import pandas as pd
import itertools

def req_per_date(df):
     # Visualize requests per date
     date_graph = dict(Counter(df['req_date']))
     x = list(date_graph.keys())
     y = list(date_graph.values())
     fig, ax = plt.subplots()
     fig.set_size_inches(10.5, 6.5, forward=True)
     ax.barh(x, y, align='center')
     ax.set_xlabel('Request',fontsize=12)
     ax.set_title('Requests per date',fontsize=20)

     return(fig)

def req_per_type(df):
     # Display available file types
     count = df['file_type'].value_counts().to_dict()
     key = list(count.keys())
     value = list(count.values())

     # Plot as histogram
     fig, ax = plt.subplots()
     fig.set_size_inches(18.5, 10.5, forward=True)
     ax.barh(key, value, align='center')
     for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	     label.set_fontsize(16)
          
     ax.set_xlabel('Request',fontsize=20)
     ax.set_title('File type and requests per type',fontsize=25)

     return(fig)

def size_delay_relationship(df):
     # Plot to view the correlation between Delay and File size
     fig, ax = plt.subplots()
     fig.set_size_inches(18.5, 15, forward=True)

     ax.scatter(df['file_size'],df['delay'])  
     for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	     label.set_fontsize(16)

     ax.set_xlabel("File size (MB)", fontsize=20)
     ax.set_ylabel("Delay (s)", fontsize=20)
     ax.set_title("Delay and File size relationship", fontsize=25)

     return(fig)

def percentage_province(df):
     # Plot a pie chart after sorting by requests frequencies, lower than threshold is considered as the minority
     threshold = 500
     status_d=dict(Counter(df["region"]))
     d = dict(sorted(status_d.items(), key=lambda item: item[1]))
     new_d = {}
     for key, group in itertools.groupby(d, lambda k: 'Other' if (d[k]<threshold) else k):
          new_d[key] = sum([d[k] for k in list(group)]) 

     key_list = list(new_d.keys())
     val_list = list(new_d.values())

     fig, ax = plt.subplots()
     fig.set_size_inches(18.5, 15, forward=True)
     ax.pie(val_list, labels=key_list, autopct='%1.1f%%',
          shadow=True, startangle=90, textprops={'fontsize': 12})
     ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

     ax.set_title("The percentage number of requests of each province in Vietnam.",fontsize=25,loc='right')

     return(fig)

def percentage_isp(df):
     # Plot a pie chart after sorting by requests frequencies
     status_d=dict(Counter(df["ISP"]))
     d = dict(sorted(status_d.items(), key=lambda item: item[1]))
     new_d = {}
     for key, group in itertools.groupby(d, lambda k: 'Other' if (d[k]<800) else k):
          new_d[key] = sum([d[k] for k in list(group)]) 

     key_list = list(new_d.keys())
     val_list = list(new_d.values())

     fig, ax = plt.subplots()
     fig.set_size_inches(18.5, 15, forward=True)
     ax.pie(val_list, labels=key_list, autopct='%1.2f%%',
          shadow=True, startangle=90, textprops={'fontsize': 14})
     ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

     ax.set_title("The proportion of number of requests between ISPs",fontsize=25,loc='right')

     return(fig)
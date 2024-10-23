import json
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def load_lottie_file(file_path: str):
    with open(file_path, "r") as f:
        lottie_json = json.load(f)
        return lottie_json


def format_label(df,column,axis):
        label_step = 1
        axis_labels = df[column].unique()
        if len(axis_labels) > 50:
            label_step = 5
        
        ax = plt.gca()
        if axis == 'x':
            ax.set_xticks(range(0, len(axis_labels) + 1)) 
            ax.set_xticklabels([label if i % label_step == 0 else '' for i, label in enumerate(axis_labels)], 
                        rotation=45, ha='right', fontsize=8)
        else:
            ax.set_yticks(range(0, len(axis_labels) + 1))
            ax.set_yticklabels([label if i % label_step == 0 else '' for i, label in enumerate(axis_labels)], 
                        rotation=45, ha='right', fontsize=8)
            
            
def Axis_Limits(df, column,axis):
    # check the data type of the column
    if df[column].dtype == 'int64' or df[column].dtype == 'float64':
        if axis == 'x':
            xlim = st.sidebar.slider("Set X-axis Limits", min_value=float(df[column].min()),
                                    max_value=float(df[column].max()),
                                    value=(float(df[column].min() - df[column].min()/3 ), float(df[column].max() + df[column].max()/3)),
                                    step=0.1)
            return xlim
        elif axis == 'y':
            ylim = st.sidebar.slider("Set Y-axis Limits", min_value=float(df[column].min()),
                                    max_value=float(df[column].max()),
                                    value=(float(df[column].min() - df[column].min()/3), float(df[column].max() + df[column].max()/3)),
                                    step=0.1)
            return ylim

#  filter column object type or numerical type
def Column_filter(df, column_type):
    if column_type == 'object':
        return list(df.select_dtypes(include=['object']).columns)
    elif column_type == 'number':
        return list(df.select_dtypes(include=[np.number]).columns)

def Column_Remover(Column_list, remove_column):
    if remove_column:
        Column_list.remove(remove_column)
    return Column_list
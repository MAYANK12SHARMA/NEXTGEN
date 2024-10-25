import json
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import shutil
import os


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

def Column_filter(df, column_type):
    if column_type == 'object':
        return list(df.select_dtypes(include=['object']).columns)
    elif column_type == 'number':
        return list(df.select_dtypes(include=[np.number]).columns)


def Column_Remover(Column_list, remove_column):
    if remove_column:
        Column_list.remove(remove_column)
    return Column_list

def column_rem_list(Column_list,remove_col_list):
    for col in remove_col_list:
        Column_list.remove(col)
    return Column_list

def find_repeating_categorical_columns(df):
    """
    This function finds the categorical columns in a DataFrame that contain repeating values
    and excludes string columns with only unique values.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    
    Returns:
    list: A list of column names that are categorical and have repeating values.
    """
    # Step 1: Identify categorical columns (object or category types)
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    
    # Step 2: Filter for columns with repeating values
    repeating_categorical_cols = []
    
    for col in categorical_columns:
        # Check if there are any duplicated values in the column
        if df[col].duplicated().any():
            repeating_categorical_cols.append(col)
    
    return repeating_categorical_cols



def copy_file(src_path):
    # Generate the destination path by appending '_copy' before the file extension
    dest_path = src_path.replace(".", "_copy.", 1)
    
    # Copy the file
    shutil.copy(src_path, dest_path)
    
    return dest_path



def delete_files(file_paths):
    """
    Deletes files from the list of file paths if they exist.

    Parameters:
    file_paths (list of str): List of file paths to delete.

    Returns:
    dict: Summary with 'deleted' and 'not_found' lists of file paths.
    """
    summary = {"deleted": [], "not_found": []}

    for file_path in file_paths:
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                summary["deleted"].append(file_path)
            except Exception as e:
                print(f"Could not delete {file_path}: {e}")
        else:
            summary["not_found"].append(file_path)
    
    return summary

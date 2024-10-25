import streamlit as st
import pandas as pd
from Visualization.PlotBox import Box_plot_visualize
from Visualization.HelperFun import load_lottie_file
from streamlit_lottie import st_lottie
from Visualization.PlotScatter import Scatter_Plot_visualize
from Visualization.PlotHeatMap import Heatmap_Visualize
from Visualization.PlotPairPlot import Paiplot_Visualization

#? ==================================== Additional Functions ====================================

def File_Upload(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        
        if df.empty:
            st.error("The uploaded file is empty. Please upload a valid CSV file.")
            return None

        st.write("### 👀 Preview of the Data:")
        st.dataframe(df.head())

        st.write("### 📊 Data Types of Each Column:")
        data_types = df.dtypes.reset_index()
        data_types.columns = ['Column', 'Data Type']
        data_type_table = data_types.groupby('Data Type')['Column'].apply(list).reset_index()
        st.dataframe(data_type_table)
        return df
    except pd.errors.EmptyDataError:
        st.error("The file is empty or invalid. Please upload a valid CSV file.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the file: {e}")
        return None

def PlotGenerator(df, choose_plot_type):
    if choose_plot_type == "Box Plot":
        Box_plot_visualize(df)
        
    elif choose_plot_type == "Scatter Plot":
        Scatter_Plot_visualize(df)
    elif choose_plot_type == "HeatMap":
        Heatmap_Visualize(df)
    elif choose_plot_type == "Pair Plot":
        Paiplot_Visualization(df)
        
    else:
        st.warning("Please Select a Plot Type")


#? ==================================== Main Function ==================================== 

import os
import streamlit as st

def PlotWizardNavigation(uploaded_file, choose_plot_type):
    with st.sidebar:
        image_path = './Visualization/assets/Images/logo.png'
        
        # Check if the file exists before trying to display it
        if os.path.exists(image_path):
            st.image(image_path, width=200)
        else:
            st.error("Logo image not found.")
    if not uploaded_file and not choose_plot_type:
        with st.sidebar:
            st.info("Please upload a CSV file and choose a plot type.")
            lottie_json = load_lottie_file("./Visualization/FilesJson/Navbar-Jif.json")
            st_lottie(lottie_json, speed=1, width=250, height=250, key="initial")
    elif not uploaded_file:
        with st.sidebar:
            st.info("Please upload a CSV file to generate a plot.")
            lottie_json = load_lottie_file("./Visualization/FilesJson/Navbar-Jif.json")
            st_lottie(lottie_json, speed=1, width=250, height=250, key="initial")
    elif not choose_plot_type:
        with st.sidebar:
            st.info("Please choose a plot type to generate a plot.")
            lottie_json = load_lottie_file("./Visualization/FilesJson/Navbar-Jif.json")
            st_lottie(lottie_json, speed=1, width=250, height=250, key="initial")
    else:
        df = File_Upload(uploaded_file)
        if df is not None:
            PlotGenerator(df, choose_plot_type)

def PlotWizard():
    uploaded_file = None
    choose_plot_type = None
    col1, col2 = st.columns([2, 2])
    
    with col1:
        # Upload a CSV file 
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])     

    with col2:
        # Select the plot type
        st.markdown("<h4 style='text-align: left; color: #FFFFFF;font-size:20px;padding-bottom: 0px;margin-bottom: 0px;'>Select the plot type</h4>", unsafe_allow_html=True)
        choose_plot_type = st.selectbox("", [None] + ["Box Plot", "Scatter Plot", "HeatMap","Pair Plot"], key="plot_type")
               
    PlotWizardNavigation(uploaded_file, choose_plot_type)


# Run the application
if __name__ == "__main__":
    PlotWizard()

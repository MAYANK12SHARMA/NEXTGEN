import os
import asyncio
import pathlib
import markdown2
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer
import streamlit as st
import matplotlib.pyplot as plt
from Visualization.AIGen import Generator_Code_AI
from multiprocessing import Process, Queue
from playwright.async_api import async_playwright
from Visualization.HelperFun import Column_filter, Axis_Limits, find_repeating_categorical_columns, column_rem_list,Column_Remover, copy_file, delete_files

files_to_delete = ["SampleScatterPlot_copy.html", "SampleScatterPlot_copy.md","SampleScatterPlot_copy.pdf","BoxPlt_copy.md","BoxPlt_copy.pdf","BoxPlt_copy.html"]

    
#? ============================================== Additional Functions ============================

#! ========================================= Pdf Generator  ======================================= 


def get_unique_markers(column):
    # Get unique values in the column
    unique_values = column.unique()
    num_unique_values = len(unique_values)
    
    # List of available markers in matplotlib
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', 'X', 'd', '|', '_']
    
    # If unique values exceed available markers, repeat markers (if needed)
    if num_unique_values > len(markers):
        marker_list = (markers * (num_unique_values // len(markers) + 1))[:num_unique_values]
    else:
        marker_list = markers[:num_unique_values]
    
    # Join markers with commas for the output format
    return ','.join(marker_list)

def replace_all_markers(file_path, marker_content_dict, end_marker=None):
    """
    Replace multiple sections of content in a Markdown file, based on a dictionary of start markers and new content.
    
    Args:
    - file_path: The path to the Markdown file.
    - marker_content_dict: A dictionary where the keys are start markers and the values are lists of new content.
    - end_marker: Optional. If provided, content between each start_marker and end_marker will be replaced.
    
    Example usage:
    replace_all_markers(
        "output.md", 
        {
            "## Existing Section 1": ["## New Section 1\n", "New content 1 here\n"],
            "## Existing Section 2": ["## New Section 2\n", "New content 2 here\n"]
        }, 
        "## Another Section"
    )
    """
    # Read the existing content of the file
    file_path = copy_file(file_path)
    with open(file_path, "r") as md_file:
        lines = md_file.readlines()  # Read all lines into a list

    for start_marker, new_content in marker_content_dict.items():
        i = 0
        while i < len(lines):
            # Find the index of the start marker
            if start_marker in lines[i]:
                start_index = i

                # If an end marker is provided, find the index of the end marker
                if end_marker:
                    end_index = None
                    for j in range(start_index + 1, len(lines)):
                        if end_marker in lines[j]:
                            end_index = j
                            break

                    # If end_marker is not found, replace content up to the end of the file
                    if end_index is None:
                        end_index = len(lines)
                else:
                    # If no end_marker is provided, replace only the start_marker line
                    end_index = start_index + 1

                # Replace the content between the start and end markers
                lines[start_index:end_index] = new_content

                # Move index past the newly inserted content
                i = start_index + len(new_content)
            else:
                i += 1

    # Write the updated content back to the file
    with open(file_path, "w") as md_file:
        md_file.writelines(lines)
    

def convert_md_to_html(input_md_file: str) -> str:
    """
    Convert a Markdown file to an HTML file.

    Args:
        input_md_file (str): Path to the input Markdown file.

    Returns:
        str: Path to the output HTML file created with the same name as the input file.
    """
    try:
        # Read the Markdown file
        with open(input_md_file, "r", encoding='utf-8') as md_file:
            markdown_content = md_file.read()

        # Convert Markdown to HTML
        html_content = markdown2.markdown(markdown_content)

        # Derive the output HTML file path
        output_html_file = os.path.splitext(input_md_file)[0] + ".html"

        # Write the HTML content to a new file
        with open(output_html_file, "w", encoding='utf-8') as html_file:
            html_file.write(html_content)

        print(f"HTML file '{output_html_file}' created successfully!")
        return output_html_file  # Return the path of the generated HTML file

    except FileNotFoundError:
        print(f"Error: The file '{input_md_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None  # Return None in case of an error



async def generate_pdf_from_html(html_file: str):
    # Convert the provided HTML file path into an absolute path
    filePath = os.path.abspath(html_file)
    # Derive the URL path of the local HTML file to be opened in the browser
    fileUrl = pathlib.Path(filePath).as_uri()
    
    # Create the output PDF file name based on the HTML file name
    pdf_file_path = os.path.splitext(filePath)[0] + ".pdf"  # Change extension to .pdf

    async with async_playwright() as p:
        # Create a browser instance
        browser = await p.chromium.launch()
        # Open a new tab in the browser
        page = await browser.new_page()
        # Go to the URL of the HTML page
        await page.goto(fileUrl)
        # Change CSS media type to screen
        await page.emulate_media(media="screen")
        # Print the HTML page as a PDF in the browser
        await page.pdf(path=pdf_file_path, format="A4", landscape=False, margin={"top": "2cm"})
        # Close the browser
        await browser.close()
    
    return pdf_file_path  # Return the path of the generated PDF

def run_html_to_pdf_conversion(html_file):
    try:
        # Get the current event loop
        loop = asyncio.get_event_loop()
        generated_pdf = loop.run_until_complete(generate_pdf_from_html(html_file))
        print(f"PDF generated: {generated_pdf}")
        return generated_pdf
    except RuntimeError as e:
        if str(e) == "asyncio.run() cannot be called from a running event loop":
            # This case might not be necessary anymore, as we are using the event loop directly
            pass
        else:
            raise
        

def generate_pdf_process(queue, html_file: str):
    """Target function for multiprocessing to generate PDF."""
    pdf_file_path = os.path.splitext(html_file)[0] + ".pdf"
    
    # Run Playwright in this function
    async def run_playwright():
        filePath = os.path.abspath(html_file)
        fileUrl = pathlib.Path(filePath).as_uri()

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(fileUrl)
            await page.emulate_media(media="screen")
            await page.pdf(path=pdf_file_path, format="A4", landscape=False, margin={"top": "2cm"})
            await browser.close()

        return pdf_file_path

    # Run the coroutine in a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    pdf_path = loop.run_until_complete(run_playwright())
    queue.put(pdf_path)  # Send the result back to the main process

def generate_pdf_with_multiprocessing(html_file: str):
    queue = Queue()
    process = Process(target=generate_pdf_process, args=(queue, html_file))
    process.start()
    process.join()  # Wait for the process to finish
    pdf_file_path = queue.get()  # Get the result from the queue
    return pdf_file_path




#? ========================================= Scatter plot Functions ======================================

def handle_missing_values(df, strategy='mean', columns=None):
    if columns is None or not isinstance(columns, list) or not columns:
        raise ValueError("Please provide a non-empty list of columns.")

    for column in columns:
        if column in df.columns:
            if strategy == 'drop_rows':
                df = df.dropna(subset=[column])
            elif strategy == 'drop_columns':
                df = df.drop(columns=[column])
            elif strategy == 'ffill':
                df[column] = df[column].ffill()
            elif strategy == 'bfill':
                df[column] = df[column].bfill()
            elif strategy == 'mean':
                imputer = SimpleImputer(strategy='mean')
                df[[column]] = imputer.fit_transform(df[[column]])
            elif strategy == 'median':
                imputer = SimpleImputer(strategy='median')
                df[[column]] = imputer.fit_transform(df[[column]])
            elif strategy == 'mode':
                imputer = SimpleImputer(strategy='most_frequent')
                df[[column]] = imputer.fit_transform(df[[column]])
            elif strategy == 'knn':
                imputer = KNNImputer(n_neighbors=5)
                df[[column]] = imputer.fit_transform(df[[column]].values.reshape(-1, 1))
            elif strategy == 'mice':
                imputer = IterativeImputer()
                df[[column]] = imputer.fit_transform(df[[column]].values.reshape(-1, 1))
            elif strategy == 'random':
                non_null_values = df[column].dropna()
                if not non_null_values.empty:
                    df[column] = df[column].apply(lambda x: np.random.choice(non_null_values) if pd.isnull(x) else x)
                else:
                    st.warning(f"No values to sample from for column: {column}")
        else:
            st.warning(f"Column '{column}' not found in DataFrame.")

    return df

def MissingValueMethod(df, strategy, columns):
    """
    Determine which missing value handling method to use based on the strategy.

    Parameters:
    - df: pandas DataFrame with missing values.
    - strategy: String specifying the missing value handling strategy.
    - columns: List of columns to apply the strategy.

    Returns:
    - df: DataFrame with missing values handled according to the specified strategy.
    """
    strategy_map = {
        "Drop Rows": "Drop rows with missing values",
        "Drop Columns": "Drop columns with missing values",
        "Use forward fill": "Fill missing values using forward fill",
        "Use backward fill": "Fill missing values using backward fill",
        "Mean Imputation": "Replace missing values with the mean of the column",
        "Median Imputation": "Replace missing values with the median of the column",
        "Mode Imputation": "Replace missing values with the mode of the column",
        "KNN Imputation": "Impute missing values using K-Nearest Neighbors",
        "MICE Imputation": "Impute missing values using Multiple Imputation by Chained Equations",
        "Random Sampling": "Randomly sample from available values to fill missing data"
    }

    if strategy in strategy_map:
        return handle_missing_values(df, strategy=strategy.lower().replace(' ', '_'), columns=columns)
    else:
        st.error(f"Invalid missing value handling method: {strategy}")
        return df


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def Paiplot_Visualization(df):
    # Check for missing values
    missing_values = df.isnull().sum().reset_index()
    missing_values.columns = ['Column', 'Missing Values']
    missing_values = missing_values[missing_values['Missing Values'] > 0]  # Filter for columns with missing values

    # Display missing values
    if not missing_values.empty:
        st.write("### ❗ Missing Values in the Data:")
        st.dataframe(missing_values)
        st.warning("Please handle missing values before proceeding.")

        # Handle missing values for each column with missing values
        updated_df = df.copy()  # Create a copy of the original DataFrame

        for index, row in missing_values.iterrows():
            column = row['Column']
            strategy = st.selectbox(f"Select method for handling missing values in '{column}':", 
                                    ["Drop Rows", "Drop Columns", "Use forward fill", 
                                     "Use backward fill", "Mean Imputation", "Median Imputation", 
                                     "Mode Imputation", "KNN Imputation", "MICE Imputation", 
                                     "Random Sampling"], key=f"strategy_{index}")

            # Apply the selected strategy using MissingValueMethod
            updated_df = MissingValueMethod(updated_df, strategy, [column])

        st.success("Missing values handled successfully!")
    else:
        st.write("### ✅ No Missing Values Found!")
        updated_df = df.copy()  # If no missing values, keep original DataFrame

    # Pairplot customization
    st.sidebar.markdown("<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Pairplot Customization </h2>", unsafe_allow_html=True)
    
    hue_column = st.sidebar.selectbox("📊 Select Hue column (optional)", [None] + find_repeating_categorical_columns(df))
    x_vars = st.sidebar.multiselect("Select Variables", Column_filter(df, "number"), Column_filter(df, "number")[0:3])
    y_vars = x_vars
    if hue_column:
        markers = st.sidebar.text_input("Enter Marker Type (comma-separated for multiple)", get_unique_markers(updated_df[hue_column] if hue_column else updated_df[x_vars[0]]))
    else:
        markers = '*'
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    st.sidebar.markdown("<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>B. 📊 Plot Type Customization </h2>", unsafe_allow_html=True)
    kind = st.sidebar.selectbox("Select Plot Type", ["scatter", "kde", "hist", "reg"])
    diag_kind = st.sidebar.selectbox("Select Diagonal Plot Type", ["auto", "hist", "kde"])
    corner = st.sidebar.checkbox("Show Corner Plot", value=False)
    st.sidebar.markdown("<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>C.📊 Pltot Size Customization </h2>", unsafe_allow_html=True)
    
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)
    bg_color = st.sidebar.color_picker("Pick background color", "#f0f0f0")
    # title = st.sidebar.text_input("Plot Title (optional)", "Pairplot Visualization")
    
    if st.sidebar.button("Generate Pair Plot"):
        if x_vars and y_vars:  # Ensure x_vars and y_vars are selected
            with st.spinner("Generating Pair plot ..."):
                create_pair_plot(data=updated_df, x_vars=x_vars, y_vars=y_vars, hue_col=hue_column, 
                             palette=palette, corner=corner, markers=markers.split(","), kind=kind, 
                             diag_kind=diag_kind, plot_width=plot_width, plot_height=plot_height, 
                             bg_color=bg_color) 
        else:
            st.error("Please select at least one variable for X and Y axes.")       
        
        with open("pair_plot.png", "rb") as file:
            st.download_button(
                label="Download Pair Plot",
                data=file,
                file_name="Pair_Plot.png",
                mime="image/png"
            ) 
    if st.sidebar.button("Generate Code and Get Report"):
        if x_vars and y_vars:  # Ensure x_vars and y_vars are selected
            with st.spinner("Generating Pair plot ..."):
                create_pair_plot(data=updated_df, x_vars=x_vars, y_vars=y_vars, hue_col=hue_column, 
                             palette=palette, corner=corner, markers=markers.split(","), kind=kind, 
                             diag_kind=diag_kind, plot_width=plot_width, plot_height=plot_height, 
                             bg_color=bg_color) 
        else:
            st.error("Please select at least one variable for X and Y axes.")       
    
        with st.spinner("Generating Code..."): 
            generated_code = pair_plot_code_generator(df, x_vars, y_vars, hue_column, palette, corner, markers, kind, diag_kind, plot_width, plot_height, bg_color)
        
        st.code(generated_code, language='python')
        
        col1, col2 = st.columns([1,1])
        
        with col1:
            with open("pair_plot.png", "rb") as file:
                st.download_button(
                    label="Download Pair Plot",
                    data=file,
                    file_name="pair_Plot.png",
                    mime="image/png"
                )
        
        with col2:
            changing_sec = {
                "ImagesofPairPlot": "pair_plot.png",
                "CodingPart": generated_code
            }
            replace_all_markers("SamplePairPlot.md", changing_sec)
            # Convert the Markdown file to HTML
            html_file = convert_md_to_html("SamplePairPlot_copy.md")
            # Generate PDF
            with st.spinner("Generating PDF..."):
                pdf_file = generate_pdf_with_multiprocessing(html_file)

            st.success("PDF generated successfully!")
                
            # Add a download button for the generated PDF
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name="SamplePairPlot.pdf",
                    mime="application/pdf",
                    on_click=lambda: delete_files(files_to_delete)
                )

    

def create_pair_plot(data, x_vars=None, y_vars=None, kind='scatter', hue_col=None, palette='Set1', 
                     corner=False, markers=['o'], diag_kind='auto', plot_width=14, plot_height=8, 
                     bg_color='#f0f0f0'):
    
    plt.figure(figsize=(plot_width, plot_height))
    
    sns.set(style="whitegrid")
    plt.gca().set_facecolor(bg_color)
    
    if x_vars and y_vars:
        # Create the pairplot with custom markers and color palette
        g = sns.pairplot(data, x_vars=x_vars, y_vars=y_vars, hue=hue_col, corner=corner, 
                         markers=markers, kind=kind, diag_kind=diag_kind, palette=palette)
        
        # Customize axes
        if corner is False:
            for ax in g.axes.flatten():
                ax.spines['top'].set_color('purple')
                ax.spines['bottom'].set_color('purple')
                ax.spines['left'].set_color('purple')
                ax.spines['right'].set_color('purple')
                ax.set_facecolor(bg_color)

    # plt.title(title, fontsize=16, fontweight='bold', color="#444444")
    if hue_col:
        unique_hues = data[hue_col].nunique()
        # Adjust markers if there are more categories than the provided marker styles
        if len(markers) != 1 and len(markers) != unique_hues:
            markers = ['o'] * unique_hues  # Default to a single marker style if there's a mismatch

    if hue_col:
        # Get the legend and set a custom location and box style
        legend = g._legend
        if legend:
            legend.set_bbox_to_anchor((1, 1))  # Position legend outside the plot to the right
            legend.set_title(hue_col)  # Title of the legend box
            legend.get_frame().set_facecolor('lightgray')  # Legend box color
            legend.get_frame().set_edgecolor('black')  # Legend box edge color
    # Display the plot on Streamlit
    st.pyplot(g)
    
    plt.tight_layout()
    plt.savefig("pair_plot.png")
    plt.clf()        

#? ========================================= Code Generator  ======================================= 
def pair_plot_code_generator(df, x_vars, y_vars, hue_col, palette, corner, markers, kind, diag_kind, plot_width, plot_height, bg_color, title=None):
    prompt = f"""
    Create a pair plot in Python using the following specifications:
    1. Use the dataset stored in the variable 'df'.
    2. Plot the variables '{x_vars}' on the x-axis.
    3. Plot the variables '{y_vars}' on the y-axis.
    4. {f"Distinguish data points by the '{hue_col}' column, using the '{palette}' color palette." if hue_col else "Do not use hue for distinguishing data points."}
    5. {f"Show a corner plot with the diagonal plots as '{diag_kind}'." if corner else "Do not show a corner plot."}
    6. Use marker styles '{markers}' for the data points.
    7. Use plot type '{kind}' for the scatter plots.
    8. Set the width of the plot to {plot_width} inches and the height to {plot_height} inches.
    9. Set the background color of the plot to '{bg_color}'.
    10. Set the title of the plot to '{title}'.
    """
    Code = Generator_Code_AI(prompt)
    return Code


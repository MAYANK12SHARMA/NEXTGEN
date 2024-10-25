import os
import asyncio
import pathlib
import markdown2
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import seaborn as sns
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Visualization.AIGen import Generator_Code_AI
from multiprocessing import Process, Queue
from playwright.async_api import async_playwright
from Visualization.HelperFun import Column_filter, Axis_Limits, find_repeating_categorical_columns, Column_Remover, copy_file, delete_files

files_to_delete = ["SampleScatterPlot_copy.html", "SampleScatterPlot_copy.md","SampleScatterPlot_copy.pdf","BoxPlt_copy.md","BoxPlt_copy.pdf","BoxPlt_copy.html"]

    
#? ============================================== Additional Functions ============================

#! ========================================= Pdf Generator  ======================================= 


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




#? ========================================= HeatMap Functions ======================================



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

def Create_Heatmap(df, cmap, annot, fmt, annot_size, annot_color, linewidths, linecolor, cbar, cbar_kws, square, mask, figsize, bg_color,title):
    """
    Create a heatmap based on the correlation matrix of the DataFrame.

    Parameters:
    - df: pd.DataFrame
    - cmap: str, colormap for the heatmap
    - annot: bool, whether to annotate cells
    - fmt: str, format for annotations
    - annot_size: int, size of annotation text
    - annot_color: str, color of annotation text
    - linewidths: float, width of lines separating cells
    - linecolor: str, color of lines
    - cbar: bool, whether to display the color bar
    - cbar_kws: dict, additional parameters for color bar
    - square: bool, whether to force square cells
    - mask: bool, whether to mask the upper triangle of the heatmap
    - figsize: tuple, size of the figure
    - bg_color: str, background color for the figure
    """
    if df.empty:
        st.error("DataFrame is empty. Please provide valid data.")
        return
    
    # Ensure there are no NaN values before computing correlation
    if df.isnull().values.any():
        st.warning("DataFrame contains NaN values. Please clean the data.")
        df = df.fillna(0)  # Optional: fill NaNs with zeros for correlation purposes
    
    if df.select_dtypes(include=[np.number]).shape[1] < 2:
        st.error("DataFrame must have at least two numeric columns for correlation.")
        return

    sns.set(style="whitegrid")
    plt.figure(figsize=figsize, facecolor=bg_color)

    # Compute correlation matrix
    corr_matrix = df.corr()

    # Mask for upper triangle if needed
    mask_matrix = np.triu(np.ones_like(corr_matrix, dtype=bool)) if mask else None

    # Generate the heatmap with the specified parameters
    heatmap = sns.heatmap(
        data=corr_matrix,
        annot=annot,
        cmap=cmap,
        cbar=False,
        cbar_kws={**{'orientation': 'vertical', 'shrink': 0.8, 'aspect': 10, 'pad': 0.05, 'ticks': [0, 0.5, 1], 'format': '%.2f', 'location': 'right'}, **cbar_kws},
        fmt=fmt if annot else None,
        annot_kws={"size": annot_size, "color": annot_color},
        linewidths=linewidths,
        linecolor=linecolor,
        square=square,
        mask=mask_matrix
    )
    if cbar:
        cbar = plt.colorbar(heatmap.collections[0], ax=heatmap, orientation='horizontal', pad=0.1, shrink=0.3, aspect=30)
        cbar.set_label('Color Bar Label', fontsize=8)  # Set the color bar label

    heatmap.set_xticklabels(heatmap.get_xticklabels(), fontsize=8, rotation=45, ha='right')  # Adjust fontsize, rotation, and alignment
    heatmap.set_yticklabels(heatmap.get_yticklabels(), fontsize=8)  # Adjust this value as needed
    

    plt.title(title, fontsize=16)
    plt.tight_layout()
    st.pyplot(plt)
    plt.savefig("heatmap.png")
    plt.clf()  # Clear the figure after saving it



#? ========================================= Visualise Scatter Plot ======================================= 

def Heatmap_Visualize(df):
    missing_values = df.isnull().sum().reset_index()
    missing_values.columns = ['Column', 'Missing Values']
    missing_values = missing_values[missing_values['Missing Values'] > 0]  # Filter to show only columns with missing values

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

    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Annotation Customization </h2>""", unsafe_allow_html=True)
    fmt_options = [".1f", ".2f", ".3f"]
    annot = st.sidebar.checkbox("Show Cells Labels", value=True)
    fmt = st.sidebar.selectbox("Select Annotation Format", fmt_options, index=1)  # Default to .2f
    annot_size = st.sidebar.slider("Select Annotation Size", min_value=3, max_value=5, value=4, step=1)
    annot_color = st.sidebar.color_picker("Select Annotation Color", "#000000")
    
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>B.📊 Labels and Axis Customization </h2>""", unsafe_allow_html=True)
    linewidths = st.sidebar.slider("Select Line Widths", min_value=0.1, max_value=5.0, value=0.5)
    linecolor = st.sidebar.color_picker("Select Line Color", "#000000")
    square = True
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>C.🖼️ Plot Size Customization </h2>""", unsafe_allow_html=True)
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)
    figsize = (plot_width, plot_height)
    
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Additional Customization </h2>""", unsafe_allow_html=True)
    title = st.sidebar.text_input("Write the title", value="Coorelation Heatmap")
    cbar = st.sidebar.checkbox("Show Colorbar", value=True)
    cmap = st.sidebar.selectbox("🎨 Select Color Map", ["coolwarm", "viridis", "magma", "cividis", "plasma", "inferno", "YlGnBu", "BuGn"])
    cbar_kws = dict(use_gridspec=False, location="right")
    mask = st.sidebar.checkbox("Mask Upper Triangle", value=False)
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")

    if st.sidebar.button("Generate Heatmap"):
        with st.spinner('Generating heatmap...'):
            Create_Heatmap(updated_df, cmap, annot, fmt, annot_size, annot_color, linewidths, linecolor, cbar, cbar_kws, square, mask, figsize, bg_color,title)
        # Provide download link
        with open("heatmap.png", "rb") as file:
            st.download_button("Download Heatmap", file, file_name="Heatmap.png", mime="image/png")

    if st.sidebar.button("Generate Code and Get Report"):
        Create_Heatmap(updated_df, cmap, annot, fmt, annot_size, annot_color, linewidths, linecolor, cbar, cbar_kws, square, mask, figsize, bg_color,title)
        with st.spinner('Generating code...'):
            generated_code = HeatMap_Code_Generator(updated_df, cmap, annot, fmt, annot_size, annot_color, linewidths, linecolor, cbar, cbar_kws, square, mask, figsize, bg_color,title)
       
        st.code(generated_code, language='python')
        
        col1, col2 = st.columns([1,1])
        
        with col1:
            with open("heatmap.png", "rb") as file:
                st.download_button(
                    label="Download Heatmap",
                    data=file,
                    file_name="Heatmap.png",
                    mime="image/png"
                )

        # Generate PDF section
        with col2:
            changing_sec = {
                "ImagesofHeatmap": "heatmap.png",
                "CodingPart": generated_code
            }
            
            # Replace all markers in the Markdown file
            replace_all_markers("SampleHeatmap.md", changing_sec)
            
            # Convert the Markdown file to HTML
            html_file = convert_md_to_html("SampleHeatmap_copy.md")
            
            # Generate PDF
            with st.spinner("Generating PDF..."):
                pdf_file = generate_pdf_with_multiprocessing(html_file)

            st.success("PDF generated successfully!")
            
            # Add a download button for the generated PDF
            with open(pdf_file, "rb") as file:
                if st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name="SampleHeatmap.pdf",
                    mime="application/pdf",
                    on_click=lambda: delete_files([pdf_file])  # Assuming files_to_delete contains the pdf_file
                ):
                    pass 

def HeatMap_Code_Generator(df, cmap, annot, fmt, annot_size, annot_color, linewidths, linecolor, cbar, cbar_kws, square, mask, figsize, bg_color,title):
    prompt = f"""
    Create a heatmap in Python using the following specifications:
    1. Use the dataset stored in the variable 'df'.
    2. Use the '{cmap}' colormap for the heatmap.
    3. {f"Annotate the cells with the values, using the format '{fmt}'." if annot else "Do not annotate the cells."}
    4. Set the annotation text size to {annot_size} and color to '{annot_color}'.
    5. Set the line width separating the cells to {linewidths} and color to '{linecolor}'.
    6. {f"Display the color bar with the following parameters: {cbar_kws}." if cbar else "Do not display the color bar."}
    7. {f"Force the cells to be square." if square else "Do not force square cells."}
    8. {f"Mask the upper triangle of the heatmap." if mask else "Do not mask the upper triangle."}
    9. Set the figure size to {figsize}.
    10. Set the background color of the plot to '{bg_color}'.
    11. Set the title of the plot to '{title}'.
    """
    Code = Generator_Code_AI(prompt)
    return Code


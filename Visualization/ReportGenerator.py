import streamlit as st
import pandas as pd
from Visualization.EDAFunctions import (
    Dataset_Overview,
    missing_values_report,
    full_numerical_statistics,
    full_correlation_matrix,
    outlier_summary,
    duplicate_summary,
)

from streamlit_lottie import st_lottie
from Visualization.EDAFunctions import (
    Dataset_Overview_html,
    missing_values_report_html,
    random_numerical_statistics_html,
    random_correlation_matrix_html,
    outlier_summary_html,
    duplicate_summary_html,
)

pdf_files_to_delete = [ "Report_copy.md", "Report_copy.pdf"]
html_files_to_delete = ["Report_copy.html"]

import pandas as pd
import streamlit as st
import markdown2
import os
import asyncio
from playwright.async_api import async_playwright
import pathlib
import os
import time
import seaborn as sns
import matplotlib.pyplot as plt
from Visualization.HelperFun import Axis_Limits, Column_filter, Column_Remover
from Visualization.AIGen import Generator_Code_AI
from Visualization.HelperFun import Column_filter, Axis_Limits, find_repeating_categorical_columns, Column_Remover, copy_file, delete_files, load_lottie_file

files_to_delete = ["SampleScatterPlot_copy.html", "SampleScatterPlot_copy.md","SampleScatterPlot_copy.pdf","BoxPlt_copy.md","BoxPlt_copy.pdf","BoxPlt_copy.html"]

    
#? =================================== Additonal Functions ===================================

import markdown2
import os
import asyncio
from playwright.async_api import async_playwright
import pathlib
import os

import shutil

def copy_file(src_path):
    # Generate the destination path by appending '_copy' before the file extension
    dest_path = src_path.replace(".", "_copy.", 1)
    
    # Copy the file
    shutil.copy(src_path, dest_path)
    
    return dest_path




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
        
import os
import pathlib
import asyncio
from playwright.async_api import async_playwright
from multiprocessing import Process, Queue

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



def display_dataframe(data):
    """Display a DataFrame in a nice format."""
    st.dataframe(data)

def generate_report(df):
    
    if df.empty:
        st.warning("The DataFrame is empty.")
        return

    st.sidebar.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 18px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>1. Show Dataset preview</h2><br>""",
        unsafe_allow_html=True
    )
    
    # Get the last index of the DataFrame
    max_index = len(df) - 2
    
    # Slider for selecting the row index
    selected_index = st.sidebar.slider(
        "Select Row Index",
        min_value=0,
        max_value=max_index,
        value=(0,max_index),
        step=1,
        label_visibility="collapsed"
    )
    
    if selected_index:
        st.markdown(
            """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 26px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>Dataset Preview</h2><br>""",
            unsafe_allow_html=True
        )
        st.dataframe(df.iloc[selected_index[0]:selected_index[1] + 1])
    
    st.sidebar.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 18px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>2. Show Dataset Overview</h2><br>""",
        unsafe_allow_html=True
    )

    # Select box for Dataset Overview with hidden label
    overview = st.sidebar.selectbox("", ["False", "True"], label_visibility="collapsed", key="overview")

    if overview == "True":
        st.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 26px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>Show Dataset Overview</h2><br>""",
        unsafe_allow_html=True
        )
        overview = Dataset_Overview(df)  # Replace with your function to get overview
        st.write(overview) 
    
    st.sidebar.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 18px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>3. Show Missing Values Report</h2><br>""",
        unsafe_allow_html=True
    )
    
    missing_values = st.sidebar.selectbox("", ["False", "True"], label_visibility="collapsed", key="missing_values")
    
    if missing_values == "True":
        st.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 26px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>Show Missing Values Report</h2><br>""",
        unsafe_allow_html=True
        )
        missing_report = missing_values_report(df)
        st.dataframe(missing_report.transpose())
        
        
    st.sidebar.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 18px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>4. Show Random Numerical Statistics</h2><br>""",
        unsafe_allow_html=True
    )
    
    statistics = st.sidebar.selectbox("", ["False", "True"], label_visibility="collapsed", key="statistics")
    
    if statistics == "True":
        st.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 26px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>Show Random Numerical Statistics</h2><br>""",
        unsafe_allow_html=True
        )
        statistics = full_numerical_statistics(df)
        display_dataframe(pd.DataFrame(statistics[1:], columns=statistics[0]))
        
    st.sidebar.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 18px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>5. Show Random Correlation Matrix</h2><br>""",
        unsafe_allow_html=True
    )
    
    correlation = st.sidebar.selectbox("", ["False", "True"], label_visibility="collapsed", key="correlation")
    
    if correlation == "True":
        st.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 26px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>Show Random Correlation Matrix</h2><br>""",
        unsafe_allow_html=True
        )
        correlation = full_correlation_matrix(df)
        display_dataframe(pd.DataFrame(correlation[1:], columns=correlation[0]))
        
    st.sidebar.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 18px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>6. Show Outlier Summary</h2><br>""",
        unsafe_allow_html=True
    )
    
    outlier = st.sidebar.selectbox("", ["False", "True"], label_visibility="collapsed", key="outlier")
    
    if outlier == "True":
        st.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 26px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>Show Outlier Summary</h2><br>""",
        unsafe_allow_html=True
        )
        outlier_report = outlier_summary(df)
        st.dataframe(pd.DataFrame(outlier_report[1:], columns=outlier_report[0]).transpose())
        
    st.sidebar.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 18px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>7. Show Duplicate Summary</h2><br>""",
        unsafe_allow_html=True
    )
    
    duplicate = st.sidebar.selectbox("", ["False", "True"], label_visibility="collapsed", key="duplicate")
    
    if duplicate == "True":
        st.markdown(
        """<h2 style='color: #FFFFFF; font-weight: bold;align-item:center;text-align:center; font-size: 26px; font-family: "Times New Roman"; border-bottom: 2px solid #FFFFFF; padding-bottom: 10px;'>Show Duplicate Summary</h2><br>""",
        unsafe_allow_html=True
        )
        duplicate_report = duplicate_summary(df)
        display_dataframe(pd.DataFrame(duplicate_report[1:], columns=duplicate_report[0]).transpose())
        
        
def ReportGenerator():
    
    with st.sidebar:
        image_path = './Visualization/assets/Images/logo.png'
        if os.path.exists(image_path):
            st.image(image_path, width=200)
        else:
            st.error("Logo image not found.")
            
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if not uploaded_file:
        with st.sidebar:
            st.info("Please upload a CSV file and choose a plot type.")
            lottie_json = load_lottie_file("./Visualization/FilesJson/Navbar-Jif.json")
            st_lottie(lottie_json, speed=1, width=250, height=250, key="initial")
            
    else:
        df = pd.read_csv(uploaded_file)

        # Generate report based on user's choice
        generate_report(df)
        
        if st.sidebar.button("Generate Report......"):
            Report_Gen(df)
            st.success("Report generated successfully!")
            
def Report_Gen(df):
    
    changing_sec =  change_content(df)
    
    replace_all_markers("Report.md", changing_sec)
    # Convert the Markdown file to HTML
    html_file = convert_md_to_html("Report_copy.md")
    
    # Generate PDF
    with st.spinner("Generating PDF..."):
        pdf_file = generate_pdf_with_multiprocessing(html_file)
        
    
    # Add a download button for the generated PDF
    col1, col2 = st.columns([1, 1])
    
    with col1:
            
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name="EDA_Report.pdf",
                    mime="application/pdf",
                    on_click=lambda: delete_files(pdf_files_to_delete)
                )
                
    with col2:
            img = "Visualization\Images\logo.png"
            create_zip_and_download(html_file, img)
                
def change_content(df):
    
    dataset_overview = Dataset_Overview_html(df)
    
    Changing_Section = {
        "I1Shape_(rows, columns)" : str(dataset_overview[0]),
        "I2Data_Types" : str(dataset_overview[1]),
        "II_Missing_Values": missing_values_report_html(df),
        "III_Summary_Numerical_Statistics": random_numerical_statistics_html(df),
        "IV_Correlation_Matrix" : random_correlation_matrix_html(df),
        "V_Outlier_Summary": outlier_summary_html(df),
        "VI_Duplicates_Summary": duplicate_summary_html(df)
        
    }
    
    return Changing_Section


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     missing_values = st.sidebar.selectbox("", ["False", "True"], label_visibility="collapsed")
    
    




















#     if st.sidebar.checkbox("Show Missing Values Report"):
#         missing_report = missing_values_report(df)
#         display_dataframe(pd.DataFrame(missing_report[1:], columns=missing_report[0]))

#     if st.sidebar.checkbox("Show Random Numerical Statistics"):
#         statistics = random_numerical_statistics(df)
#         display_dataframe(pd.DataFrame(statistics[1:], columns=statistics[0]))

#     if st.sidebar.checkbox("Show Random Correlation Matrix"):
#         correlation = random_correlation_matrix(df)
#         display_dataframe(pd.DataFrame(correlation[1:], columns=correlation[0]))

#     if st.sidebar.checkbox("Show Outlier Summary"):
#         outlier_report = outlier_summary(df)
#         display_dataframe(pd.DataFrame(outlier_report[1:], columns=outlier_report[0]))

#     if st.sidebar.checkbox("Show Duplicate Summary"):
#         duplicate_report = duplicate_summary(df)
#         display_dataframe(pd.DataFrame(duplicate_report[1:], columns=duplicate_report[0]))

# # Main function to run the Streamlit app
# def ReportGenerator():
#     with st.sidebar:
#         image_path = './Visualization/assets/Images/logo.png'
#         if os.path.exists(image_path):
#             st.image(image_path, width=200)
#         else:
#             st.error("Logo image not found.")
            
#     uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
#     if not uploaded_file:
#         with st.sidebar:
#             st.info("Please upload a CSV file and choose a plot type.")
#             lottie_json = load_lottie_file("./Visualization/FilesJson/Navbar-Jif.json")
#             st_lottie(lottie_json, speed=1, width=250, height=250, key="initial")

#     else:
#         df = pd.read_csv(uploaded_file)

#         st.subheader("Dataset Preview")
#         st.dataframe(df.head())

#         # Generate report based on user's choice
#         generate_report(df)
        
#         if st.sidebar.button("Generate Report......"):
#             Report_Gen(df)
#             st.success("Report generated successfully!")







# def Report_Gen(df):
    
#     changing_sec =  change_content(df)
    
#     replace_all_markers("Report.md", changing_sec)
#     # Convert the Markdown file to HTML
#     html_file = convert_md_to_html("Report_copy.md")

#     # Generate PDF
#     with st.spinner("Generating PDF..."):
#         pdf_file = generate_pdf_with_multiprocessing(html_file)

#     st.success("PDF generated successfully!")

#     # Add a download button for the generated PDF
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
        
#         with open(pdf_file, "rb") as file:
#             st.download_button(
#                 label="Download PDF",
#                 data=file,
#                 file_name="EDA_Report.pdf",
#                 mime="application/pdf",
#                 on_click=lambda: delete_files(pdf_files_to_delete)
#             )
            
#     with col2:
        
#         with open(html_file, "rb") as file:
#             st.download_button(
#                 label="Download HTML",
#                 data=file,
#                 file_name="EDA_Report.html",
#                 mime="text/html",
#                 on_click=lambda: delete_files(html_files_to_delete)
#             )
            
            
        

# def change_content(df):
        
#     dataset_overview = Dataset_Overview(df)    


#     Changing_Section = {
#         "I1Shape_(rows, columns)" : str(dataset_overview[0]),
#         "I2Data_Types" : str(dataset_overview[1]),
#         "II_Missing_Values": missing_values_report_html(df),
#         "III_Summary_Numerical_Statistics": random_numerical_statistics_html(df),
#         "IV_Correlation_Matrix" : random_correlation_matrix_html(df),
#         "V_Outlier_Summary": outlier_summary_html(df),
#         "VI_Duplicates_Summary": duplicate_summary_html(df)
        
#     }
#     return Changing_Section


import streamlit as st
import zipfile
import os

def create_zip_and_download(html_file, other_file):
    """
    Creates a ZIP file containing specified files and provides a download button for it.

    Parameters:
    - html_file (str): Path to the HTML file to include.
    - other_file (str): Path to another file to include.
    """
    # Function to create a ZIP file containing the specified files
    def create_zip_file(file_list, zip_file_name):
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            for file in file_list:
                zip_file.write(file, os.path.basename(file))

    # Create a ZIP file name
    zip_file_name = "report.zip"
    
    # Create the ZIP file
    create_zip_file([html_file, other_file], zip_file_name)

    # Provide a download button for the ZIP file
    with open(zip_file_name, "rb") as zip_file:
        st.download_button(
            label="HTML file",
            data=zip_file,
            file_name=zip_file_name,
            mime="application/zip",
            on_click=lambda: delete_files([html_file, other_file, zip_file_name])  # Adjust your delete logic as needed
        )

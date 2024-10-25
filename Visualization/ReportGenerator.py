import streamlit as st
import pandas as pd
from Visualization.EDAFunctions import (
    Dataset_Overview,
    missing_values_report,
    random_numerical_statistics,
    random_correlation_matrix,
    outlier_summary,
    duplicate_summary,
)

from Visualization.EDAFunctions import (
    missing_values_report_html,
    random_numerical_statistics_html,
    random_correlation_matrix_html,
    outlier_summary_html,
    duplicate_summary_html,
)

files_to_delete = ["Report_copy.html", "Report_copy.md", "Report_copy.pdf"]

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
from Visualization.HelperFun import Column_filter, Axis_Limits, find_repeating_categorical_columns, Column_Remover, copy_file, delete_files

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
    st.title("Data Analysis Report")

    # Checkboxes for different analyses
    if st.sidebar.checkbox("Show Dataset Overview"):
        overview = Dataset_Overview(df)
        display_dataframe(pd.DataFrame(overview[1:], columns=overview[0]))

    if st.sidebar.checkbox("Show Missing Values Report"):
        missing_report = missing_values_report(df)
        display_dataframe(pd.DataFrame(missing_report[1:], columns=missing_report[0]))

    if st.sidebar.checkbox("Show Random Numerical Statistics"):
        statistics = random_numerical_statistics(df)
        display_dataframe(pd.DataFrame(statistics[1:], columns=statistics[0]))

    if st.sidebar.checkbox("Show Random Correlation Matrix"):
        correlation = random_correlation_matrix(df)
        display_dataframe(pd.DataFrame(correlation[1:], columns=correlation[0]))

    if st.sidebar.checkbox("Show Outlier Summary"):
        outlier_report = outlier_summary(df)
        display_dataframe(pd.DataFrame(outlier_report[1:], columns=outlier_report[0]))

    if st.sidebar.checkbox("Show Duplicate Summary"):
        duplicate_report = duplicate_summary(df)
        display_dataframe(pd.DataFrame(duplicate_report[1:], columns=duplicate_report[0]))

# Main function to run the Streamlit app
def ReportGenerator():
    st.header("Upload Dataset")
    st.sidebar.title("Data Analysis Report")
    
    

    # File uploader for dataset
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the dataset
        df = pd.read_csv(uploaded_file)

        # Show a preview of the dataset
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        # Generate report based on user's choice
        generate_report(df)
        
        if st.sidebar.button("Generate Report......"):
            with st.spinner("Generating Report..."):
                # Generate the report
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

    st.success("PDF generated successfully!")

    # Add a download button for the generated PDF
    with open(pdf_file, "rb") as file:
        st.download_button(
            label="Download PDF",
            data=file,
            file_name="EDA_Report.pdf",
            mime="application/pdf",
            # on_click=lambda: delete_files(files_to_delete)
        )
        
        
    

def change_content(df):
        
    dataset_overview = Dataset_Overview(df)    


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
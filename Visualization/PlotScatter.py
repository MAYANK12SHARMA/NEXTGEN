import os
import asyncio
import pathlib
import markdown2
import pandas as pd
import seaborn as sns
import streamlit as st
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




#? ========================================= Scatter plot Functions ======================================

def create_scatter_plot(data, x_col, y_col, hue_col, size_col, style_col, palette, sizes, markers, bg_color, color,figsize, xlim, ylim, alpha=0.7, x_label=None, y_label=None, title=None, **kwargs):
    plt.figure(figsize=figsize)
    
    sns.set(style="whitegrid", palette=palette)  # Set style and palette
    plt.gca().set_facecolor(bg_color)  # Set background color after setting style
    
    # Scatterplot
    scatter = sns.scatterplot(
        data=data, 
        x=x_col, 
        y=y_col, 
        hue=hue_col if hue_col else None, 
        size=size_col if size_col else None, 
        style=style_col if style_col else None, 
        sizes=sizes, 
        color=color, 
        marker = markers,
        legend='full',
        alpha=alpha, 
        **kwargs
    )
    
    plt.title(title, fontsize=18, fontweight='bold', color="#444444")
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    
    if size_col or hue_col or style_col:
        plt.legend(loc='upper center', ncol=7, bbox_to_anchor=(0.5, -0.15), fancybox=True, framealpha=0.9, facecolor='lightgray', edgecolor='black')

    # Set axis limits
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
        
    # Display the plot
    st.pyplot(plt)
    
    # Save and clear
    plt.tight_layout()
    plt.savefig("scatter_plot.png")
    plt.clf()

#? ========================================= Visualise Scatter Plot ======================================= 

def Scatter_Plot_visualize(df):
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Column Customization </h2>""", unsafe_allow_html=True)
    x_column = st.sidebar.selectbox("📊 Select X-axis column", Column_filter(df, 'number'))
    y_column = st.sidebar.selectbox("📊 Select Y-axis column", Column_Remover(Column_filter(df, 'number'), x_column))
    hue_column = st.sidebar.selectbox("📊 Select Hue column (optional)", [None] + find_repeating_categorical_columns(df))
    size_column = st.sidebar.selectbox("📊 Select Size column (optional)", [None] + list(df.columns))
    style_column = st.sidebar.selectbox("📊 Select Style column (optional)", [None] + find_repeating_categorical_columns(df))
    
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>B. 📊 Marker Customization</h2>""", unsafe_allow_html=True)
    markers = st.sidebar.selectbox("Select Marker Style", ['o', 'D','*', '^', 'v', 'x', '+'])
    alpha = st.sidebar.slider("Select Marker Transparency", min_value=0.0, max_value=1.0, value=0.7)
    sizes = st.sidebar.slider("Marker Size Range", min_value=5, max_value=200, value=(20, 100))
    marker_color = st.sidebar.color_picker("Pick Marker Color", "#ff0000")

    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>C. 🎨 Box customization</h2>""", unsafe_allow_html=True)
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)
    xlim = Axis_Limits(df, x_column, 'x') if x_column else None
    ylim = Axis_Limits(df, y_column, 'y') if y_column else None
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    bg_color = st.sidebar.color_picker("Pick background color", "#f0f0f0")
    
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>D. 📊 Axis Title Customization</h2>""", unsafe_allow_html=True)
    x_label = st.sidebar.text_input("X-axis Label (optional)", x_column if x_column else "")
    y_label = st.sidebar.text_input("Y-axis Label (optional)", y_column if y_column else "")
    tit = f"Scatter Plot of {x_column} v/s {y_column}"
    title = st.sidebar.text_input("Plot Title (optional)", tit)
    
    if st.sidebar.button("Generate Scatter Plot"):
        with st.spinner("Generating Scatter plot ..."):
            create_scatter_plot(df, x_column, y_column, hue_column, size_column, style_column, palette, sizes, markers, bg_color, marker_color, alpha=alpha, xlim=xlim, ylim=ylim, figsize=(plot_width, plot_height), x_label=x_label, y_label=y_label, title=title)
        
        
        with open("scatter_plot.png", "rb") as file:
            st.download_button(
                label="Download Scatter Plot",
                data=file,
                file_name="Scatter_Plot.png",
                mime="image/png"
            ) 
    if st.sidebar.button("Generate Code and Get Report"):
        with st.spinner("Generating Scatter plot ..."):
            create_scatter_plot(df, x_column, y_column, hue_column, size_column, style_column, palette, sizes, markers, bg_color, marker_color, alpha=alpha, xlim=xlim, ylim=ylim, figsize=(plot_width, plot_height), x_label=x_label, y_label=y_label, title=title)
        
        with st.spinner("Generating Code..."): 
            generated_code = scatter_plot_code_generator(df, x_column, y_column, hue_column, size_column, style_column, palette, sizes, markers, bg_color, marker_color, alpha=alpha, xlim=xlim, ylim=ylim, x_label=x_label, y_label=y_label, title=title,figsize=(plot_width, plot_height))
        
        st.code(generated_code, language='python')
        
        col1, col2 = st.columns([1,1])
        
        with col1:
            with open("scatter_plot.png", "rb") as file:
                st.download_button(
                    label="Download Scatter Plot",
                    data=file,
                    file_name="Scatter_Plot.png",
                    mime="image/png"
                )
        
        with col2:
            changing_sec = {
                "ImagesofScatterPlot": "scatter_plot.png",
                "CodingPart": generated_code
            }
            replace_all_markers("SampleScatterPlot.md", changing_sec)
            # Convert the Markdown file to HTML
            html_file = convert_md_to_html("SampleScatterPlot_copy.md")
            # Generate PDF
            with st.spinner("Generating PDF..."):
                pdf_file = generate_pdf_with_multiprocessing(html_file)

            st.success("PDF generated successfully!")

            if 'download_triggered' not in st.session_state:
                st.session_state.download_triggered = False
                
            # Add a download button for the generated PDF
            with open(pdf_file, "rb") as file:
                if st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name="SampleScatterPlot.pdf",
                    mime="application/pdf",
                    on_click=lambda: delete_files(files_to_delete)
                ):
                    st.session_state.download_triggered = True

                     

#? ========================================= Code Generator  ======================================= 

def scatter_plot_code_generator(df, x_col, y_col, hue_col, size_col, style_col, palette, sizes, markers, bg_color, color, figsize, xlim, ylim, alpha=0.7, x_label=None, y_label=None, title=None, **kwargs):
    prompt = f"""
    Create a scatter plot in Python using the following specifications:
    1. Use the dataset stored in the variable '{df}'.
    2. Plot '{x_col}' on the x-axis.
    3. Plot '{y_col}' on the y-axis.
    4. {f"Distinguish data points by the '{hue_col}' column, using the '{palette}' color palette." if hue_col else "Do not use hue for distinguishing data points."}
    5. {f"Vary the size of the markers based on '{size_col}' with size range '{sizes}'." if size_col else "Do not vary marker sizes."}
    6. {f"Use marker style based on the '{style_col}' column with markers '{markers}'." if style_col else "Use a single marker style."}
    7. Set the background color of the plot to '{bg_color}'.
    8. Set marker color to '{color}'.
    9. Use a transparency level of {alpha}.
    10. Set the figure size to {figsize}.
    11. {f"Limit the x-axis to {xlim}." if xlim else "Do not set x-axis limits."}
    12. {f"Limit the y-axis to {ylim}." if ylim else "Do not set y-axis limits."}
    13. Label the x-axis as '{x_label}'.
    14. Label the y-axis as '{y_label}'.
    15. Set the title of the plot to '{title}'.
    """
    Code = Generator_Code_AI(prompt)
    return Code

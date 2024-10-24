import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from Visualization.HelperFun import Axis_Limits, Column_filter, Column_Remover
from Visualization.AIGen import Generator_Code_AI

def create_box_plot(data, x_col, y_col, hue_col, palette, showfliers, outlier_marker, outlier_size, outlier_color, 
                    linewidth, line_color, bg_color, showmeans, meanColor, meanMarker, figsize, 
                    xlim, ylim, x_label, y_label, title):
    plt.figure(figsize=figsize)

    # Set Seaborn style and background color
    sns.set(style="whitegrid")
    plt.gca().set_facecolor(bg_color)

    # Create the boxplot
    sns.boxplot(
        data=data,
        x=x_col,
        y=y_col,
        hue=hue_col if hue_col else None,  # Use hue_col only if not None
        palette=palette,
        showfliers=showfliers,
        showmeans=showmeans,
        flierprops={'marker': outlier_marker, 'color': outlier_color, 'markersize': outlier_size} if showfliers else None,
        meanprops={'marker': meanMarker, 'markersize': 10, 'markerfacecolor': meanColor, 'markeredgecolor': meanColor} if showmeans else None,
        linewidth=linewidth,
        whiskerprops=dict(color=line_color, linewidth=linewidth),
        capprops=dict(color=line_color, linewidth=linewidth),
        medianprops=dict(color=line_color, linewidth=linewidth),
    )

    # Set axis limits if defined
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)

    # Apply custom titles and labels
    plt.title(title, fontsize=18, fontweight='bold', color="#444444")
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)

    # Legend customization if hue_col is used
    if hue_col:
        plt.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5, -0.15), fancybox=True, framealpha=0.9, facecolor='lightgray', edgecolor='black')

    # Add grid
    plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)

    # Display plot
    st.pyplot(plt)

    # Save plot and clear figure
    plt.tight_layout()
    plt.savefig("box_plot.png")
    plt.clf()  


def Box_plot_visualize(df):
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Axis and Grid Customization</h2>""", unsafe_allow_html=True)
    x_column = st.sidebar.selectbox("📊 Select X-axis column", [None] + Column_filter(df,"number"))
    y_column = st.sidebar.selectbox("📊 Select Y-axis column", [None] + Column_Remover(list(df.columns),x_column))
    hue_column = st.sidebar.selectbox("📊 Select Hue column (optional)", [None] + Column_filter(df, 'object'))

    # Outlier customization
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>B. 📊 Outlier Customization</h2>""", unsafe_allow_html=True)
    outlier_mark = ['+', 'o', '*']
    showfliers = st.sidebar.checkbox("Show Outliers", value=True)
    outlier_marker = st.sidebar.selectbox("Select Outlier Marker", outlier_mark)
    outlier_size = st.sidebar.slider("Select Outlier Marker Size", min_value=1, max_value=10, value=5)
    outlier_color = st.sidebar.color_picker("Pick Outlier Marker Color", "#ff0000")

    # Mean customization
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>C. 📊 Mean Customization</h2>""", unsafe_allow_html=True)
    showmeans = st.sidebar.checkbox("Show Mean", value=True)
    meanMarker = st.sidebar.selectbox("Select Mean Marker", outlier_mark)
    meanColor = st.sidebar.color_picker("Pick Mean Marker Color", "#1f77b4")

    # Line customization
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>D. 🎨 Line customization</h2>""", unsafe_allow_html=True)
    linewidth = st.sidebar.slider("Select Line Width", min_value=0.5, max_value=3.0, value=1.5)
    line_color = st.sidebar.color_picker("Pick Line Color", "#000000")

    # Box customization
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>E. 🎨 Box customization</h2>""", unsafe_allow_html=True)
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")
    
    # Axis limits
    if x_column:
        xlim = Axis_Limits(df, x_column, 'x')
    else:
        xlim = None
        
    if y_column:
        ylim = Axis_Limits(df, y_column, 'y')
    else:
        ylim = None

    # Axis title customization
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>F. 📊 Axis Title Customization</h2>""", unsafe_allow_html=True)
    x_label = st.sidebar.text_input("X-axis Label (optional)", x_column if x_column else "")
    y_label = st.sidebar.text_input("Y-axis Label (optional)", y_column if y_column else "")
    title = st.sidebar.text_input("Plot Title (optional)", "Box Plot")

    # Ensure hue_column is None if the user selects "None"
    hue_column = hue_column if hue_column != "None" else None
    
    
    if st.sidebar.button("Generate Box Plot"):
        create_box_plot(data=df, x_col=x_column, y_col=y_column, hue_col=hue_column, palette=palette, showfliers=showfliers, outlier_marker=outlier_marker, outlier_size=outlier_size, outlier_color=outlier_color, 
                    linewidth=linewidth, line_color=line_color, bg_color=bg_color, showmeans=showmeans, meanColor=meanColor, meanMarker=meanMarker, figsize=(plot_width,plot_height),
                    xlim=xlim, ylim=ylim, x_label=x_label, y_label=y_label, title=title)
        
        with open('box_plot.png', "rb") as file:
            st.download_button(
                label="Download Box Plot",
                data=file,
                file_name="box_plot.png",
                mime="image/png"
            )

        st.success("Box plot generated successfully!")
    elif st.sidebar.button("Generate Code"):
        create_box_plot(data=df, x_col=x_column, y_col=y_column, hue_col=hue_column, palette=palette, showfliers=showfliers, outlier_marker=outlier_marker, outlier_size=outlier_size, outlier_color=outlier_color, 
                linewidth=linewidth, line_color=line_color, bg_color=bg_color, showmeans=showmeans, meanColor=meanColor, meanMarker=meanMarker, figsize=(plot_width,plot_height),
                xlim=xlim, ylim=ylim, x_label=x_label, y_label=y_label, title=title)
    
        with open('box_plot.png', "rb") as file:
            st.download_button(
                label="Download Box Plot",
                data=file,
                file_name="box_plot.png",
                mime="image/png"
            )
        
        Code = Generator_Code(df, x_column, y_column, hue_column, palette, showfliers, outlier_marker, outlier_size, outlier_color, linewidth, line_color, bg_color, showmeans, meanColor, meanMarker, (plot_width,plot_height), xlim, ylim, x_label, y_label, title)
        st.code(Code, language='python')
    else:
        st.info("Click on the 'Generate Box Plot' button to create the Box Plot")

        
   
   

def Generator_Code(df, x_column, y_column, hue_column, palette, showfliers, outlier_marker, outlier_size, outlier_color, linewidth, line_color, bg_color, showmeans, meanColor, meanMarker, figsize, xlim, ylim, x_label, y_label, title):
    prompt = f"""
    Create a box plot using the following parameters in python language:
    1. Use the dataset stored in the variable 'df'.
    2. For the x-axis, use the column '{x_column}'.
    3. For the y-axis, use the column '{y_column}'.
    4. {f"Group the data by the '{hue_column}' column and apply different colors." if hue_column else "Do not group the data by any hue column."}
    5. Use the color palette '{palette}'.
    6. {f"Display outliers with marker '{outlier_marker}', size '{outlier_size}', and color '{outlier_color}'." if showfliers else "Do not show outliers."}
    7. Set the thickness of the box plot lines to {linewidth} and the line color to '{line_color}'.
    8. Set the background color of the plot to '{bg_color}'.
    9. {f"Display the mean with marker '{meanMarker}' and color '{meanColor}'." if showmeans else "Do not display the mean."}
    10. Set the figure size to {figsize}.
    11. {f"Limit the x-axis to {xlim}." if xlim else "Do not set x-axis limits."}
    12. {f"Limit the y-axis to {ylim}." if ylim else "Do not set y-axis limits."}
    13. Label the x-axis as '{x_label}'.
    14. Label the y-axis as '{y_label}'.
    15. Set the title of the plot to '{title}'.
    """
    Code = Generator_Code_AI(prompt)
    return Code
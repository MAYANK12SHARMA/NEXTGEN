import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from HandlingMissingValue import MissingValueMethod  

#?=================================== Additional Function ====================================

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

#? ======================================== Box Plot Generator ======================================== 

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
  
def Box_Plot_Generator(df):
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Axis and Grid Customization</h2>""", unsafe_allow_html=True)
    x_column = st.sidebar.selectbox("📊 Select X-axis column", [None] + Column_filter(df,"number"))
    y_column = st.sidebar.selectbox("📊 Select Y-axis column", [None] + list(df.columns))
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
    if st.sidebar.button("Generate Code"):
        create_box_plot(data=df, x_col=x_column, y_col=y_column, hue_col=hue_column, palette=palette, showfliers=showfliers, outlier_marker=outlier_marker, outlier_size=outlier_size, outlier_color=outlier_color, 
                    linewidth=linewidth, line_color=line_color, bg_color=bg_color, showmeans=showmeans, meanColor=meanColor, meanMarker=meanMarker, figsize=(plot_width,plot_height),
                    xlim=xlim, ylim=ylim, x_label=x_label, y_label=y_label, title=title)
        
        generated_code = generate_code(data=df, x_col=x_column, y_col=y_column, hue_col=hue_column, palette=palette, showfliers=showfliers, outlier_marker=outlier_marker, outlier_size=outlier_size, outlier_color=outlier_color, 
                    linewidth=linewidth, line_color=line_color, bg_color=bg_color, showmeans=showmeans, meanColor=meanColor, meanMarker=meanMarker, figsize=(plot_width,plot_height),
                    xlim=xlim, ylim=ylim, x_label=x_label, y_label=y_label, title=title)

        st.code(generated_code, language='python')
        # Provide download link
            
def generate_code(data, x_col, y_col, hue_col, palette, showfliers, outlier_marker, outlier_size, outlier_color, 
                  linewidth, line_color, bg_color, showmeans, meanColor, meanMarker, figsize, 
                  xlim, ylim, x_label, y_label, title):
    code = f"""
        import seaborn as sns
        import matplotlib.pyplot as plt

        # Set the figure size
        plt.figure(figsize={figsize})

        # Set the background color
        plt.gca().set_facecolor('{bg_color}')

        # Create the boxplot
        sns.boxplot(
            data=data,
            x='{x_col}',
            y='{y_col}',
            hue='{hue_col}' if '{hue_col}' != 'None' else None,
            palette='{palette}',
            showfliers={showfliers},
            showmeans={showmeans},
            flierprops={{'marker': '{outlier_marker}', 'color': '{outlier_color}', 'markersize': {outlier_size}}} if {showfliers} else None,
            meanprops={{'marker': '{meanMarker}', 'markersize': 10, 'markerfacecolor': '{meanColor}', 'markeredgecolor': '{meanColor}'}} if {showmeans} else None,
            linewidth={linewidth},
            whiskerprops=dict(color='{line_color}', linewidth={linewidth}),
            capprops=dict(color='{line_color}', linewidth={linewidth}),
            medianprops=dict(color='{line_color}', linewidth={linewidth}),
        )

        # Set axis limits if defined
        if {xlim}:
            plt.xlim({xlim})
        if {ylim}:
            plt.ylim({ylim})

        # Set axis labels and title
        plt.xlabel('{x_label}')
        plt.ylabel('{y_label}')
        plt.title('{title}', fontsize=18, fontweight='bold')

        # Show grid
        plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)

        # Show the plot
        plt.tight_layout()
        plt.show()
            """
    return code
    
#? ======================================== Scatter Plot Generator ========================================


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

    
    
    
    plt.title(f'Scatter Plot of {y_col} vs {x_col}', fontsize=18, fontweight='bold', color="#444444")
    
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

def Scatter_Plot_Generator(df):
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Column Customization </h2>""", unsafe_allow_html=True)
    x_column = st.sidebar.selectbox("📊 Select X-axis column", df.columns)
    y_column = st.sidebar.selectbox("📊 Select Y-axis column", Column_filter(df, 'number'))
    hue_column = st.sidebar.selectbox("📊 Select Hue column (optional)", [None] + Column_filter(df,'object'))
    size_column = st.sidebar.selectbox("📊 Select Size column (optional)", [None] + list(df.columns))
    style_column = st.sidebar.selectbox("📊 Select Style column (optional)", [None] + Column_filter(df,'object'))
    
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>B. 📊 Marker Customization</h2>""", unsafe_allow_html=True)
    markers = st.sidebar.selectbox("Select Marker Style", ['o', '*', '^', 'v', 'x', '+'])
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
    title = st.sidebar.text_input("Plot Title (optional)", "Box Plot")

    if st.sidebar.button("Generate Scatter Plot"):
        create_scatter_plot(df, x_column, y_column, hue_column, size_column, style_column, palette, sizes, markers, bg_color, marker_color, alpha=alpha, xlim=xlim, ylim=ylim, figsize=(plot_width, plot_height), x_label=x_label, y_label=y_label, title=title)
        
        # Provide download link
        with open("scatter_plot.png", "rb") as file:
            st.download_button(
                label="Download Scatter Plot",
                data=file,
                file_name="Scatter_Plot.png",
                mime="image/png"
            ) 
    if st.sidebar.button("Generate Code"):
        create_scatter_plot(df, x_column, y_column, hue_column, size_column, style_column, palette, sizes, markers, bg_color, marker_color, alpha=alpha, xlim=xlim, ylim=ylim, figsize=(plot_width, plot_height), x_label=x_label, y_label=y_label, title=title)
        
        generated_code = scatter_plot_code_generator(df, x_column, y_column, hue_column, size_column, style_column, palette, sizes, markers, bg_color, marker_color, alpha=alpha, xlim=xlim, ylim=ylim, x_label=x_label, y_label=y_label, title=title,figsize=(plot_width, plot_height))
        st.code(generated_code, language='python')
        # Provide download link
        with open("scatter_plot.png", "rb") as file:
            st.download_button(
                label="Download Scatter Plot",
                data=file,
                file_name="Scatter_Plot.png",
                mime="image/png"
            )                  
 
 
def scatter_plot_code_generator(df, x_col, y_col, hue_col, size_col, style_col, palette, sizes, markers, bg_color, color, figsize, xlim, ylim, alpha=0.7, x_label=None, y_label=None, title=None, **kwargs):
    if hue_col:
        hue_col = f"{hue_col}"
    if size_col:
        size_col = f"{size_col}"
    if style_col:
        style_col = f"{style_col}"
    if xlim:
        xlim = plt.xlim(xlim)
    if ylim:
        ylim_data = "ylim"
        
    code = f"""
        import seaborn as sns
        import matplotlib.pyplot as plt

        # Set the figure size
        plt.figure(figsize={figsize})

        # Set the background color
        plt.gca().set_facecolor('{bg_color}')

        # Create the scatter plot
        sns.scatterplot(
            data=df, 
            x='{x_col}', 
            y='{y_col}', 
            hue='{hue_col}' if '{hue_col}' else None, 
            size='{size_col}' if '{size_col}' else None, 
            style='{style_col}' if '{style_col}' else None, 
            sizes={sizes}, 
            color='{color}', 
            palette='{palette}',
            legend='full',
            alpha={alpha}, 
            **kwargs
        )
        
        plt.xlim({xlim})
        """
    if {ylim_data}:
        code += f"""plt.ylim({ylim})\n"""
    code += f"""
        plt.xlabel('{x_label}')
        plt.ylabel('{y_label}')
        plt.title('{title}', fontsize=18, fontweight='bold')
    
        # Show the plot
        plt.tight_layout()
        plt.show()
            """
    return code


#? ======================================== Bar Plot Generator ========================================

def create_bar_plot(data, x_col, y_col, hue_col, palette, ci, capsize, errwidth, dodge, orient, color, bg_color, gap, log_scale, legend, figsize):
    plt.figure(figsize=figsize)
    plt.gca().set_facecolor(bg_color)
    sns.set(style="whitegrid", palette=palette)

    sns.barplot(
        data=data,
        x=x_col,
        y=y_col,
        hue=hue_col,
        ci=ci,
        capsize=capsize,
        errwidth=errwidth,
        dodge=dodge,
        orient=orient,
        color=color,
        log_scale= True if log_scale else False,
        gap=gap,
        legend=True if legend else False 
    )

    plt.title(f'Bar Plot of {y_col} vs {x_col}', fontsize=18, fontweight='bold', color="#444444")
    if x_col:
        format_label(data, x_col, 'x')
    if y_col:
        format_label(data, y_col, 'y')
        
    plt.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5, -0.15),
               fancybox=True, framealpha=0.9, facecolor='lightgray', edgecolor='black')

    plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
    st.pyplot(plt)
    plt.tight_layout()
    plt.savefig("bar_plot.png")
    plt.clf()
    
def Bar_Plot_Generator(df):
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Axis and Grid Customization</h2>""", unsafe_allow_html=True)
    x_column = st.sidebar.selectbox("📊 Select X-axis column", df.columns)
    y_column = st.sidebar.selectbox("📊 Select Y-axis column",[None] + list(df.columns))
    hue_column = st.sidebar.selectbox("📊 Select Hue column (optional)", [None] + list(df.columns))
    
    st.sidebar.markdown("""<hr style="border:3px solid #eee;margin:1px 0px 1px 0px;">""", unsafe_allow_html=True)
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>B. 📊 Advance Cutomization</h2>""", unsafe_allow_html=True) 
    ci = st.sidebar.slider("Confidence Interval", min_value=0, max_value=100, value=95)
    log_scale = st.sidebar.checkbox("Log Scale", value=False)
    gap = st.sidebar.slider("Gap between bars", min_value=0.0, max_value=1.0, value=0.2)
    dodge = st.sidebar.checkbox("Dodge Bars", value=True)
    capsize = st.sidebar.slider("Cap Size", min_value=0, max_value=10, value=5)
    
    st.sidebar.markdown("""<hr style="border:3px solid #eee;margin:1px 0px 1px 0px;">""", unsafe_allow_html=True)
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>B. 📊 Plot Styling </h2>""", unsafe_allow_html=True) 
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    legend = st.sidebar.checkbox("Show Legend", value=True)
    orient = st.sidebar.selectbox("Orientation", ["vertical", "horizontal"])
    errwidth = st.sidebar.slider("Error Width", min_value=0.0, max_value=3.0, value=1.5)
    color = st.sidebar.color_picker("Pick Bar Color", "#ff0000")
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")
    

    if st.sidebar.button("Generate Bar Plot"):
        create_bar_plot(df, x_column, y_column, hue_column, palette, ci, capsize, errwidth, dodge, orient, color, bg_color, gap, log_scale, legend, (plot_width, plot_height))

        # Provide download link
        with open("bar_plot.png", "rb") as file:
            st.download_button("Bar Plot", file, file_name="Bar_Plot.png", mime="image/png")
            


#? ======================================== Line Plot Generator ========================================

def create_line_plot(data, x_col, y_col, hue_col, style_col, palette, linewidth, markers, bg_color, color):
    plt.figure(figsize=(12, 6))
    plt.gca().set_facecolor(bg_color)
    sns.set(style="whitegrid", palette=palette)

    sns.lineplot(
        data=data,
        x=x_col,
        y=y_col,
        hue=hue_col,
        style=style_col,
        linewidth=linewidth,
        markers=markers,
        color=color
    )

    plt.title(f'Line Plot of {y_col} vs {x_col}', fontsize=18, fontweight='bold', color="#444444")
    if x_col:
        format_label(data, x_col, 'x')
    if y_col:
        format_label(data, y_col, 'y')
        
    plt.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5, -0.15),
               fancybox=True, framealpha=0.9, facecolor='lightgray', edgecolor='black')

    plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
    st.pyplot(plt)
    plt.tight_layout()
    plt.savefig("line_plot.png")
    plt.clf()
    
def Line_Plot_Generator(df):
    x_column = st.sidebar.selectbox("📊 Select X-axis column", df.columns)
    y_column = st.sidebar.selectbox("📊 Select Y-axis column", df.columns)
    hue_column = st.sidebar.selectbox("📊 Select Hue column (optional)", [None] + list(df.columns))
    style_column = st.sidebar.selectbox("📊 Select Style column (optional)", [None] + list(df.columns))

    st.sidebar.subheader("🎨 Plot Style Options")
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    linewidth = st.sidebar.slider("Line Width", min_value=0.5, max_value=3.0, value=1.5)
    markers = st.sidebar.checkbox("Show Markers", value=True)
    color = st.sidebar.color_picker("Pick Line Color", "#ff0000")
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")

    if st.sidebar.button("Generate Line Plot"):
        create_line_plot(df, x_column, y_column, hue_column, style_column, palette, linewidth, markers, bg_color, color)

        # Provide download link
        with open("line_plot.png", "rb") as file:
            st.download_button("Line Plot", file, file_name="Line_Plot.png", mime="image/png")           



#? ======================================== Violin Plot Generator ========================================

def create_violin_plot(data, x_col, y_col, hue_col, palette, bw, cut, scale, scale_hue, gridsize, width, inner, linewidth, line_color, bg_color, color,figsize):
    plt.figure(figsize=figsize)
    plt.gca().set_facecolor(bg_color)
    sns.set(style="whitegrid", palette=palette)

    sns.violinplot(
        data=data,
        x=x_col,
        y=y_col,
        hue=hue_col,
        bw=bw,
        cut=cut,
        scale=scale,
        scale_hue=scale_hue,
        gridsize=gridsize,
        width=width,
        inner=inner,
        linewidth=linewidth,
        color=color,
        linecolor=line_color
    )

    plt.title(f'Violin Plot of {y_col} vs {x_col}', fontsize=18, fontweight='bold', color="#444444")
    if x_col:
        format_label(data, x_col, 'x')
    if y_col:
        format_label(data, y_col, 'y')
        
    plt.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5, -0.15),
               fancybox=True, framealpha=0.9, facecolor='lightgray', edgecolor='black')

    plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
    st.pyplot(plt)
    plt.tight_layout()
    plt.savefig("violin_plot.png")
    plt.clf()
    
def Violin_Plot_Generator(df):
    x_column = st.sidebar.selectbox("📊 Select X-axis column", df.columns)
    y_column = st.sidebar.selectbox("📊 Select Y-axis column", df.columns)
    hue_column = st.sidebar.selectbox("📊 Select Hue column (optional)", [None] + list(df.columns))

    st.sidebar.subheader("📊 Violin Plot Customization")
    bw = st.sidebar.slider("Bandwidth", min_value=0.1, max_value=1.0, value=0.5)
    cut = st.sidebar.slider("Cut", min_value=0, max_value=10, value=2)
    scale = st.sidebar.selectbox("Scale", ["area", "count", "width"])
    scale_hue = st.sidebar.checkbox("Scale Hue", value=True)
    gridsize = st.sidebar.slider("Grid Size", min_value=50, max_value=200, value=100)
    width = st.sidebar.slider("Width", min_value=0.5, max_value=2.0, value=0.8)
    inner = st.sidebar.selectbox("Inner", ["box", "quartile", "point", "stick", None])
    linewidth = st.sidebar.slider("Line Width", min_value=0.5, max_value=3.0, value=1.5)
    line_color = st.sidebar.color_picker("Pick Line Color", "#000000")
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")
    color = st.sidebar.color_picker("Pick Violin Color", "#ff0000")
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)

    if st.sidebar.button("Generate Violin Plot"):
        create_violin_plot(df, x_column, y_column, hue_column, palette, bw, cut, scale, scale_hue, gridsize, width, inner, linewidth, line_color, bg_color, color, (plot_width, plot_height))

        # Provide download link
        with open("violin_plot.png", "rb") as file:
            st.download_button("Violin Plot", file, file_name="Violin_Plot.png", mime="image/png")
         
#? ======================================== Pair Plot Generator ========================================

def create_pair_plot(data, hue_col, palette, diag_kind, kind, markers, height, aspect, bg_color):
    plt.figure(figsize=(14, 8))
    plt.gca().set_facecolor(bg_color)
    sns.set(style="whitegrid", palette=palette)

    sns.pairplot(
        data=data,
        hue=hue_col,
        diag_kind=diag_kind,
        kind=kind,
        markers=markers,
        height=height,
        aspect=aspect
    )

    plt.title(f'Pair Plot of the Data', fontsize=18, fontweight='bold', color="#444444")
    plt.xticks(fontsize=12, rotation=45, fontstyle='italic')
    plt.yticks(fontsize=12)
    plt.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5, -0.15),
               fancybox=True, framealpha=0.9, facecolor='lightgray', edgecolor='black')

    plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
    st.pyplot(plt)
    plt.tight_layout()
    plt.savefig("pair_plot.png")
    plt.clf()
    
def Pair_Plot_Generator(df):
    hue_column = st.sidebar.selectbox("📊 Select Hue column (optional)", [None] + list(df.columns))

    st.sidebar.subheader("📊 Pair Plot Customization")
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    diag_kind = st.sidebar.selectbox("Diagonal Plot Type", ["auto", "hist", "kde"])
    kind = st.sidebar.selectbox("Plot Type", ["scatter", "reg"])
    markers = st.sidebar.selectbox("Select Marker Style", ['o', '*', '^', 'v', 'x', '+'])
    height = st.sidebar.slider("Height", min_value=4, max_value=8, value=6)
    aspect = st.sidebar.slider("Aspect", min_value=0.5, max_value=2.0, value=1.0)
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)


    if st.sidebar.button("Generate Pair Plot"):
        create_pair_plot(df, hue_column, palette, diag_kind, kind, markers, height, aspect, bg_color)

        # Provide download link
        with open("pair_plot.png", "rb") as file:
            st.download_button("Pair Plot", file, file_name="Pair_Plot.png", mime="image/png")
            
#? ======================================== Histogram Plot Generator ========================================
  
def Create_Histogram_generator(df, x_col, bins, weights, stat, palette, binwidth, cumulative, element, kde, color, legend, log_scale, xlim, alpha=0.6, plot_size=(14, 8), bg_color="#f0f0f0"):
    plt.figure(figsize=plot_size)
    plt.gca().set_facecolor("#f0f0f0")
    sns.set(style="whitegrid", palette=palette)
    plt.gca().set_facecolor(bg_color)


# Create the histogram plot with all selected customizations
    sns.histplot(
        data=df,
        x=x_col,
        bins=bins if bins != 'auto' else 'auto',
        weights=df[weights] if weights else None,
        stat=stat,
        binwidth=binwidth if binwidth is not None else None,
        cumulative=cumulative,
        element=element,
        kde=True if kde else False,
        color=color,
        legend=legend,
        log_scale=log_scale,
        alpha=alpha
    )

    plt.title(f'Histogram of {x_col}', fontsize=18, fontweight='bold', color="#444444")
    if x_col:
        format_label(df, x_col, 'x')
    
        
    plt.yticks(fontsize=12)
    plt.xlim(xlim)
    plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)

    st.pyplot(plt)
    plt.tight_layout()
    plt.savefig("advanced_histogram_plot.png")
    plt.clf()

def Histogram_Plot_Generator(df):
    st.sidebar.subheader("📏 Axes and Grid Customization")
    x_column = st.sidebar.selectbox("📊 Select X-axis column", df.columns)
    bins = st.sidebar.text_input('🗑️ Select the number of bins', ['auto', 10, 20, 30, 40, 50])
    weights = st.sidebar.selectbox('📊 Select Weights column', [None] + list(df.columns))
    stat = st.sidebar.selectbox('📊 Select the type of stat', ['count', 'frequency', 'density', 'probability'])
    binwidth = st.sidebar.slider('📏 Select the binwidth', min_value=0.1, max_value=5.0, value=1.0)
    st.sidebar.markdown("""<hr style="border:3px solid #eee">""", unsafe_allow_html=True)
    
    st.sidebar.subheader("📊 Advance Customizations")
    kde = st.sidebar.checkbox("Show KDE", value=False)
    element = st.sidebar.selectbox("📊 Select the element", ["bars", "step", "poly"])
    cumulative = st.sidebar.checkbox("Cumulative", value=False)
    log_scale = st.sidebar.checkbox("Log Scale", value=False)
    st.sidebar.markdown("""<hr style="border:3px solid #eee">""", unsafe_allow_html=True)
    
    st.sidebar.subheader("🖼️ Plot Size Customization")
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)
    
    st.sidebar.markdown("""<hr style="border:3px solid #eee">""", unsafe_allow_html=True)
    
    st.sidebar.subheader("🎨 Plot Style Options")
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    color = st.sidebar.color_picker("Pick Color", "#ff0000")
    legend = st.sidebar.checkbox("Show Legend", value=True)
    alpha = st.sidebar.slider("Set Transparency (Alpha)", min_value=0.0, max_value=1.0, value=0.6, step=0.1)
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")
    
    
    
    xlim = st.sidebar.slider("X-axis Limits", min_value=float(df[x_column].min()), max_value=float(df[x_column].max()), value=(float(df[x_column].min()), float(df[x_column].max())), step=0.1)

    if st.sidebar.button("Generate Histogram"):
        Create_Histogram_generator(df, x_column, bins, weights, stat, palette, binwidth, cumulative, element, kde, color, legend, log_scale, xlim, alpha, (plot_width, plot_height), bg_color)

        # Provide download link
        with open("advanced_histogram_plot.png", "rb") as file:
            st.download_button("Histogram Plot", file, file_name="Histogram_Plot.png", mime="image/png")
            
#? ======================================== Pie Chart Generator ========================================

def create_pie_chart(data, values, names, palette, hole, labels, label_position, label_format, title, bg_color, figsize):
    plt.figure(figsize=figsize)
    plt.gca().set_facecolor(bg_color)
    sns.set(style="whitegrid", palette=palette)

    plt.pie(
        x=values,
        labels=names,
        autopct=label_format,
        pctdistance=0.85,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=hole, edgecolor=bg_color)
    )

    plt.title(title, fontsize=18, fontweight='bold', color="#444444")
    plt.axis('equal')
    plt.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5, -0.15),
               fancybox=True, framealpha=0.9, facecolor='lightgray', edgecolor='black')

    st.pyplot(plt)
    plt.tight_layout()
    plt.savefig("pie_chart.png")
    plt.clf()
    
    
def Pie_Chart_Generator(df):
    st.sidebar.subheader("📊 Pie Chart Customization")
    values = st.sidebar.text_area("📊 Enter values (comma-separated)", value="10, 20, 30, 40")
    names = st.sidebar.text_area("📊 Enter names (comma-separated)", value="A, B, C, D")
    hole = st.sidebar.slider("🕳️ Hole Size", min_value=0.0, max_value=1.0, value=0.0)
    labels = st.sidebar.checkbox("Show Labels", value=True)
    label_position = st.sidebar.selectbox("Label Position", ["inside", "outside"])
    label_format = st.sidebar.text_input("Label Format", value="%1.1f%%")
    title = st.sidebar.text_input("Title", value="Pie Chart")
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")
    palette = st.sidebar.selectbox("Select Color Palette", ["deep", "pastel", "dark", "colorblind", "viridis", "rocket", "mako", "flare"])
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)


    if st.sidebar.button("Generate Pie Chart"):
        values = [int(x.strip()) for x in values.split(",")]
        names = [x.strip() for x in names.split(",")]
        create_pie_chart(df, values, names, palette, hole, labels, label_position, label_format, title, bg_color, (plot_width, plot_height))
        # Provide download link
        with open("pie_chart.png", "rb") as file:
            st.download_button("Pie Chart", file, file_name="Pie_Chart.png", mime="image/png")
            
            
#? ======================================== Heatmap Generator ========================================
def Create_Heatmap(df, cmap, annot, fmt, annot_size, annot_color, linewidths, linecolor, cbar, cbar_kws, square, mask, figsize):
    sns.set(style="whitegrid")
    
    # Create a figure with the desired figsize
    # plt.figure(figsize=figsize)  # Ensure the figure size is set before plotting
    sns.set(rc={"figure.figsize": figsize})

    # Compute correlation matrix
    corr_matrix = df.corr()

    # Mask for upper triangle if needed
    if mask:
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    else:
        mask = None

    # Generate the heatmap with the specified parameters
    heatmap = sns.heatmap(
        data=corr_matrix,  
        annot=annot,  # Annotate cells with numeric values
        cmap=cmap,    # Color map
        cbar=cbar,    # Show color bar
        cbar_kws={'orientation': 'vertical',   # Makes the colorbar vertical
                'shrink': 0.8,               # Shrinks the colorbar by 80%
                'aspect': 10,                # Aspect ratio of the colorbar
                'pad': 0.05,                 # Distance between heatmap and colorbar
                'ticks': [0, 0.5, 1],        # Custom tick locations
                'format': '%.2f',            # Format of the ticks (2 decimal places)
                'location': 'right'          # Location of colorbar
            }, # Color bar settings
        fmt=fmt if annot else None,  # Set format for annotation
        annot_kws={"size": annot_size, "color": annot_color},
        linewidths=linewidths,
        linecolor=linecolor,
        # cbar_kws=cbar_kws,
        square=square,
        mask=mask
    )
    
    # Show the plot using Streamlit
    st.pyplot(plt)

    # Save the plot to a file
    plt.tight_layout()
    plt.savefig("heatmap.png")
    plt.clf()  # Clear the figure after saving it

def Heatmap_Generator(df):
    st.sidebar.markdown("""<h2 style='color: #FFFF4D; font-weight: bold;font-size:18px;'>A. 📊 Heatmap Customization</h2>""", unsafe_allow_html=True)
    cmap = st.sidebar.selectbox("🎨 Select Color Map", ["coolwarm", "viridis", "magma", "cividis", "plasma", "inferno", "YlGnBu", "BuGn"])
    annot = st.sidebar.checkbox("Annotate Cells", value=True)
    fmt = st.sidebar.slider("Annotation Format", min_value=0.1, max_value=0.4, value=0.2, step=0.1)
    fmt = f".{int(fmt * 10)}f"  # Format the annotation
    annot_size = st.sidebar.slider("Annotation Size", min_value=1, max_value=5, value=1, step=1)
    annot_color = st.sidebar.color_picker("Annotation Color", "#000000")
    linewidths = st.sidebar.slider("Line Widths", min_value=0.1, max_value=0.5, value=0.5)
    linecolor = st.sidebar.color_picker("Line Color", "#000000")
    cbar = st.sidebar.checkbox("Show Colorbar", value=True)
    cbar_kws = dict(use_gridspec=False, location="right")
    square = st.sidebar.checkbox("Square Heatmap", value=True)
    mask = st.sidebar.checkbox("Mask Upper Triangle", value=False)
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")
    
    st.sidebar.subheader("🖼️ Plot Size Customization")
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)
    figsize = (plot_width, plot_height)

    if st.sidebar.button("Generate Heatmap"):
        Create_Heatmap(df, cmap, annot, fmt, annot_size, annot_color, linewidths, linecolor, cbar, cbar_kws, square, mask, figsize)

        # Provide download link
        with open("heatmap.png", "rb") as file:
            st.download_button("Download Heatmap", file, file_name="Heatmap.png", mime="image/png")
   


#? ======================================== Correlation Matrix Generator ========================================

def create_corr_matrix(data, method, annot, fmt, linewidths, linecolor, cbar, cbar_kws, square, bg_color, figsize):
    plt.figure(figsize=figsize)
    plt.gca().set_facecolor(bg_color)
    sns.set(style="whitegrid")

    corr_matrix = data.corr(method=method)
    sns.heatmap(
        data=corr_matrix,
        annot=annot,
        fmt=fmt,
        linewidths=linewidths,
        linecolor=linecolor,
        cbar=cbar,
        cbar_kws=cbar_kws,
        square=square
    )

    plt.title(f'Correlation Matrix of the Data', fontsize=18, fontweight='bold', color="#444444")
    plt.xticks(fontsize=12, rotation=45, fontstyle='italic')
    plt.yticks(fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)

    st.pyplot(plt)
    plt.tight_layout()
    plt.savefig("corr_matrix.png")
    plt.clf()
    
def Correlation_Matrix_Generator(df):
    st.sidebar.subheader("📊 Correlation Matrix Customization")
    method = st.sidebar.selectbox("📊 Correlation Method", ["pearson", "kendall", "spearman"])
    annot = st.sidebar.checkbox("Show Annotations", value=True)
    fmt = st.sidebar.text_input("Annotation Format", value=".2f")
    linewidths = st.sidebar.slider("Line Widths", min_value=0.1, max_value=5.0, value=0.5)
    linecolor = st.sidebar.color_picker("Line Color", "#000000")
    cbar = st.sidebar.checkbox("Show Colorbar", value=True)
    cbar_kws = dict(use_gridspec=False, location="right")
    square = st.sidebar.checkbox("Square Heatmap", value=True)
    bg_color = st.sidebar.color_picker("Pick Background Color", "#f0f0f0")
    plot_width = st.sidebar.slider("Select plot width (in inches)", min_value=5, max_value=20, value=14, step=1)
    plot_height = st.sidebar.slider("Select plot height (in inches)", min_value=5, max_value=20, value=8, step=1)


    if st.sidebar.button("Generate Correlation Matrix"):
        create_corr_matrix(df, method, annot, fmt, linewidths, linecolor, cbar, cbar_kws, square, bg_color, (plot_width, plot_height))

        # Provide download link
        with open("corr_matrix.png", "rb") as file:
            st.download_button("Correlation Matrix", file, file_name="Correlation_Matrix.png", mime="image/png")
            
#? ======================================== Main Function ========================================

def main():
    st.title("📊 Plot Generator")
    st.sidebar.title("📊 Plot Generator")
    
    st.sidebar.subheader("📊 Select Plot type")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        
        st.sidebar.subheader("📊 Select Plot Type")
        plot_type = st.sidebar.selectbox("Select Plot Type", ["Box Plot", "Bar Plot", "Line Plot", "Scatter Plot", "Violin Plot", "Pair Plot", "Histogram Plot", "Pie Chart", "Heatmap", "Correlation Matrix"])
        
        if plot_type == "Box Plot":
            Box_Plot_Generator(df)
        elif plot_type == "Bar Plot":
            Bar_Plot_Generator(df)
        elif plot_type == "Line Plot":
            Line_Plot_Generator(df)
        elif plot_type == "Scatter Plot":
            Scatter_Plot_Generator(df)
        elif plot_type == "Violin Plot":
            Violin_Plot_Generator(df)
        elif plot_type == "Pair Plot":
            Pair_Plot_Generator(df)
        elif plot_type == "Histogram Plot":
            Histogram_Plot_Generator(df)
        elif plot_type == "Pie Chart":
            Pie_Chart_Generator(df)
        elif plot_type == "Heatmap":
            Heatmap_Generator(df)
        elif plot_type == "Correlation Matrix":
            Correlation_Matrix_Generator(df)
            
    else:
        st.info("Upload a CSV file to get started")
        
if __name__ == "__main__":
    main()
    
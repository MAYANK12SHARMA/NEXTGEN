import streamlit as st
import json
from streamlit_lottie import st_lottie
from Visualization.HelperFun import Axis_Limits, Column_filter, Column_Remover, load_lottie_file




def MainPageNavigation():
    
    with st.sidebar:
        # Apply the logo image
        st.image("./Visualization/Images/logo.png", width=200)
        

        # Navigation with selectbox
        st.sidebar.markdown("""
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
            <style>
                .dropdown {
                    position: relative;
                    display: inline-block;
                    margin-bottom: 10px;
                }
                
                .dropbtn {
                    background-color: #08ac24; /* Dark background */
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    display: inline-flex;
                    align-items: center;
                    width: 100%;
                }

                .arrow {
                    margin-left: 100px;
                    font-size: 20px;
                    
                }

                .dropbtn:hover {
                    background-color: #1a1b24; /* Slightly lighter on hover */
                }
                .custom {
                    color: black;
                    font-size: 20px;
                }
            </style>
            
            """, unsafe_allow_html=True)
            # <div class="dropdown">
            #     <a href="https://next-gen-model-d5a8gmgth2cdbcam.canadacentral-01.azurewebsites.net/" target="_blank">
            #         <button class="dropbtn">Go to Modelling <span class="arrow"><i class="fas fa-up-right-from-square custom"></i></span></button>
            #     </a>
            # </div>

                # Short description or instructions
        
        # Lottie Animation
        lottile_json = load_lottie_file("./Visualization/FilesJson/Navbar-Jif.json")
        st_lottie(lottile_json, speed=1, width=250, height=250, key="initial")



def MainPage():
    # Introduction Section
    Col1, col2 = st.columns([3,1])
    with Col1:    
        st.markdown("""
                    <style>
                        @font-face {
                            font-family: 'Algerian';
                            src: url('font-family\Algerian-Regular.ttf') format('truetype');
                        }

                        .centered , h2 {
                            text-align: center;
                            font-family: 'Algerian', sans-serif;
                            color: #00FFFF;
                            font-weight: 300;
                        }
                        
                        .justified {
                            text-align: justify;
                            font-family: Arial, sans-serif;
                        }
                        
                        
                    </style>

                    <div class="centered">
                        <h2>👋 <b>Introduction</b></h2>
                    </div>
                    
                    <div class="justified">
                        Welcome to the <b>Visualization Tool</b>, a powerful and easy-to-use platform designed for generating stunning data visualizations with just a few clicks! Whether you're a beginner or a seasoned data scientist, our tool offers intuitive interfaces and customizable options for every use case. <br><br>
                        From selecting chart types to generating clean, reusable Python code, you’ll find everything you need to create beautiful and insightful plots. This tool supports a variety of datasets and customization options, ensuring that your visualizations are both informative and visually appealing. <br><br>
                    </div>
                    """,
                    unsafe_allow_html=True
        )

    with col2:
        lottile_json = load_lottie_file("./Visualization/FilesJson/Animation.json")
        st_lottie(lottile_json, speed=1, width=300, height=250)

    # Divider
    st.markdown("---")
    # Features Section
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>🌟 <b>Features of the Visualization Tool</b></h2>
        </div>
        """,
        unsafe_allow_html=True
    )

        # Add the CSS styles for each section
    # Add the CSS styles for each section
    st.markdown(
        """
        <style>
        /* Title style */
        .title {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
        }

        /* Subtitle style */
        .subtitle {
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
            color: #4CAF50;  /* Optional color styling */
            margin-bottom: 10px;
        }

        /* Content style */
        .content {
            text-align: justify;
            font-size: 1.1em;
            line-height: 1.6;
            margin: 0 0;
            width: 100%;  /* Optional width styling to make the content narrower */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Section 1: User Interface Design (Input and Customization)
    with st.container():
        st.markdown(
            """
            <div class="subtitle">
                1. 🎨 User Interface Design (Input and Customization)
            </div>
            <div class="content">
                ✅ <b>Graph Type Selection</b>:  
                Choose from a variety of plot types, including scatter plots, bar plots, heatmaps, boxplots, etc.  
                Support for popular libraries like <b>Matplotlib</b>, <b>Seaborn</b>, and others.
                <br><br>
                📁 <b>Data Input</b>:  
                Upload datasets in <b>CSV, Excel</b>, or JSON format for easy processing and visualization.
                <br><br>
                🎨 <b>Customization Options</b>:  
                Customize the appearance of your plots—modify axes, colors, titles, labels, and legends with simple clicks.
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("---")

    # Section 3: Visualization Options (Real-time Plotting)
    with st.container():
        st.markdown(
        '''
        <div class="subtitle">
            2. 📊 Visualization Options (Real-time Plotting)
        </div>
        ''', unsafe_allow_html=True
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
        """
        <div class="content">
            👁️ <b>Live Preview</b>:  
            Your plots update in real-time as you adjust the settings.
            <br><br>
            🔄 <b>Combine Multiple Plots</b>:  
            Effortlessly merge several plots into one figure.
            <br><br>
            📤 <b>Export Plots</b>:  
            Export your visualizations in multiple formats like <b>PNG, SVG, PDF</b> with just one click.
        </div>
        """,
        unsafe_allow_html=True
    )
    with col2:
        lottile_json = load_lottie_file("./Visualization/FilesJson/Animation.json")
        st_lottie(lottile_json, speed=52, width=300, height=200)

    # Divider
    st.markdown("---")

    # Section 2: Dynamic Code Generation
    with st.container():
        st.markdown(
        """
        <div class="subtitle">
            3. 🛠️ Dynamic Code Generation
        </div>
        <div class="content">
            ⚙️ Automatically generate <b>clean, modular Python code</b> for your plots.
            <br><br>
            📝 <b>Well-commented and reusable</b> code snippets.
            <br><br>
            💾 <b>Save the Code</b>:  
            Save your generated code as a `.py` file for future use or modifications.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Divider
    st.markdown("---")

    # Section 4: Advanced Features
    with st.container():
        st.markdown(
        '''
        <div class="subtitle">
            4. 🚀 Advanced Features
        </div>
        ''', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
        """
        <div class="content">
            🧹 <b>Data Preprocessing</b>:  
            Normalize, filter, and group your data before visualizing.
            <br><br>
            📊 <b>Statistical Plots</b>:  
            Generate <b>correlation heatmaps, regression plots</b>, and more advanced charts.
            <br><br>
            🎨 <b>Templates & Themes</b>:  
            Select from pre-defined themes or create your own. Includes a sleek <b>dark mode</b> option.
            <br><br>
            🌐 <b>Interactive Plots</b>:  
            Use <b>Plotly</b> for highly interactive visualizations.
        </div>
        """,
        unsafe_allow_html=True
    )

    with col2:
        lottile_json = load_lottie_file("./Visualization/FilesJson/Animation2.json")
        st_lottie(lottile_json, speed=52, width=300, height=200)

    st.markdown("---")


    
    with st.container():
        st.markdown(
            '''
            <div class="subtitle">
                5. 📄 Document and Dataset Insights
            </div>
            ''', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
            """
            <div class="content">
                📑 <b>Upload Documents and Datasets</b>:  
                Upload PDFs or CSV files to extract insights.
                <br><br>
                🔍 <b>Ask Questions</b>:  
                Query your documents or datasets to get detailed answers and insights instantly.
                <br><br>
                📊 <b>Perform Analysis</b>:  
                Get deep analysis of your dataset with just a few clicks.
            </div>
            """,
            unsafe_allow_html=True
        )

      
    st.markdown("---")
    
      
        
    st.markdown(
        """
        <div class="title">
            ✨ Start exploring and creating beautiful visualizations today with NEXTGEN!
        </div>
        """,
        unsafe_allow_html=True
    )

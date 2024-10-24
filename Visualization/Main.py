import streamlit as st
from streamlit_option_menu import option_menu
from Home import MainPage, MainPageNavigation
import json
from streamlit_lottie import st_lottie
from PlotWizard import PlotWizard

#? ================================== Additional part  ==================================================
 
st.set_page_config(page_title="Visualization Tool", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .css-18e3th9 {
        padding-top: 0 !important;
    }
    .css-1d391kg {
        padding-top: 0 !important;
    }
    .st-emotion-cache-13ln4jf{
        padding-top: 0 !important;
    }
    .st-emotion-cache-1jicfl2{
        padding-top: 1rem !important;
    }
    .st-emotion-cache-kgpedg{
        padding: 0 !important;
    }
    # header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def load_lottie_file(file_path: str):
    with open(file_path, "r") as f:
        lottie_json = json.load(f)
        return lottie_json


#? =============================== Navbar ================================== 
def top_nav_menu():
    selected = option_menu(
        menu_title=None,  # No title for the horizontal menu
        options=["Home", "PlotWizard", "AutoCode"],  # menu options
        icons=["house", "person", "gear"],  # icons for each option
        menu_icon="cast",  # optional menu icon
        default_index=0,  # default selected option
        orientation="horizontal",  # horizontal navigation bar at the top
        styles={
            "container": {
                "padding": "0", "margin": "0",
                "width": "100%",  # Set navbar width to 100% of the page
                "height": "40px",  # Set navbar height
                "top": "0", "position": "sticky", "z-index": "999",
            },
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#eee"},
            "icon": {"color": "orange", "font-size": "20px","padding-bottom": "2px"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )
    return selected

#! ============================================= Pages =============================================


#? ====================================== Plot Generator Page {PlotWizard} ================================== 




#? ========================================= Code Generation Page ================================== 



def settings_page():
    st.title("Settings Page")
    st.write("You can change your settings here.")

    # Sidebar content for the Settings page
    st.sidebar.header("Settings Sidebar")
    st.sidebar.write("This is the sidebar for the Settings page.")
    st.sidebar.selectbox("Choose a setting", ["Option 1", "Option 2", "Option 3"])


def main():
    st.write("<h1 style='text-align: center;'>Plots Generator</h1>", unsafe_allow_html=True)
    
    selected = top_nav_menu()  

    # Route to different pages based on user selection
    if selected == "Home":
        MainPageNavigation()   
        MainPage()
 
    elif selected == "PlotWizard":
        PlotWizard()
        
    elif selected == "AutoCode":
        settings_page()  # Settings page with Settings sidebar

# Run the main function
if __name__ == "__main__":
    main()

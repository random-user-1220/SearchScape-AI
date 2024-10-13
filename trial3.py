import streamlit as st

# Set the page configuration for a full-width layout
st.set_page_config(
    page_title="Streamlit with Background Animation",
    layout="wide",
)

# Add CSS for background animation
st.markdown(
    """
    <style>
    /* Full page gradient animation */
    body {
        background: linear-gradient(45deg, #ff9a9e, #fad0c4, #fad0c4);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Customize the main content's appearance */
    .stApp {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Customize header appearance */
    h1 {
        color: #4A90E2;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    </style>
    """, unsafe_allow_html=True
)

# Main content of the app
st.title("🌈 Welcome to the Animated Streamlit App")
st.write("""
### This Streamlit app features a background with animated gradient colors.
The animation continuously cycles through different color combinations, making the app visually dynamic.
""")

# Display columns for layout demonstration
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://via.placeholder.com/150", caption="Image 1", width=150)

with col2:
    st.image("https://via.placeholder.com/150", caption="Image 2", width=150)

with col3:
    st.image("https://via.placeholder.com/150", caption="Image 3", width=150)

st.write("Enjoy this subtle, pleasing background animation!")
797ae65a8687aa0cd78a4205d099f89af0f6ed00fd37cffca2693396c336a432 # Replace with your actual SerpAPI key

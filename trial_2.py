import requests
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image as PILImage
from io import BytesIO

# Load pre-trained BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Function to generate caption from image URL
def image_url_to_text(image_url):
    # Fetch the image from the URL
    response = requests.get(image_url)
    image = PILImage.open(BytesIO(response.content)).convert("RGB")

    # Preprocess the image and generate a caption
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)

    # Decode the generated caption
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# Function to interact with RapidAPI for web search
def search_rapidapi(query):
    url = "https://real-time-web-search.p.rapidapi.com/search"
    
    params = {
        "q": query,  # Dynamic query
        "limit": "10"  # Limit the number of results
    }

    headers = {
        "X-RapidAPI-Key": "a3d05b6a5amshe73e895247874bep1a154ejsn539371c789bf",  # Replace with your actual API key
        "X-RapidAPI-Host": "real-time-web-search.p.rapidapi.com"
    }

    try:
        # Send GET request to API with query parameters
        response = requests.get(url, headers=headers, params=params)

        # Check for a successful response
        if response.status_code == 200:
            search_results = response.json()

            # Process and extract the search results
            if "data" in search_results:
                web_results = []
                for result in search_results["data"][:10]:
                    title = result.get("title", "No title available")
                    snippet = result.get("snippet", "No description available")
                    link = result.get("url", "No URL available")
                    web_results.append((title, snippet, link))
                return web_results
            else:
                print("No 'data' key found in the response.")
                return []
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Streamlit app with enhanced UI
def main():
    # Set background colors for the sidebar and main content
    st.markdown(
        """
        <style>
            .main {
                background-color: #f7f9fc;  /* Light color for the main content */
            }
            .sidebar .sidebar-content {
                background-color: #dbe2ef;  /* Softer aesthetic color for the sidebar */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App title with enhanced styling and background design
    st.markdown("""
        <div style="background-color: #3f72af; padding: 20px; border-radius: 10px;">
            <h1 style='text-align: center; color: white;'>GOOGLE LENS PRO MAX</h1>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar for user inputs
    st.sidebar.markdown("## Enter Details")
    image_url = st.sidebar.text_input("Enter the image URL:")
    user_prompt = st.sidebar.text_input("Enter your search prompt:")

    # Add design elements below the "Enter your search prompt"
    st.sidebar.markdown("""
        <div style="padding: 10px; text-align: center;">
            <p style="color: #003366; font-weight: bold;">🌐 Searching has never been easier!</p>
            <p style="color: #003366; font-size: 16px; font-weight: bold;">Enter your prompt, sit back, and explore the web like never before!</p>
        </div>
        """, unsafe_allow_html=True)

    # Display the main content in columns
    col1, col2 = st.columns([1, 2])

    if image_url and user_prompt:
        with col1:
            st.markdown("### Input Image")
            st.image(image_url, caption="Image from URL", use_column_width=True)

        with col2:
            # Generate caption from the image
            caption = image_url_to_text(image_url)
            st.markdown("<h3 style='color: darkgreen;'>Generated Caption:</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 18px;'>{caption}</p>", unsafe_allow_html=True)

            # Combine user prompt with the generated caption
            combined_query = f"{user_prompt} given an image of {caption}"
            st.markdown("<h3 style='color: darkgreen;'>Combined Search Query:</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 18px;'>{combined_query}</p>", unsafe_allow_html=True)

        # Horizontal line separator
        st.markdown("<hr>", unsafe_allow_html=True)

        # Toggle button state with immediate switch between web and image search
        if 'search_mode' not in st.session_state:
            st.session_state.search_mode = 'web'

        # Center the button using HTML
        button_html = """
        <style>
            .center-btn {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
        <div class="center-btn">
        """

        # Toggle search mode directly with a single click
        if st.session_state.search_mode == 'web':
            if st.button("Generate Websites"):
                st.session_state.search_mode = 'images'  # Switch to image search after web results
                st.markdown("<h2 style='text-align: center; color: darkblue;'>Web Results</h2>", unsafe_allow_html=True)
                web_results = search_rapidapi(combined_query)
                if web_results:
                    for title, snippet, link in web_results:
                        st.markdown(f"**[{title}]({link})**")
                        st.write(f"{snippet}")
                        st.markdown("---")
                else:
                    st.error("No web results found.")
        else:
            if st.button("Generate Images"):
                st.session_state.search_mode = 'web'  # Switch back to web search after image results
                # Image search not included as per RapidAPI; only web search functionality implemented here

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer with additional styling
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit and RapidAPI</p>", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()

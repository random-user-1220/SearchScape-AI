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

# Updated function to interact with SerpAPI and return image and web results
def search_serpapi_images(query):
    SERPAPI_KEY = "797ae65a8687aa0cd78a4205d099f89af0f6ed00fd37cffca2693396c336a432"  # Replace with your actual SerpAPI key
    url = "https://serpapi.com/search"

    # Parameters for DuckDuckGo search query
    params = {
                "engine": "duckduckgo",  # Use DuckDuckGo as the search engine
        "q": query,  # Replace with your search query
        "num": 10,  # Number of results to return (for websites)
        "tbm": "isch",  # Use "isch" to get image search results
        "api_key": SERPAPI_KEY  # Your SerpAPI key
    }

    try:
        # Send the GET request to SerpAPI
        response = requests.get(url, params=params)

        # Check for a successful response
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and limit image results to 10
            image_results = data.get('inline_images', [])[:10]
            image_urls = []

            if image_results:
                print("Image Search Results:")
                for idx, result in enumerate(image_results):
                    print(f"\nImage Result {idx + 1}")
                    print(f"Image URL: {result.get('thumbnail')}")
                    image_urls.append(result.get('thumbnail'))
            else:
                print("No images found.")

            # Extract and limit web results to 10
            web_results = data.get('organic_results', [])[:10]
            web_urls = []

            if web_results:
                print("\nWebsite Search Results:")
                for idx, result in enumerate(web_results):
                    print(f"\nWebsite Result {idx + 1}")
                    print(f"Website URL: {result.get('link')}")
                    web_urls.append(result.get('link'))
            else:
                print("No websites found.")

            return {"images": image_urls, "websites": web_urls}

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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
                web_results = search_serpapi_images(combined_query)
                if web_results:
                    for result in web_results.get('websites', []):
                        st.markdown(f"**[{result}]**")
                        st.markdown("---")
                else:
                    st.error("No web results found.")
        else:
            if st.button("Generate Images"):
                st.session_state.search_mode = 'web'  # Switch back to web search after image results
                st.markdown("<h2 style='text-align: center; color: darkblue;'>Image Results</h2>", unsafe_allow_html=True)
                image_results = search_serpapi_images(combined_query)
                if image_results:
                    for image_url in image_results.get('images', []):
                        st.image(image_url, caption="Search Result", use_column_width=True)
                else:
                    st.warning("No image results found.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer with additional styling
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit and SerpAPI</p>", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()

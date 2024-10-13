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

# Function to perform web search using DuckDuckGo
def search_duckduckgo(query):
    url = "https://duckduckgo8.p.rapidapi.com/"
    headers = {
        "x-rapidapi-host": "duckduckgo8.p.rapidapi.com",
        "x-rapidapi-key": "a90b889914msh1eaee86181b76bfp1ec035jsn04dbb53f7d2f",  # Replace with your actual API key
    }
    params = {
        "q": query,
        "format": "json"
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        results = response.json()
        return results.get('results', [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Function to perform image search using DuckDuckGo
def search_duckduckgo_images(query):
    url = "https://duckduckgo-image-search.p.rapidapi.com/search/image"
    headers = {
        "x-rapidapi-host": "duckduckgo-image-search.p.rapidapi.com",
        "x-rapidapi-key": "a90b889914msh1eaee86181b76bfp1ec035jsn04dbb53f7d2f",  # Replace with your actual API key
    }
    params = {
        "q": query,
        "format": "json",
        "max_results": 10  # This limits the number of results to 10
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        results = response.json()
        # Explicitly limit the results to 10, in case the API returns more than that
        return results.get('results', [])[:10]  # Limit to first 10 results
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Streamlit app with enhanced UI
def main():
    # Set background colors for the sidebar and main content
    st.markdown(
        """
        <style>
            .main {
                background-color: #f7f9fc;
            }
            .sidebar .sidebar-content {
                background-color: #dbe2ef;
            }
        </style>
        """, unsafe_allow_html=True,
    )

    # App title with enhanced styling
    st.markdown("""
        <div style="background-color: #3f72af; padding: 20px; border-radius: 10px;">
            <h1 style='text-align: center; color: white;'>GOOGLE LENS PRO MAX</h1>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar for user inputs
    st.sidebar.markdown("## Enter Details")
    image_url = st.sidebar.text_input("Enter the image URL:")
    user_prompt = st.sidebar.text_input("Enter your search prompt:")

    # Sidebar with a message
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
            combined_query = f"{user_prompt} ,given an image of  {caption}"
            st.markdown("<h3 style='color: darkgreen;'>Combined Search Query:</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 18px;'>{combined_query}</p>", unsafe_allow_html=True)
            query=f"{user_prompt},context= {caption}"
        # Horizontal line separator
        st.markdown("<hr>", unsafe_allow_html=True)

        # Perform web search
        if st.button("Generate Web Results"):
            st.markdown("<h2 style='text-align: center; color: darkblue;'>Web Results</h2>", unsafe_allow_html=True)
            web_results = search_duckduckgo(combined_query)
            if web_results:
                for result in web_results:
                    title = result.get("title", "No title available")
                    snippet = result.get("description", "No description available")
                    link = result.get("url", "No URL available")
                    st.markdown(f"**[{title}]({link})**")
                    st.write(f"{snippet}")
                    st.markdown("---")
            else:
                st.error("No web results found.")

        # Perform image search
        if st.button("Generate Image Results"):
            st.markdown("<h2 style='text-align: center; color: darkblue;'>Image Results</h2>", unsafe_allow_html=True)
            image_results = search_duckduckgo_images(query)
            if image_results:
                for image in image_results:
                    title = image.get('title', 'No title available')
                    image_url = image.get('image', '')
                    st.image(image_url, caption=title, use_column_width=True)
                    st.markdown("---")
            else:
                st.error("No image results found.")

    # Footer with additional styling
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit and RapidAPI</p>", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()

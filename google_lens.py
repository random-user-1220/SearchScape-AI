import requests
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from sentence_transformers import SentenceTransformer
import numpy as np
from PIL import Image as PILImage
from io import BytesIO

# Load pre-trained BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load the keyword extraction model
keyword_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to generate caption from image
def image_to_text(image):
    # Preprocess the image and generate a caption
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    # Decode the generated caption
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# Function to extract keywords from a text
def extract_keywords(text,x):
    words = text.split()
    text_embedding = keyword_model.encode([text])[0]
    word_embeddings = keyword_model.encode(words)
    
    keyword_scores = {}
    for word, word_embedding in zip(words, word_embeddings):
        cosine_similarity = np.dot(text_embedding, word_embedding) / (np.linalg.norm(text_embedding) * np.linalg.norm(word_embedding))
        keyword_scores[word] = cosine_similarity

    sorted_keywords = sorted(keyword_scores.items(), key=lambda item: item[1], reverse=True)
    return [keyword for keyword, score in sorted_keywords[:max(3, x)]]  # Return top keywords

# Function to perform web search using DuckDuckGo
def search_duckduckgo(query):
    url = "https://duckduckgo8.p.rapidapi.com/"
    headers = {
        "x-rapidapi-host": "duckduckgo8.p.rapidapi.com",
        "x-rapidapi-key": "a90b889914msh1eaee86181b76bfp1ec035jsn04dbb53f7d2f",  # Replace with your actual API key
    }
    params = {"q": query, "format": "json"}

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
        "x-rapidapi-key": "d41da8ab71msh2ff75deecd8f2a7p1ba445jsn11fe2bb464f9",  # Replace with your actual API key
    }
    params = {"q": query, "format": "json", "max_results": 10}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        results = response.json()
        return results.get('results', [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []
def sort_results_by_keywords(results, keywords):
    sorted_results = []
    for keyword in keywords:
        for result in results:
            title = result.get("title", "").lower()
            description = result.get("description", "").lower()
            if keyword.lower() in title or keyword.lower() in description:
                sorted_results.append(result)
    return sorted_results
# Sort results based on keywords for images
def sort_image_results_by_keywords(results, user_keywords):
    # filtered_results = []

    # # Step 1: Filter results that match **any one** caption keyword
    # for result in results:
    #     title = result.get("title", "").lower()
    #     description = result.get("description", "").lower()
    #     title_description = title + " " + description
    #     if any(keyword.lower() in title_description for keyword in caption_keywords):  # Match any keyword
    #         filtered_results.append(result)

    # Step 2: Sort the filtered results based on user keywords
    sorted_results = []
    for keyword in user_keywords:
        for result in results:
            title = result.get("title", "").lower()
            description = result.get("description", "").lower()
            if keyword.lower() in title or keyword.lower() in description:
                sorted_results.append(result)

    # Step 3: Add remaining filtered results that do not match user keywords, to retain all relevant results
    remaining_results = [result for result in results if result not in sorted_results]
    sorted_results.extend(remaining_results)

    return sorted_results

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
            <h1 style='text-align: center; color: white;'>SearchScape AI</h1>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar for user inputs
    st.sidebar.markdown("## Enter Details")
    
    # Option to enter an image URL or upload a file
    image_url = st.sidebar.text_input("Enter the image URL:")
    uploaded_file = st.sidebar.file_uploader("Or upload an image:", type=["png", "jpg", "jpeg"])

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

    image = None
    if image_url:
        # Fetch the image from the URL
        response = requests.get(image_url)
        image = PILImage.open(BytesIO(response.content)).convert("RGB")

    if uploaded_file:
        # Load the uploaded image
        image = PILImage.open(uploaded_file).convert("RGB")

    if image and user_prompt:
        with col1:
            st.markdown("### Input Image")
            st.image(image, caption="Uploaded Image", use_column_width=True)

        with col2:
            # Generate caption from the image
            caption = image_to_text(image)
            st.markdown("<h3 style='color: darkgreen;'>Generated Caption:</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 18px;'>{caption}</p>", unsafe_allow_html=True)

            # Combine user prompt with the generated caption
            if "show me" not in user_prompt.lower() and "give me" not in user_prompt.lower():
                user_prompt = f"show me {user_prompt.lower()}"
            combined_query = f"{user_prompt}, given an image of {caption}"
            st.markdown("<h3 style='color: darkgreen;'>Combined Search Query:</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 18px;'>{combined_query}</p>", unsafe_allow_html=True)
            query=f"{user_prompt} ,context= {caption}"
            # Extract keywords from the user prompt and caption
            user_keywords = extract_keywords(user_prompt,int(len(user_prompt.split()) / 5))
            caption_keywords = extract_keywords(caption,len(caption.split()))

        # Horizontal line separator
        st.markdown("<hr>", unsafe_allow_html=True)

        # Perform web search
        if st.button("Generate Web Results"):
            st.markdown("<h2 style='text-align: center; color: darkblue;'>Web Results</h2>", unsafe_allow_html=True)
            web_results = search_duckduckgo(combined_query)
            if web_results:
                sorted_web_results = sort_results_by_keywords(web_results, user_keywords)
                if sorted_web_results:
                    for result in sorted_web_results:
                        title = result.get("title", "No title available")
                        snippet = result.get("description", "No description available")
                        link = result.get("url", "No URL available")
                        st.markdown(f"**[{title}]({link})**")
                        st.write(f"{snippet}")
                        st.markdown("---")
                else:
                    st.warning("No web results found matching the keywords.")
            else:
                st.error("No web results found.")

        # Perform image search
        if st.button("Generate Image Results"):
            st.markdown("<h2 style='text-align: center; color: darkblue;'>Image Results</h2>", unsafe_allow_html=True)
            image_results = search_duckduckgo_images(query)
            if image_results:
                sorted_image_results = sort_image_results_by_keywords(image_results, user_keywords)
                if sorted_image_results:
                    for image in sorted_image_results[:15]:
                        title = image.get('title', 'No title available')
                        image_url = image.get('image', '')
                        st.image(image_url, caption=title, use_column_width=True)
                        st.markdown("---")
                else:
                    st.warning("No image results found matching the keywords.")
            else:
                st.error("No image results found.")

    # Footer with additional styling
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit and RapidAPI</p>", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()

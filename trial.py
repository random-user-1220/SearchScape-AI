import requests
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from io import BytesIO

# Load pre-trained BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Function to generate caption from image URL
def image_url_to_text(image_url):
    # Fetch the image from the URL
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGB")

    # Preprocess the image and generate a caption
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    
    # Decode the generated caption
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# Function to interact with SerpAPI
def search_serpapi(query):
    # Your SerpAPI key
    api_key = "797ae65a8687aa0cd78a4205d099f89af0f6ed00fd37cffca2693396c336a432"  # Replace with your actual SerpAPI key

    # Set up the endpoint and parameters
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": api_key
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()

        # Extract the web results
        web_results = data.get('organic_results', [])
        image_results = data.get('images_results', [])

        return web_results, image_results
    else:
        return None, None

# Streamlit UI
def main():
    # Title of the app
    st.title("BLIP Image Captioning & SerpAPI Search")

    # Get user input for image URL and search query
    image_url = st.text_input("Enter the image URL:")
    user_prompt = st.text_input("Enter your search prompt:")

    if image_url and user_prompt:
        # Generate caption from the image
        caption = image_url_to_text(image_url)
        st.subheader("Generated Caption:")
        st.write(caption)

        # Combine user prompt with the generated caption
        combined_query = f"{user_prompt} {caption}"
        st.subheader("Combined Search Query:")
        st.write(combined_query)

        # Perform search using SerpAPI
        web_results, image_results = search_serpapi(combined_query)

        # Display search results
        if web_results:
            st.subheader("Web Results")
            for result in web_results:
                st.write(f"**{result.get('title')}**")
                st.write(f"[{result.get('link')}]({result.get('link')})")
                st.write(result.get('snippet', 'No description available'))
                st.markdown("---")
        else:
            st.error("No web results found.")

        # Display images (if available)
        if image_results:
            st.subheader("Image Results")
            for image in image_results[:5]:  # Limit to first 5 images
                image_url = image.get('original')
                try:
                    # Display the image
                    img_data = requests.get(image_url).content
                    img = Image.open(BytesIO(img_data))
                    st.image(img, caption=f"Image from {image.get('source')}", use_column_width=True)
                except Exception as e:
                    st.warning(f"Failed to load image: {e}")
        else:
            st.warning("No image results found.")
    
# Run the Streamlit app
if __name__ == "__main__":
    main()

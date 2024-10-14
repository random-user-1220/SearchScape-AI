# SearchScape AI: Enhanced Web & Image Search

**SearchScape AI** is a Streamlit-based web application that combines the power of image captioning and web search capabilities to help users explore the web like never before. By uploading an image or entering a search prompt, the application generates relevant captions for images and uses them to perform both web and image searches.

---

## Features

- **Image Captioning**: Upload an image via URL, and the app will generate a meaningful caption using the BLIP (Bootstrapping Language-Image Pretraining) model.
- **Web Search**: Based on the generated caption and user-provided search prompt, the app performs a DuckDuckGo search to find relevant web results.
- **Image Search**: Additionally, the app uses DuckDuckGo Image Search API to fetch images related to the search query.

---

## Tech Stack

The following technologies and libraries are used in this project:

- **Streamlit**: A fast, easy-to-use framework for building interactive web applications with Python.
- **Transformers**: Hugging Face’s library for state-of-the-art natural language processing (NLP) models, used here for the BLIP model to generate captions from images.
- **Torch**: PyTorch is used to run the deep learning models (BLIP in this case).
- **DuckDuckGo API (From RapidApi)**: Provides web and image search capabilities.
- **Pillow (PIL)**: Python Imaging Library for handling image processing tasks such as resizing, cropping, etc.
- **Requests**: For making HTTP requests to external APIs like DuckDuckGo.

---

## Prerequisites

Before running the app, make sure you have the following dependencies installed:

1. **Python** (preferably 3.7+)
2. **Streamlit**: For building the interactive web app.
3. **Transformers**: For using the pre-trained BLIP model for image captioning.
4. **Pillow (PIL)**: For handling images.
5. **Requests**: For making API calls.

---

### Install Dependencies

To install the required dependencies, you can use the `requirements.txt` file provided in the repository.

Run the following command to install the dependencies:

```bash
pip install -r requirements.txt


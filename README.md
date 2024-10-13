# inter_iit
# Google Lens Pro Max: Enhanced Web & Image Search

**GOOGLE LENS PRO MAX** is a Streamlit-based web application that combines the power of image captioning and web search capabilities to help users explore the web like never before. By uploading an image or entering a search prompt, the application generates relevant captions for images and uses them to perform both web and image searches.

## Features
- **Image Captioning**: Upload an image via URL, and the app will generate a meaningful caption using the BLIP (Bootstrapping Language-Image Pretraining) model.
- **Web Search**: Based on the generated caption and user-provided search prompt, the app performs a DuckDuckGo search to find relevant web results.
- **Image Search**: Additionally, the app uses DuckDuckGo Image Search API to fetch images related to the search query.

## Prerequisites

Before running the app, make sure you have the following dependencies installed:

1. Python (preferably 3.7+)
2. [Streamlit](https://streamlit.io/)
3. [Transformers](https://huggingface.co/transformers/)
4. [PIL (Pillow)](https://pillow.readthedocs.io/en/stable/)
5. [requests](https://docs.python-requests.org/en/master/)

### Install dependencies

To install the required dependencies, run the following command:

```bash
pip install streamlit transformers pillow requests

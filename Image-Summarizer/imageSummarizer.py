import streamlit as st
import google.generativeai as genai
from PIL import Image
import logging

logging.basicConfig(level=logging.ERROR)

# Configure the Gemini API (you'll need to set up your API key)
try:
    GOOGLE_API_KEY=st.secrets["API_KEY"]
except:
    st.error("API_KEY is not set in the environment variables. Please set it and restart the application.")
    st.stop()

if not GOOGLE_API_KEY:
    raise ValueError("API_KEY not found in environment variables")
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model setup
gemini_model = genai.GenerativeModel('models/gemini-1.5-pro')
embedding_model = 'models/embedding-001'

def get_image_details(image_path):
    """Fetch details about the image."""
    try:
        prompt = f"""
        Analyze the following image. 

        Generate a summary of the image, breaking it down into the following sections:
        1. Make the explaination like a blog with a main tile and sub headings,
        2. Overview: Provide a brief overview of the Image's main topic and purpose.
        3. Detailed Summary: Expand on the key points, providing more context and explanation.
        4. Conclusion: Summarize the main takeaways or conclusions from the document.
        5. Key Points: List the main components or arguments presented in the image.
        Please format the summary in a clear, structured manner.
        """
        image = Image.open(image_path)
        response = gemini_model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        logging.error(f"Error processing image {image_path}: {e}")
        return None


def main():
    st.title("Image Summarizer")
    image = st.file_uploader("Upload PDF File", type=['png','jpg','jpeg'])
    with st.spinner("Generating summary..."):
        if image is not None:
            print(image)
            details = get_image_details(image)
        if details:
            st.subheader("Here is a summary of the Image")
            st.markdown(f"```\n{details}\n```")
        else:
            st.warning("Failed to generate summary. Please try again or adjust your input.")

if __name__ == "__main__":
    main()

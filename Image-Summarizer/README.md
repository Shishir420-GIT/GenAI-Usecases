## 1. Image Summarizer

Located in the `Image-Summarizer` folder, this application gets the summary of any image instantly.

### Features
- Image upload functionality
- AI-powered image analysis
- Providing description of the image

## Dependencies
- Python 3.7+
- Streamlit
- Pillow (PIL)
- google.generativeai

## Installation
1. Clone this repository:
  ```git
  git clone https://github.com/yourusername/GenAI-Usecases.git
  cd Image-Summarizer
  ```

2. Install the required packages:
  ```python
  pip install streamlit pillow google.generativeai
  ```

## Configuration

1. Set up gemini API key:
- Create a `.streamlit/secrets.toml` file in the project directory
- Add your API key:
  ```toml
  API_KEY = "your_api_key_id"
  ```
- Do not commit this file to version control

2. Ensure you have project created in Google Cloud with valid billing.


## Usage

1. Run the Streamlit app:
   ```cmd
    streamlit run imageSummarizer.py
   ```
2. Open the provided URL in your web browser.

3. Upload an image and click "Generating summary" to analyze the image.

4. Review the summary generated for you by AI.


## Deployment

- For Streamlit Cloud deployment, add your Gemini API Key in the Streamlit Cloud dashboard under the "Secrets" section.
- For other deployment options, ensure to set the  Gemini API Key as environment variables securely.

## Notes

- This application uses Gemini API Key Bedrock, which may incur costs. Please review Gemini pricing before extended use.
- Ensure your Google cloud project is created properly and is attached to a Billing.


# Image Caption Generator

This Streamlit application allows users to upload an image and create an HTML page using AWS Bedrock and Claude 3 Sonnet AI model.

## Features

- Image upload functionality
- AI-powered image analysis and HTML generation
- Option to regenerate HTML and Preview it

## Dependencies

- Python 3.7+
- Streamlit
- Pillow (PIL)
- Boto3

## Installation

1. Clone this repository:
git clone https://github.com/yourusername/GenAI-Usecases.git
cd '<Choice of folder>'

2. Install the required packages:
pip install streamlit pillow boto3

## Configuration

1. Set up AWS credentials:
- Create a `.streamlit/secrets.toml` file in the project directory
- Add your AWS credentials:
  ```toml
  AWS_ACCESS_KEY_ID = "your_access_key_id"
  AWS_SECRET_ACCESS_KEY = "your_secret_access_key"
  ```
- Do not commit this file to version control

2. Ensure you have access to AWS Bedrock and the Claude 3 Sonnet model in your AWS account.

## Usage

1. Run the Streamlit app:
streamlit run app.py

2. Open the provided URL in your web browser.

3. Upload an image and click "Extract Menu Content" to analyze the image.

4. Review the content generated and click "Generate HTML" to create HTML.

5. Preview and download your HTML file.

## Deployment

- For Streamlit Cloud deployment, add your AWS credentials in the Streamlit Cloud dashboard under the "Secrets" section.
- For other deployment options, ensure to set the AWS credentials as environment variables securely.

## Notes

- This application uses AWS Bedrock, which may incur costs. Please review AWS pricing before extended use.
- Ensure your AWS credentials have the necessary permissions to access Bedrock services.
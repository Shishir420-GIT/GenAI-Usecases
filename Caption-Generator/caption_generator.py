import boto3
from PIL import Image
import streamlit as st
from botocore.exceptions import ClientError

# Set up AWS Bedrock client
def get_bedrock_client():
    try:
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1',  # Replace with your region
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
        )
        return bedrock
    except ClientError as e:
        st.error(f"Error creating Bedrock client: {e}")
        return None

# Function to analyze image and generate caption
def analyze_image_and_generate_caption_old(image_bytes, bedrock_client):
    try:
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "prompt": "Analyze this image and generate a creative caption for it:",
                "image": base64.b64encode(image_bytes).decode('utf-8'),
                "max_tokens": 100
            })
        )
        return json.loads(response['body'].read())['completion']
    except ClientError as e:
        st.error(f"Error invoking Bedrock model: {e}")
        return None

def analyze_image_and_generate_caption(image_bytes, bedrock_client):
    try:
        # Encode the image
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Construct the prompt with the image
        prompt = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image
                        }
                    },
                    {
                        "type": "text",
                        "text": "Analyze this image and generate a creative caption for it."
                    }
                ]
            }
        ]

        # Invoke the model
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": prompt
            })
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    except ClientError as e:
        st.error(f"Error invoking Bedrock model: {e}")
        return None

# Streamlit app
def main():
    st.title("Image Caption Generator")

    # Initialize session state for storing the current caption
    if 'current_caption' not in st.session_state:
        st.session_state.current_caption = ""

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Get Bedrock client
        bedrock_client = get_bedrock_client()

        if bedrock_client:
            # Button to generate/regenerate caption
            if st.button("Generate Caption"):
                with st.spinner("Analyzing image and generating caption..."):
                    image_bytes = uploaded_file.getvalue()
                    caption = analyze_image_and_generate_caption(image_bytes, bedrock_client)
                    if caption:
                        st.session_state.current_caption = caption

            # Display the current caption
            if st.session_state.current_caption:
                st.subheader("Generated Caption:")
                st.write(st.session_state.current_caption)

if __name__ == "__main__":
    main()
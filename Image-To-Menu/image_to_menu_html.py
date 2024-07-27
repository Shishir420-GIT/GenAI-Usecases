import json
import boto3
import base64
import streamlit as st
from PIL import Image
from botocore.exceptions import ClientError

def get_bedrock_client():
    try:
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1',
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
        )
        return bedrock
    except ClientError as e:
        st.error(f"Error creating Bedrock client: {e}")
        return None

def extract_menu_content(image_bytes, bedrock_client):
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
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
                        "text": "You are en expert Image analyzer, please extract and list the menu items and their price from this image. Format the output."
                    }
                ]
            }
        ]

        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": prompt
            })
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    except ClientError as e:
        st.error(f"Error invoking Bedrock model: {e}")
        return None

def generate_html_with_css(menu_content, bedrock_client):
    try:
        prompt = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create an HTML file with embedded CSS for the following menu content. Make it visually appealing and responsive:\n\n{menu_content}"
                    }
                ]
            }
        ]

        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "messages": prompt
            })
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    except ClientError as e:
        st.error(f"Error invoking Bedrock model: {e}")
        return None

def main():
    st.title("Menu Card to HTML Converter")

    if 'menu_content' not in st.session_state:
        st.session_state.menu_content = ""
    if 'html_content' not in st.session_state:
        st.session_state.html_content = ""

    uploaded_file = st.file_uploader("Choose a menu card image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Menu Card', use_column_width=True)

        bedrock_client = get_bedrock_client()

        if bedrock_client:
            if st.button("Extract Menu Content"):
                with st.spinner("Extracting menu content..."):
                    image_bytes = uploaded_file.getvalue()
                    menu_content = extract_menu_content(image_bytes, bedrock_client)
                    if menu_content:
                        st.session_state.menu_content = menu_content

            if st.session_state.menu_content:
                st.subheader("Extracted Menu Content:")
                st.write(st.session_state.menu_content)

                if st.button("Generate HTML"):
                    with st.spinner("Generating HTML with CSS..."):
                        html_content = generate_html_with_css(st.session_state.menu_content, bedrock_client)
                        if html_content:
                            st.session_state.html_content = html_content

            if st.session_state.html_content:
                st.subheader("Generated HTML:")
                st.code(st.session_state.html_content, language="html")

                # Create a download button for the HTML file
                b64 = base64.b64encode(st.session_state.html_content.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" download="menu.html">Download HTML file</a>'
                st.markdown(href, unsafe_allow_html=True)

                # Preview HTML
                if st.button("Preview HTML"):
                    st.components.v1.html(st.session_state.html_content, height=600)

if __name__ == "__main__":
    main()
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from ollama import chat, ChatResponse

st.set_page_config(page_title="YouTube Transcript Summarizer", layout="centered")

st.title("🎬 YouTube Transcript Summarizer with Ollama")
st.write("Paste a YouTube video URL to generate a summary using the DeepSeek model.")

# Input field for YouTube URL
url = st.text_input("📥 Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=Hm0DZtiKUI8")

if st.button("🔍 Summarize"):
    if "watch?v=" not in url:
        st.error("Please enter a valid YouTube URL.")
    else:
        try:
            video_id = url.split("watch?v=")[1].split("&")[0]
            st.info(f"Extracted Video ID: `{video_id}`")

            # Fetch transcript
            fetched_transcript = YouTubeTranscriptApi.get_transcript(video_id)
            all_transcript = " ".join([snippet["text"] for snippet in fetched_transcript])

            st.subheader("📝 Transcript (truncated):")
            st.text(all_transcript[:1000] + "..." if len(all_transcript) > 1000 else all_transcript)

            # Ask Ollama to summarize
            with st.spinner("Summarizing using deepseek-r1:1.5b model..."):
                response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=[
                    {
                        'role': 'user',
                        'content': f'Summarise the below content: \n {all_transcript}',
                    },
                ])
                summary = response.message.content

            st.subheader("📄 AI Summary:")
            st.success(summary)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

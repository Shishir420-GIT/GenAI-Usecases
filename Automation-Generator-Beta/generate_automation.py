import PyPDF2
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API (you'll need to set up your API key)
genai.configure(api_key=st.secrets["API_KEY"])

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to generate summary using Gemini
def gemini_summarize(text, domain, extra_info):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Analyze the following text from a PDF document related to the {domain} domain. 
    Additional context: {extra_info}

    Generate a summary of the document, breaking it down into the following sections:
    1. Overview: Provide a brief overview of the document's main topic and purpose.
    2. Key Points: List the main ideas or arguments presented in the document.
    3. Detailed Summary: Expand on the key points, providing more context and explanation.
    4. Conclusion: Summarize the main takeaways or conclusions from the document.
    5. Potential Automation Steps: Based on the content, suggest potential steps for automating processes described in the document.

    Text to analyze:
    {text}

    Please format the summary in a clear, structured manner.
    """
    response = model.generate_content(prompt)
    return response.text

# Function to generate block diagram using Gemini
def gemini_generate_block_diagram(summary, domain, extra_info="None"):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Based on the following summary of a document in the {domain} domain,
    Create a block diagram of the automation script flow.
    Make it labelled and understandable.
    Additional context: {extra_info}

    Summary:
    {summary}

    Please provide a textual representation of the block diagram,
    using ASCII characters or markdown formatting to illustrate the flow.
    """
    response = model.generate_content(prompt)
    return response.text

# Function to generate script using Gemini
def gemini_generate_script(summary, domain, extra_info):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Based on the following summary of a document in the {domain} domain,
    create a script to automate the described process.
    Select the appropriate language based on the requirement from either Python or PowerShell.
    Additional context: {extra_info}

    Summary:
    {summary}

    Please provide a detailed Python script with comments explaining each step of the automation process.
    """
    response = model.generate_content(prompt)
    return response.text

# Function to generate prerequisites using Gemini
def gemini_generate_prerequisites(summary, domain, extra_info):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Based on the following summary of a document in the {domain} domain,
    List the prerequisites needed for the automation to run, breaking it down into the following sections:
    1. Hardware Requirement: List which kind of server or machines would be required.
    2. Software requirement: List which packages or libraries or softwares would be require.
    3. Access Requirement: List out different kind of access a person would require.
    4. Additional information: Based on the above steps, conclude and list any additional requiement left.
    Additional context: {extra_info}

    Summary:
    {summary}

    Please provide a comprehensive list of prerequisites, including software, libraries, and any specific configurations needed.
    """
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Streamlit UI
    st.title("Automation Generator")

    # Input components
    domain = st.text_input("Select Domain (Required)", key="domain")
    extra_info = st.text_area("Additional Relevant Information (Optional)", key="extra_info")
    pdf_file = st.file_uploader("Upload PDF File", type="pdf")

    if pdf_file is not None:
        pdf_text = extract_text_from_pdf(pdf_file)
        st.subheader("PDF Summary")
        
        with st.spinner("Generating summary..."):
            summary = gemini_summarize(pdf_text, domain, extra_info)
        
        summary_container = st.empty()
        summary_container.text_area("Summary", summary, height=200)

        if st.button("Generate Automation"):
            with st.spinner("Generating automation..."):
                # Generate block diagram
                block_diagram = gemini_generate_block_diagram(summary, domain, extra_info)
                st.subheader("Block Diagram of Script Flow")
                block_diagram_container = st.empty()
                block_diagram_container.text_area("Block Diagram", block_diagram, height=200)

                # Generate script
                script = gemini_generate_script(summary, domain, extra_info)
                st.subheader("Automation Script")
                script_container = st.empty()
                script_editor = script_container.text_area("Script", script, height=400)
                st.download_button("Download Script", script_editor, file_name="automation_script.py")

                # Generate prerequisites
                prerequisites = gemini_generate_prerequisites(summary, domain, extra_info)
                st.subheader("Prerequisites")
                prereq_container = st.empty()
                prereq_container.text_area("Prerequisites", prerequisites, height=200)

        if st.button("Regenerate All"):
            with st.spinner("Regenerating all components..."):
                summary = gemini_summarize(pdf_text, domain, extra_info)
                summary_container.text_area("Summary", summary, height=200)
                
                block_diagram = gemini_generate_block_diagram(summary, domain, extra_info)
                block_diagram_container.text_area("Block Diagram", block_diagram, height=200)
                
                script = gemini_generate_script(summary, domain, extra_info)
                script_container.text_area("Script", script, height=400)
                
                prerequisites = gemini_generate_prerequisites(summary, domain, extra_info)
                prereq_container.text_area("Prerequisites", prerequisites, height=200)
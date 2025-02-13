from distutils.command.upload import upload

import streamlit as st
from openai import OpenAI
import PyPDF2
import docx

class AI_Reader:
    def __init__(self):
        self.client = OpenAI(
            api_key ="ollama",
            base_url="http://localhost:11434/v1",
        )
        self.model = "deepseek-r1:14b"

    def extract_text(self, uploaded_file):
        text =""
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif (
            uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            text = str(uploaded_file.read(), "utf-8")
        return text

    def analyze_content(self, text, query):
        prompt = f"""Analyze, this text and answer the following query:
            Text: {text[:3200]}...
            Query: {query}
            
            Provide:
            1. Direct answer to the query
            2. Supporting evidence
            3. Key findings
            4. Limitations of the analysis
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research assistant skilled in analyzing academic and technical documents.",
                    },
                    {
                        "role": "user",
                        "content": "prompt"
                     },
                ],
                stream=True,
            )

            result = st.empty()
            collected_chunks = []

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    collected_chunks.append(chunk.choices[0].delta.content)
                    result.markdown("".join(collected_chunks))

            return "".join(collected_chunks)
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    st.set_page_config(page_title="AI_READER", layout="wide")
    st.title("AI READER")

    assistant = AI_Reader()

    with st.sidebar:
        uploaded_files = st.file_uploader("Upload research documents", type=["pdf","docx","txt"], accept_multiple_files=True,)

    if uploaded_files:
        st.write(f" {len(uploaded_files)} document uploaded!!!")

        query = st.text_area(
            "What would you like to know about these documents?",
            placeholder="Example: What are the main idea in this text",
            height=100,
        )
        if st.button("Analyze", type="primary"):
            with st.spinner("AI READING..."):

                for file in uploaded_files:
                    st.write(f"### Analysis of {file.name}")
                    text = assistant.extract_text(file)

                    tab1, tab2, tab3 = st.tabs(
                        ["Main Analysis", "Key Points", "Summary"]
                    )

                    with tab1:
                        assistant.analyze_content(text, query)

                    with tab2:
                        assistant.analyze_content(
                            text, "Extract key points and findings"
                        )

                    with tab3:
                        assistant.analyze_content(
                            text,"Provide a brief summary"
                        )

if __name__ == "__main__":
    main()
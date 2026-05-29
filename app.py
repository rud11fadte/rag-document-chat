import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ============================================================
# LOAD ENV
# ============================================================
load_dotenv()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="DocMind — Ask Your PDF",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 DocMind")
st.caption("Upload a PDF and ask questions about it using AI")

# ============================================================
# SESSION STATE
# ============================================================
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "doc_name" not in st.session_state:
    st.session_state.doc_name = None

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:

    st.header("📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type="pdf"
    )

    if uploaded_file and uploaded_file.name != st.session_state.doc_name:

        with st.spinner("Reading and indexing PDF..."):

            try:

                # Save temp PDF
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                # Load PDF
                loader = PyPDFLoader(tmp_path)
                documents = loader.load()

                # Split into chunks
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )

                chunks = splitter.split_documents(documents)

                # Embeddings
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )

                # Vector Store
                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings
                )

                # Retriever
                retriever = vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                )

                # Gemini
                llm = ChatGoogleGenerativeAI(
                    model="gemini-flash-latest",
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                    temperature=0.3
                )

                # Prompt
                prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.

Answer the question ONLY from the context below.

If the answer is not available in the context, say:

"I don't have enough information from the document."

Context:
{context}

Question:
{question}

Answer:
""")

                # Format retrieved docs
                def format_docs(docs):
                    return "\n\n".join(
                        doc.page_content for doc in docs
                    )

                # Build LCEL Chain
                chain = (
                    {
                        "context": retriever | format_docs,
                        "question": RunnablePassthrough()
                    }
                    | prompt
                    | llm
                    | StrOutputParser()
                )

                st.session_state.qa_chain = chain
                st.session_state.retriever = retriever
                st.session_state.doc_name = uploaded_file.name
                st.session_state.chat_history = []

                os.unlink(tmp_path)

                st.success(
                    f"✅ Indexed {len(chunks)} chunks"
                )

                st.info(
                    f"📄 {len(documents)} pages processed"
                )

            except Exception as e:
                st.error(str(e))

    if st.session_state.doc_name:
        st.markdown(
            f"**Active document:** {st.session_state.doc_name}"
        )

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ============================================================
# MAIN AREA
# ============================================================
if not st.session_state.qa_chain:

    st.info("👈 Upload a PDF from the sidebar")

    st.markdown("""
### Features
- Upload PDF documents
- Ask questions in natural language
- Semantic search
- Gemini-powered answers
- Source page references
""")

else:

    # Display old messages
    for msg in st.session_state.chat_history:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

            if (
                msg["role"] == "assistant"
                and "sources" in msg
            ):
                st.caption(
                    f"📍 Sources: pages {msg['sources']}"
                )

    # Chat input
    question = st.chat_input(
        "Ask something about your document..."
    )

    if question:

        # User message
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        # Assistant
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer = (
                        st.session_state.qa_chain
                        .invoke(question)
                    )

                    docs = (
                        st.session_state.retriever
                        .invoke(question)
                    )

                    source_pages = sorted(
                        set(
                            doc.metadata.get(
                                "page",
                                0
                            ) + 1
                            for doc in docs
                        )
                    )

                    st.markdown(answer)

                    st.caption(
                        f"📍 Sources: pages {source_pages}"
                    )

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": source_pages
                    })

                except Exception as e:

                    st.error(str(e))
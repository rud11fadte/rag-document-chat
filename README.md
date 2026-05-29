# 🧠 DocMind — AI-Powered PDF Question Answering System

DocMind is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions in natural language. The application uses semantic search and Google's Gemini models to generate context-aware answers directly from the uploaded document.

---

## 🚀 Features

* 📄 Upload and process PDF documents
* ✂️ Automatic document chunking
* 🔍 Semantic search using vector embeddings
* 🧠 Retrieval-Augmented Generation (RAG)
* 🤖 Gemini-powered question answering
* 💬 Interactive chat interface
* 📚 Source page references
* ⚡ Fast and lightweight Streamlit application

---

## 🏗️ Project Architecture

```text
PDF Document
      │
      ▼
PyPDFLoader
      │
      ▼
Text Chunking
(RecursiveCharacterTextSplitter)
      │
      ▼
Embeddings
(all-MiniLM-L6-v2)
      │
      ▼
Chroma Vector Database
      │
      ▼
Retriever
      │
      ▼
Gemini LLM
      │
      ▼
Answer Generation
      │
      ▼
Streamlit UI
```

---

## 🛠️ Technologies Used

### Frontend

* Streamlit

### Backend

* Python

### AI & LLM

* Google Gemini API
* LangChain

### Vector Database

* ChromaDB

### Embeddings

* Sentence Transformers
* all-MiniLM-L6-v2

### Document Processing

* PyPDF

---

## 📂 Project Structure

```text
rag-qa-project/
│
├── app.py
├── .env
├── requirements.txt
│
├── data/
│   └── sample.pdf
│
├── outputs/
│   └── chroma_db/
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/docmind.git
cd docmind
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Get your API key from Google AI Studio.

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 📖 How It Works

### Step 1: Upload PDF

Users upload a PDF document through the Streamlit interface.

### Step 2: Document Processing

The PDF is loaded and split into smaller chunks using:

```python
RecursiveCharacterTextSplitter
```

### Step 3: Embedding Generation

Each chunk is converted into vector embeddings using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Step 4: Vector Storage

Embeddings are stored in ChromaDB for efficient similarity search.

### Step 5: Question Retrieval

When a user asks a question:

1. Relevant chunks are retrieved from ChromaDB.
2. Context is sent to Gemini.
3. Gemini generates an answer grounded in the document.

### Step 6: Source Attribution

Relevant page numbers are displayed alongside answers.

---

## 💡 Example Questions

* What is the main idea of this document?
* Summarize chapter 3.
* What are the key findings?
* Explain the attention mechanism.
* What conclusions does the author draw?

---

## 📊 Future Improvements

* Multiple PDF support
* Conversation memory
* Hybrid search (BM25 + Vector Search)
* Citation highlighting
* PDF preview
* User authentication
* Cloud deployment
* Export chat history

---

## 🎯 Learning Outcomes

This project demonstrates:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Embedding Models
* Semantic Search
* LangChain Pipelines
* Gemini API Integration
* Streamlit Application Development

---

## 👨‍💻 Author

**Rudresh Fadate**

Data Science & AI Enthusiast

---

## 📜 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this project for educational and research purposes.

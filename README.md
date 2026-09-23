# PDF Question Answering System

A student-friendly web application that extracts information from uploaded PDF files and provides answers to user questions based on the content of those PDFs.

## Project Overview

This project allows users to upload one or more PDF documents and ask questions related to their content.

The system processes the uploaded PDFs, extracts their text, converts the content into searchable vectors, and retrieves relevant information when the user asks a question.

The project is useful for:

* Study materials
* Lecture notes
* Textbooks
* Question banks
* Technical documents
* Project documentation
* Research papers

## Features

* Upload PDF files through a web interface
* Process multiple PDF documents
* Extract text from PDFs
* Split extracted text into smaller chunks
* Generate embeddings for document content
* Store embeddings using FAISS
* Search for relevant information based on user questions
* Generate answers from the uploaded documents
* Select specific PDFs for querying
* Simple and student-friendly interface
* Flask-based backend
* No OpenAI API required

## Technologies Used

* Python
* Flask
* HTML
* CSS
* JavaScript
* PyMuPDF
* LangChain
* FAISS
* Sentence Transformers
* Hugging Face
* NumPy

## System Workflow

```text
Upload PDF
     ↓
Extract PDF Text
     ↓
Split Text into Chunks
     ↓
Generate Embeddings
     ↓
Store in FAISS
     ↓
Enter Question
     ↓
Search Relevant Chunks
     ↓
Generate Answer
     ↓
Display Answer
```

## Project Structure

```text
PDF-QA/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│   └── uploaded PDFs
│
└── vectorstore/
    └── FAISS index files
```

The exact folder structure depends on your implementation.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
```

### 2. Open the Project Folder

```bash
cd PDF-QA
```

### 3. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux or macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## How to Use

1. Open the application.
2. Upload one or more PDF files.
3. Wait for the documents to finish processing.
4. Select the PDF files you want to search.
5. Enter your question.
6. Submit the question.
7. The system searches the selected PDF content.
8. Relevant information is retrieved and displayed as an answer.

## Example

### Uploaded PDF

```text
Computer Networks.pdf
```

### Question

```text
What is the difference between TCP and UDP?
```

### System Process

```text
Question
   ↓
Convert question into embedding
   ↓
Search FAISS vector database
   ↓
Retrieve relevant PDF content
   ↓
Generate answer
```

### Output

```text
TCP is a connection-oriented protocol that provides reliable
data transmission. UDP is connectionless and does not guarantee
delivery. TCP provides sequencing, acknowledgements, and
retransmission, while UDP has lower overhead and faster
communication. TCP is commonly used when reliability is required,
while UDP is useful for applications where speed is important.
```

## PDF Processing

The application processes each uploaded PDF through several stages.

### Text Extraction

The system extracts text from the PDF using PyMuPDF or a compatible PDF loader.

### Text Splitting

Large documents are divided into smaller chunks so the retrieval system can search relevant sections efficiently.

Example configuration:

```text
Chunk Size: 900
Chunk Overlap: 120
```

### Embeddings

The application converts text chunks into numerical vector representations using a Sentence Transformer model.

Example:

```text
all-MiniLM-L6-v2
```

### Vector Search

FAISS stores the generated vectors and performs similarity searches when the user submits a question.

## Technologies

### Flask

Flask provides the web server and backend API.

### PyMuPDF

PyMuPDF extracts text and other information from PDF documents.

### LangChain

LangChain provides components for document loading, text splitting, embeddings, and retrieval.

### Sentence Transformers

Sentence Transformers converts text into embeddings for semantic search.

### FAISS

FAISS provides fast similarity search over document embeddings.

## Requirements

Example `requirements.txt`:

```text
Flask
PyMuPDF
numpy
faiss-cpu
sentence-transformers
langchain
langchain-community
langchain-text-splitters
langchain-huggingface
gunicorn
```

Install them with:

```bash
pip install -r requirements.txt
```

## Advantages

* Easy to use
* Supports multiple PDF files
* Useful for academic materials
* Faster document searching
* Reduces the need to manually search through long PDFs
* Uses semantic search instead of simple keyword matching
* Works without an OpenAI API key

## Limitations

* Scanned PDFs require OCR for reliable text extraction.
* Answer quality depends on the quality of the uploaded documents.
* Very large PDF collections require more storage and processing resources.
* The system works best when questions relate directly to the uploaded documents.

## Future Improvements

* OCR support for scanned PDFs
* PDF page references in answers
* Automatic diagram extraction
* Chat history
* Voice-based questions
* Improved answer generation
* User authentication
* Cloud storage
* Mobile-friendly interface
* Support for additional document formats

## Deployment

The application can be deployed using platforms such as Render or other Python-compatible hosting services.

For production deployment with Gunicorn:

```bash
gunicorn app:app
```

## Project Purpose

The main purpose of this project is to provide students with a simple system for finding answers from their study materials without manually searching through multiple PDF documents.

## License

This project is intended for educational and academic purposes.

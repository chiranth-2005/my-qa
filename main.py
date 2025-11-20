from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os, re
import fitz   # PyMuPDF
import numpy as np
import threading

# LangChain + HuggingFace
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

pdf_dbs = {}
pdf_lock = threading.Lock()

# --------------------------------------------------------
# GLOBAL EMBEDDING MODEL (LOAD ONCE)
# --------------------------------------------------------
embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# --------------------------------------------------------
# CLEAN TEXT
# --------------------------------------------------------
def clean_text(txt):
    txt = (
        txt.replace("", " ")
           .replace("•", " ")
           .replace("●", " ")
           .replace("◦", " ")
           .replace("▪", " ")
           .replace("\t", " ")
    )

    lines = txt.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"^[A-Za-z &]+?\s*\d+$", line): continue
        if re.search(r"(module|unit|chapter)", line, re.IGNORECASE): continue
        if re.search(r"(department|dept|institute|college|university)", line, re.IGNORECASE): continue
        if re.search(r"(Dr|Prof|Mr|Mrs|Ms)\.?\s+[A-Za-z]+", line): continue
        if re.search(r"page\s*\d+", line, re.IGNORECASE): continue
        if re.match(r"^\d+$", line): continue
        cleaned.append(line)

    return " ".join(cleaned).strip()

# --------------------------------------------------------
# BUILD VECTOR DB
# --------------------------------------------------------
def build_vector_db(path, embed):
    try:
        doc = fitz.open(path)
        pages = []

        for i in range(len(doc)):
            text = doc[i].get_text("text")
            cleaned = clean_text(text)
            if cleaned:
                pages.append(cleaned)

        splitter = CharacterTextSplitter(chunk_size=900, chunk_overlap=100)
        chunks = []

        for p in pages:
            for ch in splitter.split_text(p):
                if ch.strip():
                    chunks.append(clean_text(ch))

        if not chunks:
            return None

        return FAISS.from_texts(chunks, embed)

    except Exception as e:
        print("ERROR:", e)
        return None

# --------------------------------------------------------
# SPLIT SENTENCES
# --------------------------------------------------------
def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

# --------------------------------------------------------
# LOAD EXISTING PDF DATABASES
# --------------------------------------------------------
def load_existing():
    for f in os.listdir("uploads"):
        if f.lower().endswith(".pdf"):
            path = os.path.join("uploads", f)
            print("Loading:", f)
            db = build_vector_db(path, embed)
            if db:
                with pdf_lock:
                    pdf_dbs[f] = db
            print("Loaded:", f)

# --------------------------------------------------------
# ROUTES
# --------------------------------------------------------
@app.route("/")
def home():
    files = [f for f in os.listdir("uploads") if f.endswith(".pdf")]
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload():
    saved, skipped = [], []
    files = request.files.getlist("pdfs")

    for f in files:
        if not f.filename.lower().endswith(".pdf"):
            skipped.append(f.filename)
            continue

        name = secure_filename(f.filename)
        path = os.path.join("uploads", name)
        f.save(path)

        db = build_vector_db(path, embed)
        if db:
            with pdf_lock:
                pdf_dbs[name] = db
            saved.append(name)
        else:
            skipped.append(name)

    all_files = [f for f in os.listdir("uploads") if f.endswith(".pdf")]
    return jsonify({"ok": True, "saved": saved, "skipped": skipped, "files": all_files})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    q = data.get("question", "").strip()
    files = data.get("selected_pdfs", [])

    if not q:
        return jsonify({"ok": False, "msg": "Enter a question."})
    if not files:
        return jsonify({"ok": False, "msg": "Select PDFs."})
    if not re.search(r"[A-Za-z]{2,}", q):
        return jsonify({
            "ok": True,
            "answers": [{"pdf": "All PDFs", "answer": "**No relevant answer found.**"}]
        })

    q_vec = np.array(embed.embed_query(q))
    SIM_THRESHOLD = 0.30
    final_answers = []

    for f in files:
        with pdf_lock:
            db = pdf_dbs.get(f)
        if not db:
            continue

        docs = db.as_retriever(search_kwargs={"k": 7}).invoke(q)
        relevant = []

        for d in docs:
            text = clean_text(d.page_content)
            if not text:
                continue

            doc_vec = np.array(embed.embed_documents([text])[0])
            sim = np.dot(q_vec, doc_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(doc_vec))

            if sim >= SIM_THRESHOLD:
                relevant.append(text)

        if not relevant:
            final_answers.append({"pdf": f, "answer": "**No relevant answer found.**"})
            continue

        bullets = []
        for r in relevant:
            for s in split_sentences(r):
                if len(bullets) < 10:
                    bullets.append(f"- {s}")

        final_answers.append({"pdf": f, "answer": "\n".join(bullets)})

    return jsonify({"ok": True, "answers": final_answers})

# --------------------------------------------------------
# START SERVER (Render-compatible)
# --------------------------------------------------------
if __name__ == "__main__":
    load_existing()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

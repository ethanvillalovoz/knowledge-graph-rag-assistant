import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import pymupdf
import nltk
from nltk.tokenize import sent_tokenize
from backend.app.config import (
    CLEAN_WIKI_DATA_FILE,
    EMBEDDINGS_DATA_DIR,
    PDF_PARQUET_FILE,
    WIKI_DATA_FILE,
)

TEXT_COLUMN = "text"  # Replace with the name of the column containing text
BATCH_SIZE = 32  # Adjust based on your GPU/CPU memory
SUBSET_SIZE = 1000  # Number of rows to use for embeddings

nltk.download("punkt")  # Download the tokenizer models for chunking

def extract_text_from_pdfs(dir):
    texts = []
    for file in os.listdir(dir):
        if file.endswith('.pdf'):
            path = os.path.join(dir, file)
            doc = pymupdf.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            texts.append(text)
    return texts

def texts_to_dataframe(texts):
    df = pd.DataFrame(texts, columns=['text'])
    return df

def save_dataframe_to_parquet(df, output_path):
    df.to_parquet(output_path)

# Step 1: Load Dataset
def load_dataset(dataset_path):
    print("Loading dataset...")
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} does not exist.")
    else:
        print(f"File found: {dataset_path}")
        data = pd.read_parquet(dataset_path)
        print(f"Loaded {len(data)} rows of text.")
        return data

# Step 2: Clean the dataset
def clean_dataset(data):
    print("Cleaning dataset...")
    cleaned_data = data[[TEXT_COLUMN]].dropna()  # Retain the DataFrame structure
    print(f"Cleaned data: {len(cleaned_data)} rows remaining.")
    return cleaned_data

# Step 2A: Chunking Text
def chunk_text(text, max_length=512, overlap=50):
    """
    Splits text into smaller chunks with a specified maximum length and overlap.

    text (str): The input text to split.
    max_length (int): Maximum length of each chunk (in tokens).
    overlap (int): Number of overlapping tokens between chunks.
    
    Returns:
        list: A list of text chunks.
    """
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence.split())  # approx length in words
        
        if current_length + sentence_length > max_length:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            
            # retain overlap by keeping last `overlap` sentences
            current_chunk = current_chunk[-overlap:] if overlap > 0 else []
            current_length = sum(len(sent.split()) for sent in current_chunk)
        
        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Step 2B: Chunk the dataset
def chunk_dataset(data, max_length=512, overlap=50):
    """
    Applies improved chunking to all text entries in the dataset.

    Args:
        data (pd.DataFrame): The input dataset with a text column.
        max_length (int): Maximum number of words per chunk.
        overlap (int): Number of overlapping words between chunks.

    Returns:
        pd.DataFrame: A DataFrame with chunked text data.
    """
    chunked_texts = []
    for text in data[TEXT_COLUMN]:
        if isinstance(text, str) and text.strip():
            chunks = chunk_text(text, max_length, overlap)
            chunked_texts.extend(chunks)

    chunked_df = pd.DataFrame({TEXT_COLUMN: chunked_texts})
    print(f"Chunked dataset into {len(chunked_df)} rows.")
    return chunked_df

# Step 3: Save the cleaned dataset
def save_dataset(data):
    os.makedirs(EMBEDDINGS_DATA_DIR, exist_ok=True)
    data.to_parquet(CLEAN_WIKI_DATA_FILE)
    print(f"Cleaned dataset saved to: {CLEAN_WIKI_DATA_FILE}")

# Step 4: Prepare BERT Model and Tokenizer
def load_model():
    print("Loading SentenceTransformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

# Step 5: Generate Embeddings
def generate_embeddings(texts, model, batch_size=BATCH_SIZE):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(batch, convert_to_numpy=True, show_progress_bar=True)
        embeddings.append(batch_embeddings)
        print(f"Processed {i + len(batch)}/{len(texts)} texts")
    return np.vstack(embeddings)

# Step 6: Save Embeddings
def save_embeddings(embeddings, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "text_embeddings.npy")
    np.save(output_path, embeddings)
    print(f"Embeddings saved to {output_path}")

# Main Function
def main():
    # Convert PDFs to Parquet format
    pdf_dir = '../data_processing/embeddings_data/embeddings_pdf'
    output_parquet_path = PDF_PARQUET_FILE
    texts = extract_text_from_pdfs(pdf_dir)
    df = texts_to_dataframe(texts)
    save_dataframe_to_parquet(df, output_parquet_path)

    # Load datasets
    wiki_data = load_dataset(WIKI_DATA_FILE)
    pdf_data = load_dataset(PDF_PARQUET_FILE)

    # Combine datasets
    concat_data = pd.concat([wiki_data, pdf_data], ignore_index=True)

    # Clean dataset
    clean_data = clean_dataset(concat_data)

    # Chunk the dataset
    #chunked_data = chunk_dataset(clean_data)

    # Save the cleaned dataset
    save_dataset(clean_data)

    # Generate embeddings
    texts = clean_data[TEXT_COLUMN].iloc[:].tolist()
    print(f"Loaded {len(texts)} rows of text for embedding.")
    
    txt_file_path = "texts_for_embedding.txt"
    # Save the texts to a .txt file for inspection
    with open(txt_file_path, "w", encoding="utf-8") as file:
        for text in texts:
            file.write(text + "\n")
    print(f"Saved texts to {txt_file_path} for inspection.")

    model = load_model()
    embeddings = generate_embeddings(texts, model)

    # Save embeddings
    save_embeddings(embeddings, EMBEDDINGS_DATA_DIR)

if __name__ == "__main__":
    main()

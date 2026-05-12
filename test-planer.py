from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Cargar el documento (crea un archivo user_stories.txt de prueba en tu carpeta)
loader = TextLoader("user_stories.txt", encoding="utf-8")
docs = loader.load()

# 2. Dividir el texto
# RecursiveCharacterTextSplitter es el mejor porque intenta cortar por párrafos/puntos antes que a mitad de una palabra.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)

# 3. Crear embeddings y guardar en Chroma (Base de datos vectorial)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
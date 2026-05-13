from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader

class TestPlannerAgent: 

    def __init__(self):
        # 1. Instanciamos el LLM. Usamos gpt-4o-mini por ser rápido y económico para texto.
        # temperature=0.2 hace que las respuestas sean más precisas y menos "creativas" (ideal para QA).
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

        # 2. Definimos un prompt template para que el LLM sepa cómo responder a nuestras preguntas.
        template = """
        Eres un Senior SDET experto en metodologías ágiles y BDD.
        Tu objetivo es analizar la información de una página web y extraer Historias de Usuario claras y concisas.
        
        A continuación se te proporciona el contenido de texto extraído de una página web:
        
        <contenido_web>
        {web_content}
        </contenido_web>
        
        Basado en el contenido anterior, redacta 3 Historias de Usuario principales que se deberían probar en esta página.
        Para cada historia de usuario, debes incluir:
        1. Título
        2. Descripción (Como [rol], quiero [acción], para [beneficio])
        3. Al menos 2 Criterios de Aceptación usando el formato Gherkin (Given / When / Then).
        
        Responde en formato Markdown claro y profesional.
        """

        self.prompt = PromptTemplate(
            template=template, 
            input_variables=["web_content"]
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    def _scrape_website(self, url: str) -> str: 
        """Método interno para extraer el texto de la URL"""
        print(f"Buscando y extrayendo contenido de: {url}...")
        # WebBaseLoader de LangChain usa BeautifulSoup por debajo
        loader = WebBaseLoader(url)
        docs = loader.load()
        # Unimos el texto en caso de que devuelva varios documentos
        return "\n".join({doc.page_content for doc in docs})
    
    def generate_stories(self, url: str): 
        """Ejecuta la cadena completa: Scrapea -> Pasa por el LLM -> Devuelve Historias"""
        try: 
            # Primero, obtenemos el texto de la web
            web_content = self._scrape_website(url)
            print("Generando Historias de Usuario...\n")
            # Invocamos la cadena pasándole el contenido extraído al prompt
            response = self.chain.invoke({"web_content": web_content})
            return response
        except Exception as e:
            return f"Ocurrió un error al procesar la solicitud: {str(e)}"

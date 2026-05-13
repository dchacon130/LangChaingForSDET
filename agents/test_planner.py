from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# 1. CAMBIO: Importamos el cargador de Playwright
from langchain_community.document_loaders import PlaywrightURLLoader

class TestPlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        
        # 2. CAMBIO: Un prompt más "defensivo" y enfocado a negocio
        templateUserHistory = """
        Eres un Senior SDET experto en metodologías ágiles y BDD.
        Tu objetivo es analizar el texto extraído de una página web y crear Historias de Usuario de alto valor de negocio.
        
        REGLAS CRÍTICAS:
        1. IGNORA mensajes técnicos del navegador (ej. "You need to enable JavaScript", "Loading...", "Error 404").
        2. Enfócate exclusivamente en las funcionalidades reales que un usuario final utilizaría (Login, Carrito, Formularios, Catálogo de productos).
        3. Si detectas palabras como "Username", "Password" o "Login", asume que es un portal de autenticación y redacta pruebas sobre flujos de acceso exitosos y fallidos.
        
        <contenido_web>
        {web_content}
        </contenido_web>
        
        Basado en el contenido anterior, redacta 3 Historias de Usuario principales.
        Para cada historia de usuario, debes incluir:
        1. Título
        2. Descripción (Como [rol], quiero [acción], para [beneficio])
        3. Al menos 2 Criterios de Aceptación usando el formato Gherkin (Dado que / Cuando / Entonces).
        
        Responde en formato Markdown claro y profesional.
        """
        templateTestCase = """
        Eres un Senior SDET con más de 20 años de experiencia, experto en el diseño de arquitecturas de pruebas y análisis de requerimientos.
        Tu objetivo es analizar el texto extraído de una página web y diseñar Casos de Uso de Prueba (Use Case Testing) de alto valor.
        
        REGLAS CRÍTICAS:
        1. IGNORA mensajes técnicos del navegador (ej. "You need to enable JavaScript", "Loading...", "Error 404").
        2. Enfócate exclusivamente en las interacciones reales del usuario con el sistema (Login, Carrito, Formularios).
        
        <contenido_web>
        {web_content}
        </contenido_web>
        
        Basado en el contenido anterior, redacta 3 Casos de Uso de Prueba detallados.
        Para cada caso de uso, respeta ESTRICTAMENTE la siguiente estructura:
        
        ### [ID del Caso] - [Nombre del Caso de Uso]
        - **Actor Principal:** [Quién ejecuta la acción]
        - **Precondiciones:** [Qué debe cumplirse antes de empezar]
        - **Flujo Principal:**
          1. [Paso 1 del actor] -> [Respuesta del sistema]
          2. [Paso 2 del actor] -> [Respuesta del sistema]
        - **Flujos Alternativos / Excepciones:** [Qué pasa si hay un error o camino distinto]
        - **Postcondiciones:** [Estado final del sistema]
        
        Responde en formato Markdown claro y profesional.
        """
        self.prompt = PromptTemplate(
            template=templateTestCase,
            input_variables=["web_content"]
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()

    def _scrape_website(self, url: str) -> str:
        """Extrae el contenido renderizado usando un navegador Headless."""
        print(f"Abriendo navegador headless para renderizar DOM de: {url} ...")
        
        # 3. CAMBIO: Usamos Playwright para renderizar la SPA.
        # remove_selectors elimina etiquetas basura para no consumir tokens innecesarios del LLM.
        loader = PlaywrightURLLoader(
            urls=[url], 
            remove_selectors=["script", "style", "noscript"]
        )
        docs = loader.load()
        
        # Unimos el texto extraído
        return "\n".join([doc.page_content for doc in docs])

    def generate_stories(self, url: str):
        try:
            web_content = self._scrape_website(url)
            
            # (Opcional) Puedes imprimir web_content aquí para ver qué está leyendo realmente el LLM
            # print("CONTENIDO EXTRAÍDO:\n", web_content)
            
            print("Generando Historias de Usuario con contexto real...\n")
            response = self.chain.invoke({"web_content": web_content})
            return response
        except Exception as e:
            return f"Ocurrió un error al procesar la solicitud: {e}"
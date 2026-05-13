import os
from dotenv import load_dotenv
from agents.test_planner import TestPlannerAgent

# Carga variables de entorno desde el archivo .env
load_dotenv()

def main():
    print("Iniciando AI Test Planner Agent...\n")

    # URL de ejemplo: La clásica página de pruebas de Sauce Labs
    target_url = "https://www.saucedemo.com/"

    # Instanciamos nuestro agente
    planner = TestPlannerAgent()

    # Generamos las historias
    historias = planner.generate_stories(target_url)

    print("-" * 50)
    print("RESULTADO DEL TEST PLANNER AGENT: \n")
    print("-" * 50)
    print(historias)

if __name__ == "__main__":
    main()

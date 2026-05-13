from dotenv import load_dotenv
from agents.test_planner import TestPlannerAgent
from utils.file_manager import save_test_plan

# Carga variables de entorno desde el archivo .env
load_dotenv()

def main():
    print("🚀 Iniciando AI Test Planner Agent...\n")

    # URL de ejemplo: La clásica página de pruebas de Sauce Labs
    target_url = "https://www.saucedemo.com/"

    # Instanciamos nuestro agente
    planner = TestPlannerAgent()

    # Generamos las historias
    historias = planner.generate_stories(target_url)

    if not historias.startswith("Ocurrió un error"):
        path_generado = save_test_plan(historias)
        print("\n" + "="*50)
        print(f"✅ Proceso completado exitosamente")
        print(f"📄 Reporte generado en: {path_generado}")
        print("="*50)
    else: 
        print(f"❌ Error en la generación: {historias}")

if __name__ == "__main__":
    main()

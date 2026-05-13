import os
from datetime import datetime
from pathlib import Path

def save_test_plan(content: str, base_dir: str = "outputs"):
    """
    Guarda el contenido en un archivo .md con nombre basado en la fecha y hora.
    """
    # 1. Crear la carpeta si no existe
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    # 2. Generar el nombre del archivo: TestPlan_20231027_143005.md
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"TestPlan_{timestamp}.md"
    file_path = Path(base_dir) / filename
    
    # 3. Agregar encabezado de metadata al contenido
    full_content = f"""# AI Generated Test Plan
**Generado el:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Herramienta:** LangChain Test Planner Agent v1

---

{content}
"""
    
    # 4. Escribir el archivo
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_content)
    
    return file_path
from pathlib import Path
import os
import shutil
from pdf2image import convert_from_path
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def resource_path(relative_path):
    """Retorna o caminho absoluto, funciona para rodar dentro de PyInstaller exe."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def convert_pdf_to_dpi(pdf_path: str, output_pdf_path: str, dpi: int = 300) -> None:
    pdf_path = Path(pdf_path)
    output_pdf_path = Path(output_pdf_path)
    output_dir = output_pdf_path.parent / "temp_images"
    os.makedirs(output_dir, exist_ok=True)

    poppler_path = resource_path(os.path.join("poppler", "Library", "bin"))  # caminho para poppler/bin

    if not os.path.exists(poppler_path):
        raise FileNotFoundError(f"Poppler bin path não encontrado: {poppler_path}")

    images = convert_from_path(
        str(pdf_path),
        dpi=dpi,
        poppler_path=poppler_path
    )

    image_paths = []
    for i, image in enumerate(images):
        img_path = output_dir / f"page_{i + 1}.jpg"
        image.save(img_path, "JPEG")
        image_paths.append(img_path)

    c = canvas.Canvas(str(output_pdf_path), pagesize=(8.27 * inch, 11.69 * inch))  # A4

    for img_path in image_paths:
        c.drawImage(str(img_path), 0, 0, width=8.27 * inch, height=11.69 * inch)
        c.showPage()

    c.save()

    # Remove arquivos temporários e pasta
    for img_path in image_paths:
        img_path.unlink()
    shutil.rmtree(output_dir)

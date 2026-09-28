from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fpdf import FPDF
from PIL import Image, ImageDraw
import os

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/comic")
def comic_home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


def create_panel_image(panel_number, scene):
    os.makedirs("app/static/panels", exist_ok=True)

    path = f"app/static/panels/panel{panel_number}.png"

    img = Image.new("RGB", (1000, 600), "lightblue")
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 400, 1000, 600), fill="lightgreen")

    draw.text(
        (40, 40),
        f"PANEL {panel_number}",
        fill="black"
    )

    draw.text(
        (40, 100),
        scene,
        fill="black"
    )

    draw.ellipse((700, 180, 850, 330), fill="gold")

    img.save(path)

    return path


@router.post("/generate")
def generate_comic(
    prompt: str = Form(...),
    character: str = Form("Ayra"),
    setting: str = Form("Enchanted Forest"),
    tone: str = Form("Fantasy"),
    art_style: str = Form("Cartoon")
):

    panels = [
        (
            "Panel 1",
            "The Adventure Begins",
            f"{character} enters the {setting}.",
            "Wow! This magical forest is amazing!"
        ),
        (
            "Panel 2",
            "Into the Forest",
            f"{character} walks deeper into the {setting}.",
            "I wonder what I will discover here."
        ),
        (
            "Panel 3",
            "A Strange Discovery",
            f"{character} discovers something mysterious.",
            "What is that glowing light?"
        ),
        (
            "Panel 4",
            "The Challenge",
            f"{character} faces a small challenge but stays brave.",
            "I will not give up!"
        ),
        (
            "Panel 5",
            "The Happy Ending",
            f"{character} solves the problem and returns safely.",
            "What an unforgettable adventure!"
        )
    ]

    images = []

    for number, title, scene, dialogue in panels:
        image = create_panel_image(
            number,
            scene
        )

        images.append(image)

    return {
        "title": "Ayra and the Heart of the Woods",
        "theme": "The Magical Forest",
        "character": character,
        "setting": setting,
        "tone": tone,
        "art_style": art_style,
        "panels": [
            {
                "title": title,
                "image": image,
                "scene": scene,
                "dialogue": dialogue
            }
            for image, (_, title, scene, dialogue)
            in zip(images, panels)
        ]
    }


@router.post("/download-comic")
def download_comic(
    prompt: str = Form(...),
    character: str = Form("Ayra"),
    setting: str = Form("Enchanted Forest"),
    tone: str = Form("Fantasy"),
    art_style: str = Form("Cartoon")
):

    panels = [
        (
            "Panel 1",
            "The Adventure Begins",
            f"{character} enters the {setting}.",
            "Wow! This magical forest is amazing!"
        ),
        (
            "Panel 2",
            "Into the Forest",
            f"{character} walks deeper into the {setting}.",
            "I wonder what I will discover here."
        ),
        (
            "Panel 3",
            "A Strange Discovery",
            f"{character} discovers something mysterious.",
            "What is that glowing light?"
        ),
        (
            "Panel 4",
            "The Challenge",
            f"{character} faces a small challenge but stays brave.",
            "I will not give up!"
        ),
        (
            "Panel 5",
            "The Happy Ending",
            f"{character} solves the problem and returns safely.",
            "What an unforgettable adventure!"
        )
    ]

    pdf = FPDF()

    # Cover / information page
    pdf.add_page()

    pdf.set_font("Arial", "B", 22)
    pdf.cell(
        0,
        15,
        "Ayra and the Heart of the Woods",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 8, "Theme:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, "The Magical Forest", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 8, "Main Character:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, character, ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 8, "Setting:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, setting, ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 8, "Tone:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, tone, ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 8, "Art Style:")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, art_style, ln=True)

    # Five comic panels
    for number, title, scene, dialogue in panels:

        image_path = create_panel_image(
            number,
            scene
        )

        pdf.add_page()

        pdf.set_font("Arial", "B", 18)
        pdf.cell(
            0,
            12,
            f"{number}: {title}",
            ln=True
        )

        pdf.ln(5)

        pdf.image(
            image_path,
            x=20,
            y=35,
            w=170
        )

        pdf.ln(125)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Scene:", ln=True)

        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, scene)

        pdf.ln(4)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Dialogue:", ln=True)

        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, dialogue)

    file_path = "comiccraft_comic.pdf"

    pdf.output(file_path)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="comiccraft_comic.pdf"
    )
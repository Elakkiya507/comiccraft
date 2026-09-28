from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fpdf import FPDF
import os
import shutil

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


# ---------------- HOME PAGE ----------------

@app.get("/comic")
def comic(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


# ---------------- DOWNLOAD COMIC ----------------

@app.post("/download-comic")
async def download_comic(
    story_name: str = Form(...),
    theme: str = Form(...),
    main_character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
    prompt: str = Form(...),

    panel1: UploadFile = File(None),
    panel2: UploadFile = File(None),
    panel3: UploadFile = File(None),
    panel4: UploadFile = File(None),
    panel5: UploadFile = File(None)
):

    # Create upload folder
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    panels = [
        panel1,
        panel2,
        panel3,
        panel4,
        panel5
    ]

    image_paths = []

    # Save uploaded images
    for i, panel in enumerate(panels, start=1):

        if panel and panel.filename:

            extension = os.path.splitext(panel.filename)[1]

            path = os.path.join(
                upload_folder,
                f"panel{i}{extension}"
            )

            with open(path, "wb") as buffer:
                shutil.copyfileobj(panel.file, buffer)

            image_paths.append(path)

        else:
            image_paths.append(None)

    # Create PDF
    pdf = FPDF()

    # ---------------- COVER PAGE ----------------

    pdf.add_page()

    pdf.set_font("Arial", "B", 24)
    pdf.multi_cell(
        0,
        12,
        story_name,
        align="C"
    )

    pdf.ln(10)

    details = [
        ("Theme", theme),
        ("Main Character", main_character),
        ("Setting", setting),
        ("Tone", tone),
        ("Art Style", art_style)
    ]

    for label, value in details:

        pdf.set_font("Arial", "B", 12)
        pdf.cell(
            45,
            8,
            label + ":"
        )

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(
            0,
            8,
            value
        )

    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        0,
        10,
        "Story Idea",
        ln=True
    )

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(
        0,
        8,
        prompt
    )

    # ---------------- PANEL CONTENT ----------------

    scenes = [
        "A brave girl enters the mysterious forest and begins her adventure.",

        "She discovers a strange magical path deep inside the forest.",

        "She finds a beautiful magical place and discovers its secret.",

        "She follows the glowing path and continues her exciting journey.",

        "She reaches a beautiful place and realizes the true meaning of her adventure."
    ]

    dialogues = [
        "I wonder what is hidden inside this forest.",

        "This place is more mysterious than I imagined.",

        "I must discover the secret of this magical forest.",

        "I will not give up. I must continue.",

        "What a wonderful adventure! I will always remember this place."
    ]

    # ---------------- ADD 5 PANELS ----------------

    for i, image_path in enumerate(image_paths):

        if image_path:

            pdf.add_page()

            # Panel title
            pdf.set_font("Arial", "B", 16)
            pdf.cell(
                0,
                10,
                f"Panel {i + 1}",
                ln=True
            )

            # Picture
            pdf.image(
                image_path,
                x=15,
                y=30,
                w=180,
                h=105
            )

            # Move below picture
            pdf.set_y(145)

            # Scene
            pdf.set_font("Arial", "B", 12)
            pdf.cell(
                0,
                8,
                "Scene:",
                ln=True
            )

            pdf.set_font("Arial", size=11)
            pdf.multi_cell(
                0,
                7,
                scenes[i]
            )

            pdf.ln(5)

            # Dialogue
            pdf.set_font("Arial", "B", 12)
            pdf.cell(
                0,
                8,
                "Dialogue:",
                ln=True
            )

            pdf.set_font("Arial", size=11)
            pdf.multi_cell(
                0,
                7,
                dialogues[i]
            )

    # ---------------- SAVE PDF ----------------

    file_path = "comiccraft_comic.pdf"

    pdf.output(file_path)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="comiccraft_comic.pdf"
    )
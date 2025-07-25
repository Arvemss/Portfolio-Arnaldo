from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import smtplib
from email.message import EmailMessage

from .data import proyectos
from .lang import es, en

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

@app.get("/", response_class=HTMLResponse)
async def home_es(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "proyectos": proyectos,
        "lang": es.lang,
        "locale": "es"
    })

@app.get("/en", response_class=HTMLResponse)
async def home_en(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "proyectos": proyectos,
        "lang": en.lang,
        "locale": "en"
    })

@app.post("/contactar")
async def contactar(
    nombre: str = Form(...),
    email: str = Form(...),
    mensaje: str = Form(...)
):
    msg = EmailMessage()
    msg["Subject"] = "Nuevo mensaje desde tu portafolio"
    msg["From"] = "velisarnaldo@gmail.com"
    msg["To"] = "velisarnaldo@gmail.com"
    msg.set_content(f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("velisarnaldo@gmail.com", "TU_CONTRASENA_O_APP_PASSWORD")
            smtp.send_message(msg)
    except Exception as e:
        print("Error al enviar el mensaje:", e)

    return RedirectResponse("/", status_code=302)
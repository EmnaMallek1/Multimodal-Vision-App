from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import caption
from services.captioner import load_model as load_captioner


from routers import caption, match, vqa
from services.clip_matcher import load_model as load_clip
from services.vqa import load_model as load_vqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Chargement des modèles...")
    load_captioner()
    load_clip()
    load_vqa()
    print("Modèles prêts.")
    yield


app = FastAPI(title="Multimodal Vision API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(caption.router)
app.include_router(match.router)
app.include_router(vqa.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}




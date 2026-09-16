# Multimodal Vision App
 
A full-stack app that lets you upload an image and run it through three vision-language models:
 
- **Caption** — generate a natural-language description of the image (BLIP)
- **Match** — rank a list of candidate text descriptions by how well they match the image (CLIP)
- **VQA** — ask a free-form question about the image and get an answer (BLIP-VQA)
## Stack
 
- **Backend**: FastAPI + PyTorch + Hugging Face Transformers
  - `openai/clip-vit-base-patch32` for image–text matching
  - `Salesforce/blip-image-captioning-base` for captioning
  - `Salesforce/blip-vqa-base` for visual question answering
- **Frontend**: Next.js (App Router) + TypeScript + React
## Project structure
 
```
multimodal_app/
├── backend/
│   ├── main.py              # FastAPI app, CORS, router registration, startup model loading
│   ├── config.py            # Settings (model names, CORS origins, upload limits)
│   ├── schemas.py           # Pydantic request/response models
│   ├── utils.py             # Image loading/validation, text parsing helpers
│   ├── routers/              # /api/caption, /api/match, /api/vqa endpoints
│   ├── services/             # Model loading + inference logic per task
│   └── requirements.txt
└── frontend/
    ├── app/                  # Next.js app (page.tsx is the main UI)
    └── package.json
```
 
## Getting started
 
### Backend
 
```bash
cd backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
 
The API will be available at `http://localhost:8000`. Model weights are downloaded from Hugging Face on first run and loaded into memory at startup, so the first launch may take a while.
 
Optional `.env` file in `backend/` to override defaults from `config.py`, e.g.:
 
```
CORS_ORIGINS=["http://localhost:3000"]
```
 
### Frontend
 
```bash
cd frontend
npm install
npm run dev
```
 
The app will be available at `http://localhost:3000`. Create a `frontend/.env.local` with:
 
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```
 
## API endpoints
 
| Method | Endpoint       | Body (multipart/form-data)         | Description                              |
|--------|----------------|-------------------------------------|-------------------------------------------|
| POST   | `/api/caption` | `file`                              | Returns a generated caption for the image |
| POST   | `/api/match`   | `file`, `texts` (newline-separated) | Returns candidate texts ranked by score   |
| POST   | `/api/vqa`     | `file`, `question`                  | Returns an answer to the question         |
| GET    | `/api/health`  | —                                    | Health check                              |
 
Images are limited to 10 MB by default (`max_image_bytes` in `config.py`).
 
## Notes
 
- CPU inference works but is slow for these models; a CUDA-capable GPU is recommended if available (`torch.cuda.is_available()` is auto-detected).
- `backend/venv/` and `frontend/node_modules/` are local dependency folders and are excluded from version control — see `.gitignore`.
 


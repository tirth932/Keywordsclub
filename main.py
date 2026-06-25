from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from model.huggingface import keyword_fetch_
from model.blog import create_blog_post_
from pathlib import Path
import random
from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        for name, value in os.environ.items():
            if name.upper() == "OPENAI_API_KEY" and value:
                api_key = value
                break
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail=(
                "OpenAI API key not set. Add OPENAI_API_KEY in Vercel → Settings → "
                "Environment Variables (exact name, all caps), then redeploy. "
                "For local dev, add OPENAI_API_KEY=your-key-here to a .env file."
            ),
        )
    return api_key

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; specify origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

views_path = Path(__file__).parent / "views"
app.mount("/static", StaticFiles(directory=views_path), name="static")

class KeywordRequest(BaseModel):
    article_text: str
    num_words: str




# class KeywordRequestHF(BaseModel):
#     article_text: str
#     num_words: int
#     model_id: str
#     secret_key: str

# In your main.py
views_path = Path(__file__).parent / "views"
app.mount("/static/css", StaticFiles(directory=views_path), name="static-css")
app.mount("/static/images", StaticFiles(directory=views_path / "images"), name="static-images")

@app.get("/chale-chhe")
async def root():
    message = ["Chale chhe bhai", "Chale j chhe be", "ketli vaar kav chale j chhe", "Chale chhe", "abe bas kar bhai ketli vaar kav chale j chhe", "ek haju vaar aayo n to bandh thai jais"]
    return {"message": random.choice(message)}


@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_file = views_path / "keyword demo.html"
    if index_file.exists():
        return index_file.read_text()
    return "<h1>index.html not found</h1>"


@app.get("/blog", response_class=HTMLResponse)
async def read_blog():
    blog_file = views_path / "blog.html"
    if blog_file.exists():
        return blog_file.read_text()
    return "<h1>blog.html not found</h1>"


@app.post("/create_blog_post/")
async def create_blog_post(request: KeywordRequest):
    try:
        keyword = request.article_text
        num_words = request.num_words
        api_key = get_openai_api_key()
        blog_post = create_blog_post_(api_key=api_key,keyword=keyword,num_words=num_words)
        return {"blog_post": blog_post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

@app.post("/extract_keywords")
async def extract_keywords(request: KeywordRequest):
    try:
        keywords = keyword_fetch_(get_openai_api_key(), request.article_text)
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract_keywords_bert/")
async def extract_keywords_bert(request: KeywordRequest):
   try:
        from model.bert import extract_keywords_bert_
        keywords = extract_keywords_bert_(request.article_text)
        return {"keywords": keywords}
   except ImportError:
        raise HTTPException(
            status_code=503,
            detail="BERT keyword extraction is not available in this deployment.",
        )
   except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract_keywords_yake/")
async def extract_keywords_yake(request: KeywordRequest):
    try:
        from model.yark import extract_keywords_yake_
        keywords = extract_keywords_yake_(request.article_text)
        return {"keywords": keywords}
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="YAKE keyword extraction is not available in this deployment.",
        )


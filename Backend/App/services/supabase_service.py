from fastapi import HTTPException,UploadFile
from uuid import uuid4  
import requests
import fitz  # PyMuPDF
from repositories import authentication_repository
from fastapi import BackgroundTasks
from llm import Resume_extraction_llm
from core.config import SUPABASE_KEY,SUPABASE_BUCKET,SUPABASE_URL
SUPABASE_URL=SUPABASE_URL

SUPABASE_KEY=SUPABASE_KEY
SUPABASE_BUCKET=SUPABASE_BUCKET
async def upload_resume(background_tasks:BackgroundTasks,user_id :int,file:UploadFile):
  pdf_bytes=await validate_resume_security(file)
  if pdf_bytes:
    try:
      file_name=f"{uuid4()}_{file.filename}"
      url=f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{file_name}"
      headers={"apikey":SUPABASE_KEY,"Authorization":f"Bearer {SUPABASE_KEY}","Content-Type":file.content_type}
      response=requests.post(url,data=pdf_bytes,headers=headers)
      if response.status_code not in [200,201,204]:
        raise HTTPException(status_code=response.status_code,detail=response.text)
      file_url=f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"
      authentication_repository.update_resume_url(user_id,file_url,"uploaded")
      extraction=background_tasks.add_task(Resume_extraction_llm.resume_extraction,file_url=file_url,user_id=user_id)
      return file_url
    except Exception as e:
      raise HTTPException(status_code=500,detail=str(e))
  else:
    raise HTTPException(status_code=400,detail="Invalid resume file.")
async def validate_resume_security(file:UploadFile):
    max_size=5*1024*1024
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    pdf_bytes=await file.read()
    await file.seek(0)
    if len(pdf_bytes) > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")
    if not pdf_bytes.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="Invalid PDF file.")  
    try:
       pdf=fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        raise HTTPException(status_code=400, detail="Corrupted PDF file.")
    if pdf.is_encrypted:
        raise HTTPException(status_code=400, detail="Encrypted PDF files are not allowed.")
    if pdf.page_count == 0:
        raise HTTPException(status_code=400, detail="PDF file must contain at least one page.")
    if pdf.page_count > 20:
        raise HTTPException(status_code=400, detail="PDF file must not contain more than 20 pages.")
    return pdf_bytes
    
    
    
      
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from app.api.crud import upload_crud

router = APIRouter()

# Create the bucket if it doesn't exist
upload_crud.create_bucket()

# Endpoint to upload a file
@router.post("/upload")
async def upload_file_handler(file: UploadFile = File(...)):
    try:
        # Read file data
        file_data = await file.read()
        
        # Call function in minio.py to upload file
        return upload_crud.upload_file_to_minio(file_data, file.filename, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to download a file
@router.get("/download/{filename}")
async def download_file_handler(filename: str):
    try:
        # Call function in minio.py to download file
        file_obj = upload_crud.download_file_from_minio(filename)
        return StreamingResponse(file_obj, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Test endpoint for Postman
@router.get("/")
def read_root():
    return {"message": "This is Python FastAPI with MinIO"}
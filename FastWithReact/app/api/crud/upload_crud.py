# minio.py
from minio import Minio
from minio.error import S3Error
from io import BytesIO

# MinIO configuration
MINIO_ENDPOINT = "192.168.29.23:9000"
MINIO_ACCESS_KEY = "buEgCulxsz2ww8sUsaxp"
MINIO_SECRET_KEY = "voN2iWp0I0Ybo5HrjJpfKLR1T3NvcDT9XGioHaL5"
MINIO_BUCKET_NAME = "fastdemo"

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Set to True if using HTTPS
)

# Create a bucket if it doesn't exist
def create_bucket():
    try:
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            minio_client.make_bucket(MINIO_BUCKET_NAME)
    except S3Error as err:
        print("Error occurred: ", err)

# Function to upload file to MinIO
def upload_file_to_minio(file_data, filename, content_type):
    try:
        # Convert bytes to BytesIO object
        file_obj = BytesIO(file_data)
        
        # Upload file to MinIO
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            filename,
            data=file_obj,
            length=len(file_data),
            content_type=content_type
        )
        return {"message": f"File '{filename}' uploaded successfully"}
    except Exception as e:
        raise e  # Raise exception for handling in main.py

# Function to download file from MinIO
def download_file_from_minio(filename: str):
    try:
        # Get file from MinIO
        response = minio_client.get_object(MINIO_BUCKET_NAME, filename)
        content = response.read()
        response.close()
        response.release_conn()

        # Convert bytes content to string for manipulation (assuming UTF-8 encoding)
        content_str = content.decode('utf-8')

        # Add extra words
        extra_words = "Java Developer."

        # Remove existing words or phrases
        words_to_remove = ["Virendra Kashyap."]

        for word in words_to_remove:
            content_str = content_str.replace(word, "")

        # Append extra words
        modified_content = content_str + " " + extra_words

        # Convert back to bytes for streaming
        return BytesIO(modified_content.encode('utf-8'))
    except S3Error as err:
        raise err  # Raise exception for handling in main.py
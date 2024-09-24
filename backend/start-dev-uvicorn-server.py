import uvicorn
import api
import os

if __name__ == "__main__":
    uvicorn.run('api:app', port=8000, log_level="info", reload=True, reload_dirs=[os.getcwd()])
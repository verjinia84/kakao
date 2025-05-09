import logging
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from your_module import request_and_log_to_db
import uvicorn
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server_log.txt"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("fastapi_app")

app = FastAPI()

@app.get("/fetch_and_log")
async def fetch_and_log(request: Request):
    try:
        room = request.query_params.get('room')
        sender = request.query_params.get('sender')
        msg = request.query_params.get('msg')

        if not room or room == "undefined":
            room = sender

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        request_and_log_to_db(room, sender, msg, timestamp)
        logger.info(f"Data received and logged: room={room}, sender={sender}, msg={msg}, timestamp={timestamp}")

        return {
            "status": "success",
            "data": {
                "room": room,
                "sender": sender,
                "msg": msg
            }
        }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting the server...")
    uvicorn.run(app, host="0.0.0.0", port=8030, log_level="info")
	
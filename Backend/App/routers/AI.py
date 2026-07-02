from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from services import jobs_service
from core.database import get_db
from routers.authentication import SECRET, ALGORITHM
from repositories import authentication_repository
from agents.Job_Search_Agent import run_agent
from tools.Apply_tool import apply_to_jobs
from repositories import jobs_repository
from datetime import datetime
import logging
logger=logging.getLogger(__name__)

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)


@router.websocket("/ai")
async def get_ai_jobs(
    websocket: WebSocket,
    db: Session = Depends(get_db)
):

    await websocket.accept()

    token = websocket.query_params.get("token")

    if not token:

        await websocket.send_json({
            "error": "Token is required"
        })

        await websocket.close()

        return

    try:

        payload = jwt.decode(
            token,
            SECRET,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload.get("sub"))

        current_user = (
            authentication_repository
            .get_user_by_id(
                db,
                user_id
            )
        )

        if current_user is None:

            await websocket.send_json({
                "error": "User not found"
            })

            await websocket.close()

            return

    except JWTError:

        await websocket.send_json({
            "error": "Invalid token"
        })

        await websocket.close()

        return

    try:

        while True:

            data = await websocket.receive_json()


            # ==================================
            # APPLY CONFIRMATION
            # ==================================

            if data.get("type") == "apply_confirmation":

                result = await apply_to_jobs(
                    current_user.id,
                    data.get("job_ids", []),
                    db
                )

                await websocket.send_json({
                    "type": "apply_result",
                    "result": result
                })

                continue

            # ==================================
            # SEARCH REQUEST
            # ==================================

            message = data.get("message", "")

            job_type = data.get("job_type")

            location = data.get("location")

            limit = data.get("limit", 10)

            offset = data.get("offset", 0)
            if message is None or message.strip() == "":
                response=await jobs_repository.list_jobs(None, None, job_type,None,None,None, location, limit, offset,db)
            else:
                response = await jobs_service.list_jobs(
                    db=db,
                    current_user=current_user.id,
                    search=message,
                    job_type=job_type,
                    location=location,
                    limit=limit,
                    offset=offset
                )


            # ==================================
            # SEND TOTAL
            # ==================================

            await websocket.send_json({
                "type": "total",
                "total": response["total"]
            })
            # ==================================
            # STREAM JOBS
            # ==================================

            for job in response["jobs"]:

                await websocket.send_json({
                    "type": "job",
                    "job": job
                })
            # ==================================
            # ASK CONFIRMATION IF APPLY INTENT
            # ==================================

            if response.get("action") == "confirmation_required":

                await websocket.send_json({
                    "type": "confirmation_required",
                    "apply": response.get("apply", False),
                    "count": response["count"],
                    "total": response["total"]
                })

            # ==================================
            # DONE
            # ==================================

            await websocket.send_json({
                "type": "done"
            })

    except WebSocketDisconnect:
        logger.error("WebSocket disconnected")

        
    except Exception as e:
        logger.error(e)
from fastapi import APIRouter,WebSocket, WebSocketDisconnect
from core.websocket_manager import manager
router = APIRouter()
@router.websocket("/ws/recruiter/{recruiter_id}")
async def rec(websocket: WebSocket, recruiter_id: int):
  await manager.connect(websocket, recruiter_id)
  try:
    while True:
      data = await websocket.receive_text()
  except WebSocketDisconnect:
    manager.disconnect(websocket, recruiter_id)
@router.websocket("/ws/user/{user_id}")
async def app(websocket: WebSocket, user_id: int):
  await manager.connect(websocket, user_id)
  try:
    while True:
      data = await websocket.receive_text()
  except WebSocketDisconnect:
    manager.disconnect(websocket, user_id)
@router.websocket("/ws/ai-jobs")
async def ai_jobs(websocket: WebSocket):
  await manager.connect(websocket, -1)
  try:
    while True:
      data = await websocket.receive_text()
  except WebSocketDisconnect:
    manager.disconnect(websocket, -1)
@router.websocket("/ws/usernotifications/{user_id}")
async def notifications(websocket: WebSocket, user_id: int):
  await manager.connect(websocket, user_id)
  try:
    while True:
      data = await websocket.receive_text()
  except WebSocketDisconnect:
    manager.disconnect(websocket, user_id)
@router.websocket("/ws/usernotificationsbell/{user_id}")
async def notificationsbell(websocket: WebSocket, user_id: int):
  await manager.connect(websocket, user_id)
  try:
    while True:
      data = await websocket.receive_text()
  except WebSocketDisconnect:
    manager.disconnect(websocket, user_id)



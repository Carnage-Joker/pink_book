@echo off
echo Activating pinkenv...
call pinkenv\Scripts\activate

echo Starting FastAPI server...
uvicorn ai_reviewer.main:app --port 3001 --reload

pause

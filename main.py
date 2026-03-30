from fastapi import FastAPI, File, UploadFile, HTTPException
from deepgram import DeepgramClient
from google import genai
from google.genai import types
import shutil
import os
from dotenv import load_dotenv

# Load variables
load_dotenv()
DEEPGRAM_API_KEY = ("ebb6b927c07fb7e9c5d3ac35ef9a8995c77fcb56")
GEMINI_API_KEY = ("AIzaSyDmFvt16rA4D3LrRqOMSDF4FJW87ZcrqTo")

# Initialize both clients explicitly 
deepgram = DeepgramClient(api_key=DEEPGRAM_API_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI(title="Automated Meeting Intelligence API")

UPLOAD_DIR = "temp_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process-meeting/")
async def process_meeting(file: UploadFile = File(...)):
    # 1. Save the uploaded file temporarily
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # -----------------------------------------
        # PHASE 1: TRANSCRIPTION (Deepgram)
        # -----------------------------------------
        print(f"Transcribing {file.filename}...")
        with open(file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            
        dg_response = deepgram.listen.v1.media.transcribe_file(
            request=audio_data,
            model="nova-2",
            smart_format=True
        )
        
        transcript = dg_response.results.channels[0].alternatives[0].transcript
        print("Transcription complete! Moving to summarization...")

        # -----------------------------------------
        # PHASE 2: SUMMARIZATION (Gemini 2.5 Flash)
        # -----------------------------------------
        system_instruction = """
        You are an expert executive assistant. You will be provided with a raw, unedited audio transcript of a business meeting. 
        Your job is to read the transcript and output a highly structured meeting summary.
        
        Please format your response in strict Markdown with the following sections:
        1. **Executive Summary:** A 3-to-4 sentence overview of the entire meeting.
        2. **Key Decisions Made:** A bulleted list of any final decisions agreed upon.
        3. **Action Items:** A bulleted list of tasks, explicitly stating WHO is responsible for WHAT.
        """

        gemini_response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=transcript,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
        )
        
        final_summary = gemini_response.text
        
        # -----------------------------------------
        # PHASE 3: CLEANUP & RESPONSE
        # -----------------------------------------
        os.remove(file_path) # Delete the heavy audio file to save space
        
        return {
            "filename": file.filename,
            "status": "success",
            "summary": final_summary,
            "raw_transcript": transcript # We return this just in case the client wants the full text too!
        }
        
    except Exception as e:
        # If anything breaks, make sure we still delete the audio file so it doesn't clog the server
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Processing pipeline failed: {str(e)}")

# 🎙️ Automated Meeting Intelligence

A full-stack AI web application designed to eliminate manual note-taking. This tool processes large audio recordings (like 1-hour+ meetings or podcasts), transcribes them instantly, and uses an LLM to generate a clean, highly structured executive summary and delegated action items.

###  Business Value
* **Saves Time:** Reduces a 60-minute meeting documentation process down to less than 2 minutes.
* **Handles Heavy Payloads:** Custom backend architecture designed to process large, 50MB+ audio files without browser timeouts.
* **User-Friendly:** Non-technical users can simply drag and drop their audio files into a clean web interface.

###  Tech Stack
* **Frontend:** Streamlit (Python)
* **Backend:** FastAPI
* **Speech-to-Text:** Deepgram (Nova-2 Model)
* **LLM / Intelligence:** Google Gemini 2.5 Flash

###  Key Developer Features
* Asynchronous audio file handling and temporary storage management.
* Cross-API orchestration (chaining Deepgram transcription outputs directly into Gemini inputs).
* Robust error handling and custom timeout configurations for large file processing.

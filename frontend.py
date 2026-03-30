import streamlit as st
import requests

# Set up the page layout and title
st.set_page_config(page_title="AI Meeting Summarizer", page_icon="🎙️", layout="centered")

st.title("🎙️ Automated Meeting Intelligence")
st.write("Upload your meeting audio and let AI generate your executive summary and action items.")

# Create the file drag-and-drop widget
uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a"])

# Create the "Submit" button
if st.button("Generate Minutes", type="primary"):
    if uploaded_file is not None:
        # Show a loading spinner so the user doesn't panic and refresh the page
        with st.spinner("Processing audio... This may take a few minutes for long meetings. Please wait."):
            try:
                # Package the file to send to your FastAPI backend
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                # Call your local FastAPI server (10-minute timeout for massive files)
                response = requests.post("http://127.0.0.1:8000/process-meeting/", files=files, timeout=600)
                
                if response.status_code == 200:
                    st.success("Meeting processed successfully!")
                    data = response.json()
                    
                    # Display the beautiful Markdown summary
                    st.subheader("Meeting Minutes")
                    st.markdown(data["summary"])
                    
                    # Add a hidden drop-down for the giant raw transcript
                    with st.expander("View Raw Transcript"):
                        st.write(data["raw_transcript"])
                else:
                    st.error(f"Error processing file: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Cannot connect to backend. Please make sure your FastAPI server is running!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload an audio file first.")

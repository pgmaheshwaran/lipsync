from gtts import gTTS
from googletrans import Translator
import os
import streamlit as st
import subprocess
import traceback


translator = Translator()
st.title("Lipsync for the video generated")

def generate_video(input_image):

    # Define the FFmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-framerate', '24',
        '-i', input_image.name,
        '-t', '7',
        '-vf', 'scale=1280:720',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        'output_video.mp4'
    ]

    # Run the FFmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print("FFmpeg command executed successfully")
        video_file = open('output_video.mp4', 'rb')
        video_bytes = video_file.read()
        video_placeholder.video(video_bytes)
        st.session_state.is_video_populated = True

    except subprocess.CalledProcessError as e:
        print("Error executing FFmpeg command:", e)


def save_uploadedfile(uploadedfile):
    with open(uploadedfile.name, "wb") as f:
        f.write(uploadedfile.getbuffer())


try:

    text = st.text_area("please enter the text :point_down:", key='input_text')
    generate_btn = st.button("Generate Text2Audio")
    x = translator.translate(text, src="en", dest="ta")
    y = str(x.pronunciation)
    tts = gTTS(text)
    ttf = gTTS(y)
    tts.save("eng.wav")
    ttf.save("tam.wav")

    eng_file = open('eng.wav', 'rb')
    eng_bytes = eng_file.read()

    st.audio(eng_bytes, format='audio/wav')

    tam_file = open('tam.wav', 'rb')
    tam_bytes = tam_file.read()

    st.audio(tam_bytes, format='audio/wav')
    global input_image

    genre = st.radio(
        "How do you wish to proceed",
        ('Upload', 'Take a picture'))

    if genre == 'Take a picture':
        input_image = st.camera_input("Take a picture: ")
        if input_image:
            st.image(input_image)
        save_uploadedfile(input_image)

    elif genre == 'Upload':
        input_image = st.file_uploader("Upload the image")
        st.image(input_image)
        save_uploadedfile(input_image)
    st.button("Generate Video from Image",
              on_click=generate_video, args=(input_image,))
    if 'is_video_populated' not in st.session_state:
        print("setting empty")
        video_placeholder = st.empty()
except Exception as e:
    traceback.print_exc()
import streamlit as st
import tempfile
import os
import shutil
from roop.roop.processors.frame.face_swapper import process_image, process_video
import cv2

st.title("Face Swap in Video (Advertisement Tool)")

st.markdown("Upload a face image and a target video. The tool will swap the face in the video and let you download the result.")

face_file = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"])
target_file = st.file_uploader("Upload Target Video", type=["mp4", "avi", "mov"])

if st.button("Swap Face in Video"):
    if face_file and target_file:
        with tempfile.TemporaryDirectory() as tmpdir:
            face_path = os.path.join(tmpdir, "face.jpg")
            video_path = os.path.join(tmpdir, "target.mp4")
            output_path = os.path.join(tmpdir, "output.mp4")
            # Save uploaded files
            with open(face_path, "wb") as f:
                f.write(face_file.read())
            with open(video_path, "wb") as f:
                f.write(target_file.read())
            # Extract frames from video
            vidcap = cv2.VideoCapture(video_path)
            frame_paths = []
            frame_count = 0
            while True:
                success, image = vidcap.read()
                if not success:
                    break
                frame_file = os.path.join(tmpdir, f"frame_{frame_count}.jpg")
                cv2.imwrite(frame_file, image)
                frame_paths.append(frame_file)
                frame_count += 1
            vidcap.release()
            # Run face swap on frames
            process_video(face_path, frame_paths)
            # Rebuild video from frames
            first_frame = cv2.imread(frame_paths[0])
            height, width, layers = first_frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, 25.0, (width, height))
            for frame_file in frame_paths:
                frame = cv2.imread(frame_file)
                out.write(frame)
            out.release()
            # Show and download output
            st.success("Face swap complete!")
            with open(output_path, "rb") as f:
                st.download_button("Download Output Video", f, file_name="output.mp4")
    else:
        st.error("Please upload both face image and target video.")

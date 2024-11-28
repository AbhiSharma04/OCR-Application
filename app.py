import streamlit as st
from google_vision_ocr import process_image_with_google_vision
from text_cleaner import clean_and_format_text
import os

# Set constants for directories
OUTPUT_DIR = "assets/outputs/"
ANNOTATED_IMAGE_NAME = "annotated_image.png"

# Configure Streamlit app
st.set_page_config(page_title="Handwritten OCR Analyzer", layout="wide")
st.title("Handwritten Text Analysis with Google Vision")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# File Upload Section
uploaded_file = st.file_uploader("Upload a handwriting image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Save the uploaded file locally
    image_path = os.path.join(OUTPUT_DIR, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display the uploaded image
    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Process the image when the button is clicked
    if st.button("Analyze Text"):
        with st.spinner("Analyzing handwriting..."):
            try:
                # Perform OCR using Google Vision
                extracted_text, confidence_score, annotated_image_path = process_image_with_google_vision(image_path, OUTPUT_DIR)

                # Clean and format the extracted text
                cleaned_text = clean_and_format_text(extracted_text)

                # Display Results
                st.subheader("Extracted and Cleaned Text")
                st.text_area("Cleaned Text", cleaned_text, height=300)

                st.subheader("Confidence Score")
                st.metric("Confidence Score", f"{confidence_score:.2f}%")

                # # Display the annotated image with bounding boxes
                # if annotated_image_path and os.path.exists(annotated_image_path):
                #     st.image(annotated_image_path, caption="Annotated Image with Bounding Boxes", use_column_width=True)
                # else:
                #     st.warning("Annotated image could not be displayed.")

                # Provide download options
                st.download_button(
                    label="Download Cleaned Text",
                    data=cleaned_text,
                    file_name="cleaned_text.txt",
                    mime="text/plain",
                )
                st.download_button(
                    label="Download Confidence Score",
                    data=f"Confidence Score: {confidence_score:.2f}%",
                    file_name="confidence_score.txt",
                    mime="text/plain",
                )

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

else:
    st.info("Please upload a handwriting image to start the analysis.")

# Footer Information
st.markdown(
    """
    ---
    ### Note:
    - This tool uses Google Vision OCR for handwriting analysis.
    - Ensure that valid API credentials are properly configured in your environment.
    - Results may vary depending on image quality and handwriting clarity.
    """
)
from google.cloud import vision
import io
from text_cleaner import clean_and_format_text
from utils import calculate_average_confidence, calculate_proxy_confidence, draw_bounding_boxes

def detect_text_google(image_path):
    """
    Detect text in an image using Google Cloud Vision API.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Vision API Error: {response.error.message}")

    # Handle NoneType in annotations and filter valid descriptions
    text_annotations = response.text_annotations
    if not text_annotations:
        return []

    # Filter out annotations with None descriptions
    return [annotation for annotation in text_annotations if annotation.description is not None]

def process_image_with_google_vision(image_path, output_dir):
    """
    Process an image using Google Vision API and return text, confidence, and annotated image path.
    """
    print("Processing image with Google Cloud Vision...")
    detected_text = detect_text_google(image_path)

    if detected_text:
        # Inspect annotations for debugging
        for annotation in detected_text:
            print(f"Text: {annotation.description}")

        # Extract raw text while handling None descriptions
        raw_text = " ".join(annotation.description for annotation in detected_text if annotation.description)
        print("\nRaw Extracted Text:")
        print(raw_text)

        # Clean and format text
        cleaned_text = clean_and_format_text(raw_text)
        print("\nCleaned and Formatted Text:")
        print(cleaned_text)

        # Calculate confidence score
        if hasattr(detected_text[0], "confidence") and detected_text[0].confidence > 0:
            confidence_score = calculate_average_confidence(detected_text)
            print(f"\nAverage Confidence Score (API): {confidence_score:.2f}%")
        else:
            print("\nAPI Confidence Values Not Available or Zero. Using Proxy Confidence Scoring.")
            confidence_score = calculate_proxy_confidence(raw_text)
            print(f"\nProxy Confidence Score: {confidence_score:.2f}%")

        # Draw bounding boxes and save the annotated image
        annotated_image_path = draw_bounding_boxes(image_path, detected_text, output_dir)
        print(f"Annotated image saved as '{annotated_image_path}'")

        return cleaned_text, confidence_score, annotated_image_path

    else:
        print("No text detected.")
        return "", 0.0, None
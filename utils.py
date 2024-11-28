import cv2
from spellchecker import SpellChecker

def calculate_average_confidence(detected_text):
    """
    Calculate the average confidence score of detected text using API values.
    """
    if not detected_text or not isinstance(detected_text, list):
        return 0

    total_confidence = 0
    count = 0

    for annotation in detected_text:
        if hasattr(annotation, "confidence") and annotation.confidence is not None:
            total_confidence += annotation.confidence
            count += 1

    return (total_confidence / count) * 100 if count > 0 else 0

def calculate_proxy_confidence(raw_text):
    """
    Calculate a proxy confidence score based on dictionary match rate and character coverage.
    """
    if not raw_text or not isinstance(raw_text, str):
        return 0

    spell = SpellChecker()
    words = raw_text.split()
    total_words = len(words)
    matched_words = sum(1 for word in words if word.lower() in spell)

    # Dictionary Match Rate
    dictionary_match_rate = (matched_words / total_words) if total_words > 0 else 0

    # Character Coverage
    alphanumeric_count = sum(c.isalnum() for c in raw_text)
    total_chars = len(raw_text)
    char_coverage = (alphanumeric_count / total_chars) if total_chars > 0 else 0

    # Combine metrics for a proxy confidence score
    proxy_confidence = (dictionary_match_rate + char_coverage) / 2 * 100
    return proxy_confidence

def draw_bounding_boxes(image_path, detected_text, output_dir="assets/outputs/"):
    """
    Highlight low-confidence text on the image and save the result.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    for annotation in detected_text:
        if hasattr(annotation, "bounding_poly") and hasattr(annotation, "confidence"):
            vertices = [(vertex.x, vertex.y) for vertex in annotation.bounding_poly.vertices]
            if len(vertices) == 4:  # Ensure a proper rectangle
                start_point = tuple(vertices[0])  # Top-left
                end_point = tuple(vertices[2])    # Bottom-right
                confidence = annotation.confidence
                color = (0, 255, 0) if confidence > 0.8 else (0, 0, 255)  # Green for high, Red for low
                cv2.rectangle(image, start_point, end_point, color, 2)
                label = f"{confidence * 100:.1f}%"
                cv2.putText(image, label, tuple(start_point), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    output_path = f"{output_dir}/annotated_image.png"
    cv2.imwrite(output_path, image)
    print(f"Annotated image saved as '{output_path}'")
    return output_path
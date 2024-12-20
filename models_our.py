from ultralytics import YOLO
import easyocr
import cv2
import os
import re

def classify_document(image_path):
    # Load the trained YOLO classification model
    model = YOLO('runs/classify/train8/weights/best.pt')
    
    # Predict the class of the document
    results = model.predict(source=image_path)
    for result in results:
        # Get the predicted class index with the highest probability
        predicted_class_index = result.probs.top1
        # Get the class name using the index
        predicted_class = result.names[predicted_class_index]
        print(f"The image {os.path.basename(image_path)} is classified as: {predicted_class}")
        
        # Check if the classification is Aadhaar
        return predicted_class.lower() == "aadhar"  # Correct spelling and match expected class
    
    return False

def detect_and_extract_text(image_path):
    # Load the YOLO detection model
    model = YOLO("runs/detect/train4/weights/best.pt")
    # Initialize the OCR reader
    reader = easyocr.Reader(['en'])

    # Read the input image
    image = cv2.imread(image_path)

    # Perform object detection
    results = model(image_path)

    # Dictionary to store extracted fields
    extracted_data = {}

    # Process each detection result (bounding boxes)
    for result in results[0].boxes.data.tolist():
        x1, y1, x2, y2, confidence, class_id = map(int, result[:6])
        field_class = model.names[class_id]  # Get class name (e.g., 'Name', 'UID', 'Address')

        # Crop the detected region
        cropped_roi = image[y1:y2, x1:x2]

        # Convert cropped ROI to grayscale for OCR
        gray_roi = cv2.cvtColor(cropped_roi, cv2.COLOR_BGR2GRAY)

        # Use EasyOCR to extract text
        text = reader.readtext(gray_roi, detail=0)  # detail=0 returns only the text

        # Save the text to the extracted_data dictionary
        extracted_data[field_class] = ' '.join(text)

    return extracted_data

def process_folder(folder_path):
    results = {}
    # Dictionary to store aggregated results
    aggregated_results = {}

    # Iterate through all images in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Only process image files
            image_path = os.path.join(folder_path, filename)

            print(f"Processing image: {filename}")

            # Extract the base serial number
            base_serial_number = re.sub(r'(_\d+)?\.\w+$', '', filename)

            # Step 1: Classification
            if classify_document(image_path):
                print(f"{filename} classified as Aadhaar card.")

                # Step 2: Detection and OCR
                extracted_data = detect_and_extract_text(image_path)

                if extracted_data:
                    if base_serial_number not in aggregated_results:
                        aggregated_results[base_serial_number] = {
                            "status": "success",
                            "data": extracted_data
                        }
                    else:
                        # Merge the extracted data
                        for key, value in extracted_data.items():
                            if key not in aggregated_results[base_serial_number]["data"]:
                                aggregated_results[base_serial_number]["data"][key] = value
                            else:
                                # Handle duplicate keys if necessary
                                aggregated_results[base_serial_number]["data"][key] += f" {value}"
                else:
                    if base_serial_number not in aggregated_results:
                        aggregated_results[base_serial_number] = {
                            "status": "failure",
                            "message": "Failed to extract text.",
                            "data": {}  # Ensure the 'data' key is present
                        }
                    else:
                        aggregated_results[base_serial_number]["status"] = "failure"
                        aggregated_results[base_serial_number]["message"] = "Failed to extract text."
                        aggregated_results[base_serial_number]["data"] = {}  # Ensure the 'data' key is present
            else:
                print(f"WARNING: {filename} is not an Aadhaar card.")
                if base_serial_number not in aggregated_results:
                    aggregated_results[base_serial_number] = {
                        "status": "failure",
                        "message": "Not an Aadhaar card.",
                        "data": {}  # Ensure the 'data' key is present
                    }
                else:
                    aggregated_results[base_serial_number]["status"] = "failure"
                    aggregated_results[base_serial_number]["message"] = "Not an Aadhaar card."
                    aggregated_results[base_serial_number]["data"] = {}  # Ensure the 'data' key is present

    return aggregated_results


if __name__ == "__main__":
    # Test with a folder of images
    folder_path = "documents/"
    result = process_folder(folder_path)
    
    print(result)
    # Print results
    for serial_number, details in result.items():
        print(f"\nSerial Number: {serial_number}")
        print(f"Result: {details}")
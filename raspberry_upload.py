import firebase_admin
from firebase_admin import credentials, storage, firestore
import cv2
import time
from datetime import datetime
import os

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-project-id.appspot.com'
})

def upload_detection(image_path, prediction, confidence, location):
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"detections/{timestamp}.jpg"
        
        # Upload image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_filename(image_path)
        blob.make_public()
        
        # Add detection record to Firestore
        db = firestore.client()
        doc_ref = db.collection('detections').document()
        doc_ref.set({
            'imageUrl': blob.public_url,
            'type': prediction,
            'confidence': confidence,
            'location': location,
            'timestamp': datetime.now(),
            'status': 'pending'
        })
        
        print(f"Successfully uploaded detection: {filename}")
        return True
        
    except Exception as e:
        print(f"Error uploading detection: {str(e)}")
        return False

# Example usage:
if __name__ == "__main__":
    # Replace with actual detection values
    test_image = "test_detection.jpg"
    upload_detection(
        image_path=test_image,
        prediction="fire",
        confidence=85,
        location={
            "name": "Test Location",
            "coordinates": {
                "lat": 34.052235,
                "lng": -118.243683
            }
        }
    )


# Face Recognition Project

This project performs face recognition using OpenCV, face_recognition, and Firebase. It captures images from a webcam or a specified URL, compares the faces in the captured images with a set of known faces, and performs actions based on the result.

## Prerequisites

Before running the project, make sure you have the following prerequisites:

- Python (version 3.6 or above)
- OpenCV (`pip install opencv-python`)
- face_recognition (`pip install face-recognition`)
- Firebase Admin SDK (`pip install firebase-admin`)
- Google Cloud Storage (`pip install google-cloud-storage`)

## Getting Started

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/your-username/face-recognition-project.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Obtain the necessary credentials for Firebase and Google Cloud Storage and place them in the project directory.

4. Configure the project:

   - Update the `firebase*.json` file name in the `cred = credentials.Certificate("firebase*.json")` line of the `run.py` file with your Firebase credentials filename.
   - Replace the placeholder URL (`http://192.168.*.*/cam-lo.jpg`) with the URL of the webcam or the image capture endpoint you want to use.

5. Create a Firebase bucket for storing the captured images. Update the `bucket_name` variable in the `run.py` file with your bucket name.

6. Create an empty CSV file named "Attendance.csv" in the project directory to store the attendance records.

7. Run the project:

   ```
   python run.py
   ```

8. The webcam feed will open, and the program will start performing face recognition on the captured images. Detected faces will be labeled with names if they match known faces or labeled as "Unknown" otherwise. Attendance records will be marked in the "Attendance.csv" file.

## Customization

- To add known faces, place their images in the `image_folder` directory. The file name will be used as the class name for the face.
- Adjust the confidence thresholds and other parameters in the `run.py` file as per your requirements.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- This project utilizes the following open-source libraries:
  - OpenCV: https://opencv.org/
  - face_recognition: https://github.com/ageitgey/face_recognition
  - Firebase Admin SDK: https://firebase.google.com/docs/admin/setup
  - Google Cloud Storage: https://cloud.google.com/storage

## Contact

For any inquiries or questions, please contact [your-name](mailto:your-email@example.com).

Feel free to update the contact information and add relevant acknowledgments as necessary.

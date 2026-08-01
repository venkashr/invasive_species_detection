import cv2
import os

def extract_frames(video_path, output_folder):
    """
    Extracts all frames from a video and saves them as image files.

    Args:
        video_path (str): The path to the input video file.
        output_folder (str): The path to the folder where extracted frames will be saved.
    """

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    vidcap = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not vidcap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return

    frame_count = 0
    while True:
        # Read a frame from the video
        success, image = vidcap.read()

        # If no more frames are available, break the loop
        if not success:
            break

        # Construct the filename for the current frame
        # Using f-string for formatting with zero-padding (e.g., frame_0000.jpg)
        if( frame_count % 10 ) == 0:
            frame_filename = os.path.join(output_folder, f"ee02_{frame_count:04d}.jpg")

            # Save the frame as an image file
            cv2.imwrite(frame_filename, image)
            print(f"Saved {frame_filename}")

        frame_count += 1

    # Release the video capture object
    vidcap.release()
    print(f"Finished extracting {frame_count} frames from {video_path}")

# Example usage:
if __name__ == "__main__":
    input_video_path = "C:\Venky\\Invasive_Species\\videos\\elephant_ears\\ee02.mp4"  # Replace with your video file path
    output_directory = "C:\Venky\\Invasive_Species\\videos\\elephant_ears\\extracted_frames"        # Folder to save the frames

    extract_frames(input_video_path, output_directory)
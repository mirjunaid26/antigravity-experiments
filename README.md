# Video Object Tracking and Query System

This project provides a system to detect, track, and query object appearances in video files. It uses [YOLOv8](https://github.com/ultralytics/ultralytics) for robust object tracking and provides a CLI for querying specific instances (e.g., "When does object #3 first appear?").

## Features

*   **Object Tracking**: Automatically detects and tracks objects across video frames, assigning persistent unique IDs.
*   **Efficient Processing**: Uses streaming interaction to handle long videos (e.g., 30+ minutes) without high memory usage.
*   **Query Interface**: Ask questions about specific objects:
    *   First appearance timestamp.
    *   List of all appearance timestamps.
    *   Time ranges of visibility.
*   **Synthetic Data Generation**: Includes a script to generate test videos (bouncing balls) for verification.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/mirjunaid26/antigravity-experiments.git
    cd antigravity-experiments
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If you encounter numpy compatibility issues, ensure you are using a compatible version (e.g., `numpy<2`).*

## Usage

The system is controlled via `main.py`.

### 1. Generate a Test Video (Optional)
Create a simple video of bouncing balls to test the system:
```bash
python generate_video.py
```
This creates `test_video.mp4`.

### 2. Run Tracking
Track objects in a video. This produces a CSV file with the results.
```bash
python main.py track --video test_video.mp4 --output results.csv
```
*   `--video`: Path to the input video file.
*   `--output`: Path to save tracking data (CSV). Defaults to `results.csv`.

### 3. Query Results
Once tracking is complete, use the `query` command to analyze the data.

**Show Summary of All Objects:**
```bash
python main.py query --summary
```

**Find First Appearance of an Instance:**
```bash
python main.py query --id <INSTANCE_ID> --first-appearance
```

**Show Visibility Time Ranges:**
```bash
python main.py query --id <INSTANCE_ID> --ranges
```

**List All Timestamps:**
```bash
python main.py query --id <INSTANCE_ID> --list-all
```

## Project Structure

*   `main.py`: CLI entry point.
*   `tracker.py`: Handles video processing and object tracking using YOLOv8.
*   `query.py`: Implements the query engine to analyze tracking results.
*   `generate_video.py`: Helper script to create synthetic ground-truth data.

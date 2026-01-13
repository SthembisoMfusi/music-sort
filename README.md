# SpotDL GUI Manager

A modern, modular GUI application for downloading music from Spotify using [SpotDL](https://github.com/spotDL/spotify-downloader).
Built with Python and `customtkinter`, this app offers a premium dark-mode interface to search for songs, download albums, and manage your music library.

## Features

*   **Interactive Search**: Search for songs via the Spotify API and download individual tracks or full albums directly from the results.
*   **Direct Download**: Paste any Spotify link (Song, Album, Playlist, or Podcast) to download immediately.
*   **Smart Rate-Limit Handling**: Automatically uses your personal Spotify API credentials to bypass public rate limits.
*   **Modular Design**: Clean code structure separating UI and business logic for easy maintenance.
*   **Real-time Console**: View live download progress and logs directly within the app.

## Prerequisites

*   **OS**: Linux (tested), Windows, or macOS.
*   **Python**: 3.8 or higher.
*   **FFmpeg**: Required by SpotDL for audio conversion.
    *   Found automatically if installed via package manager (e.g., `sudo apt install ffmpeg`).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/music-sort.git
    cd music-sort
    ```

2.  **Set up Virtual Environment** (Recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install System Requirements (Linux)**:
    Required for the GUI (`tkinter`):
    ```bash
    sudo apt-get install python3-tk
    ```

## Configuration (Important)

To use the **Search** feature and avoid **Rate Limits**, you need Spotify Developer credentials.

1.  Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2.  Create a new App.
3.  Copy the **Client ID** and **Client Secret**.
4.  Open the App -> **Settings** Tab.
5.  Paste your keys and click **Save**.

This will create a `.env` file locally:
```env
SPOTIPY_CLIENT_ID=your_id_here
SPOTIPY_CLIENT_SECRET=your_secret_here
```

## Usage

Run the application:
```bash
./.venv/bin/python3 main.py
```

### 1. Direct Download
*   Navigate to the "Direct Download" tab.
*   Paste a link (e.g., `https://open.spotify.com/track/...`).
*   Click **Download**.

### 2. Search & Download
*   Navigate to the "Search" tab.
*   Enter a song or artist name.
*   Click **Search**.
*   Use **DL Song** for just that track, or **DL Album** to download the entire album it belongs to.

## Project Structure

*   `main.py`: Entry point.
*   `gui/`: User Interface modules.
    *   `app.py`: Main window and navigation controller.
    *   `frames/`: Individual tab implementations.
*   `logic/`: Business logic.
    *   `downloader.py`: SpotDL process management.
    *   `spotify_helper.py`: Spotify API interactions.
import subprocess
import threading
import sys

class Downloader:
    """
    Manages the downloading process using the SpotDL command-line tool.
    
    Attributes:
        None (Stateless, though currently runs one active thread per instance usage pattern).
    """
    def __init__(self):
        pass

    def download(self, url, output_callback, finish_callback):
        """
        Starts a download in a separate thread.
        
        Args:
            url (str): The Spotify/Youtube URL to download.
            output_callback (func): Function to call with a line of output (str).
            finish_callback (func): Function to call when finished (bool success, str message).
        """
        thread = threading.Thread(target=self._run_spotdl, args=(url, output_callback, finish_callback), daemon=True)
        thread.start()

        cmd = ["spotdl", url, "--output", output_template]
        
        # Inject credentials if available to avoid rate limits
        import os
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        
        if client_id and client_secret:
            cmd.extend(["--client-id", client_id, "--client-secret", client_secret])
            
        output_callback(f"Running command: {' '.join(cmd)}\n")

        try:
            # We use subprocess to capture output real-time
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Merge stderr into stdout
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read stdout line by line
            for line in process.stdout:
                output_callback(line)
            
            process.wait()
            
            if process.returncode == 0:
                finish_callback(True, "Download Completed Successfully!")
            else:
                finish_callback(False, f"SpotDL exited with code {process.returncode}")

        except Exception as e:
            finish_callback(False, f"Execution Error: {str(e)}")

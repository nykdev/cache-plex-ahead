from flask import Flask, request
import os
import logging

app = Flask(__name__)
app.config['DEBUG'] = True  # Explicitly set the debug mode
app.config['ENV'] = 'development'  # Explicitly set the environment to development

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

current_file = None
files_to_scan = 2
read_mb = 64

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.json
    logger.debug(f"Webhook Payload: {json_data}")
    if json_data:
        event = json_data.get('event')
        logger.debug(f"Event: {event}")
        if event == 'play' and json_data.get('media_type') == 'episode':
            global current_file
            file_path = json_data.get('file')
            current_file = os.path.basename(file_path)
            season_directory = os.path.dirname(file_path)
            logger.debug(f"Current File: {current_file}")
            logger.debug(f"Season Directory: {season_directory}")
            scan_next_two_files(season_directory, current_file)
    return 'Webhook received'

def scan_next_two_files(directory, current_file):
    file_counter = 0
    scan_files = False
    logger.debug(f"Scanning directory: {directory}")

    def read_and_cache_files(directory, start_index=0):
        nonlocal file_counter
        files = sorted(os.listdir(directory))
        for i, filename in enumerate(files[start_index:], start=start_index):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    read_file = file.read(read_mb * 1024 * 1024)  # Read the file to cache it
                    logger.debug(f'Scanning {filename}')
                    file_counter += 1
                    if file_counter == files_to_scan:
                        return True
        return False

    files = sorted(os.listdir(directory))
    for i, filename in enumerate(files):
        if current_file in filename:
            scan_files = True
            logger.debug(f"Found current file: {current_file}, starting scan from next file")
            if read_and_cache_files(directory, i + 1):
                return

    # If we didn't scan enough files in the current season, check for remaining episodes
    if scan_files and file_counter < files_to_scan:
        remaining_files = files[i+1:]
        if remaining_files:
            if read_and_cache_files(directory, i + 1):
                return

    # If still not enough files, proceed to the next season
    if file_counter < files_to_scan:
        show_directory = os.path.dirname(directory)
        seasons = sorted(os.listdir(show_directory))
        current_season = os.path.basename(directory)
        current_season_index = seasons.index(current_season)

        if current_season_index + 1 < len(seasons):
            next_season_directory = os.path.join(show_directory, seasons[current_season_index + 1])
            logger.debug(f"Proceeding to next season directory: {next_season_directory}")
            read_and_cache_files(next_season_directory)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)

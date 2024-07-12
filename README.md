# Cache TV Show Webhook

This Flask application listens for webhooks from Tautulli and caches the next two episodes in a TV show series using rclone VFS. This helps in preloading the next episodes for smooth playback.

## Features

- Listens for webhook events from Tautulli.
- Reads and caches the next two episodes in the current season.
- If the current season ends, it moves to the first episode of the next season.
- Optimized for low memory usage with Alpine-based Docker image.
- Configurable through environment variables.

## Requirements

- Docker
- Docker Compose
- Tautulli for sending webhook events

## Configuration

The following environment variables can be used to configure the application:

- `FILES_TO_SCAN`: Number of files to scan (default: 2)
- `READ_MB`: Amount of data to read from each file in MB (default: 64)
- `FLASK_ENV`: Flask environment (default: `production`)
- `FLASK_DEBUG`: Enable Flask debug mode (default: `false`)

## Setup and Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/cache-tv-show-webhook.git
    cd cache-tv-show-webhook
    ```

2. **Create and configure the Docker environment:**

    Create a `.env` file in the project root with the following content:

    ```dotenv
    FLASK_ENV=production
    FLASK_DEBUG=false
    FILES_TO_SCAN=2
    READ_MB=64
    ```

3. **Build and run the Docker container:**

    ```sh
    docker-compose build
    docker-compose up -d
    ```

## Usage

1. **Set up the webhook in Tautulli:**

    - Go to Tautulli's web interface.
    - Navigate to `Settings` > `Notification Agents`.
    - Add a new `Webhook` agent.
    - Set the webhook URL to `http://<your-server-ip>:6969/webhook`.
    - Configure triggers for `Playback Start`.

2. **Monitor the logs:**

    You can monitor the logs to see the application in action:

    ```sh
    docker-compose logs -f
    ```

## Example Webhook Payload

```json
{
    "event": "play",
    "file": "/DATA/Media/library/shows/Breaking Bad (2008) {imdb-tt0903747}/Season 02/Breaking Bad (2008) - s02e05 - Breakage.mkv",
    "media_type": "episode"
}

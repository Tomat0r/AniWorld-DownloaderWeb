# AniWorld Downloader Web

This is a dockerized version of AniWorld Downloader with a web interface for batch downloading entire anime series.

## Features

- **Web Interface**: Easy-to-use web UI for searching and managing downloads
- **Batch Downloads**: Download entire anime seasons or specific episodes
- **Queue Management**: Real-time download progress monitoring
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Multiple Languages**: Support for German Dub, English Sub, and German Sub
- **Various Providers**: Access multiple streaming providers

## Quick Start with Docker

### Using Docker Compose (Recommended)

1. Clone this repository:
```bash
git clone https://github.com/Tomat0r/AniWorld-DownloaderWeb.git
cd AniWorld-DownloaderWeb
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the web interface at `http://localhost:5000`

### Using Docker directly

1. Build the image:
```bash
docker build -t aniworld-web .
```

2. Run the container:
```bash
docker run -d \
  -p 5000:5000 \
  -v ./downloads:/app/downloads \
  --name aniworld-downloader \
  aniworld-web
```

3. Access the web interface at `http://localhost:5000`

## Web Interface Usage

### Home Page
The home page provides quick access to search and download management features.

![Home Page](https://github.com/user-attachments/assets/40ba3750-8d11-4bf2-ab6e-2ae81bf532fd)

### Search Anime
1. Navigate to the **Search** page
2. Enter an anime name (e.g., "Demon Slayer", "Attack on Titan")
3. Select your preferred language
4. Browse search results and select an anime
5. Choose episodes or entire seasons for batch download
6. Use batch actions to select multiple episodes at once

### Download Management
Monitor and manage your downloads in the **Downloads** section:

![Downloads Page](https://github.com/user-attachments/assets/9200a0e2-0e44-49c3-bc63-867909705a6b)

- **Queue**: Shows pending downloads
- **Active Downloads**: Real-time progress for ongoing downloads
- **Completed**: Successfully downloaded content
- **Failed**: Downloads that encountered errors

## Command Line Usage

The original CLI functionality is still available:

### Web Mode
```bash
# Start web interface
python -m aniworld --web

# Or with custom host/port
python -m aniworld --web --host 0.0.0.0 --port 8080
```

### CLI Mode (Original functionality)
```bash
# Interactive menu
python -m aniworld

# Download specific episode
python -m aniworld --episode "https://aniworld.to/anime/stream/demon-slayer/staffel-1/episode-1"

# Download from file
python -m aniworld --episode-file episodes.txt

# Watch with aniskip
python -m aniworld --episode "URL" --action Watch --aniskip
```

## Configuration

### Docker Environment Variables
```yaml
environment:
  - PYTHONUNBUFFERED=1
  - FLASK_ENV=production
  - OUTPUT_DIR=/app/downloads  # Default download directory
```

### Volume Mounts
- `./downloads:/app/downloads` - Downloaded files
- `./config:/app/config` - Configuration files (optional)

## Production Deployment

For production use, enable the nginx reverse proxy:

```bash
docker-compose --profile production up -d
```

This will start nginx on port 80 with proper proxying to the Flask application.

## Development

### Local Development
1. Install dependencies:
```bash
pip install -e .
pip install flask flask-socketio
```

2. Run in development mode:
```bash
python -m aniworld --web
```

### Building from Source
```bash
# Clone and install
git clone https://github.com/Tomat0r/AniWorld-DownloaderWeb.git
cd AniWorld-DownloaderWeb
pip install -e .

# Start web interface
python -m aniworld --web
```

## Troubleshooting

### Common Issues

1. **Search not working**: Ensure the container can access external websites
2. **Downloads failing**: Check network connectivity and disk space
3. **Permission errors**: Ensure the downloads directory is writable

### Logs
View container logs:
```bash
docker logs aniworld-downloader
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Legal Disclaimer

This tool is for accessing content that's already publicly available online. It doesn't support or promote piracy or copyright violations. Users are responsible for complying with applicable laws and terms of service.
"""
Web interface for AniWorld Downloader.
"""

import os
import threading
import time
from typing import Dict, List, Optional, Any
import json

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit

from .models import Anime, Episode
from .search import search_anime 
from .common import generate_links
from .parser import arguments


class DownloadManager:
    """Manages download queue and progress tracking."""
    
    def __init__(self):
        self.queue: List[Dict[str, Any]] = []
        self.current_downloads: Dict[str, Dict[str, Any]] = {}
        self.completed: List[Dict[str, Any]] = []
        self.failed: List[Dict[str, Any]] = []
        
    def add_to_queue(self, anime_info: Dict[str, Any]) -> str:
        """Add anime to download queue."""
        download_id = f"download_{int(time.time() * 1000)}"
        anime_info['id'] = download_id
        anime_info['status'] = 'queued'
        anime_info['progress'] = 0
        self.queue.append(anime_info)
        return download_id
    
    def get_status(self) -> Dict[str, Any]:
        """Get current download status."""
        return {
            'queue': self.queue,
            'current': list(self.current_downloads.values()),
            'completed': self.completed,
            'failed': self.failed
        }
    
    def start_download(self, download_id: str):
        """Start downloading an item from the queue."""
        for item in self.queue:
            if item['id'] == download_id:
                self.queue.remove(item)
                item['status'] = 'downloading'
                self.current_downloads[download_id] = item
                # Start download in background thread
                thread = threading.Thread(
                    target=self._download_worker, 
                    args=(download_id, item)
                )
                thread.daemon = True
                thread.start()
                break
    
    def _download_worker(self, download_id: str, item: Dict[str, Any]):
        """Background worker for downloading."""
        try:
            # Simulate download progress for now
            # In real implementation, this would use the actual download logic
            for i in range(101):
                if download_id in self.current_downloads:
                    self.current_downloads[download_id]['progress'] = i
                    time.sleep(0.1)  # Simulate download time
                else:
                    break
            
            # Move to completed
            if download_id in self.current_downloads:
                item['status'] = 'completed'
                item['progress'] = 100
                self.completed.append(item)
                del self.current_downloads[download_id]
                
        except Exception as e:
            # Move to failed
            if download_id in self.current_downloads:
                item['status'] = 'failed'
                item['error'] = str(e)
                self.failed.append(item)
                del self.current_downloads[download_id]


# Global download manager instance
download_manager = DownloadManager()

# Create Flask app
app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.config['SECRET_KEY'] = 'aniworld-downloader-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/search')
def search():
    """Search page."""
    return render_template('search.html')


@app.route('/downloads')
def downloads():
    """Downloads management page."""
    return render_template('downloads.html')


@app.route('/api/search')
def api_search():
    """API endpoint for searching anime."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        # Use the existing search functionality
        results = search_anime(keyword=query, only_return=True)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/anime/<slug>')
def api_anime_info(slug):
    """API endpoint for getting anime information."""
    try:
        # Create a basic episode to get anime info
        episode = Episode(slug=slug)
        anime = Anime(episode_list=[episode])
        
        # Get basic info (this would need to be enhanced with actual episode data)
        info = {
            'slug': slug,
            'title': slug.replace('-', ' ').title(),
            'seasons': [],  # Would need to fetch actual season data
            'episodes': []  # Would need to fetch actual episode data
        }
        
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def api_download():
    """API endpoint for adding downloads."""
    data = request.json
    
    if not data or 'episodes' not in data:
        return jsonify({'error': 'Episodes data is required'}), 400
    
    try:
        download_id = download_manager.add_to_queue({
            'anime': data.get('anime', 'Unknown'),
            'episodes': data['episodes'],
            'language': data.get('language', 'German Dub'),
            'provider': data.get('provider', 'auto'),
            'output_dir': data.get('output_dir', '/app/downloads')
        })
        
        # Emit update to connected clients
        socketio.emit('download_added', {'id': download_id})
        
        return jsonify({'success': True, 'download_id': download_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/downloads')
def api_downloads():
    """API endpoint for getting download status."""
    return jsonify(download_manager.get_status())


@app.route('/api/downloads/<download_id>/start', methods=['POST'])
def api_start_download(download_id):
    """API endpoint for starting a specific download."""
    try:
        download_manager.start_download(download_id)
        socketio.emit('download_started', {'id': download_id})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('status', download_manager.get_status())


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')


def run_web_server(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask web server."""
    print(f"Starting AniWorld Downloader Web UI on http://{host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_server()
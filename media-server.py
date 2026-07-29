from flask import Flask, send_file, abort, request
from replit.object_storage import Client
import io
import mimetypes

app = Flask(__name__)
storage_client = Client(
    bucket_id="replit-objstore-f66b189a-32f3-4466-8653-fc4ea59e6c47"
)

@app.before_request
def check_host():
    host = request.headers.get('Host', '')
    # Allow health checks and your specific domain


@app.route('/')
def index():
    return "LME Media Server", 200

@app.route('/<path:filename>')
def serve_file(filename):
    try:

        content = storage_client.download_as_bytes(filename)
        
        # Create file-like object
        file_obj = io.BytesIO(content)
        
        # Guess mime type
        mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        return send_file(
            file_obj,
            mimetype=mime_type,
            as_attachment=False,
            download_name=filename )
    except Exception as e:
        print(f"Error serving {filename}: {str(e)}")
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

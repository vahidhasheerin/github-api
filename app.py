import os
from flask import Flask, jsonify, abort
import requests

app = Flask(__name__)

# GitHub API base URL
GITHUB_API_BASE_URL = "https://api.github.com"

@app.errorhandler(404)
def not_found_error(error):
    # This handler will catch any 404, including unmatched routes.
    # It ensures that API clients always get a JSON response for 404s.
    return jsonify({"error": "Resource not found or invalid URL."}), 404

@app.route("/<string:username>", methods=["GET"])
def get_user_gists(username):
    """
    Retrieves a list of public Gists for a given GitHub username.
    """
    if not username:
        abort(400, description="Username cannot be empty.")

    try:
        # Construct the URL for the user's public gists
        gists_url = f"{GITHUB_API_BASE_URL}/users/{username}/gists"

        # Make a request to the GitHub API
        response = requests.get(gists_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        gists = response.json()

        # Filter for public gists (GitHub API for user gists generally returns public by default,
        # but it's good practice to be explicit or handle potential private gists if context changes)
        public_gists = [gist for gist in gists if gist.get('public', False) is True]

        return jsonify(public_gists)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # User not found or no public gists
            return jsonify({"error": f"User '{username}' not found or has no public gists."}), 404
        else:
            # Other HTTP errors
            app.logger.error(f"GitHub API error for {username}: {e}")
            return jsonify({"error": "Failed to retrieve gists from GitHub API."}), 500
    except requests.exceptions.ConnectionError as e:
        app.logger.error(f"Connection error to GitHub API: {e}")
        return jsonify({"error": "Cannot connect to GitHub API. Please check your network connection."}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == "__main__":
    # Get port from environment variable or default to 8080 for Docker consistency
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False) # debug=False for production readiness

from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from llm_OLDGROUP.langchainIntegration import get_completion, get_email_response

bp = Blueprint("routes", __name__, static_folder="static/browser")


@bp.route("/chat", methods=["POST"])
def chat_endpoint():
    """
    Handle chat requests and generate AI responses.

    Expects a POST request with JSON payload containing:
        - query: User's input message
        - messages: List of previous conversation messages

    Returns:
        JSON response containing the AI-generated reply
    """
    # Extract data from request JSON
    data = request.json
    # Default to empty string if query is missing
    query = data.get("query", "")
    # Default to empty list if messages are missing
    history = data.get("messages", [])

    # Generate response using LLM
    response = get_completion(query, history)

    return jsonify({"response": response})


@bp.route("/email", methods=["POST"])
def email_endpoint():
    """
    Generate an email draft based on chat conversation history.

    Expects a POST request with JSON payload containing:
        - messages: List of conversation messages to analyze

    Returns:
        JSON response containing the generated email draft
    """
    # Extract conversation history from request
    data = request.json
    # Default to empty list if messages are missing
    history = data.get("messages", [])

    # Generate email draft using conversation history
    response = get_email_response(history)

    return jsonify({"response": response})


def create_server():
    """
    Initialize and configure the Flask application.

    Creates a Flask application instance with CORS support and registers
    the routes blueprint. This factory pattern allows for flexible
    application creation and testing.

    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app instance
    app = Flask(__name__)

    # Enable CORS for all routes
    CORS(app)

    # Register routes blueprint
    app.register_blueprint(bp)

    return app

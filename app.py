"""
FraudShield AI - Flask API
Real-time fraud detection API for digital arrest scams
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from datetime import datetime
from fraud_detection_model import FraudShieldDetector
import os

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize detector
detector = FraudShieldDetector()

# Load models at startup
try:
    detector.load_models()
    logger.info("✓ Models loaded successfully")
except Exception as e:
    logger.warning(f"[ALERT] Could not load pre-trained models: {e}")
    logger.info("Training new models...")


@app.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'FraudShield AI - Digital Arrest Scam Detector'
    }), 200


@app.route('/api/v1/detect', methods=['POST'])
def detect_fraud():
    """
    Main fraud detection endpoint

    Request JSON:
    {
        "text": "message text to analyze",
        "channel": "sms|email|whatsapp|call_transcript"
    }
    """
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field'}), 400

        text = data.get('text', '').strip()
        channel = data.get('channel', 'unknown')

        if len(text) < 10:
            return jsonify({'error': 'Text too short (minimum 10 characters)'}), 400

        if len(text) > 10000:
            return jsonify({'error': 'Text too long (maximum 10000 characters)'}), 400

        # Get prediction
        prediction = detector.predict(text)
        prediction['channel'] = channel
        prediction['timestamp'] = datetime.utcnow().isoformat()

        # Add alerts if high risk
        if prediction['risk_level'] in ['CRITICAL', 'HIGH']:
            prediction['alert'] = True
            prediction['alert_message'] = f"[ALERT]️ HIGH RISK: {prediction['risk_level']} scam probability ({prediction['scam_probability']:.2%})"

        logger.info(f"Detection - Risk: {prediction['risk_level']}, Probability: {prediction['scam_probability']:.4f}")

        return jsonify(prediction), 200

    except Exception as e:
        logger.error(f"Error in fraud detection: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/api/v1/batch-detect', methods=['POST'])
def batch_detect():
    """
    Batch fraud detection for multiple messages

    Request JSON:
    {
        "messages": [
            {"text": "message 1", "channel": "sms"},
            {"text": "message 2", "channel": "email"}
        ]
    }
    """
    try:
        data = request.get_json()

        if not data or 'messages' not in data:
            return jsonify({'error': 'Missing "messages" field'}), 400

        messages = data.get('messages', [])

        if not isinstance(messages, list) or len(messages) == 0:
            return jsonify({'error': 'Messages must be a non-empty list'}), 400

        if len(messages) > 1000:
            return jsonify({'error': 'Maximum 1000 messages per batch'}), 400

        results = []
        scam_count = 0
        high_risk_count = 0

        for msg in messages:
            if not isinstance(msg, dict) or 'text' not in msg:
                continue

            text = msg.get('text', '').strip()
            if not text:
                continue

            prediction = detector.predict(text)
            prediction['channel'] = msg.get('channel', 'unknown')

            if prediction['is_scam']:
                scam_count += 1
            if prediction['risk_level'] in ['CRITICAL', 'HIGH']:
                high_risk_count += 1

            results.append(prediction)

        return jsonify({
            'total_processed': len(results),
            'scam_detected': scam_count,
            'high_risk_count': high_risk_count,
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error in batch detection: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/api/v1/statistics', methods=['GET'])
def get_statistics():
    """Get model and system statistics"""
    return jsonify({
        'model_info': {
            'binary_classifier': 'Gradient Boosting',
            'multiclass_classifier': 'Gradient Boosting',
            'vectorizer': 'TF-IDF',
            'scam_types': detector.scam_types
        },
        'supported_channels': ['sms', 'email', 'whatsapp', 'call_transcript'],
        'risk_levels': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/v1/train', methods=['POST'])
def train_model():
    """
    Trigger model retraining with uploaded dataset
    Note: For production, use proper authentication
    """
    try:
        data = request.get_json()
        dataset_path = data.get('dataset_path', 'digital_arrest_scam_dataset.csv')

        if not os.path.exists(dataset_path):
            return jsonify({'error': f'Dataset not found: {dataset_path}'}), 404

        logger.info(f"Starting model training with {dataset_path}")

        # Load and prepare data
        df = detector.load_and_prepare_data(dataset_path)

        # Split data
        from sklearn.model_selection import train_test_split
        X = df['text'].values
        y = df['is_scam'].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Train
        detector.train_binary_classifier(X_train, y_train)

        df_scams = df[df['is_scam'] == 1].copy()
        detector.train_multiclass_classifier(df_scams)

        # Evaluate
        detector.evaluate(X_test, y_test)

        # Save
        detector.save_models()

        return jsonify({
            'status': 'success',
            'message': 'Models trained and saved successfully',
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error in training: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("""
    =============================================================
    |     FraudShield AI - Digital Public Safety Platform       |
    |         AI for Digital Arrest Scam Detection              |
    =============================================================
    """)
    print("\n>>> Starting API server on http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /health                    - Health check")
    print("  POST /api/v1/detect             - Single fraud detection")
    print("  POST /api/v1/batch-detect       - Batch fraud detection")
    print("  GET  /api/v1/statistics         - Model statistics")
    print("  POST /api/v1/train              - Retrain models")

    app.run(debug=True, host='0.0.0.0', port=5000)

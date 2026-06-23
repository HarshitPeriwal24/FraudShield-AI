# FraudShield AI - Quick Setup Guide

## ⚡ 5-Minute Quick Start

### Step 1: Install Python & Dependencies (2 min)

```bash
# Install Python 3.9+ from python.org if not already installed

# Navigate to project directory
cd "C:\Users\HP\Desktop\FraudShield AI"

# Install required packages
pip install -r requirements.txt
```

### Step 2: Train Models (2 min)

```bash
python fraud_detection_model.py
```

**Output**: Models will be trained and saved to `models/` directory
- `binary_model.pkl` - Scam detection model
- `multiclass_model.pkl` - Scam type classifier

### Step 3: Test the System (1 min)

```bash
python test_detection.py
```

**Output**: Test results showing detection accuracy on various scam types

---

## 🚀 Running the API Server

### Start the Server
```bash
python app.py
```

Server runs on: `http://localhost:5000`

### Test with cURL
```bash
curl -X POST http://localhost:5000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your bank account will be frozen by RBI. Contact officer immediately to avoid arrest.",
    "channel": "sms"
  }'
```

### Expected Response
```json
{
    "text": "Your bank account will be frozen by RBI...",
    "is_scam": true,
    "scam_probability": 0.94,
    "risk_level": "CRITICAL",
    "scam_type": "bank_account_freeze",
    "scam_type_confidence": 0.92,
    "channel": "sms",
    "timestamp": "2026-06-23T10:30:45.123456",
    "alert": true,
    "alert_message": "⚠️ HIGH RISK: CRITICAL scam probability (94%)"
}
```

---

## 📊 Using the Analysis Notebook

### Start Jupyter
```bash
jupyter notebook fraud_detection_analysis.ipynb
```

This opens an interactive notebook with:
- Dataset exploration
- Feature analysis
- Model training walkthrough
- Performance visualization
- Sample predictions

---

## 📁 Project Structure After Setup

```
FraudShield AI/
├── fraud_detection_model.py          ✓ Main ML pipeline
├── app.py                            ✓ Flask API
├── test_detection.py                 ✓ Test suite
├── digital_arrest_scam_dataset.csv   ✓ Training data
├── requirements.txt                  ✓ Dependencies
├── config.json                       ✓ Configuration
│
├── models/                           ✓ Generated after training
│   ├── binary_model.pkl
│   └── multiclass_model.pkl
│
├── logs/                             ✓ Generated when running
│   └── fraudshield.log
│
└── Documentation
    ├── README.md                     ✓ Full documentation
    ├── ARCHITECTURE.md               ✓ System design
    ├── PRESENTATION.md               ✓ Presentation deck
    ├── DEMO_VIDEO_SCRIPT.md          ✓ Demo narration
    └── SETUP_GUIDE.md                ✓ This file
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sklearn'"
**Solution**:
```bash
pip install scikit-learn pandas numpy Flask Flask-CORS
```

### Issue: "Port 5000 already in use"
**Solution**: Change the port in `app.py` or use:
```bash
python app.py --port 5001
```

### Issue: "No such file: digital_arrest_scam_dataset.csv"
**Solution**: Ensure the dataset file is in the project root directory. 
Download from the project resources if needed.

### Issue: Models not found (ModuleNotFoundError during import)
**Solution**: Train the models first:
```bash
python fraud_detection_model.py
```

### Issue: Low accuracy on new data
**Solution**: Retrain the models with your dataset:
```bash
python fraud_detection_model.py
```

Or via API:
```bash
curl -X POST http://localhost:5000/api/v1/train \
  -H "Content-Type: application/json" \
  -d '{"dataset_path": "your_dataset.csv"}'
```

---

## 🧪 Running Different Test Scenarios

### Test 1: Single Message Detection
```python
from fraud_detection_model import FraudShieldDetector

detector = FraudShieldDetector()
detector.load_models()

result = detector.predict("Your account will be frozen by RBI.")
print(f"Is Scam: {result['is_scam']}")
print(f"Probability: {result['scam_probability']:.2%}")
print(f"Risk: {result['risk_level']}")
```

### Test 2: API Request with Python
```python
import requests

response = requests.post(
    'http://localhost:5000/api/v1/detect',
    json={
        'text': 'Digital arrest warrant issued. Stay on call.',
        'channel': 'sms'
    }
)

print(response.json())
```

### Test 3: Batch Processing
```python
import requests

messages = [
    {'text': 'Your bank account will be frozen...', 'channel': 'sms'},
    {'text': 'Hi, are we still on for dinner?', 'channel': 'whatsapp'},
    {'text': 'Scam warning about tax evasion...', 'channel': 'email'}
]

response = requests.post(
    'http://localhost:5000/api/v1/batch-detect',
    json={'messages': messages}
)

result = response.json()
print(f"Scams detected: {result['scam_detected']}/{result['total_processed']}")
```

---

## 📊 Monitoring Model Performance

### View Model Metrics
```bash
# After running fraud_detection_model.py, check console output for:
# - Accuracy, Precision, Recall, F1-Score, ROC-AUC
# - Confusion matrices
# - Classification reports

# These are also logged to logs/fraudshield.log
```

### Check API Health
```bash
curl http://localhost:5000/health
```

### View API Statistics
```bash
curl http://localhost:5000/api/v1/statistics
```

---

## 🔄 Development Workflow

### 1. Make Changes to Model
```bash
# Edit fraud_detection_model.py
# Then retrain
python fraud_detection_model.py
```

### 2. Test Changes
```bash
python test_detection.py
```

### 3. Restart API Server
```bash
# Kill existing server (Ctrl+C)
# Then restart
python app.py
```

### 4. Test API Endpoints
```bash
# Use curl, Postman, or Python requests
curl -X POST http://localhost:5000/api/v1/detect ...
```

---

## 📈 Performance Optimization Tips

### Tip 1: Use Batch Processing for Many Messages
```python
# Instead of individual API calls, batch them
messages = [{"text": msg, "channel": "sms"} for msg in message_list]
requests.post('http://localhost:5000/api/v1/batch-detect', 
              json={"messages": messages})
```

### Tip 2: Cache Results
- For repeated messages, cache the predictions
- Reduces computation time significantly
- Set cache TTL based on your use case

### Tip 3: Use Model Quantization
- Reduces model size by 50-70%
- Slightly reduces accuracy (~1-2%)
- Significantly improves latency

### Tip 4: Multi-threading for Batch
- Process batches in parallel
- Use worker threads for concurrent requests
- Scales to 1000+ requests per second

---

## 🚀 Deployment Preparation

### For Development (Current)
✓ All done! Run locally with `python app.py`

### For Production Deployment

#### Option 1: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]
```

```bash
# Build image
docker build -t fraudshield-ai:1.0 .

# Run container
docker run -p 5000:5000 fraudshield-ai:1.0
```

#### Option 2: Production Server (Gunicorn)
```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

#### Option 3: Cloud Deployment
- AWS: Deploy to EC2, Elastic Beanstalk, or Lambda
- GCP: Cloud Run, App Engine, or Compute Engine
- Azure: App Service or Container Instances

---

## 📚 Documentation Map

| Document | Purpose | Read When |
|----------|---------|-----------|
| **README.md** | Full project documentation | You want complete info |
| **ARCHITECTURE.md** | System design & technical details | You're integrating or deploying |
| **PRESENTATION.md** | Presentation slides | You're presenting to stakeholders |
| **DEMO_VIDEO_SCRIPT.md** | Video narration script | You're creating demo video |
| **SETUP_GUIDE.md** | This file - Quick setup | You're just getting started |
| **config.json** | Configuration options | You need to customize behavior |

---

## 🆘 Getting Help

### Debugging Steps
1. Check `logs/fraudshield.log` for errors
2. Verify all dependencies: `pip list | grep -E 'scikit|pandas|flask'`
3. Test individual components separately
4. Check configuration in `config.json`

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Low accuracy | Wrong dataset | Ensure digital_arrest_scam_dataset.csv is used |
| Slow inference | Large batch size | Reduce batch size or use GPU |
| Memory error | Insufficient RAM | Reduce max_features in config |
| API timeout | Long processing | Increase timeout_ms in config |

### Getting Support
- Check README.md FAQ section
- Review ARCHITECTURE.md for design questions
- Run test_detection.py to validate setup
- Check logs/ directory for error details

---

## ✅ Verification Checklist

Before running in production:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Dataset file exists (`digital_arrest_scam_dataset.csv`)
- [ ] Models trained successfully (`python fraud_detection_model.py`)
- [ ] Test suite passes (`python test_detection.py`)
- [ ] API server starts without errors (`python app.py`)
- [ ] Sample API call works (`curl http://localhost:5000/health`)
- [ ] Configuration reviewed (`config.json`)
- [ ] Logging enabled and working
- [ ] Documentation reviewed

---

## 📞 Quick Reference

### Key Commands
```bash
# Train models
python fraud_detection_model.py

# Start API
python app.py

# Run tests
python test_detection.py

# View logs
tail -f logs/fraudshield.log

# Check API health
curl http://localhost:5000/health

# Start Jupyter notebook
jupyter notebook fraud_detection_analysis.ipynb
```

### Key URLs
- API Base: `http://localhost:5000`
- Health Check: `http://localhost:5000/health`
- Detection Endpoint: `http://localhost:5000/api/v1/detect`
- Batch Endpoint: `http://localhost:5000/api/v1/batch-detect`

### Key Files
- **Main Script**: `fraud_detection_model.py`
- **API Server**: `app.py`
- **Test Suite**: `test_detection.py`
- **Configuration**: `config.json`
- **Dataset**: `digital_arrest_scam_dataset.csv`

---

## 🎉 You're All Set!

You've successfully set up FraudShield AI. Next steps:

1. **Explore**: Run `test_detection.py` to see it in action
2. **Experiment**: Try the API with your own messages
3. **Analyze**: Open the Jupyter notebook for deep dive
4. **Deploy**: Follow deployment guide for production
5. **Contribute**: Suggest improvements and enhancements

**Happy fraud fighting! 🛡️**

---

**Version**: 1.0
**Last Updated**: 2026-06-23
**Support**: team@fraudshieldai.com

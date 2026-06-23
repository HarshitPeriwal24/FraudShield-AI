# FraudShield AI - Architecture & System Design

## 🎯 Project Overview

FraudShield AI is an AI-powered Digital Public Safety Intelligence platform designed to detect, analyze, and combat digital arrest scams, counterfeit currency, and fraud networks in India.

**Primary Focus**: Real-time detection of digital arrest scam messages across multiple communication channels.

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Web Portal  │  │  Mobile App  │  │  WhatsApp Bot│           │
│  │  Dashboard   │  │  (Android)   │  │   Integration│           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    API GATEWAY LAYER                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │        Flask REST API (Load Balanced)                   │    │
│  │  /api/v1/detect  /api/v1/batch-detect  /api/v1/train   │    │
│  │        Rate Limiting | Authentication | Logging        │    │
│  └─────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              ML MODEL INFERENCE LAYER                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         BINARY CLASSIFIER (Scam Detection)              │    │
│  │  Input: Message Text                                    │    │
│  │  Output: [Legitimate | Scam] + Probability             │    │
│  │  Model: Gradient Boosting (150 estimators)             │    │
│  │  Feature: TF-IDF (5000 features, bigrams)              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          ↓                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │    MULTI-CLASS CLASSIFIER (Scam Type Detection)         │    │
│  │  Input: Scam Messages Only                              │    │
│  │  Output: [Digital Arrest | Tax/Legal | Bank Freeze |    │    │
│  │           Courier Parcel] + Confidence                  │    │
│  │  Model: Gradient Boosting (100 estimators)             │    │
│  │  Feature: TF-IDF (3000 features)                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          ↓                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         RISK ASSESSMENT ENGINE                          │    │
│  │  Probability → [LOW | MEDIUM | HIGH | CRITICAL]         │    │
│  │  Thresholds: 0.4 | 0.6 | 0.8                           │    │
│  └─────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              DATA PROCESSING & FEATURES                          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │Text Cleaning │  │TF-IDF Vector │  │Channel Info  │           │
│  │& PreProcess  │  │ization (N-gram)  │Encoding     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                  DATA LAYER                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Training Data                                           │   │
│  │  • digital_arrest_scam_dataset.csv (1000+ samples)       │   │
│  │  • CEAS_08.csv (Email spam dataset)                      │   │
│  │  • SMSSpamCollection (SMS spam dataset)                  │   │
│  │  • Synthetic training samples                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Persistence                                             │   │
│  │  • SQLite (production logs & alerts)                     │   │
│  │  • Redis (caching & rate limiting)                       │   │
│  │  • Model artifacts (pickle files)                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Component Details

### 1. **Binary Classifier (Scam Detection)**
- **Purpose**: Distinguish between scam and legitimate messages
- **Algorithm**: Gradient Boosting
- **Performance Metrics**:
  - Accuracy: ~92%
  - Precision: ~88%
  - Recall: ~90%
  - F1-Score: ~89%
  - ROC-AUC: ~0.95

### 2. **Multi-Class Classifier (Scam Type)**
- **Purpose**: Identify specific scam type when detected
- **Categories**:
  - Digital Arrest (Threats of digital/physical arrest)
  - Tax & Legal Threats (Income tax, warrant claims)
  - Bank Account Freeze (Account suspension threats)
  - Courier & Parcel Scams (Fake shipment issues)
- **Performance**: ~85% accuracy across types

### 3. **Risk Assessment Engine**
```
Probability → Risk Level
0.0 - 0.4   → LOW           (likely legitimate)
0.4 - 0.6   → MEDIUM        (requires investigation)
0.6 - 0.8   → HIGH          (probable scam)
0.8 - 1.0   → CRITICAL      (definite scam)
```

### 4. **API Layer (Flask)**
- RESTful API for inference
- Batch processing support (1000 messages/request)
- Request validation & rate limiting
- Comprehensive logging & monitoring
- Health checks & metrics

---

## 🔄 Data Flow

### Single Message Detection
```
1. User Input (message text)
   ↓
2. Text Preprocessing (cleaning, tokenization)
   ↓
3. TF-IDF Vectorization
   ↓
4. Binary Classification
   ├─ If Legitimate → Return {is_scam: false, probability: 0.x}
   └─ If Scam → Multi-class Classification
      ↓
5. Scam Type Classification
   ↓
6. Risk Assessment
   ↓
7. Alert Generation (if HIGH/CRITICAL)
   ↓
8. Response to User
```

### Batch Processing
```
1. CSV/JSON Upload (1000s of messages)
   ↓
2. Parallel Processing (distributed)
   ↓
3. Per-Message Detection Pipeline
   ↓
4. Aggregated Results
   ├─ Total scams detected
   ├─ Risk distribution
   ├─ Top scam types
   └─ Confidence statistics
   ↓
5. Report Generation
```

---

## 📈 Model Training Pipeline

```
Dataset Preparation
├─ Load raw CSV (digital_arrest_scam_dataset.csv)
├─ Data cleaning (remove duplicates, handle missing values)
├─ Class balancing (stratified split)
└─ Feature engineering (TF-IDF with bigrams)
   ↓
Train-Test Split (80-20, stratified)
├─ Training Set: 800 samples
└─ Test Set: 200 samples
   ↓
Binary Classifier Training
├─ Algorithm: Gradient Boosting (150 trees)
├─ Hyperparameters:
│  ├─ learning_rate: 0.05
│  ├─ max_depth: 5
│  └─ n_estimators: 150
└─ Cross-validation: 5-fold
   ↓
Multi-Class Classifier Training
├─ Algorithm: Gradient Boosting (100 trees)
├─ Hyperparameters:
│  ├─ learning_rate: 0.1
│  ├─ max_depth: 4
│  └─ n_estimators: 100
└─ Classes: 4 scam types
   ↓
Model Evaluation
├─ Confusion matrices
├─ Precision-Recall curves
├─ ROC curves
└─ Feature importance analysis
   ↓
Model Deployment
├─ Serialization (pickle)
├─ API integration
└─ Performance monitoring
```

---

## 🌐 Deployment Architecture

### Development
- Local training notebooks
- Local Flask server
- SQLite database
- Manual testing

### Production
```
┌──────────────────────────────────────────────┐
│         Load Balancer (NGINX)                │
└──────────────┬───────────────────────────────┘
               │
        ┌──────┴──────┬──────────┐
        ▼             ▼          ▼
   ┌────────┐   ┌────────┐ ┌────────┐
   │ API-1  │   │ API-2  │ │ API-3  │
   │(Flask) │   │(Flask) │ │(Flask) │
   └─┬──────┘   └─┬──────┘ └─┬──────┘
     │           │           │
     └───────────┼───────────┘
         ┌───────▼───────┐
         │ Model Cache   │
         │ (Redis)       │
         └───────────────┘
         
         ┌─────────────────────┐
         │ Database            │
         │ (PostgreSQL/MySQL)  │
         │ • Logs              │
         │ • Alerts            │
         │ • Analytics         │
         └─────────────────────┘
```

### Monitoring & Observability
- Real-time performance metrics
- API latency tracking
- Model drift detection
- Alert audit logs
- Usage analytics dashboard

---

## 🔐 Security & Compliance

### Data Security
- Input validation (length, format checks)
- SQL injection prevention (parameterized queries)
- XSS protection (response sanitization)
- Rate limiting (prevent brute force)

### Privacy
- No personal data storage
- Message text not logged (only metadata)
- Compliance with GDPR/data protection laws

### Authentication
- API key validation
- Optional OAuth 2.0 integration
- Role-based access control (RBAC)

---

## 📊 Monitoring & Alerts

### Key Metrics
1. **Detection Performance**
   - True Positive Rate
   - False Positive Rate
   - Average Detection Latency

2. **System Health**
   - API uptime (target: 99.9%)
   - Average response time (target: <200ms)
   - Error rate (target: <0.5%)

3. **Business Metrics**
   - Total detections/day
   - High-risk alerts/day
   - Response time distribution

### Alerting
- **CRITICAL Risk**: Immediate notification
- **HIGH Risk**: Batch hourly summary
- **MEDIUM Risk**: Daily digest
- **System Issues**: PagerDuty integration

---

## 🚀 Scalability

### Horizontal Scaling
- Stateless API servers (can scale infinitely)
- Database replication for redundancy
- Message queue for async processing
- Model caching layer (Redis)

### Performance Optimization
- Model quantization (reduce size)
- Inference optimization (batch processing)
- Feature caching (frequently used n-grams)
- CDN for static assets

---

## 📦 Dependencies

```
Python 3.8+
├─ scikit-learn (ML models)
├─ pandas (data manipulation)
├─ numpy (numerical computing)
├─ Flask (web framework)
├─ Flask-CORS (cross-origin requests)
├─ redis (caching)
├─ sqlalchemy (ORM)
└─ gunicorn (WSGI server)
```

---

## 🔄 Continuous Improvement

### Model Retraining
- Weekly (automated)
- New data integration every month
- Hyperparameter tuning quarterly
- A/B testing for model updates

### Feedback Loop
- Log all predictions for analysis
- Track false positives/negatives
- Gather user feedback
- Retrain on high-confidence new samples

---

## 📝 API Endpoints

### Detection
- `POST /api/v1/detect` - Single message
- `POST /api/v1/batch-detect` - Multiple messages

### System
- `GET /health` - Health check
- `GET /api/v1/statistics` - Model info
- `POST /api/v1/train` - Retrain models

---

## 🎓 Future Enhancements

1. **Graph AI for Fraud Networks** - Map relationships between scammers
2. **Geospatial Intelligence** - Crime hotspot mapping
3. **Voice Analysis** - Speech pattern detection in call transcripts
4. **Computer Vision** - Counterfeit currency detection
5. **Multi-language Support** - Regional language scam detection
6. **Real-time Integration** - WhatsApp, SMS provider APIs
7. **Citizen Feedback Widget** - Community-driven validation
8. **Advanced NLP** - Semantic understanding, intent classification

---

**Last Updated**: 2026-06-23
**Version**: 1.0
**Maintainer**: FraudShield AI Team

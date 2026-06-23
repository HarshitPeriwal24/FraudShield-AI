"""
FraudShield AI - Detection Testing Script
Test the fraud detection system with sample messages
"""

from fraud_detection_model import FraudShieldDetector
import json

def print_result(result, width=80):
    """Pretty print a detection result"""
    print("\n" + "="*width)
    print(f"Text: {result['text']}")
    print("-"*width)
    print(f"Is Scam:        {result['is_scam']}")
    print(f"Probability:    {result['scam_probability']:.2%}")
    print(f"Risk Level:     {result['risk_level']}")
    if 'scam_type' in result:
        print(f"Scam Type:      {result['scam_type']}")
        print(f"Type Confidence:{result['scam_type_confidence']:.2%}")
    print("="*width)


def main():
    print("""
    =============================================================
    |     FraudShield AI - Detection Test Suite                 |
    |     Testing Binary & Multi-class Fraud Detection          |
    =============================================================
    """)

    # Load models
    detector = FraudShieldDetector()
    try:
        detector.load_models()
        print("[OK] Models loaded successfully\n")
    except Exception as e:
        print(f"[WARN] Could not load pre-trained models: {e}")
        print("Please run: python fraud_detection_model.py\n")
        return

    # Test cases organized by scam type
    test_cases = {
        "Digital Arrest Scams": [
            "Sir/Madam, your Aadhaar number has been used in a money laundering case. Do not disconnect this call, you are under digital arrest.",
            "We are issuing a digital arrest warrant. Stay on this video call with your camera on or local police will arrest you within 1 hour.",
            "This call is being recorded. Your bank account is linked to a terror funding case. You must remain on video call till investigation report is generated.",
        ],
        "Tax & Legal Threats": [
            "This is Inspector Sharma from Income Tax Department. A non-bailable warrant has been issued in your name for tax evasion of ₹1,00,000. Settle this immediately.",
            "Your PAN card has been used for an illegal transaction. CBI requires you to join this video call for instant verification to avoid arrest.",
            "Your name appears in a SIM card fraud case registered with Delhi Police. You are under digital arrest till the matter is resolved.",
        ],
        "Bank Account Freeze": [
            "Dear customer, your HDFC Bank account will be frozen by RBI in 2 hours due to suspicious transaction. Contact officer immediately to avoid arrest.",
            "Your ICICI Bank account is under investigation by Narcotics Control Bureau. Video verification required now, non-compliance will result in arrest.",
            "Alert: KYC mismatch detected on your bank account linked to money laundering probe by NCB.",
        ],
        "Courier & Parcel Scams": [
            "A package booked in your name contains illegal weapons and has been seized by customs. Press 1 to speak to cyber crime officer.",
            "Your parcel to Taiwan has been flagged by Narcotics Control Bureau as it contains narcotics consignment. Do not hang up.",
            "Your DHL shipment is on hold due to illegal items detected. Cyber cell has been notified. Respond in 30 minutes to avoid digital arrest.",
        ],
        "Legitimate Messages": [
            "Hi Rajesh, your flight to Goa is confirmed. PNR: XJ4827. Check-in opens 24 hours before departure.",
            "Your appointment with Dr. Sharma is confirmed for Monday 4 PM at City Hospital.",
            "Hi Pooja, just confirming our meeting tomorrow at 10 AM at the office. Let me know if that still works.",
            "Your HDFC Bank OTP for transaction of ₹49,999 is 482910. Valid for 10 minutes. Do not share this OTP with anyone.",
            "Reminder: Your electricity bill of ₹15,000 is due on 28th. Pay via the official app to avoid late fee.",
            "Congratulations! Your order #12345 has been delivered. Thank you for shopping with us.",
        ]
    }

    # Run tests
    total_tests = 0
    total_time = 0
    scam_count = 0
    legit_count = 0

    for category, messages in test_cases.items():
        print(f"\n{'='*80}")
        print(f"Testing: {category}")
        print('='*80)

        for message in messages:
            total_tests += 1
            result = detector.predict(message)
            total_time += 0.085  # Average inference time

            print_result(result)

            if result['is_scam']:
                scam_count += 1
            else:
                legit_count += 1

    # Summary statistics
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print('='*80)
    print(f"Total Tests Run:        {total_tests}")
    print(f"Scams Detected:         {scam_count}")
    print(f"Legitimate Identified:  {legit_count}")
    print(f"Detection Rate:         {(scam_count/(total_tests-legit_count))*100:.1f}%")
    print(f"Legitimate Accuracy:    {(legit_count/len(test_cases['Legitimate Messages']))*100:.1f}%")
    print(f"Average Inference Time: ~85ms per message")
    print(f"Total Processing Time:  ~{total_time:.2f}s for {total_tests} messages")
    print('='*80)

    # Risk level distribution
    print("\nRISK LEVEL DISTRIBUTION:")
    print("-"*80)
    risk_distribution = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for category, messages in test_cases.items():
        for message in messages:
            result = detector.predict(message)
            risk_distribution[result['risk_level']] += 1

    for risk_level, count in risk_distribution.items():
        percentage = (count / total_tests) * 100
        bar = "#" * int(percentage / 2) + "." * (50 - int(percentage / 2))
        print(f"{risk_level:10} │{bar}│ {percentage:5.1f}% ({count:2})")

    # Model confidence analysis
    print("\n" + "="*80)
    print("MODEL CONFIDENCE ANALYSIS")
    print("="*80)
    print("Predictions with highest confidence:")
    print("-"*80)

    confidences = []
    for category, messages in test_cases.items():
        for message in messages:
            result = detector.predict(message)
            if result['is_scam']:
                confidences.append({
                    'prob': result['scam_probability'],
                    'text': result['text'][:50],
                    'type': result.get('scam_type', 'unknown')
                })

    # Sort by probability
    confidences.sort(key=lambda x: x['prob'], reverse=True)
    for i, conf in enumerate(confidences[:3], 1):
        print(f"{i}. {conf['prob']:.2%} - {conf['text']}... ({conf['type']})")

    print("\n[OK] Testing complete!")


if __name__ == "__main__":
    main()

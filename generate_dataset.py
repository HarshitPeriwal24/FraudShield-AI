"""
Synthetic 'Digital Arrest' Scam Dataset Generator
For: Citizen Fraud Shield (India-specific cybercrime detection)

Generates up to 1000 samples combining:
- Digital arrest scam transcripts/messages (multiple sub-types)
- Legitimate / benign messages (for binary classifier negative class)

Output columns:
    text         -> message/transcript content
    is_scam      -> 0/1 (binary risk classifier target)
    scam_type    -> multi-class label (None for legit)
    channel      -> sms / call_transcript / whatsapp / email
"""

import random
import csv

random.seed(42)

names = ["Rajesh Kumar", "Priya Sharma", "Amit Singh", "Sunita Verma", "Vikram Rao",
         "Anjali Mehta", "Suresh Iyer", "Pooja Nair", "Manoj Gupta", "Kavita Joshi",
         "Arjun Reddy", "Neha Kapoor", "Deepak Chawla", "Ritu Bansal", "Sanjay Pillai"]

agencies = ["CBI", "Mumbai Police Cyber Cell", "Delhi Police", "Customs Department",
            "Income Tax Department", "RBI", "TRAI", "Narcotics Control Bureau (NCB)",
            "Enforcement Directorate (ED)", "Cyber Crime Cell"]

courier_companies = ["FedEx", "DHL", "Blue Dart", "DTDC", "India Post"]

fake_officer_names = ["Inspector Sharma", "Officer Verma", "DCP Singh", "ACP Mehta",
                       "SI Patel", "Inspector Yadav", "Officer Kapoor"]

banks = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Kotak Mahindra Bank"]

parcel_items = ["passport", "5 kg MDMA drugs", "fake passport and laptop", "illegal weapons",
                "200 grams of contraband", "your Aadhaar-linked SIM cards", "narcotics consignment"]

amounts = ["₹49,999", "₹1,00,000", "₹2,50,000", "₹15,000", "₹75,000", "₹5,00,000", "₹35,000"]

# ---------------------------------------------------------------------------
# SCAM TEMPLATES (grouped by scam_type)
# ---------------------------------------------------------------------------

templates_digital_arrest = [
    "This is {officer} from {agency}. A parcel addressed to you containing {item} has been intercepted at Mumbai Customs. You are required to stay on this video call or you will be digitally arrested immediately.",
    "Sir/Madam, your Aadhaar number has been used in a money laundering case under investigation by {agency}. Do not disconnect this call, you are under digital arrest until further verification.",
    "We are issuing a digital arrest warrant against {name} under Section 420 IPC. Stay on this video call with your camera on or local police will arrest you within 1 hour.",
    "This call is being recorded by {agency} Cyber Crime Cell. Your bank account is linked to a terror funding case. You must remain on video call till the investigation report is generated, or face digital arrest.",
    "Attention {name}, as per Supreme Court order your case file is open under {agency}. You cannot leave this call, switch off your phone, or contact anyone. This is a digital arrest procedure.",
    "Your mobile number is linked to an FIR registered in {agency}. To avoid physical arrest, you must cooperate on this video call and transfer {amount} for 'verification' immediately.",
]

templates_courier_parcel = [
    "Hello, this is {courier} customer care. A package booked in your name contains {item} and has been seized by customs. Press 1 to speak to a cyber crime officer or your number will be blocked.",
    "Your parcel sent via {courier} to Taiwan has been flagged by Narcotics Control Bureau as it contains {item}. Connecting you to {agency} now, please do not hang up.",
    "Dear customer, your {courier} shipment is on hold due to illegal items detected: {item}. Cyber cell has been notified. Failure to respond in 30 minutes will lead to digital arrest.",
]

templates_bank_freeze = [
    "Dear customer, your {bank} account will be frozen by RBI in 2 hours due to suspicious transaction of {amount}. Connect to our verification officer on video call immediately to avoid digital arrest.",
    "This is {officer} from {bank} fraud department. Your account is under investigation by {agency}. Share OTP or stay on this call to prevent permanent suspension and legal action.",
    "Alert: KYC mismatch detected on your {bank} account linked to a money laundering probe by {agency}. Video verification required now, non-compliance will result in arrest.",
]

templates_tax_legal = [
    "This is {officer}, {agency}. A non-bailable warrant has been issued in your name for tax evasion of {amount}. You must settle this on call right now or be digitally arrested before evening.",
    "Notice: {name}, your PAN card has been used for an illegal transaction of {amount}. {agency} requires you to join this video call for instant verification to avoid arrest.",
    "Your name appears in a SIM card fraud case registered with {agency}. As per protocol you are under digital arrest till the matter is resolved over this video call.",
]

scam_template_groups = {
    "digital_arrest_general": templates_digital_arrest,
    "courier_parcel_scam": templates_courier_parcel,
    "bank_account_freeze": templates_bank_freeze,
    "tax_legal_threat": templates_tax_legal,
}

# ---------------------------------------------------------------------------
# LEGITIMATE / BENIGN TEMPLATES
# ---------------------------------------------------------------------------

templates_legit = [
    "Hi {name}, just confirming our meeting tomorrow at 10 AM at the office. Let me know if that still works.",
    "Your {bank} OTP for transaction of {amount} is 482910. Valid for 10 minutes. Do not share this OTP with anyone.",
    "Dear {name}, your {courier} order #45213 has been delivered. Thank you for shopping with us.",
    "Reminder: Your electricity bill of {amount} is due on 28th. Pay via the official app to avoid late fee.",
    "Hey, are we still on for dinner this Saturday? Let me know the restaurant you picked.",
    "Your {bank} statement for this month is ready. You can download it from the mobile app or net banking portal.",
    "Congratulations {name}! Your flight booking to Goa is confirmed. PNR: XJ4827. Check-in opens 24 hours before departure.",
    "Team, please submit the quarterly report by Friday EOD. Reach out if you need an extension.",
    "Your appointment with Dr. Sharma is confirmed for Monday 4 PM at City Hospital.",
    "Thanks for the quick turnaround on the project, really appreciate the effort from the whole team.",
    "Hi {name}, your subscription renewal of {amount} was processed successfully. Receipt attached.",
    "Just a heads up, the school PTM has been rescheduled to next Tuesday at 9 AM.",
    "Your {bank} credit card bill of {amount} is generated. Due date is the 5th of next month.",
    "Hello, this is a reminder that your gym membership renewal is due next week.",
    "Hi {name}, the documents you requested have been emailed to you. Please check your inbox.",
]

channels_scam = ["call_transcript", "call_transcript", "sms", "whatsapp"]
channels_legit = ["sms", "email", "whatsapp"]


def random_case_ref():
    prefixes = ["FIR", "CASE", "REF", "CC", "ECIR"]
    return f"{random.choice(prefixes)}/{random.randint(1000,9999)}/{random.choice(['2024','2025','2026'])}"


def fill(template):
    base = template.format(
        name=random.choice(names),
        agency=random.choice(agencies),
        item=random.choice(parcel_items),
        officer=random.choice(fake_officer_names),
        bank=random.choice(banks),
        courier=random.choice(courier_companies),
        amount=random.choice(amounts),
    )
    return base


def add_variation(text, is_scam):
    """Append small randomized detail so near-duplicate template fills become unique."""
    if is_scam:
        extras = [
            f" Case reference: {random_case_ref()}.",
            f" Reference number: {random.randint(100000,999999)}.",
            f" You have {random.choice([10,15,20,30,45,60])} minutes to respond.",
            f" Contact officer ID {random.randint(1000,9999)} for verification.",
            "",
        ]
    else:
        extras = [
            f" Ticket ID: {random.randint(10000,99999)}.",
            f" Ref: {random_case_ref()}.",
            "",
            "",
        ]
    return text + random.choice(extras)


def generate_dataset(n_total=1000, scam_ratio=0.55):
    n_scam = int(n_total * scam_ratio)
    n_legit = n_total - n_scam

    rows = []

    # Generate scam samples, cycling through scam types evenly
    scam_types = list(scam_template_groups.keys())
    for i in range(n_scam):
        scam_type = scam_types[i % len(scam_types)]
        template = random.choice(scam_template_groups[scam_type])
        text = add_variation(fill(template), is_scam=True)
        channel = random.choice(channels_scam)
        rows.append({
            "text": text,
            "is_scam": 1,
            "scam_type": scam_type,
            "channel": channel,
        })

    # Generate legit samples
    for i in range(n_legit):
        template = random.choice(templates_legit)
        text = add_variation(fill(template), is_scam=False)
        channel = random.choice(channels_legit)
        rows.append({
            "text": text,
            "is_scam": 0,
            "scam_type": "none",
            "channel": channel,
        })

    random.shuffle(rows)
    return rows


def main():
    rows = generate_dataset(n_total=1400, scam_ratio=0.55)

    # Deduplicate while preserving order (templates + slot-filling can repeat)
    seen = set()
    unique_rows = []
    for r in rows:
        key = r["text"]
        if key not in seen:
            seen.add(key)
            unique_rows.append(r)

    unique_rows = unique_rows[:1000]

    out_path = "/home/claude/digital_arrest_scam_dataset.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "is_scam", "scam_type", "channel"])
        writer.writeheader()
        writer.writerows(unique_rows)

    print(f"Total unique rows written: {len(unique_rows)}")
    print(f"Scam rows: {sum(1 for r in unique_rows if r['is_scam']==1)}")
    print(f"Legit rows: {sum(1 for r in unique_rows if r['is_scam']==0)}")


if __name__ == "__main__":
    main()

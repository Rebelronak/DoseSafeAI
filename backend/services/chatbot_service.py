def generate_chatbot_response(question, context):
    """
    Simple rule-based chatbot for patient-friendly explanations.
    context: may include 'interactions', 'warnings', 'medicines'
    """
    # If there are interactions or warnings, explain them
    interactions = context.get('interactions', [])
    warnings = context.get('warnings', [])
    medicines = context.get('medicines', [])

    if interactions:
        msg = []
        for i in interactions:
            msg.append(f"❗ {i['drug1'].title()} and {i['drug2'].title()} may cause {i['note']} (Severity: {i['severity']}).")
        return " ".join(msg)
    if warnings:
        msg = []
        for w in warnings:
            msg.append(f"⚠️ {w['drug']} warning: {w['warning']}. {w['note']}")
        return " ".join(msg)
    if medicines:
        med_names = ', '.join([m['name'] for m in medicines])
        return f"You are taking: {med_names}. Please consult your doctor for more information."
    # Fallback
    return "I'm here to help with your prescription questions. Please upload your prescription or ask about a specific medicine."
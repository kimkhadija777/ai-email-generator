# ============================================================
# AI EMAIL GENERATOR
# Streamlit + Groq
# ============================================================

import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="📧",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: gray;
    font-size: 18px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<p class="main-title">📧 AI Email Generator</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Create professional emails using AI and Groq</p>',
    unsafe_allow_html=True
)


# ============================================================
# GET GROQ API KEY FROM STREAMLIT SECRETS
# ============================================================

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

except Exception:
    st.error("❌ GROQ_API_KEY was not found in Streamlit Secrets.")
    st.info("Please add your Groq API key in Streamlit Cloud Secrets.")
    st.stop()


# ============================================================
# INITIALIZE GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# AVAILABLE MODELS
# ============================================================

MODELS = {
    "GPT-OSS 120B": "openai/gpt-oss-120b",
    "Qwen 3.6 27B": "qwen/qwen3-27b"
}


# ============================================================
# EMAIL GENERATION FUNCTION
# ============================================================

def generate_email(
    email_type,
    recipient_name,
    recipient_relation,
    purpose,
    tone,
    sender_name,
    additional_details,
    model_name
):

    model_id = MODELS[model_name]

    # Validation
    if not purpose or purpose.strip() == "":
        return None, "Please enter the purpose of your email."

    # Handle empty fields
    if not recipient_name.strip():
        recipient_name = "Recipient"

    if not recipient_relation.strip():
        recipient_relation = "Not specified"

    if not sender_name.strip():
        sender_name = "Sender"

    if not additional_details.strip():
        additional_details = "No additional details provided."

    # ========================================================
    # AI PROMPT
    # ========================================================

    prompt = f"""
You are an expert professional email writing assistant.

Generate a complete, clear, natural, and human-like email.

EMAIL INFORMATION:

Email Type: {email_type}

Recipient Name: {recipient_name}

Recipient Role or Relationship: {recipient_relation}

Purpose:
{purpose}

Tone:
{tone}

Sender Name:
{sender_name}

Additional Details:
{additional_details}

INSTRUCTIONS:

1. Generate a clear and relevant subject line.
2. Write a complete email body.
3. Match the requested tone.
4. Use the recipient information appropriately.
5. Include all important information from the purpose and additional details.
6. Keep the email natural and human-like.
7. Do not add explanations outside the email.
8. Return only the final email in this format:

Subject: [Generated Subject]

Dear [Recipient Name],

[Email Body]

Best regards,
[Sender Name]
"""

    try:

        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert email writer who creates "
                        "professional, clear, natural, and well-structured emails."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_completion_tokens=1000
        )

        generated_email = response.choices[0].message.content

        return generated_email, None

    except Exception as e:

        return None, str(e)


# ============================================================
# INPUT FORM
# ============================================================

with st.form("email_form"):

    st.subheader("✍️ Enter Email Details")

    email_type = st.selectbox(
        "📌 Email Type",
        [
            "Professional",
            "Job Application",
            "Meeting Request",
            "Follow-up",
            "Thank You",
            "Complaint",
            "Leave Request",
            "Apology",
            "Custom"
        ]
    )

    recipient_name = st.text_input(
        "👤 Recipient Name",
        placeholder="Example: Mr. Ahmed"
    )

    recipient_relation = st.text_input(
        "🏢 Recipient Role / Relationship",
        placeholder="Example: HR Manager, Professor, Client"
    )

    purpose = st.text_area(
        "📝 Email Purpose / Topic",
        placeholder="Explain what you want to write about...",
        height=120
    )

    tone = st.selectbox(
        "🎭 Email Tone",
        [
            "Professional",
            "Formal",
            "Friendly",
            "Polite",
            "Casual"
        ]
    )

    sender_name = st.text_input(
        "✍️ Your Name",
        placeholder="Enter your name"
    )

    additional_details = st.text_area(
        "➕ Additional Details",
        placeholder="Add any important information you want included...",
        height=120
    )

    model_name = st.selectbox(
        "🤖 Groq AI Model",
        list(MODELS.keys())
    )

    submitted = st.form_submit_button(
        "✨ Generate Email",
        use_container_width=True
    )


# ============================================================
# GENERATE EMAIL
# ============================================================

if submitted:

    if not purpose.strip():

        st.warning(
            "⚠️ Please enter the purpose or topic of your email."
        )

    else:

        with st.spinner("🤖 AI is generating your email..."):

            generated_email, error = generate_email(
                email_type,
                recipient_name,
                recipient_relation,
                purpose,
                tone,
                sender_name,
                additional_details,
                model_name
            )

        if error:

            st.error("❌ Email generation failed.")
            st.code(error)

        else:

            st.success("✅ Your email has been generated!")

            st.subheader("📧 Generated Email")

            st.text_area(
                "Your AI Generated Email",
                value=generated_email,
                height=400
            )

            st.download_button(
                label="⬇️ Download Email as TXT",
                data=generated_email,
                file_name="generated_email.txt",
                mime="text/plain",
                use_container_width=True
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    "<center>Built with ❤️ using Streamlit and Groq AI</center>",
    unsafe_allow_html=True
)

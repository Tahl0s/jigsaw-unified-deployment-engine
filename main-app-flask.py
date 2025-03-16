import os
import sys
import subprocess
import datetime
import ntplib
from time import ctime

try:
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-ollama", "langchain-core"])
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate

from flask import Flask, render_template, request, jsonify

# === Setup Flask and Memory File Paths === #
app = Flask(__name__)

# Define directory to store memory files.
MEMORY_DIR = "memory"
if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)

# File paths for conversation, personality, and long-term memory (stored in the MEMORY_DIR).
CHAT_LOG_PATH = os.path.join(MEMORY_DIR, "chat_log.txt")
CHAT_SUMMARY_PATH = os.path.join(MEMORY_DIR, "chat_summary.txt")
PERSONALITY_PATH = os.path.join(MEMORY_DIR, "personality.txt")
LT_SUMMARY_HISTORY_PATH = os.path.join(MEMORY_DIR, "lt_summary_history.txt")
LONG_TERM_MEMORY_PATH = os.path.join(MEMORY_DIR, "long_term_memory.txt")

# Config
MAX_CHAT_LOG_LINES = 20          # How many lines to keep before summarizing
SUMMARY_DELIMITER = "\n####\n"   # Unique delimiter to separate summaries

# === Default content for memory-related files (excluding personality) === #
# Personality is not reset; its default value is applied only if it doesn't exist.
TEMPLATE_FILES = {
    CHAT_LOG_PATH: "",
    CHAT_SUMMARY_PATH: "",
    LT_SUMMARY_HISTORY_PATH: "",
    LONG_TERM_MEMORY_PATH: ""
}

# Create missing files.
if not os.path.exists(PERSONALITY_PATH):
    with open(PERSONALITY_PATH, "w", encoding="utf-8") as f:
        f.write("Friendly, concise, and informative.")
for filepath, default_content in TEMPLATE_FILES.items():
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(default_content)

# === Helper File Functions === #
def load_file(file_path, default=""):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    return default

def save_file(file_path, content, mode="w"):
    with open(file_path, mode, encoding="utf-8") as file:
        file.write(content)

def append_to_file(file_path, content):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)

def load_chat_log():
    return load_file(CHAT_LOG_PATH, "")

def save_chat_log(user_input, ai_response):
    log_entry = f"User: {user_input}\nAI: {ai_response}\n"
    append_to_file(CHAT_LOG_PATH, log_entry)

# === Summarization Functions === #
def summarize_chat():
    chat_log = load_chat_log()
    if chat_log:
        summary_prompt = f"Summarize this conversation:\n{chat_log}"
        summary = model.invoke(summary_prompt)
        save_file(CHAT_SUMMARY_PATH, summary)
        history = load_file(LT_SUMMARY_HISTORY_PATH)
        new_history = history + SUMMARY_DELIMITER + summary if history else summary
        save_file(LT_SUMMARY_HISTORY_PATH, new_history)
        update_long_term_memory()

def update_long_term_memory():
    history = load_file(LT_SUMMARY_HISTORY_PATH)
    if not history:
        return
    summaries = [s.strip() for s in history.split(SUMMARY_DELIMITER) if s.strip()]
    if len(summaries) >= 5:
        five_summaries = "\n\n".join(summaries[-5:])
        condense_prompt = f"Condense the following 5 conversation summaries into one coherent long-term memory summary:\n\n{five_summaries}"
        condensed_summary = model.invoke(condense_prompt)
        save_file(LONG_TERM_MEMORY_PATH, condensed_summary)
        remaining_summaries = summaries[:-5]
        new_history = SUMMARY_DELIMITER.join(remaining_summaries)
        save_file(LT_SUMMARY_HISTORY_PATH, new_history)

# === Memory Purge Function (Excluding Personality) === #
def purge_memory():
    """
    Resets all memory-related files except the personality file.
    """
    for filepath, default_content in TEMPLATE_FILES.items():
        save_file(filepath, default_content)
    print("Memory files (chat log, chat summary, etc.) have been purged.")

# === Time Handling (NTP) === #
def get_ntp_time():
    client = ntplib.NTPClient()
    try:
        response = client.request('pool.ntp.org', version=3, timeout=2)
        return ctime(response.tx_time)
    except Exception:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# === Topic Switching Function === #
def handle_topic_switch(user_input):
    end_keywords = {'exit', 'quit', 'stop', 'done', 'no more'}
    switch_keywords = {"let's talk about something else", "change subject", "new topic"}
    lower_input = user_input.lower()
    if any(keyword in lower_input for keyword in end_keywords):
        return "Goodbye!", True
    elif any(keyword in lower_input for keyword in switch_keywords):
        return "Got it! Let's talk about something else.", False
    return None, False

# === AI Model and Prompt Setup === #
TEMPLATE = """
You are Jude or J.U.D.E, an AI with the following personality traits:

{personality}

Do not refer to yourself in the 3rd person.
Follow the conversation.
Reply in short if asked something simple.
Answer questions concisely.
Communicate like a human.
If stuck in a loop or unsure as to what the user is asking, ask for specification.
Don't ask an excessive amount of questions.
Don't introduce yourself in every answer unless the user greets you.
You do not always have to reflect on everything in the previous message.
You do not always have to list references with examples being "I'm glad you shared x"

**Current Date and Time:** {current_time}

**Memory from previous conversations:**
{summary}

**Recent conversation history:**
{context}

**User's Question:** {question}

**Your response:""
"""
prompt = ChatPromptTemplate.from_template(TEMPLATE)
model = OllamaLLM(model="llama3")
chain = prompt | model

# === Flask Routes === #
@app.route("/")
def index():
    # Render the index template.
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"].strip()
    message, end_conversation = handle_topic_switch(user_input)
    if end_conversation:
        return jsonify({"message": message})

    personality = load_file(PERSONALITY_PATH, "Friendly, concise, and informative.")
    summary = load_file(CHAT_SUMMARY_PATH, "No prior knowledge available.")
    context = load_chat_log()
    current_time = get_ntp_time()

    result = chain.invoke({
        "personality": personality,
        "summary": summary,
        "context": context,
        "question": user_input,
        "current_time": current_time,
    })

    save_chat_log(user_input, result)
    if sum(1 for _ in open(CHAT_LOG_PATH, encoding="utf-8")) >= MAX_CHAT_LOG_LINES:
        summarize_chat()

    return jsonify({"message": result.replace("\n", "<br>")})

# New route to purge memory (excluding personality)
@app.route("/purge", methods=["POST"])
def purge():
    try:
        purge_memory()  # Function that clears chat history files
        return jsonify({"message": "Memory purged successfully (except personality)."})
    except Exception as e:
        return jsonify({"message": f"Failed to purge memory: {e}"}), 500

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)

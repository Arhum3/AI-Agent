import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import re

# Configure Gemini API
genai.configure(api_key="<API Key>")

# Load knowledge base
def load_knowledge_base():
    return {
        "What are your working hours?": "Our working hours are from 9 AM to 6 PM, Monday to Friday.",
        "Do you offer international flights?": "Yes, we offer international flights to multiple destinations worldwide.",
        "How can I cancel my booking?": "You can cancel your booking by visiting our website or calling our support line.",
        "Do you provide hotel bookings?": "Yes, we offer hotel bookings along with flight reservations."
    }

# Text-to-Speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Speech-to-Text (Listens until the user stops speaking)
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... (Speak or remain silent to end)")

        try:
            # Wait for the first phrase, then timeout if silence > 10s
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            print("Silence detected. Ending call.")
            return None  # Indicate end of conversation
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Sorry, I'm having trouble understanding right now."


# Get AI response from Gemini API
def get_ai_response(user_input, knowledge_base):
    knowledge_text = "\n".join([f"Q: {k}\nA: {v}" for k, v in knowledge_base.items()])

    model = genai.GenerativeModel("gemini-2.0-flash")
    chat = model.start_chat(history=[])

    prompt = f"""
    You are an AI travel assistant helping customers book flights and hotels.
    Here is some knowledge to assist users:
    
    {knowledge_text}
    
    User: {user_input}
    """

    response = chat.send_message(prompt)
    cleaned_response = re.sub(r'[*_`]', '', response.text.strip())  # Remove special characters
    return cleaned_response

# Main function to run the agent
def main():
    knowledge_base = load_knowledge_base()
    text_to_speech("Hello! Welcome to ABC Travels. How can I assist you today?")
    
    while True:
        user_input = speech_to_text()
        if user_input is None:
            text_to_speech("Call ended due to inactivity. Goodbye!")
            break

        print(f"User: {user_input}")

        if "exit" in user_input.lower():
            text_to_speech("Thank you for calling. Have a great day!")
            break

        response = get_ai_response(user_input, knowledge_base)
        print(f"AI: {response}")
        text_to_speech(response)

if __name__ == "__main__":
    main()

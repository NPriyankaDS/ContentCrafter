from dotenv import load_dotenv
import streamlit as st
from langflow.load import run_flow_from_json
import pythoncom  # Required for COM initialization on Windows
import pyttsx3
import tempfile
import os

# # Load environment variables from .env file
# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# SERPER_API_KEY =os.getenv("SERPER_API_KEY")
st.set_page_config(page_title="ContentCrafter", page_icon="📜")
# Load CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS styles
load_css()

def about_page():
    col1, col2 = st.columns([1, 5])  # Adjust column width proportions as needed
    with col1:
        st.image("static/logo_2.png", width=500)  # Replace with your logo file and adjust width
    with col2:
        st.title("ContentCrafter - About & How to Use")
    st.divider()
    st.markdown("""
    ## 📃Introduction
    ContentCrafter is an AI-powered tool developed using langflow that helps you create high-quality blog content effortlessly. 
    Simply enter a topic, and our app generates a blog post for you. The content is fetched using the Google Serper tool which searches the google websites.
    Additionally, you can listen to your blog content using the text-to-speech feature.

    ## 📌How to Use
    1. **Enter your API keys**: In the sidebar, enter your API keys for Groq and Serper dev.
    2. **Enter a Topic**: Type in the topic you want to write about.
    3. **Generate Blog**: Click the "Generate Blog" button. The app will process your request and generate a blog post based on your topic.
    4. **Listen to the Blog**: Once the blog is generated, you can listen to it by clicking the audio player that appears.
    5. **Download the Blog**: If you prefer to save your blog content, you can download it as a text file.

    ## 🧩Features
    - **AI-Generated Blog Posts**: Generate high-quality, well-structured blog posts in just a few clicks.
    - **Text-to-Speech**: Listen to your blog content with the text-to-speech feature.
    - **Download Option**: Download your generated blog post as a text file.
    
    ## 🔗Technologies and Tools Used
    Our application is powered by cutting-edge technologies to ensure a seamless and intelligent experience:

    1. **Langflow**: Orchestrates a series of AI agents for smooth task execution.
    2. **Groq API (Llama3-70B)**: Generates high-quality, context-aware text.
    3. **Serper API**: Fetches data to enrich the content with relevant information.
    4. **Streamlit**: Provides an easy-to-use interface for interaction.
    5. **Python Libraries**: A mix of powerful libraries, including dotenv, for environment management and pyttsx3 for text-to-speech functionality.

    ## 💡FAQs
    **Q: What happens if my topic doesn't generate a blog?**  
    A: Make sure the topic is relevant and descriptive. If it still doesn't work, try rephrasing your input.

    **Q: Can I generate more than one blog post?**  
    A: Currently, the app is designed to generate one blog post at a time based on the topic you provide.

    ## 🖋Contact or Feedback
    If you have any questions or feedback, feel free to contact us at [Priyanka N](mailto:nprinka235@gmail.com) and [Sabiha Anjum](mailto:sabihaanjum067@gmail.com).
    """)

def ask_ai(topic):
    TWEAKS = {
        "GroqModel-NucS9": {
        "groq_api_base": "https://api.groq.com",
        "groq_api_key": GROQ_API_KEY,
        "input_value": "",
        "max_tokens": None,
        "model_name": "llama3-70b-8192",
        "n": None,
        "stream": True,
        "system_message": "",
        "temperature": 0.1
        },
    
        "TextInput-KCZ3t": {
            "input_value": topic
        },
        "GoogleSerperAPI-TM8V4": {
            "input_value": "",
            "k": 4,
            "serper_api_key": SERPER_API_KEY
        }
    }

    result = run_flow_from_json(flow="Blog_creation.json",
                                input_value="message",
                                fallback_to_env_vars=True, # False by default
                                tweaks=TWEAKS)
    return result

def text_to_speech(text):
    # Initialize COM for the current thread
    pythoncom.CoInitialize()
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    
    # Save the speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        temp_file_path = temp_file.name
    
    # Set properties if needed (optional)
    engine.save_to_file(text, temp_file_path)
    engine.runAndWait()
    
    return temp_file_path

# Run the Streamlit app
if __name__ == "__main__":
    st.sidebar.title("Welcome")
    st.sidebar.image("static/logo_2.png", caption="Blogging Made Effortless", use_container_width=True)  # Add logo to sidebar
    page = st.sidebar.radio("Choose a page", ["Home", "About"])
    if page == "Home":
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image("static/logo_2.png", width=500)
        with col2:
            st.title("ContentCrafter")
            st.markdown("<h3 style='text-align: center;'>Blogging Made Effortless</h3>", unsafe_allow_html=True)
        # Input for API keys
        with st.sidebar:
            GROQ_API_KEY = st.text_input(label = "**Groq API key**", placeholder="Ex gsk-2twmA8tfCb8un4...",
                key ="groq_api_key_input", help = "How to get a Groq api key: Visit https://console.groq.com/login", type="password")
            SERPER_API_KEY =st.text_input(label = "**Serper API key**", placeholder="Ex 1hdjkjkda......",
                key="serper_api_key_input", help = "How to get a Serper API key: Visit https://serper.dev/", type="password")
        # Store API keys in session state for persistence
        if GROQ_API_KEY:
            st.session_state["GROQ_API_KEY"] = GROQ_API_KEY
        if SERPER_API_KEY:
            st.session_state["SERPER_API_KEY"] = SERPER_API_KEY
        # Check if both API keys are provided
        if "GROQ_API_KEY" not in st.session_state or "SERPER_API_KEY" not in st.session_state:
            st.info("Please enter both your GROQ API key and Serper API key in the sidebar to continue.")
        else:
            st.sidebar.info("API keys successfully loaded! Ready to proceed.")   
            # Input message from user
            with st.sidebar:    
                topic = st.text_input("Enter the topic:")
                
                button = st.button("Generate Blog")
            # Button to run the flow
            if button:
                if topic:
                    try:
                        with st.spinner("Crafting Content for you... Please wait."):
                            # Run the flow from JSON
                            result = ask_ai(topic)
                            # Extract the result
                    
                            outputs = result[0].outputs
                            result_data = outputs[0]  # Access the first ResultData object
                            message = result_data.results["message"]  # Extract the 'message' key from results
                            message_data = message.data  # Access the 'data' dictionary
                            text = message_data["text"]  # Retrieve the 'text' value

                            # Display the result
                            st.subheader("Generated Blog Content:")
                            st.markdown(text)
                            st.download_button(label="Download the blog post", data=text, file_name="blog_post.txt")

                            # Provide text-to-speech functionality
                            audio_file = text_to_speech(text)
                            st.audio(audio_file, format='audio/wav')

                    except Exception as e:
                        error_message = str(e)
                        if "Invalid API Key" in error_message or "401" in error_message:
                            st.error("Invalid API Key. Please check your credentials.")
                            st.rerun()
                        else:
                            st.error(f"An unexpected error occurred: {error_message}")
                            st.rerun()  # Stop further execution if there's an error
                else:
                    st.info("Please enter a topic before generating the blog.")
            else:
                st.info("Click on the generate button")        

    elif page == "About":
        about_page()  # Call the about page function

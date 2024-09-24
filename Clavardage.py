import streamlit as st
import urllib.request
import json
import os
import re
import ssl

st.set_page_config(
    page_title="Clavardage",
    page_icon="👋",
)
# Azure Endpoint Key
api_key = st.secrets.credentials.api_key

def make_urls_clickable(text):
    # Regex to detect markdown-style links [text](url)
    markdown_link_pattern = r'\[([^\]]+)\]\((https?://[^\s)]+)\)'
    
    # Replace markdown-style links with actual HTML anchor tags
    return re.sub(markdown_link_pattern, r'<a href="\2" target="_blank">\1</a>', text)

def transform_chat_history_keys(streamlit_history):
    transformed_history = []
    
    for entry in streamlit_history:
        transformed_entry = {
            'inputs': {
                'chat_input': entry['inputs']['question']
            },
            'outputs': {
                'chat_output': entry['outputs']['answer']
            }
        }
        transformed_history.append(transformed_entry)
    
    return transformed_history

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def main():
    allowSelfSignedHttps(True)


    #with st.popover("Open popover"):
        

    # Start of the outer frame using a Streamlit container


    with st.expander("**Clavardage**",expanded=True,icon=":material/chat:"):
        #st.markdown('<div class="outer-frame">', unsafe_allow_html=True)
        if st.button("🗘 Nouvelle conversation"):
            st.session_state.chat_history = []  # Reset chat history
            st.session_state.chat_history.append({
                "inputs": {"question": ""},
                "outputs": {"answer": "Bonjour, Comment puis-je vous aider aujourd'hui? Sélectionnez un sujet ou écrivez votre question 😊"}
            })
            st.session_state.first_interaction = True  # Restart first interaction
            st.session_state.user_input = ""  # Clear any existing input
        if "first_interaction" not in st.session_state:
            st.session_state.first_interaction = True

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            st.session_state.chat_history.append({
                "inputs": {"question": ""},
                "outputs": {"answer": "Bonjour, Comment puis-je vous aider aujourd'hui? Sélectionnez un sujet ou écrivez votre question 😊"}
            })
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        # Add a "New Conversation" button at the top



        col1, col2 = st.columns([1, 5])
        
        with col1:
            st.image("https://i.imgur.com/JyPrR9l.png", width=80)   # Load and display the logo from the new URL
            
        with col2:
            st.markdown("<h1 style='color:#005EB8; margin-top: 0; padding-top: 0;'>Assistant Virtuel Municipal</h1>", unsafe_allow_html=True)
        
        # Custom CSS to style the chat and remove the form border
        st.markdown("""
        <style>
        .outer-frame {
            border: 2px solid #005EB8; /* Frame border color */
            border-radius: 15px;
            padding: 20px;
            margin: 20px auto;
            background-color: white; /* Optional: background color for the outer frame */
            max-width: 800px; /* Optional: max-width for the frame */
        }
        .chat-container {
            background-color: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .user-message {
            background-color: #0054A6;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-size: 16px;
            width: 60%;
            text-align: left;
            float: right; 
            clear: both;
        }
        .assistant-message  {
            background-color: #E6E7E8;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-size: 16px;
            width: 60%;
            text-align: left;
            float: left; 
            clear: both;
        }
        /* Flexbox container to align input and button */
        .input-container {
            display: flex;
            align-items: center;
        }
        /* Custom styling for the text input and submit button */
        .stTextInput input {
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 10px;
            border: none;
            box-shadow: none;
            outline: none;
            width: 100%;
            height: 44px;
            margin-right: 10px;
        }
        .stForm .stButton button {
            background-color: #005EB8;
            color: white;
            border: none;
            font-size: 18px;
            height: 44px;
            padding: 0 20px;
            border-radius: 10px;
            cursor: pointer;
        }

        </style>
        """, unsafe_allow_html=True)


        # Display predefined options only for the first interaction
        for interaction in st.session_state.chat_history:
            if interaction["inputs"]["question"]:
                st.markdown(f"<div class='user-message'><strong></strong> {interaction['inputs']['question']}</div>", unsafe_allow_html=True)
            if interaction["outputs"]["answer"]:
                answer_with_links = make_urls_clickable(interaction["outputs"]["answer"].replace('$','Dollars CAD'))
                st.markdown(f"<div class='assistant-message'>{answer_with_links}</div>", unsafe_allow_html=True)


        # Clear floats after messages to avoid layout issues
                st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

        if st.session_state.first_interaction:
            st.markdown("""
                <style>

                div.stButton > button {
                    width: 200px;  /* Apply the same width to all buttons */
                    height: 60px;  /* Apply the same width to all buttons */
                }
                </style>
            """, unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Calendrier des collectes", on_click=handle_option_selection, args=("Calendrier des collectes",))
            with col2:
                st.button("Assermentation", on_click=handle_option_selection, args=("Assermentation",))
            with col3:
                st.button("Opérations déneigement", on_click=handle_option_selection, args=("Opérations d'entretien sur le déneigement",))
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Écocentre", on_click=handle_option_selection, args=("Écocentre",))
            with col2:
                st.button("Bac brisé", on_click=handle_option_selection, args=("Bac brisé",))
            with col3:
                st.button("Coupure d'eau", on_click=handle_option_selection, args=("Coupure d'eau",))
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)






            
        # Display input field and send button
        col3, col4 = st.columns([12, 5])
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        with col3:
            st.text_input("Écrivez un message", placeholder="Écrivez un message...", key="user_input", label_visibility="collapsed")
        with col4:
            st.button("➤", key="send_button", on_click=submit_input,help="Envoyer le message")
        st.markdown('</div>', unsafe_allow_html=True)





def submit_input():
    user_input = st.session_state.user_input
    if user_input:
        # Process the user input
        handle_option_selection(user_input)
        # Clear the input after submission by resetting the session state variable
        st.session_state.user_input = ""  # Clear the input for the next round

def handle_option_selection(option):
    # Disable the predefined options after the first interaction
    st.session_state.first_interaction = False

    # Display the selected option or user input in the chat
    st.session_state.chat_history.append({
        "inputs": {"question": option},
        "outputs": {"answer": ""}
    })

    send_request_to_custom_api(option)

def send_request_to_custom_api(user_input):
    # Prepare data for the API request
    with st.spinner('Nous acheminons votre requête ...'):
        chat_history_formatted = transform_chat_history_keys(st.session_state.chat_history)
        data = {"chat_history": chat_history_formatted, 'chat_input': user_input}
        body = json.dumps(data).encode('utf-8')
        
        url = st.secrets.credentials.url
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}

        # Create the request object
        req = urllib.request.Request(url, body, headers)
        try:
            # Send the request and get the response
            response = urllib.request.urlopen(req)
            response_data = json.loads(response.read().decode('utf-8'))
            

            # Extract the assistant's response
            answer = response_data.get('chat_output', "No answer provided")
            st.session_state.chat_history[-1]["outputs"]["answer"] = answer

        except urllib.error.HTTPError as error:
            # Handle HTTP errors
            #st.error(f"The request failed with status code: {error.code}")
            #st.text(error.read().decode("utf8", 'ignore'))
            st.error("Oups ! Il semble que le filtre Microsoft a détecté du contenu inapproprié dans votre question. Veuillez reformuler votre question ou demander des informations sur le périmétre du POC. Merci ! ")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_link__qRIco {visibility: hidden;}  /* This should target the footer specifically */
    .stAppViewMain main st-emotion-cache-bm2z3a ea3mdgi8 {visibility: hidden;}  /* This should target the footer specifically */

    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
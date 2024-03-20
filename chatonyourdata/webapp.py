import streamlit as st
from streamlit_option_menu import option_menu
import random
import time
import os
from openai import AzureOpenAI
import json
from chatonyourdata import *
import base64
from azure.storage.blob import BlobServiceClient
import urllib
# from streamlit_float import *

# float_init(theme=True, include_unstable_primary=False)

with st.sidebar:
    menu_index = ['Home', 'References', 'Settings', 'Upload file', 'Chat']
    menu_icons = ['house', 'list-task',  'gear', 'cloud-upload',  'chat', ]
    selected = option_menu("Main Menu",menu_index, icons=menu_icons, menu_icon="cast", default_index=0)

# Streamed response emulator
def response_generator(value):

    print('make request')
    references = []
    blah = ChatOnYourData(index="good-vector", role="test-role")
    #content, references  = blah.make_request(value)
    content, references  = blah.make_request2(value, st.session_state.messages)
    st.session_state.references = []
    for x in references:
        st.session_state.references.append(x)
    return content

if selected == 'Settings':
    st.title("Settings")
    st.write("Settings page")
    if st.button('Clear Chat history'):
        st.write('Clear Chat History & References')
        st.session_state.messages = []
        st.session_state.references = []



if selected == 'Home':
    st.title("Simple chat")
    
    blah = ChatOnYourData(index="good-vector", role="test-role")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "references" not in st.session_state:
        st.session_state.references = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Float the footer container and provide CSS to target it with
    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                data   = response_generator(prompt)
            st.markdown(data)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": data})


if selected == 'References':
        st.title("References")

        if len(st.session_state.references) == 0:
            st.write("No references found")
        else:
            for x in st.session_state.references:
                file = x
                #file = x + "?sp=r&st=xxxxx"
                #print(file)
                st.write("Reference: ")
                #file = "https://storagename.blob.core.windows.net/good-raw-splits/container/fish_0.pdf?sp=r&st=xxxxx"
                with urllib.request.urlopen(file) as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

                # Embedding PDF in HTML
                pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="950" type="application/pdf"></iframe>'

                # Displaying File
                st.markdown(pdf_display, unsafe_allow_html=True)

if selected == 'Upload file':      
    st.subheader("DocumentFiles")
    docx_file = st.file_uploader("Upload Document", type=["pdf","docx","txt"])  

    if docx_file is not None:
        # TO See details
        file_details = {"filename":docx_file.name, "filetype":docx_file.type,
                              "filesize":docx_file.size}
        st.write(file_details)

        if docx_file.type == "text/plain":
		    # Read as string (decode bytes to string)
            raw_text = str(docx_file.read(),"utf-8")
            st.text(raw_text)

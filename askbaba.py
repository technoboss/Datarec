import streamlit as st
from streamlit_chat import message
import openai
from  PIL import Image
from settings import API_KEY

# Set GPT-3 API Key
openai.api_key = API_KEY 
# Defining a function to generate calls from the API
def generate_response(prompt):
    completions = openai.Completion.create (
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    message = completions.choices[0].text
    return message

def main():
    # Set a Title
    st.title("👽 Baba, your virtual :red[**_AI_**].")
    st.markdown(":orange[**_Here, to assist you!_**]")
    with st.expander(":red[**Read more**]"):
        st.markdown(":orange[**Baba**] is your virtual AI assistant.\
                   Don't be shy, you can ask anything to Baba. He will be \
                   very delighted to support you. Please, be as specific as \
                   you can in your questions. Hey smile! this will be :violet[**fun**]🎈.")

    # Initializing streamlit session statement
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    # Defining function to handle user input
    def get_text():
        input_text = st.text_input("You: ","", key="input")
        return input_text 

    # Assigning the function to a variable 
    user_input = get_text()
    
    # Defining a condition to handle the response to the user input 
    if user_input:
        output = generate_response(user_input)
        # adding input and output to a session state
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    # Checking if there is an ouput 
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

if __name__ == '__main__':
    main()
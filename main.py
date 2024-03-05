import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_timeline import timeline
import yaml
from yaml.loader import SafeLoader
from authenticate import Authenticate
from captcha.image import ImageCaptcha
import random, string
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

EXAMPLE_NO = 1

#define constant
length_captcha = 4
width = 200
height = 150



def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        selected = option_menu(
            menu_title = None,  # required
            options=["Home", "Login"],  # required
            icons=["house", "people"],  # optional
            default_index=0,  # optional
            orientation="horizontal"
        )
        return selected

def captcha_control():
    #control if the captcha is correct

    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        st.title("Captcha Control on streamlit")

        #define the session state for control if the captcha is correct
        st.session_state['controllo'] = False
        col1,col2 = st.columns(2)

        #define the session state for the captcha text because it doesn't change
        if 'Captcha' not in st.session_state:
            st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k = length_captcha))
        print("The captcha is:", st.session_state['Captcha'])

        #Setup the captcha widget
        image = ImageCaptcha(width = width, height= height)
        data = image.generate(st.session_state['Captcha'])
        col1.image(data)
        capta2_text = col2.text_area("Enter captcha text", height = 30)

        if st.button("Reload"):
            del st.session_state['controllo']
            st.rerun()

        if st.button("Verify the code"):
            print(capta2_text,st.session_state['Captcha'])
            capta2_text = capta2_text.replace(" "," ")
            #if the captcha is correct, the controllo session state is set to True
            if st.session_state['Captcha'].lower() == capta2_text.lower().strip():
                del st.session_state['Captcha']
                col1.empty()
                col2.empty()
                st.session_state['controllo'] = True
                st.rerun()

            else:
                st.error("Error")
                del st.session_state['Captcha']
                del st.session_state['controllo']
                st.rerun()

        else:
            #Wait for the button click
            st.stop()

selected = streamlit_menu(example=EXAMPLE_NO)



if selected== "Home":
    st.header("Summary")
    st.write("As a DataScientist , my passion is research new technology AI special NLP for application"
             " in industry.I love to learn new things and eager explore them to please my curiosity. With my"
             " passion, I want to dedicate my career to AI for the betterment of the world :technologist:.\n")
    st.header("Projects")
    with st.spinner(text = "Building line"):
        with open('time-line.json', "r") as f:
            data = f.read()
            timeline(data,height = 500)
    st.header('Skills & Tools :hammer_and_pick:')
    col,col2,col3 = st.columns(3)
    with col:
        st.button("DataScience")
        st.button("Python")
        st.button("R")
    with col2:
        st.button("Tableau")
        st.button("Tensorflow")
        st.button("Pytorch")
    with col3:
        st.button("Streamlit")
        st.button("GenAI")

    st.header("Education :open_book:")
    st.subheader("University of Science")

    st.image("hcmus.jpg", width=250)
    st.markdown("Bachelor: DataScience")
    st.header("Achievements :sports_medal:")
    st.markdown("Top 7 coder girl :male-technologist: VNG code tour ")

    st.header("Hobby")
    col4,col5,col6 = st.columns(3)
    with col4:
        st.button("Travel :airplane: :sunglasses:")
    with col5:
        st.button("Music :notes:")
    with col6:
        st.button("Food :sandwich:")


if selected == "Login":
    _RELEASE = True
    #result = ""

    if _RELEASE:
        # Loading config file
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        # Creating the authenticator object
        authenticator = Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )

        # Creating a login widget
        try:
            authenticator.login()
        except Exception as e:
            st.error(e)

        # Get the session object
        session_id = get_report_ctx().session_id

        # Get the session state object
        session_state = Server.get_current()._get_session_info(session_id).session_state

        try:
            if session_state.get("authentication_status", None):
                authenticator.logout()
                st.write(f'Welcome *{session_state["name"]}*')
                st.title('Home')
                st.image('sunrise.jpg')
            elif session_state.get("authentication_status", None) is False:
                st.error('Username/password is incorrect')
            elif session_state.get("authentication_status", None) is None:
                st.warning('Please Enter Username/password')
        except Exception as e:
            st.error(e)
  


        # Saving config file
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

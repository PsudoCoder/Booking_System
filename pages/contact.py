import streamlit as st
from courier.client import Courier
import boto3
import re


def show_contact():
    st.title("Contact Us")

    st.write("""
    We'd love to hear from you! Whether you have a question about our services, pricing, or anything else, our team is ready to answer all your questions.
    Please fill out the form below and we'll get back to you as soon as possible.
    """)

    # Contact form
    with st.form("contact_form"):
        # Full Name
        full_name = st.text_input("Full Name")

        email = st.text_input("Email Address")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        submit_button = st.form_submit_button(label="Send Message")

        # Form submission handling
        if submit_button:
            if not full_name or not email or not message:
                st.error("Please fill out all required fields: Name, Email and Message.")
            else:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, email):
                    st.error("Invalid email address. Please enter a valid email.")
                else:
                    ssm = boto3.client('ssm',
                                       region_name="us-east-1",
                                       aws_access_key_id=st.secrets["aws_key"],
                                       aws_secret_access_key=st.secrets["aws_secret"]
                                       )
                    auth_token = ssm.get_parameter(Name='/prod/courier_token', WithDecryption=True)
                    template_id = ssm.get_parameter(Name='/prod/courier_contact_template', WithDecryption=True)

                    client = Courier(authorization_token=auth_token['Parameter']['Value'])

                    client.send(
                        message={
                            "to": {
                                "email": "islandbreezeagency@gmail.com",
                            },
                            "template": template_id['Parameter']['Value'],
                            "data": {
                                "name": full_name,
                                "topic": subject,
                                "message": message,
                                "email": email
                            }
                        }
                    )
                    st.success(f"Thank you, {full_name}! Your message has been sent.")





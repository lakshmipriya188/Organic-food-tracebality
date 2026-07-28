
"""Login / account page. Demo-only auth stored in session state."""

import streamlit as st
from utils.cart_manager import go_to


def render_login_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown('<div class="om-section-title">Account</div>', unsafe_allow_html=True)

    if st.session_state.get("user"):
        st.success(f"You're logged in as **{st.session_state.user}**.")
        coop = st.toggle("Co-Op Member pricing", value=st.session_state.get("is_coop_member", False))
        st.session_state.is_coop_member = coop
        if st.button("Log out"):
            st.session_state.user = None
            st.rerun()
        return

    tab_login, tab_signup = st.tabs(["Log in", "Create account"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in", use_container_width=True)
            if submitted:
                if email and password:
                    st.session_state.user = email
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Please enter both email and password.")

    with tab_signup:
        with st.form("signup_form"):
            name = st.text_input("Full name")
            email2 = st.text_input("Email", key="signup_email")
            password2 = st.text_input("Password", type="password", key="signup_pw")
            join_coop = st.checkbox("Join the Farmer Co-Op for member pricing")
            submitted2 = st.form_submit_button("Create account", use_container_width=True)
            if submitted2:
                if name and email2 and password2:
                    st.session_state.user = email2
                    st.session_state.is_coop_member = join_coop
                    st.success(f"Welcome, {name}! Your account has been created.")
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")
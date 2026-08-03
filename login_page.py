import streamlit as st
from config import CURRENCY
from utils.cart_manager import go_to, logout_user, load_cart_from_db
from db_manager import verify_customer_login, register_customer, fetch_order_history_db


def render_login_page():
    if st.session_state.get("user"):
        if st.button("← Back to home"):
            go_to("home")
            st.rerun()

    st.markdown(
        """
        <div style="text-align:center; margin-bottom:1.8rem;">
            <div style="font-size:0.82rem; font-weight:800; color:#16A34A; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:4px;">
                ORGANIC FOOD TRACEABILITY PORTAL
            </div>
            <div style="font-size:2.3rem; font-weight:800; font-family:'Playfair Display', serif; color:#1B4D3E;">
                Customer Portal & Order History 👤
            </div>
            <div style="font-size:0.92rem; color:#64748B; margin-top:6px;">
                Please log in with your registered email ID to access the store UI & product traceability details.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. LOGGED IN STATE DISPLAY
    if st.session_state.get("user"):
        user_name = st.session_state.get("user", "Customer")
        user_email = st.session_state.get("user_email", "")
        user_id = st.session_state.get("user_id", "N/A")

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #1B4D3E 0%, #0F291E 100%);
                border-radius: 20px;
                padding: 2rem;
                color: #FFFFFF;
                box-shadow: 0 15px 35px rgba(27, 77, 62, 0.2);
                margin-bottom: 2rem;
            ">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                    <div>
                        <span style="background: rgba(34, 197, 94, 0.2); color: #4ADE80; font-size: 0.75rem; font-weight: 800; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(74, 222, 128, 0.3); text-transform: uppercase; letter-spacing: 1px;">
                            Verified Customer Account
                        </span>
                        <h2 style="font-family:'Playfair Display', serif; color: #FFFFFF !important; margin: 0.6rem 0 0.2rem 0; font-size: 2rem;">
                            Welcome, {user_name}!
                        </h2>
                        <p style="color: #A3B8AD; margin: 0; font-size: 0.95rem;">
                            Registered Email ID: <b>{user_email}</b> | Customer ID: <b>#{user_id}</b>
                        </p>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size: 2.5rem;">🌱</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        btn_col1, btn_col2, _ = st.columns([1.8, 1.5, 3])
        with btn_col1:
            if st.button("🌱 Continue to Organic Store", type="primary", use_container_width=True):
                go_to("home")
                st.rerun()
        with btn_col2:
            if st.button("🚪 Log Out", use_container_width=True):
                logout_user()
                st.success("Successfully logged out.")
                st.rerun()

        st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 2rem 0;'>", unsafe_allow_html=True)

        # ORDER HISTORY SECTION
        st.markdown(
            """
            <div style="font-family:'Poppins', sans-serif; font-size:1.4rem; font-weight:700; color:#1B4D3E; margin-bottom:1rem;">
                Your Order History 📜
            </div>
            """,
            unsafe_allow_html=True
        )

        orders = []
        if user_id and str(user_id).isdigit():
            orders = fetch_order_history_db(int(user_id))

        if not orders:
            st.info("No past orders found in Order_Details for your account. Add items to your cart and place an order to view them here!")
        else:
            for order in orders:
                o_id = order.get("order_id")
                p_name = order.get("product_name", "Organic Product")
                p_count = order.get("product_count", 1)
                p_unit = order.get("unit") or "kg"
                p_price = float(order.get("price_after_discount") or order.get("product_price") or 0.0)
                unit_price = float(order.get("product_price") or 0.0)
                o_date = str(order.get("order_date") or "")
                o_time = str(order.get("order_time") or "")
                cat_name = order.get("category_name") or "Organic Produce"
                item_total = round(p_price * p_count, 2)

                st.markdown(
                    f"""
                    <div style="
                        background: #FFFFFF;
                        border: 1px solid #E2E9E3;
                        border-radius: 16px;
                        padding: 1.2rem;
                        margin-bottom: 1rem;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; border-bottom: 1px solid #F0F4F1; padding-bottom: 8px; margin-bottom: 10px;">
                            <div>
                                <span style="font-weight: 700; color: #1B4D3E; font-size: 1rem;">Order #{o_id}</span>
                                <span style="color: #64748B; font-size: 0.85rem; margin-left: 12px;">📅 {o_date} at {o_time}</span>
                            </div>
                            <span style="background: #DCFCE7; color: #166534; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 12px;">
                                COMPLETED
                            </span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                            <div>
                                <div style="font-weight: 700; color: #0F291E; font-size: 1.05rem;">{p_name}</div>
                                <div style="font-size: 0.85rem; color: #4A6B5D; margin-top: 2px;">
                                    Category: <b>{cat_name}</b> | Quantity: <b>{p_count} {p_unit}</b> | Unit Price: <b>{CURRENCY}{unit_price:,.2f}/{p_unit}</b>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.78rem; color: #64748B;">Total Amount</div>
                                <div style="font-family: 'Poppins', sans-serif; font-size: 1.25rem; font-weight: 800; color: #16A34A;">
                                    {CURRENCY}{item_total:,.2f}
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        return

    # 2. LOG IN / SIGN UP FORM VIEW
    _, col_center, _ = st.columns([1, 2.2, 1])

    with col_center:
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                border: 1px solid #E2E9E3;
                border-radius: 20px;
                padding: 2.2rem;
                box-shadow: 0 15px 35px rgba(27, 77, 62, 0.08);
            ">
            """,
            unsafe_allow_html=True
        )

        tab_login, tab_signup = st.tabs(["🔒 Customer Log In", "📝 Register New Customer"])

        with tab_login:
            st.markdown(
                "<p style='font-size:0.88rem; color:#64748B; margin-bottom:1.2rem;'>Enter your registered email ID and password to log in.</p>",
                unsafe_allow_html=True
            )
            with st.form("login_form"):
                email_input = st.text_input("Email ID", placeholder="Enter your email ID (e.g. rahul@gmail.com)")
                password_input = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Log In & Enter Store", use_container_width=True)

                if submitted:
                    if not email_input or not password_input:
                        st.error("Please enter both email ID and password.")
                    else:
                        cust = verify_customer_login(email_input, password_input)
                        if cust:
                            st.session_state.user = cust["customer_name"]
                            st.session_state.user_email = cust["email_id"]
                            st.session_state.user_id = cust["customer_id"]
                            load_cart_from_db(cust["customer_id"])
                            st.session_state.page = "home"
                            st.success(f"Welcome back, {cust['customer_name']}! Redirecting to store...")
                            st.rerun()
                        else:
                            st.error("Invalid email ID or password. Please check your credentials and try again.")

        with tab_signup:
            st.markdown(
                "<p style='font-size:0.88rem; color:#64748B; margin-bottom:1.2rem;'>Create a new account to record your details in the Customer_Details table.</p>",
                unsafe_allow_html=True
            )
            with st.form("signup_form"):
                name_new = st.text_input("Full Name", placeholder="e.g. Rajesh Kumar")
                email_new = st.text_input("Email ID", key="signup_email", placeholder="e.g. rajesh@gmail.com")
                password_new = st.text_input("Password", key="signup_pw", type="password", placeholder="Create password")
                submitted_new = st.form_submit_button("Register & Log In", use_container_width=True)

                if submitted_new:
                    if not name_new or not email_new or not password_new:
                        st.error("Please fill in all required fields.")
                    else:
                        success, msg, new_cust = register_customer(name_new, email_new, password_new)
                        if success and new_cust:
                            st.session_state.user = new_cust["customer_name"]
                            st.session_state.user_email = new_cust["email_id"]
                            st.session_state.user_id = new_cust["customer_id"]
                            load_cart_from_db(new_cust["customer_id"])
                            st.session_state.page = "home"
                            st.success(f"Account created successfully for {new_cust['customer_name']}!")
                            st.rerun()
                        else:
                            st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)
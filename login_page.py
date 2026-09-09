import streamlit as st
from config import CURRENCY, APP_NAME, APP_SUBTITLE
from utils.cart_manager import go_to, logout_user, load_cart_from_db, load_wishlist_from_db
from db_manager import verify_customer_login, register_customer, fetch_order_history_db
from utils.image_utils import get_image_src


def render_login_page():
    # 1. LOGGED IN STATE DISPLAY
    if st.session_state.get("user"):
        if st.button("← Back to home"):
            go_to("home")
            st.rerun()

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
                            Verified {APP_NAME} Customer Account
                        </span>
                        <h2 style="font-family:'Poppins', sans-serif; color: #FFFFFF !important; margin: 0.6rem 0 0.2rem 0; font-size: 2rem;">
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

        # ORDER HISTORY SECTION FOR LOGGED-IN USERS
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

    # 2. PRE-LOGIN HERO & CUSTOMER PORTAL VIEW
    hero_left, portal_right = st.columns([1.15, 0.85], gap="large")

    with hero_left:
        # Organic Farming Hero Card Showcase
        st.markdown(
            f"""
<div style="
background: linear-gradient(145deg, #0F382C 0%, #1B4D3E 60%, #15803D 100%);
border-radius: 24px;
padding: 2.8rem 2.4rem;
color: #FFFFFF;
box-shadow: 0 20px 45px rgba(15, 56, 44, 0.22);
height: 100%;
display: flex;
flex-direction: column;
justify-content: space-between;
">
<div>
<div style="
display: inline-flex;
align-items: center;
gap: 6px;
background: rgba(34, 197, 94, 0.2);
border: 1px solid rgba(134, 239, 172, 0.35);
padding: 5px 14px;
border-radius: 20px;
font-size: 0.75rem;
font-weight: 800;
color: #86EFAC;
letter-spacing: 2px;
text-transform: uppercase;
margin-bottom: 1.2rem;
">
🌱 100% CERTIFIED PURE ORGANIC HARVEST
</div>
<div style="
font-family: 'Poppins', sans-serif;
font-size: 2.6rem;
font-weight: 800;
color: #FFFFFF;
line-height: 1.15;
letter-spacing: -0.5px;
margin-bottom: 1rem;
">
Pure Organic Harvest,<br>
<span style="color: #86EFAC;">Direct From Farm To Table.</span>
</div>
<div style="
font-size: 0.98rem;
color: #E2E8F0;
line-height: 1.6;
margin-bottom: 2rem;
">
Welcome to <b>{APP_NAME}</b> — your trusted co-operative platform for 100% pesticide-free staples, ancient millets, cold pressed oils, and A2 Desi cow ghee with transparent farm batch traceability.
</div>
</div>

<div>
<div style="
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 10px;
margin-bottom: 1.5rem;
">
<div style="
background: rgba(255, 255, 255, 0.12);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 14px;
padding: 8px;
text-align: center;
">
<img src="{get_image_src('assets/images/fruits.jpg')}" style="width:100%; height:75px; object-fit:cover; border-radius:10px; margin-bottom:4px;">
<div style="font-size:0.72rem; font-weight:800; color:#FFFFFF;">Fruits</div>
<div style="font-size:0.65rem; color:#86EFAC;">Farm Fresh</div>
</div>
<div style="
background: rgba(255, 255, 255, 0.12);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 14px;
padding: 8px;
text-align: center;
">
<img src="{get_image_src('assets/images/vegetables.jpg')}" style="width:100%; height:75px; object-fit:cover; border-radius:10px; margin-bottom:4px;">
<div style="font-size:0.72rem; font-weight:800; color:#FFFFFF;">Veggies</div>
<div style="font-size:0.65rem; color:#86EFAC;">100% Organic</div>
</div>
<div style="
background: rgba(255, 255, 255, 0.12);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 14px;
padding: 8px;
text-align: center;
">
<img src="{get_image_src('assets/images/millets.jpg')}" style="width:100%; height:75px; object-fit:cover; border-radius:10px; margin-bottom:4px;">
<div style="font-size:0.72rem; font-weight:800; color:#FFFFFF;">Millets</div>
<div style="font-size:0.65rem; color:#86EFAC;">Ancient Grains</div>
</div>
<div style="
background: rgba(255, 255, 255, 0.12);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.2);
border-radius: 14px;
padding: 8px;
text-align: center;
">
<img src="{get_image_src('assets/images/oils.jpg')}" style="width:100%; height:75px; object-fit:cover; border-radius:10px; margin-bottom:4px;">
<div style="font-size:0.72rem; font-weight:800; color:#FFFFFF;">Cold Oils</div>
<div style="font-size:0.65rem; color:#86EFAC;">Pure Ghani</div>
</div>
</div>

<div style="
background: rgba(0, 0, 0, 0.2);
border-radius: 14px;
padding: 10px 14px;
display: flex;
justify-content: space-around;
align-items: center;
font-size: 0.75rem;
font-weight: 700;
color: #DCFCE7;
letter-spacing: 0.5px;
flex-wrap: wrap;
gap: 6px;
">
<div>⚡ 100% Pesticide-Free</div>
<div>🩺 Lab Audited</div>
<div>👨‍🌾 Farmer Co-Op</div>
<div>🔍 Traceable</div>
</div>
</div>
</div>
""",
            unsafe_allow_html=True
        )

    with portal_right:
        # SINGLE DECENT & CLASSY CUSTOMER LOGIN CARD
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                border: 1px solid #E2E9E3;
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 12px 32px rgba(15, 41, 30, 0.06);
            ">
                <div style="margin-bottom: 1.4rem;">
                    <div style="font-family:'Poppins', sans-serif; font-size: 1.8rem; font-weight: 800; color: #1B4D3E;">
                        Customer Login
                    </div>
                    <div style="font-size: 0.88rem; color: #4A6B5D; margin-top: 4px;">
                        Log in with your registered email ID to access the store & farm traceability details.
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )

        tab_login, tab_signup = st.tabs(["🔒 Customer Log In", "📝 Register New Customer"])

        with tab_login:
            st.markdown(
                "<p style='font-size:0.85rem; color:#64748B; margin-bottom:1rem; margin-top: 0.5rem;'>Enter your registered email ID and password to log in.</p>",
                unsafe_allow_html=True
            )
            with st.form("login_form"):
                email_input = st.text_input("Email ID", placeholder="Enter your email ID (e.g. rahul@gmail.com)")
                password_input = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Log In & Enter Store", use_container_width=True, type="primary")

                if submitted:
                    if not email_input or not password_input:
                        st.error("Please enter both email ID and password.")
                    else:
                        cust = verify_customer_login(email_input, password_input)
                        if cust:
                            st.session_state.user = cust["customer_name"]
                            st.session_state.user_email = cust["email_id"]
                            st.session_state.user_id = cust["customer_id"]
                            st.session_state.show_ai_login_dialog = True
                            load_cart_from_db(cust["customer_id"])
                            load_wishlist_from_db(cust["customer_id"])
                            st.session_state.page = "home"
                            st.success(f"Welcome back, {cust['customer_name']}! Redirecting to store...")
                            st.rerun()
                        else:
                            st.error("Invalid email ID or password. Please check your credentials and try again.")

        with tab_signup:
            st.markdown(
                "<p style='font-size:0.85rem; color:#64748B; margin-bottom:1rem; margin-top: 0.5rem;'>Create a new account to record your details in the Customer_Details table.</p>",
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
                            st.session_state.show_ai_login_dialog = True
                            load_cart_from_db(new_cust["customer_id"])
                            load_wishlist_from_db(new_cust["customer_id"])
                            st.session_state.page = "home"
                            st.success(f"Account created successfully for {new_cust['customer_name']}!")
                            st.rerun()
                        else:
                            st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)
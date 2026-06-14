import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mahindra University Carpool",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "rides" not in st.session_state:
    st.session_state.rides = [
        {"Driver": "Rohan Kumar",  "Vehicle": "Hyundai i20", "Route": "Hostel A → University", "Seats": 3, "Time": "08:30 AM", "Gender": "Male"},
        {"Driver": "Sneha Sharma", "Vehicle": "Honda City",  "Route": "G Block → University",  "Seats": 2, "Time": "09:00 AM", "Gender": "Female"},
    ]
if "requests" not in st.session_state:
    st.session_state.requests = [
        {"Name": "Ananya Verma", "Pickup": "Hostel C", "Destination": "University", "Time": "08:45 AM", "Gender": "Female", "Female Only": True},
        {"Name": "Vikram Singh",  "Pickup": "Hostel B", "Destination": "University", "Time": "09:15 AM", "Gender": "Male",   "Female Only": False},
    ]
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ─────────────────────────────────────────────
# CSS — matches the image exactly
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 0 !important; max-width: 100% !important;}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1a1f3a !important;
    width: 220px !important;
    min-width: 220px !important;
}
[data-testid="stSidebar"] * {color: #ffffff !important;}
[data-testid="stSidebarContent"] {padding: 0 !important;}

/* sidebar logo */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 22px 18px 18px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 10px;
}
.sidebar-logo-icon {
    background: #e31837;
    border-radius: 8px;
    width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 900; color: white;
}
.sidebar-logo-text {font-size: 13px; font-weight: 700; line-height: 1.2; color: white;}

/* nav buttons */
.stButton > button {
    width: 100%;
    text-align: left !important;
    background: transparent !important;
    color: #b0b8d9 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    margin-bottom: 2px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
}

/* sidebar contact card */
.contact-card {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 16px;
    margin: 12px;
}
.contact-title {font-size:14px; font-weight:700; margin-bottom:6px;}
.contact-sub   {font-size:11px; color:#b0b8d9; margin-bottom:12px;}
.contact-item  {font-size:11px; color:#b0b8d9; margin:4px 0; display:flex; align-items:center; gap:6px;}

/* social icons row */
.socials {display:flex; gap:8px; margin-top:8px;}
.social-btn {
    width:30px; height:30px; border-radius:50%; display:flex;
    align-items:center; justify-content:center; font-size:14px;
    text-decoration:none;
}
.si   {background:#E1306C;}
.sl   {background:#0A66C2;}
.st2  {background:#1DA1F2;}
.sw   {background:#25D366;}

/* eco card */
.eco-card {
    background: rgba(255,255,255,0.05);
    border-radius:12px;
    padding:14px;
    margin:12px;
    text-align:center;
    font-size:12px; color:#b0b8d9;
}

/* ── Main content area ── */
.main-content {
    background: #f0f2f8;
    min-height: 100vh;
    padding: 0;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 40%, #7b4fa6 70%, #c471ed 100%);
    padding: 30px 36px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 180px;
}
.hero-left {max-width: 55%;}
.hero-title {font-size: 38px; font-weight: 800; color: white; line-height: 1.1; margin: 0;}
.hero-title span {color: #e31837;}
.hero-sub {font-size: 15px; color: rgba(255,255,255,0.8); margin: 8px 0 16px;}
.pill-row {display: flex; gap: 8px; flex-wrap: wrap;}
.pill {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: white;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px; font-weight: 600;
}
.pill.red   {background:rgba(227,24,55,0.3);  border-color:#e31837;}
.pill.green {background:rgba(34,197,94,0.3);  border-color:#22c55e;}
.pill.leaf  {background:rgba(34,197,94,0.3);  border-color:#22c55e;}
.pill.blue  {background:rgba(99,102,241,0.3); border-color:#6366f1;}
.hero-img {font-size: 90px; text-align:center;}

/* ── Stat cards ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    padding: 20px 24px;
}
.stat-card {
    background: white;
    border-radius: 14px;
    padding: 16px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stat-icon {
    width: 48px; height: 48px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.si-red   {background:#fde8ec;}
.si-green {background:#dcfce7;}
.si-blue  {background:#dbeafe;}
.si-purple{background:#ede9fe;}
.stat-num {font-size: 28px; font-weight: 800; color: #1a1f3a;}
.stat-num.green  {color:#16a34a;}
.stat-num.blue   {color:#2563eb;}
.stat-num.purple {color:#7c3aed;}
.stat-label {font-size: 12px; color: #6b7280; font-weight:500;}
.stat-sub   {font-size: 11px; color:#9ca3af;}

/* ── Tab strip ── */
.tab-strip {
    display: flex;
    gap: 0;
    border-bottom: 2px solid #e5e7eb;
    margin: 0 24px;
    background: white;
    border-radius: 12px 12px 0 0;
    overflow: hidden;
}
.tab-btn {
    padding: 14px 24px;
    font-size: 14px; font-weight: 600;
    color: #6b7280;
    border: none; background: transparent;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
}
.tab-btn.active {color: #e31837; border-bottom-color: #e31837;}
.tab-btn:hover:not(.active) {color: #374151; background: #f9fafb;}

/* ── Forms area ── */
.forms-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    padding: 20px 24px;
    background: white;
    margin: 0 24px;
}
.form-section {padding: 4px 0;}
.form-title {
    font-size: 16px; font-weight: 700; color: #1a1f3a;
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 16px;
}
.form-label {font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 4px;}

/* custom input — muted, soft background */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border: 1.5px solid #d1d5db !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 9px 12px !important;
    background: #f3f4f6 !important;
    color: #1f2937 !important;
    transition: border 0.2s, background 0.2s;
}
.stTextInput > div > div > input::placeholder,
.stNumberInput > div > div > input::placeholder {
    color: #9ca3af !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #e31837 !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(227,24,55,0.08) !important;
}
/* selectbox */
.stSelectbox > div > div {
    border: 1.5px solid #d1d5db !important;
    border-radius: 8px !important;
    background: #f3f4f6 !important;
    font-size: 13px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #e31837 !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(227,24,55,0.08) !important;
}

/* female-only box */
.female-only-box {
    border: 1.5px solid #e31837;
    border-radius: 10px;
    padding: 10px 14px;
    display: flex; align-items: center; gap: 10px;
    background: #fff5f6;
    margin: 12px 0;
}
.female-only-box span {font-size: 13px; color: #e31837; font-weight:600;}
.female-only-box small {font-size: 11px; color: #9ca3af; display:block;}

/* big action buttons */
.find-btn, .offer-btn {
    width: 100%;
    padding: 13px;
    border-radius: 10px;
    font-size: 15px; font-weight: 700;
    border: none; cursor: pointer;
    margin-top: 8px;
    transition: opacity 0.2s;
}
.find-btn  {background: #e31837; color: white;}
.offer-btn {background: #7c3aed; color: white;}
.find-btn:hover, .offer-btn:hover {opacity: 0.9;}

/* Streamlit button overrides for action buttons */
div[data-testid="stButton"].find > button {
    background: #e31837 !important;
    color: white !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 13px !important;
    border: none !important;
    width: 100% !important;
}
div[data-testid="stButton"].offer > button {
    background: #7c3aed !important;
    color: white !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 13px !important;
    border: none !important;
    width: 100% !important;
}

/* ── Table area ── */
.table-section {
    padding: 20px 24px;
    background: white;
    margin: 0 24px 4px;
    border-top: 1px solid #f3f4f6;
}
.table-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 14px;
}
.table-title {font-size: 16px; font-weight: 700; color: #1a1f3a; display:flex; align-items:center; gap:8px;}
.view-btn {
    border: 1.5px solid #e31837;
    color: #e31837;
    background: transparent;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px; font-weight:600;
    cursor:pointer;
}
.view-btn.purple {border-color:#7c3aed; color:#7c3aed;}

/* seats badge */
.seats-badge {
    background: #dbeafe;
    color: #1d4ed8;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 12px; font-weight: 700;
    display:inline-block;
}

/* ── Divider ── */
.hdivider {height:20px; background:#f0f2f8;}

/* ── Footer ── */
.footer {
    background: #1a1f3a;
    color: rgba(255,255,255,0.6);
    font-size: 12px;
    padding: 18px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0 24px 0;
}
.footer-heart {color: #e31837;}

/* ── Home page ── */
.home-card {
    background: white;
    border-radius: 14px;
    padding: 20px 24px;
    margin: 12px 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.home-card h3 {color:#1a1f3a; font-size:16px; font-weight:700; margin-bottom:12px;}
.benefit-row {display:flex; align-items:center; gap:10px; padding:6px 0; font-size:14px; color:#374151;}
.benefit-icon {color:#22c55e; font-size:16px;}

/* Dashboard page */
.dash-card {
    background: white; border-radius: 14px; padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align:center;
}
.dash-num {font-size:36px; font-weight:800;}

/* Notification success/error override */
[data-testid="stAlert"] {border-radius:10px !important; margin:8px 0;}

/* Checkbox override */
.stCheckbox label {font-size:13px !important; color:#e31837 !important; font-weight:600;}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Logo — Mahindra University official SVG rendered inline
    st.markdown("""
    <div class="sidebar-logo" style="flex-direction:column; align-items:flex-start; gap:6px; padding:18px 16px 14px;">
        <!-- Mahindra "M" chevron wordmark -->
        <svg viewBox="0 0 220 52" xmlns="http://www.w3.org/2000/svg" style="width:170px; height:auto;">
            <!-- Red chevron M icon -->
            <g transform="translate(0,4)">
                <polygon points="0,36 8,36 8,8 20,36 28,36 40,8 40,36 48,36 48,0 34,0 24,24 14,0 0,0" fill="#e31837"/>
            </g>
            <!-- MAHINDRA text -->
            <text x="56" y="28" font-family="Arial,sans-serif" font-size="15" font-weight="800"
                  fill="white" letter-spacing="2">MAHINDRA</text>
            <!-- UNIVERSITY text -->
            <text x="56" y="44" font-family="Arial,sans-serif" font-size="9.5" font-weight="500"
                  fill="#b0b8d9" letter-spacing="3">UNIVERSITY</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    # Nav
    pages = [("🏠", "Home"), ("🔍", "Find Ride"), ("🚘", "Offer Ride"), ("📊", "Dashboard"), ("ℹ️", "About Us")]
    for icon, label in pages:
        if st.button(f"{icon}  {label}", key=f"nav_{label}"):
            st.session_state.page = label

    st.markdown("<div style='margin:12px 0; border-top:1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)

    # Contact card
    st.markdown("""
    <div class="contact-card">
        <div class="contact-title">🎧 Contact Us</div>
        <div class="contact-sub">Have questions or need help?<br>We're here for you!</div>
        <div class="contact-item">📞 +91 98765 43210</div>
        <div class="contact-item">✉️ support@mahindra-carpool.in</div>
        <div class="contact-item">📍 Mahindra University,<br>&nbsp;&nbsp;&nbsp;&nbsp;Bahadurpally, Hyderabad,<br>&nbsp;&nbsp;&nbsp;&nbsp;Telangana 500043</div>
        <div class="contact-item">🕐 Mon - Sat: 8:00 AM - 8:00 PM</div>
        <br>
        <div style="font-size:12px; font-weight:700; margin-bottom:8px;">Follow Us</div>
        <div class="socials">
            <a href="#" class="social-btn si">📷</a>
            <a href="#" class="social-btn sl">💼</a>
            <a href="#" class="social-btn st2">🐦</a>
            <a href="#" class="social-btn sw">💬</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Eco card
    st.markdown("""
    <div class="eco-card">
        🌍<br>
        <strong>Together we can<br>reduce carbon<br>emissions!</strong>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-left">
        <!-- Mahindra University wordmark logo -->
        <div style="margin-bottom:14px;">
            <svg viewBox="0 0 260 56" xmlns="http://www.w3.org/2000/svg" style="width:205px;height:auto;">
                <g transform="translate(0,6)">
                    <polygon points="0,36 8,36 8,8 20,36 28,36 40,8 40,36 48,36 48,0 34,0 24,24 14,0 0,0" fill="#e31837"/>
                </g>
                <text x="58" y="30" font-family="Arial,sans-serif" font-size="16" font-weight="800"
                      fill="white" letter-spacing="2">MAHINDRA</text>
                <text x="58" y="46" font-family="Arial,sans-serif" font-size="10" font-weight="500"
                      fill="rgba(255,255,255,0.72)" letter-spacing="3.5">UNIVERSITY</text>
            </svg>
        </div>
        <div class="hero-title"><span>Carpool</span> 🚗</div>
        <div class="hero-sub">Share the Ride. Save Money. Protect the Planet.</div>
        <div class="pill-row">
            <span class="pill red">🚗 Affordable</span>
            <span class="pill green">🛡️ Safe</span>
            <span class="pill leaf">🌿 Eco-Friendly</span>
            <span class="pill blue">👥 Community Driven</span>
        </div>
    </div>
    <div class="hero-img">👨‍👩‍👧‍👦🚗🏫</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STAT CARDS
# ─────────────────────────────────────────────
n_offers   = len(st.session_state.rides)
n_requests = len(st.session_state.requests)
money_saved = n_requests * 120
co2_saved   = n_offers * 2

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-icon si-red">🚗</div>
        <div>
            <div class="stat-num">{n_offers}</div>
            <div class="stat-label">Ride Offers</div>
            <div class="stat-sub">Active offers</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon si-green">👥</div>
        <div>
            <div class="stat-num green">{n_requests}</div>
            <div class="stat-label">Ride Requests</div>
            <div class="stat-sub">Active requests</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon si-blue">₹</div>
        <div>
            <div class="stat-num blue">₹{money_saved}</div>
            <div class="stat-label">Estimated Money Saved</div>
            <div class="stat-sub">By students</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon si-purple">🌿</div>
        <div>
            <div class="stat-num purple">{co2_saved} kg</div>
            <div class="stat-label">CO₂ Saved</div>
            <div class="stat-sub">Less emissions</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────
page = st.session_state.page

# ── Quick nav strip shown on all pages ──
col_tabs = st.columns([1, 1, 1, 4])
with col_tabs[0]:
    if st.button("🏠 Home", key="tab_home"):
        st.session_state.page = "Home"; st.rerun()
with col_tabs[1]:
    if st.button("🔍 Find Ride", key="tab_find"):
        st.session_state.page = "Find Ride"; st.rerun()
with col_tabs[2]:
    if st.button("🚘 Offer Ride", key="tab_offer"):
        st.session_state.page = "Offer Ride"; st.rerun()

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
if page == "Home":
    st.markdown("""
    <div class="home-card">
        <h3>🚧 Problem We Solve</h3>
        <p style="color:#6b7280; font-size:14px; line-height:1.6;">
            Students struggle with high Uber costs, traffic congestion, parking shortages,
            and safety concerns during late-night travel. This platform connects students
            travelling on similar routes and allows them to share rides — saving money,
            reducing emissions, and making campus life safer.
        </p>
    </div>
    <div class="home-card">
        <h3>✅ Benefits</h3>
        <div class="benefit-row"><span class="benefit-icon">✅</span> Lower travel costs — save up to ₹3,000/month</div>
        <div class="benefit-row"><span class="benefit-icon">✅</span> Reduced traffic congestion around campus</div>
        <div class="benefit-row"><span class="benefit-icon">✅</span> Better parking availability for everyone</div>
        <div class="benefit-row"><span class="benefit-icon">✅</span> Safer commuting with verified student profiles</div>
        <div class="benefit-row"><span class="benefit-icon">✅</span> Lower carbon emissions — good for the planet</div>
        <div class="benefit-row"><span class="benefit-icon">✅</span> Female-only matching for added safety</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FIND RIDE PAGE
# ─────────────────────────────────────────────
elif page == "Find Ride":
    st.markdown("""
    <div style="padding:10px 24px 0;">
        <h3 style="color:#1a1f3a; font-size:20px; font-weight:700; margin-bottom:4px;">🔍 Find a Ride</h3>
        <p style="color:#6b7280; font-size:13px; margin-bottom:16px;">Fill in your details below and we'll match you with available rides.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col_form, col_gap = st.columns([1.4, 1])
        with col_form:
            name        = st.text_input("Your Name", placeholder="e.g. Ananya Verma", key="f_name")
            c1, c2      = st.columns(2)
            pickup      = c1.text_input("Pickup Location", placeholder="e.g. Hostel C", key="f_pickup")
            destination = c2.text_input("Destination", placeholder="e.g. University", key="f_dest")
            c3, c4      = st.columns(2)
            time_r      = c3.text_input("Travel Time", placeholder="e.g. 08:30 AM", key="f_time")
            gender_r    = c4.selectbox("Gender", ["Male", "Female"], key="f_gender")
            female_only = st.checkbox("🛡️ Female Only Matching — Match only with female drivers", key="f_fo")

            if st.button("🔍 Find Ride", key="btn_find", use_container_width=True):
                if name and pickup and destination:
                    st.session_state.requests.append({
                        "Name": name, "Pickup": pickup, "Destination": destination,
                        "Time": time_r, "Gender": gender_r, "Female Only": female_only
                    })
                    st.success("✅ Ride request submitted! We'll match you with a driver.")
                    st.rerun()
                else:
                    st.error("Please fill in your Name, Pickup Location, and Destination.")

        with col_gap:
            st.markdown("""
            <div style="background:#f8fafc; border:1.5px dashed #e5e7eb; border-radius:14px;
                        padding:24px; margin-top:8px; text-align:center;">
                <div style="font-size:40px; margin-bottom:10px;">🚗</div>
                <div style="font-size:14px; font-weight:700; color:#1a1f3a; margin-bottom:6px;">How it works</div>
                <div style="font-size:12px; color:#6b7280; line-height:1.8;">
                    1️⃣ Enter your route details<br>
                    2️⃣ Choose Female Only if needed<br>
                    3️⃣ Submit your request<br>
                    4️⃣ Driver will contact you<br>
                    5️⃣ Share the ride & save money!
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("##### 🚗 Available Rides You Can Join")
    if st.session_state.rides:
        df = pd.DataFrame(st.session_state.rides)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No rides available yet. Check back soon!")

# ─────────────────────────────────────────────
# OFFER RIDE PAGE
# ─────────────────────────────────────────────
elif page == "Offer Ride":
    st.markdown("""
    <div style="padding:10px 24px 0;">
        <h3 style="color:#1a1f3a; font-size:20px; font-weight:700; margin-bottom:4px;">🚘 Offer a Ride</h3>
        <p style="color:#6b7280; font-size:13px; margin-bottom:16px;">Share your ride with fellow students and help them commute safely.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col_form2, col_gap2 = st.columns([1.4, 1])
        with col_form2:
            driver  = st.text_input("Your Name", placeholder="e.g. Rohan Kumar", key="o_driver")
            vehicle = st.text_input("Vehicle", placeholder="e.g. Hyundai i20", key="o_vehicle")
            route   = st.text_input("Route", placeholder="e.g. Hostel A → University Gate", key="o_route")
            c5, c6  = st.columns(2)
            seats   = c5.number_input("Available Seats", 1, 10, 3, key="o_seats")
            ride_time = c6.text_input("Departure Time", placeholder="e.g. 08:30 AM", key="o_time")
            driver_g = st.selectbox("Your Gender", ["Male", "Female"], key="o_gender")

            if st.button("🚘 Offer This Ride", key="btn_offer", use_container_width=True):
                if driver and vehicle and route:
                    st.session_state.rides.append({
                        "Driver": driver, "Vehicle": vehicle, "Route": route,
                        "Seats": seats, "Time": ride_time, "Gender": driver_g
                    })
                    st.success("✅ Your ride is now listed! Students can see it.")
                    st.rerun()
                else:
                    st.error("Please fill in your Name, Vehicle, and Route.")

        with col_gap2:
            st.markdown("""
            <div style="background:#f8fafc; border:1.5px dashed #e5e7eb; border-radius:14px;
                        padding:24px; margin-top:8px; text-align:center;">
                <div style="font-size:40px; margin-bottom:10px;">💰</div>
                <div style="font-size:14px; font-weight:700; color:#1a1f3a; margin-bottom:6px;">Why offer a ride?</div>
                <div style="font-size:12px; color:#6b7280; line-height:1.8;">
                    ✅ Split fuel costs with riders<br>
                    ✅ Help fellow students commute<br>
                    ✅ Reduce campus traffic<br>
                    ✅ Earn goodwill & connections<br>
                    ✅ Save the planet 🌍
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("##### 👥 Current Ride Requests (Students Looking for Rides)")
    if st.session_state.requests:
        df2 = pd.DataFrame(st.session_state.requests)
        df2["Female Only"] = df2["Female Only"].map({True: "✅", False: "❌"})
        st.dataframe(df2, use_container_width=True, hide_index=True)
    else:
        st.warning("No ride requests yet.")

# ─────────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────────
elif page == "Dashboard":
    st.markdown("### 📊 Dashboard")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Total Ride Offers",    n_offers)
    d2.metric("Total Ride Requests",  n_requests)
    d3.metric("Estimated Money Saved", f"₹{money_saved}")
    d4.metric("CO₂ Saved",            f"{co2_saved} kg")

    st.divider()
    if st.session_state.rides:
        st.markdown("#### All Ride Offers")
        st.dataframe(pd.DataFrame(st.session_state.rides), use_container_width=True, hide_index=True)
    if st.session_state.requests:
        st.markdown("#### All Ride Requests")
        df3 = pd.DataFrame(st.session_state.requests)
        df3["Female Only"] = df3["Female Only"].map({True: "✅", False: "❌"})
        st.dataframe(df3, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# ABOUT US PAGE
# ─────────────────────────────────────────────
elif page == "About Us":
    st.markdown("""
    <div class="home-card">
        <h3>About Mahindra University Carpool</h3>
        <p style="color:#6b7280; font-size:14px; line-height:1.6;">
            This platform was built as a college project to address the real commuting challenges
            faced by students at Mahindra University, Hyderabad. Our goal is to reduce travel costs,
            ease congestion, and promote sustainable campus commuting through peer-to-peer ride sharing.
        </p>
        <br>
        <p style="color:#6b7280; font-size:14px;"><strong>📍 Campus:</strong> Mahindra University, Bahadurpally, Hyderabad, Telangana 500043</p>
        <p style="color:#6b7280; font-size:14px;"><strong>📧 Contact:</strong> support@mahindra-carpool.in</p>
        <p style="color:#6b7280; font-size:14px;"><strong>📞 Phone:</strong> +91 98765 43210</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="height:24px;"></div>
<div class="footer">
    <span>© 2025 Mahindra University Carpool. All rights reserved.</span>
    <span>Made with <span class="footer-heart">♥</span> for Mahindra University Students</span>
    <span>🚗</span>
</div>
""", unsafe_allow_html=True)
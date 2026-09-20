import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap');

        h1, h2, h3 {
            font-family: 'Poppins', sans-serif;
        }

        [data-testid="stSidebar"] {
            background-color: #15151F;
            border-right: 1px solid #2A2A3A;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 6px;
        }

        .kpi-card {
            background-color: #1A1A26;
            border-radius: 10px;
            padding: 18px 20px;
            border-left: 4px solid var(--accent-color);
        }
        .kpi-label {
            color: #A6A3B3;
            font-size: 0.85rem;
            margin-bottom: 6px;
        }
        .kpi-value {
            color: #F4F2F7;
            font-size: 1.8rem;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)


def kpi_card(label, value, accent="#F5A623"):
    st.markdown(f"""
        <div class="kpi-card" style="--accent-color: {accent};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style="padding: 10px 0 20px 0;">
                <div style="font-size: 1.4rem; font-weight: 700; color: #F4F2F7;">
                    🍬 Nassau Candy
                </div>
                <div style="color: #A6A3B3; font-size: 0.85rem; margin-top: 2px;">
                    Shipping Analytics Dashboard
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("""
            <div style="color: #A6A3B3; font-size: 0.85rem; line-height: 1.5;">
                Factory-to-customer shipping route efficiency analysis across 
                5 factories and 49 US states/DC.
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("""
            <div style="color: #6B6878; font-size: 0.75rem; margin-top: 30px;">
                Built by Kehkasha Ansari<br>
                Unified Mentor · Business Analyst Internship
            </div>
        """, unsafe_allow_html=True)


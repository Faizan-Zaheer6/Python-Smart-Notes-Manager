import streamlit as st
from datetime import datetime
from fpdf import FPDF

# --- Step 1: UI Customization (CSS) ---
st.set_page_config(page_title="Smart Notes Hub", layout="wide")

design_style = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    /* Top Banner Styling */
    .top-title {
        text-align: center;
        padding: 20px;
        font-family: 'Trebuchet MS', sans-serif;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        border-radius: 8px !important;
        background: linear-gradient(45deg, #00dbde, #fc00ff) !important;
        color: white !important;
        font-weight: bold !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(design_style, unsafe_allow_html=True)

# --- Step 2: Session State & Logic ---
if 'all_notes' not in st.session_state:
    st.session_state.all_notes = []

def create_pdf(notes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Smart Notes by FZ - Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for n in notes:
        pdf.set_text_color(30, 30, 30)
        pdf.cell(200, 10, txt=f"Title: {n['title']}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Content: {n['content']}")
        pdf.set_text_color(100, 100, 100)
        pdf.cell(200, 10, txt=f"Date: {n['time']} | Tags: {n['tags']}", ln=True)
        pdf.ln(5)
        pdf.cell(200, 0, txt="", border='T', ln=True)
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

# --- Step 3: NEW TOP HEADER ---
# Page ke bilkul top par Title
st.markdown("<div class='top-title'><h1 style='color: #00dbde; margin:0;'>🗒️ Smart Notes by FZ</h1><p style='color: #fc00ff; margin:0;'>Your Personal Digital Workspace</p></div>", unsafe_allow_html=True)

# --- Step 4: Actions Row ---
# Ab Title upar chala gaya hai, toh Actions yahan side par hon gy
act_col1, act_col2, act_col3 = st.columns([2, 1, 1])

with act_col1:
     search = st.text_input("🔍 Search notes by title...", label_visibility="collapsed", placeholder="Search your notes here...")

with act_col2:
    if st.session_state.all_notes:
        pdf_data = create_pdf(st.session_state.all_notes)
        st.download_button(label="📥 Export as PDF", data=pdf_data, file_name="notes_fz.pdf", mime="application/pdf", use_container_width=True)
    else:
        st.button("📥 Export as PDF", disabled=True, use_container_width=True)

with act_col3:
    if st.button("Clear All", use_container_width=True):
        st.session_state.all_notes = []
        st.rerun()

st.divider()

# --- Step 5: Sidebar & Main Display ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📝 New Note</h2>", unsafe_allow_html=True)
    t = st.text_input("Title")
    c = st.text_area("Content")
    tags = st.text_input("Tags")
    if st.button("Save to List", use_container_width=True):
        if t and c:
            new_note = {"title": t, "content": c, "tags": tags, "time": datetime.now().strftime("%Y-%m-%d %H:%M")}
            st.session_state.all_notes.insert(0, new_note)
            st.rerun()

if not st.session_state.all_notes:
    st.info("Your list is empty. Sidebar se naya note add karein! ✨")
else:
    with st.expander("📂 View My Notes", expanded=True):
        filtered = [n for n in st.session_state.all_notes if search.lower() in n['title'].lower()]
        for index, note in enumerate(filtered):
            with st.container(border=True):
                st.markdown(f"<h3 style='color: #00dbde;'>{note['title']}</h3>", unsafe_allow_html=True)
                st.write(note['content'])
                st.caption(f"📅 {note['time']} | 🏷️ {note['tags']}")
                if st.button(f"Remove Note", key=f"del_{index}"):
                    st.session_state.all_notes.remove(note)
                    st.rerun()
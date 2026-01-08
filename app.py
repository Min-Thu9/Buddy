import streamlit as st
import time
import base64

st.set_page_config(page_title="StudyBuddy", layout="wide")
st.title("📚 StudyBuddy")

# -------------------- Session State Initialization --------------------
if "video_notes" not in st.session_state:
    st.session_state.video_notes = ""
if "pdf_notes_area" not in st.session_state:
    st.session_state.pdf_notes_area = ""
if "article_notes_area" not in st.session_state:
    st.session_state.article_notes_area = ""
if "reflection_text" not in st.session_state:
    st.session_state.reflection_text = ""
if "running" not in st.session_state:
    st.session_state.running = False
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()
if "break_seconds" not in st.session_state:
    st.session_state.break_seconds = 0

# -------------------- Timer Update --------------------
def update_timer():
    if st.session_state.running:
        now = time.time()
        elapsed = now - st.session_state.last_tick
        st.session_state.total_seconds += int(elapsed)
        st.session_state.last_tick = now

update_timer()

def format_hms(total_sec):
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

# -------------------- Device Selector --------------------
device = st.radio("Select your device", ["Laptop/Desktop", "Phone"])

# -------------------- Tabs --------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎥 Video + Note",
    "📄 PDF + Note",
    "📰 Article + Note",
    "📊 Study Summary",
    "✏ Reflection",
    "📝 Feedback"
])

# -------------------- Tab 1: Video + Note --------------------
with tab1:
    st.subheader("⏱ Study Timer")
    st.metric("Elapsed Time", format_hms(st.session_state.total_seconds))

    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
    if btn_col1.button("▶ Start"):
        if not st.session_state.running:
            st.session_state.running = True
            st.session_state.last_tick = time.time()
    if btn_col2.button("⏸ Pause"):
        st.session_state.running = False
    if btn_col3.button("⏯ Resume"):
        if not st.session_state.running:
            st.session_state.running = True
            st.session_state.last_tick = time.time()
    if btn_col4.button("⏹ Reset"):
        st.session_state.running = False
        st.session_state.total_seconds = 0
        st.session_state.last_tick = time.time()
        st.session_state.break_seconds = 0

    st.markdown("---")
    st.subheader("🎥 Study Video + Notes")
    video_url = st.text_input("Paste video URL", placeholder="https://www.youtube.com/watch?v=...")

    def save_video_notes():
        st.session_state.video_notes = st.session_state.video_notes

    if video_url:
        if device == "Laptop/Desktop":
            col_video, col_notes = st.columns([1, 1])
        else:
            col_video = st.container()
            col_notes = st.container()

        with col_video:
            st.video(video_url)

        with col_notes:
            st.subheader("📝 Take Notes")
            st.text_area(
                "Write notes here",
                value=st.session_state.video_notes,
                height=300,
                key="video_notes",
                on_change=save_video_notes
            )
            words = len(st.session_state.video_notes.split())
            chars = len(st.session_state.video_notes)
            w1, w2 = st.columns(2)
            w1.metric("Words", words)
            w2.metric("Characters", chars)
            st.download_button(
                "⬇ Download Notes (TXT)",
                st.session_state.video_notes,
                "video_notes.txt",
                mime="text/plain"
            )
    else:
        st.info("Paste a video URL to start taking notes.")

# -------------------- Tab 2: PDF + Note --------------------
with tab2:
    st.subheader("📄 PDF Viewer + Notes")
    uploaded_pdf = st.file_uploader("Upload PDF", type="pdf", key="pdf_uploader")

    def save_pdf_notes():
        st.session_state.pdf_notes_area = st.session_state.pdf_notes_area

    if uploaded_pdf:
        pdf_bytes = uploaded_pdf.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        col_pdf, col_notes = st.columns([3, 2])

        with col_pdf:
            pdf_display = f'''
            <iframe src="data:application/pdf;base64,{b64}" width="100%" height="800"></iframe>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)

        with col_notes:
            st.subheader("📝 Take Notes")
            st.text_area(
                "Write your notes here",
                value=st.session_state.pdf_notes_area,
                height=800,
                key="pdf_notes_area",
                on_change=save_pdf_notes
            )
            words = len(st.session_state.pdf_notes_area.split())
            chars = len(st.session_state.pdf_notes_area)
            w1, w2 = st.columns(2)
            w1.metric("Words", words)
            w2.metric("Characters", chars)
            st.download_button(
                "⬇ Download Notes (TXT)",
                st.session_state.pdf_notes_area,
                "pdf_notes.txt",
                mime="text/plain"
            )
    else:
        st.info("Upload a PDF to start taking notes.")

# -------------------- Tab 3: Article + Note --------------------
with tab3:
    st.subheader("📰 Article Viewer + Notes")
    st.info("Note: Some articles may not display due to access restrictions or embedding limitations.")

    article_url = st.text_input("Paste Article URL", placeholder="https://example.com/article")

    def save_article_notes():
        st.session_state.article_notes_area = st.session_state.article_notes_area

    if article_url:
        col_article, col_notes = st.columns([3, 2])

        with col_article:
            try:
                st.markdown(
                    f'<iframe src="{article_url}" width="100%" height="800"></iframe>',
                    unsafe_allow_html=True
                )
            except:
                st.warning("⚠️ Cannot display this article. The URL might be unavailable or blocked from embedding.")

        with col_notes:
            st.subheader("📝 Take Notes")
            st.text_area(
                "Write your notes here",
                value=st.session_state.article_notes_area,
                height=800,
                key="article_notes_area",
                on_change=save_article_notes
            )
            words = len(st.session_state.article_notes_area.split())
            chars = len(st.session_state.article_notes_area)
            w1, w2 = st.columns(2)
            w1.metric("Words", words)
            w2.metric("Characters", chars)
            st.download_button(
                "⬇ Download Notes (TXT)",
                st.session_state.article_notes_area,
                "article_notes.txt",
                mime="text/plain"
            )
    else:
        st.info("Paste an article URL to start taking notes.")

# -------------------- Tab 4: Study Summary --------------------
with tab4:
    st.subheader("📊 Study Summary")
    total_sec = st.session_state.total_seconds
    total_minutes = total_sec // 60
    video_words = len(st.session_state.video_notes.split())
    pdf_words = len(st.session_state.pdf_notes_area.split())
    total_words = video_words + pdf_words
    video_chars = len(st.session_state.video_notes)
    pdf_chars = len(st.session_state.pdf_notes_area)
    total_chars = video_chars + pdf_chars
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Study Time", format_hms(total_sec))
    s2.metric("Total Words Written", total_words)
    s3.metric("Total Characters", total_chars)
    s4.metric("Words per Minute", round(total_words / total_minutes, 2) if total_minutes > 0 else 0)
    st.caption("Summary includes both Video + Note and PDF + Note tabs.")

    summary_text = (
        f"Total Study Time: {format_hms(total_sec)}\n"
        f"Total Words Written: {total_words}\n"
        f"Total Characters: {total_chars}\n"
        f"Words per Minute: {round(total_words / total_minutes, 2) if total_minutes > 0 else 0}\n\n"
        "Video Notes:\n"
        f"{st.session_state.video_notes}\n\n"
        "PDF Notes:\n"
        f"{st.session_state.pdf_notes_area}"
    )
    st.download_button(
        "⬇ Download Study Summary (TXT)",
        summary_text,
        "study_summary.txt",
        mime="text/plain"
    )

# -------------------- Tab 5: Reflection --------------------
with tab5:
    st.subheader("✏ Reflect on Your Learning")

    def save_reflection():
        st.session_state.reflection_text = st.session_state.reflection_text

    st.text_area(
        "Write what you learned in this session...",
        value=st.session_state.reflection_text,
        height=300,
        key="reflection_text",
        on_change=save_reflection
    )
    st.download_button(
        "⬇ Download Reflection (TXT)",
        st.session_state.reflection_text,
        "study_reflection.txt",
        mime="text/plain"
    )

# -------------------- Tab 6: Feedback --------------------
with tab6:
    st.subheader("📝 Give Feedback")
    if st.button("Go to Feedback Form"):
        st.markdown(
            "[Click here to submit feedback](https://docs.google.com/forms/d/e/1FAIpQLSesG3CtkAOL2EZVMS5U4DUtunCo9Q4p6l9WbSqSOuoezp-b7Q/viewform)",
            unsafe_allow_html=True
        )

import streamlit as st
import time

st.set_page_config(page_title="StudyBuddy", layout="wide")
st.title("📚 StudyBuddy")

# -------------------- Session State --------------------
if "notes" not in st.session_state:
    st.session_state.notes = ""
if "running" not in st.session_state:
    st.session_state.running = False
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()
if "break_seconds" not in st.session_state:
    st.session_state.break_seconds = 0
if "reflection" not in st.session_state:
    st.session_state.reflection = ""

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
tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 Study Session",
    "📊 Study Summary",
    "✏ Reflection",
    "📝 Feedback"
])

# -------------------- Tab 1: Study Session --------------------
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

    if video_url:
        if device == "Laptop/Desktop":
            col_video, col_notes = st.columns([1, 1])
        else:
            col_video = st.container()
            col_notes = st.container()

        with col_video:
            st.video(video_url)

        with col_notes:
            st.markdown("📝 Take Notes")
            st.session_state.notes = st.text_area(
                "Write notes here",
                value=st.session_state.notes,
                height=300,
                placeholder="Write your notes while watching the video..."
            )
            words = len(st.session_state.notes.split())
            chars = len(st.session_state.notes)
            w1, w2 = st.columns(2)
            w1.metric("Words", words)
            w2.metric("Characters", chars)
            st.download_button(
                "⬇ Download Notes (TXT)",
                st.session_state.notes,
                "study_notes.txt",
                mime="text/plain"
            )
    else:
        st.info("Paste a video URL to start studying.")

# -------------------- Tab 2: Study Summary --------------------
with tab2:
    st.subheader("📊 Study Summary")
    total_sec = st.session_state.total_seconds
    total_minutes = total_sec // 60
    words = len(st.session_state.notes.split())
    chars = len(st.session_state.notes)
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Study Time", format_hms(total_sec))
    s2.metric("Total Words Written", words)
    s3.metric("Total Characters", chars)
    s4.metric("Words per Minute", round(words / total_minutes, 2) if total_minutes > 0 else 0)
    st.caption("Summary updates in real-time while you study.")

    summary_text = (
        f"Total Study Time: {format_hms(total_sec)}\n"
        f"Total Words Written: {words}\n"
        f"Total Characters: {chars}\n"
        f"Words per Minute: {round(words / total_minutes, 2) if total_minutes > 0 else 0}\n\n"
        "Notes:\n"
        f"{st.session_state.notes}"
    )
    st.download_button(
        "⬇ Download Study Summary (TXT)",
        summary_text,
        "study_summary.txt",
        mime="text/plain"
    )

# -------------------- Tab 3: Reflection --------------------
with tab3:
    st.subheader("🖋 Reflect on Your Learning")
    st.session_state.reflection = st.text_area(
        "Write what you learned in this session...",
        value=st.session_state.reflection,
        height=300
    )
    st.download_button(
        "⬇ Download Reflection (TXT)",
        st.session_state.reflection,
        "study_reflection.txt",
        mime="text/plain"
    )

# -------------------- Tab 4: Feedback --------------------
with tab4:
    st.subheader("💬 Give Feedback")
    if st.button("Go to Feedback Form"):
        st.markdown(
            "[Click here to submit feedback](https://docs.google.com/forms/d/e/1FAIpQLSesG3CtkAOL2EZVMS5U4DUtunCo9Q4p6l9WbSqSOuoezp-b7Q/viewform)",
            unsafe_allow_html=True
        )

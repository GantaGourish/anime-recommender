import html
import random
import re

import streamlit as st
from dotenv import load_dotenv

from pipeline.pipeline import AnimeRecommendationPipeline

st.set_page_config(
    page_title="AniMatch · AI Anime Recommender",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()


@st.cache_resource(show_spinner=False)
def init_pipeline():
    return AnimeRecommendationPipeline()


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stMarkdown, .stTextInput input, button {
    font-family: 'Poppins', sans-serif;
}

/* Animated night-sky background with drifting sakura glow */
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(255, 79, 163, 0.18), transparent 40%),
        radial-gradient(circle at 85% 10%, rgba(124, 92, 255, 0.22), transparent 45%),
        radial-gradient(circle at 50% 100%, rgba(0, 212, 255, 0.12), transparent 50%),
        #0b0a1a;
    background-attachment: fixed;
}
.stApp::before {
    content: "";
    position: fixed; inset: 0;
    pointer-events: none;
    background-image:
        radial-gradient(1.5px 1.5px at 10% 30%, #fff8, transparent),
        radial-gradient(1px 1px at 30% 70%, #fff6, transparent),
        radial-gradient(1.5px 1.5px at 55% 20%, #fff7, transparent),
        radial-gradient(1px 1px at 75% 60%, #fff5, transparent),
        radial-gradient(1.5px 1.5px at 90% 85%, #fff6, transparent),
        radial-gradient(1px 1px at 20% 90%, #fff5, transparent);
    animation: twinkle 6s ease-in-out infinite alternate;
}
@keyframes twinkle { from { opacity: .35 } to { opacity: 1 } }

.block-container { padding-top: 2rem; max-width: 1150px; }
header[data-testid="stHeader"] { background: transparent; }

/* Falling petals */
.petal {
    position: fixed; top: -40px; z-index: 0; pointer-events: none;
    font-size: 18px; opacity: .75;
    animation: fall linear infinite;
}
@keyframes fall {
    0%   { transform: translateY(0) rotate(0deg) translateX(0); }
    50%  { transform: translateY(55vh) rotate(180deg) translateX(40px); }
    100% { transform: translateY(110vh) rotate(360deg) translateX(-20px); }
}

/* Hero */
.hero {
    position: relative;
    text-align: center;
    padding: 2.6rem 1.5rem 2.2rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,79,163,.16), rgba(124,92,255,.16) 55%, rgba(0,212,255,.10));
    border: 1px solid rgba(255,255,255,.10);
    box-shadow: 0 20px 60px rgba(124,92,255,.18), inset 0 1px 0 rgba(255,255,255,.08);
    overflow: hidden;
    margin-bottom: 1.6rem;
}
.hero .jp {
    position: absolute; right: -10px; top: -28px;
    font-family: 'Dela Gothic One', sans-serif;
    font-size: 8.5rem; line-height: 1;
    color: rgba(255,255,255,.04);
    user-select: none;
}
.hero .badge {
    display: inline-block;
    padding: .3rem .9rem;
    border-radius: 999px;
    font-size: .78rem; font-weight: 600; letter-spacing: .12em;
    color: #ffd1e8;
    background: rgba(255,79,163,.15);
    border: 1px solid rgba(255,79,163,.35);
    margin-bottom: .9rem;
}
.hero h1 {
    font-family: 'Dela Gothic One', sans-serif !important;
    font-size: clamp(2.4rem, 6vw, 4.2rem) !important;
    line-height: 1.05 !important;
    margin: 0 !important; padding: 0 !important;
    background: linear-gradient(90deg, #ff4fa3, #b18cff 45%, #4fd8ff);
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 4px 24px rgba(255,79,163,.35));
}
.hero p {
    color: #cfc6f5; font-size: 1.1rem; margin: .8rem auto 0; max-width: 640px;
}
.stats { display: flex; justify-content: center; gap: 2.2rem; margin-top: 1.4rem; flex-wrap: wrap; }
.stats div { color: #a99fd6; font-size: .85rem; }
.stats b { display: block; font-size: 1.35rem; color: #fff; }

/* Section labels */
.section-label {
    font-weight: 700; font-size: .8rem; letter-spacing: .18em;
    text-transform: uppercase; color: #ff8cc6; margin: .4rem 0 .6rem;
}

/* Vibe chips (all buttons inside the vibes container) */
.st-key-vibes button {
    width: 100%;
    border-radius: 999px !important;
    border: 1px solid rgba(177,140,255,.35) !important;
    background: rgba(124,92,255,.10) !important;
    color: #e6deff !important;
    font-weight: 500 !important;
    transition: all .2s ease;
}
.st-key-vibes button:hover {
    transform: translateY(-2px);
    border-color: #ff4fa3 !important;
    background: rgba(255,79,163,.18) !important;
    box-shadow: 0 8px 22px rgba(255,79,163,.25);
}

/* Search form */
[data-testid="stForm"] {
    border: 1px solid rgba(255,255,255,.10) !important;
    border-radius: 22px !important;
    background: rgba(23,20,46,.70);
    backdrop-filter: blur(8px);
    padding: 1.2rem 1.3rem .6rem !important;
}
.stTextInput input {
    border-radius: 14px !important;
    background: rgba(11,10,26,.85) !important;
    border: 1px solid rgba(177,140,255,.35) !important;
    font-size: 1.05rem !important;
    padding: .85rem 1rem !important;
}
.stTextInput input:focus {
    border-color: #ff4fa3 !important;
    box-shadow: 0 0 0 3px rgba(255,79,163,.25) !important;
}
[data-testid="stFormSubmitButton"] button {
    width: 100%;
    border: none !important;
    border-radius: 14px !important;
    padding: .7rem 1rem !important;
    font-weight: 700 !important; font-size: 1.05rem !important;
    color: white !important;
    background: linear-gradient(90deg, #ff4fa3, #7c5cff) !important;
    box-shadow: 0 10px 30px rgba(255,79,163,.35);
    transition: transform .15s ease, box-shadow .15s ease;
}
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 36px rgba(124,92,255,.45);
}

/* Result card */
.st-key-result_card {
    position: relative;
    border-radius: 24px;
    padding: 1.6rem 1.8rem;
    background: linear-gradient(160deg, rgba(36,28,74,.92), rgba(18,15,40,.92));
    border: 1px solid rgba(255,79,163,.35);
    box-shadow: 0 0 0 1px rgba(124,92,255,.15), 0 24px 70px rgba(255,79,163,.18);
    animation: rise .5s ease-out;
}
@keyframes rise { from { opacity: 0; transform: translateY(14px) } to { opacity: 1; transform: none } }
.st-key-result_card h1, .st-key-result_card h2, .st-key-result_card h3 {
    color: #ffb3da !important;
}
.st-key-result_card strong { color: #ffd1e8; }
.st-key-result_card li { margin-bottom: .55rem; line-height: 1.65; }
.st-key-result_card p { line-height: 1.7; color: #e3dcff; }
.result-head {
    display: flex; align-items: center; gap: .7rem; margin-bottom: .4rem;
}
.result-head span.icon {
    font-size: 1.6rem;
    filter: drop-shadow(0 0 12px rgba(255,79,163,.6));
}
.result-head h3 { margin: 0 !important; color: #fff !important; font-weight: 700; }
.query-pill {
    display: inline-block; margin: .2rem 0 1rem;
    padding: .35rem .85rem; border-radius: 999px; font-size: .85rem;
    background: rgba(79,216,255,.10); border: 1px solid rgba(79,216,255,.35); color: #bdf0ff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17142e, #0e0c22) !important;
    border-right: 1px solid rgba(255,255,255,.06);
}
[data-testid="stSidebar"] h2 {
    font-family: 'Dela Gothic One', sans-serif; font-weight: 400;
    background: linear-gradient(90deg, #ff4fa3, #b18cff);
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.st-key-history button {
    width: 100%; text-align: left; justify-content: flex-start;
    border-radius: 12px !important; font-size: .85rem !important;
    background: rgba(255,255,255,.03) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
}

.empty-state {
    text-align: center; padding: 2.4rem 1rem 1rem; color: #8f86bd;
}
.empty-state .big { font-size: 3rem; display: block; margin-bottom: .4rem; }

.footer { text-align: center; color: #6f6799; font-size: .8rem; margin-top: 3rem; }
</style>
""",
    unsafe_allow_html=True,
)

# Falling sakura petals (purely decorative)
petals = "".join(
    f'<div class="petal" style="left:{random.randint(0, 100)}%;'
    f'animation-duration:{random.uniform(9, 18):.1f}s;'
    f'animation-delay:{random.uniform(0, 12):.1f}s;'
    f'font-size:{random.randint(12, 22)}px">🌸</div>'
    for _ in range(14)
)
st.markdown(petals, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
VIBES = {
    "🏫 Cozy school life": "light-hearted, cozy slice of life anime set in a high school with lovable friends",
    "⚔️ Epic battles": "action-packed shonen anime with epic fights, power systems and a strong protagonist",
    "💘 Sweet romance": "heartwarming romance anime with great chemistry and emotional moments",
    "🧠 Mind games": "psychological thriller anime with clever plot twists and mind games",
    "🚀 Space & mecha": "sci-fi anime set in space or with giant mecha and deep world-building",
    "😭 Make me cry": "emotional, tear-jerking anime with a beautiful story about loss and growth",
    "👻 Dark & spooky": "dark horror or supernatural anime with a creepy, mysterious atmosphere",
    "😂 Pure comedy": "hilarious comedy anime with absurd humour and great gags",
}

SURPRISE_PROMPTS = [
    "a hidden gem anime most people have never heard of but is amazing",
    "an underrated fantasy adventure anime with a unique magic system",
    "a short anime I can finish in one weekend with a satisfying ending",
    "a classic 90s anime that still holds up today",
    "an anime with stunning animation and a breathtaking soundtrack",
]

st.session_state.setdefault("query_text", "")
st.session_state.setdefault("history", [])
st.session_state.setdefault("result", None)
st.session_state.setdefault("pending", None)


def queue_query(text: str):
    st.session_state.query_text = text
    st.session_state.pending = text


def surprise_me():
    queue_query(random.choice(SURPRISE_PROMPTS))


# ---------------------------------------------------------------------------
# Sidebar: refine filters + history
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎛️ Tune your taste")
    genres = st.multiselect(
        "Genres",
        ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Isekai",
         "Mecha", "Mystery", "Psychological", "Romance", "Sci-Fi", "Slice of Life",
         "Sports", "Supernatural", "Thriller"],
        placeholder="Pick any genres",
    )
    mood = st.select_slider(
        "Mood",
        options=["Wholesome", "Chill", "Balanced", "Intense", "Dark"],
        value="Balanced",
    )
    length = st.radio(
        "Commitment level",
        ["Any length", "Short (≤ 13 eps)", "Medium (~24 eps)", "Long journey (50+ eps)"],
    )
    st.button("🎲 Surprise me!", use_container_width=True, on_click=surprise_me)

    if st.session_state.history:
        st.markdown("---")
        st.markdown("**🕘 Recent searches**")
        with st.container(key="history"):
            for i, past in enumerate(reversed(st.session_state.history[-6:])):
                label = past if len(past) <= 42 else past[:40] + "…"
                st.button(label, key=f"hist_{i}", on_click=queue_query, args=(past,))


def build_query(text: str) -> str:
    parts = [text.strip()]
    if genres:
        parts.append(f"Preferred genres: {', '.join(genres)}.")
    if mood != "Balanced":
        parts.append(f"Overall mood should be {mood.lower()}.")
    if length != "Any length":
        parts.append(f"Preferred length: {length}.")
    return " ".join(parts)


def clean_response(text: str) -> str:
    # Reasoning models (e.g. qwen) can leak <think> blocks — hide them.
    return re.sub(r"<think>.*?</think>", "", text or "", flags=re.DOTALL).strip()


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="hero">
  <div class="jp">アニメ</div>
  <div class="badge">✦ AI-POWERED ANIME DISCOVERY ✦</div>
  <h1>AniMatch</h1>
  <p>Tell us your vibe and we'll find your next obsession. 🌙</p>
  <div class="stats">
    <div><b>260+</b>titles indexed</div>
    <div><b>3</b>hand-picked matches</div>
    <div><b>∞</b>binge potential</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Vibe chips
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Pick a vibe</div>', unsafe_allow_html=True)
with st.container(key="vibes"):
    cols = st.columns(4)
    for i, (label, prompt) in enumerate(VIBES.items()):
        cols[i % 4].button(label, key=f"vibe_{i}", on_click=queue_query, args=(prompt,))

# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">…or describe it yourself</div>', unsafe_allow_html=True)
with st.form("search", border=True):
    col_in, col_btn = st.columns([5, 1.3], vertical_alignment="bottom")
    text = col_in.text_input(
        "What are you in the mood for?",
        key="query_text",
        placeholder="e.g. a bittersweet story about friendship with gorgeous animation",
        label_visibility="collapsed",
    )
    submitted = col_btn.form_submit_button("Find my anime ✨")

run_text = None
if submitted and text.strip():
    run_text = text.strip()
elif st.session_state.pending:
    run_text = st.session_state.pending
st.session_state.pending = None

if run_text:
    with st.spinner("🔮 Summoning the perfect picks from the anime multiverse…"):
        try:
            pipeline = init_pipeline()
            answer = clean_response(pipeline.recommend(build_query(run_text)))
            st.session_state.result = {"query": run_text, "answer": answer}
            if run_text not in st.session_state.history:
                st.session_state.history.append(run_text)
        except Exception:
            st.session_state.result = None
            st.error("😵 Our recommender tripped over a plot twist. Please try again in a moment!")
elif submitted:
    st.warning("Type a vibe first, senpai! 🙏")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
st.write("")
result = st.session_state.result
if result:
    with st.container(key="result_card"):
        st.markdown(
            '<div class="result-head"><span class="icon">🎴</span>'
            "<h3>Your Recommendations</h3></div>"
            f'<div class="query-pill">🔎 {html.escape(result["query"])}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(result["answer"])
else:
    st.markdown(
        """
<div class="empty-state">
  <span class="big">🍙</span>
  Pick a vibe above or type what you're craving — your next favourite anime is one click away.
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footer">Made with 💖 for anime lovers · Powered by RAG + LLMs</div>',
    unsafe_allow_html=True,
)

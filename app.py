import streamlit as st
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import base64
import pandas as pd

from pathlib import Path
from html import escape
from matplotlib.lines import Line2D
from threading import RLock
from io import BytesIO


# ============================================================
# 01. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Fitness Mountain",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 02. BACKGROUND IMAGE
# ============================================================

@st.cache_data
def load_background():

    path = Path(__file__).parent / "background.jpg"

    if path.exists():

        return base64.b64encode(
            path.read_bytes()
        ).decode("utf-8")

    return ""


background = load_background()

/* ==========================================================
   WELCOME SCREEN COMPACT FIX
   ========================================================== */

.st-key-welcome_screen {
    max-width: 720px;
    padding: 18px 26px !important;
    margin: 0 auto !important;
}

.welcome-mountain {
    width: 100%;
    max-width: 350px;
    max-height: 105px;
    margin: 0 auto 8px;
}

.welcome-title {
    font-size: 36px;
}

.welcome-subtitle {
    margin: 6px 0 10px;
}

.welcome-mission-text {
    font-size: 13px;
    margin-bottom: 12px;
}

.instruction-row {
    padding: 8px 12px;
    margin-bottom: 6px;
}

.instruction-number {
    width: 35px;
    height: 35px;
    font-size: 15px;
}

.instructions-heading {
    margin-bottom: 8px;
}

.st-key-start_game_button button {
    min-height: 42px !important;
}

# ============================================================
# 03. GLOBAL CSS
# ============================================================

CSS = """
<style>

/* ==========================================================
   GLOBAL THEME
   ========================================================== */

:root {
    --background: #080D1C;
    --panel: #111827;
    --border: #29384C;
    --cyan: #22D3EE;
    --light-cyan: #67E8F9;
    --gold: #FBBF24;
    --purple: #E879F9;
    --text: #E2E8F0;
    --muted: #94A3B8;
    --success: #4ADE80;
    --danger: #F87171;
}

.stApp {
    background-color: var(--background);

    background-image:
        linear-gradient(
            rgba(5, 10, 25, 0.87),
            rgba(5, 10, 25, 0.87)
        ),
        url("data:image/jpeg;base64,__BACKGROUND__");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    color: var(--text);

    min-height: 100dvh;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="stMain"] {
    overflow-x: hidden;
    overflow-y: auto !important;
}

.block-container {
    width: 100%;
    max-width: 1800px;

    padding: 1rem 2rem 0.65rem !important;

    box-sizing: border-box;
}

.block-container > [data-testid="stVerticalBlock"] {
    gap: 0.65rem !important;
}

[data-testid="stColumn"] {
    min-width: 0;
}

[data-testid="stWidgetLabel"] p {
    color: var(--text);
}


/* ==========================================================
   APPLICATION HEADER
   ========================================================== */

.hero {
    width: 100%;
    text-align: center;

    padding: 0 0 12px;
    margin: 0 0 3px;

    box-sizing: border-box;
}

.hero-label {
    color: var(--cyan);

    font-size: 10px;
    font-weight: 700;

    letter-spacing: 5px;
    line-height: 1.4;

    margin-bottom: 6px;
}

.hero-title {
    color: #E0F2FE;

    font-size: clamp(25px, 3vw, 34px);
    font-weight: 900;

    letter-spacing: 5px;
    line-height: 1.2;

    margin-bottom: 7px;

    text-shadow: 0 0 22px #0891B2;
}

.hero-subtitle {
    color: var(--muted);

    font-size: 10px;

    letter-spacing: 3px;
    line-height: 1.5;
}


/* ==========================================================
   WELCOME SCREEN
   ========================================================== */

.st-key-welcome_screen {
    width: 100%;
    max-width: 720px;

    margin: 2vh auto 0 !important;

    padding: 24px 30px !important;

    border: 1px solid #164E63;
    border-radius: 18px;

    background: rgba(8, 13, 28, 0.96);

    box-shadow:
        0 0 45px rgba(34, 211, 238, 0.10),
        inset 0 0 30px rgba(34, 211, 238, 0.025);

    box-sizing: border-box;
}

.welcome-label {
    color: #22D3EE;

    font-size: 10px;
    font-weight: 700;

    letter-spacing: 4px;

    text-align: center;

    margin-bottom: 10px;
}

.welcome-title {
    color: #E0F2FE;

    font-size: clamp(28px, 4vw, 42px);
    font-weight: 900;

    letter-spacing: 4px;
    line-height: 1.2;

    text-align: center;

    text-shadow: 0 0 24px #0891B2;
}

.welcome-subtitle {
    color: #94A3B8;

    font-size: 11px;

    letter-spacing: 2px;

    text-align: center;

    margin: 9px 0 16px;
}

.welcome-mountain {
    width: 100%;
    max-width: 430px;

    display: block;

    margin: 0 auto 10px;
}

.welcome-mission {
    color: #FBBF24;

    font-size: 19px;
    font-weight: 800;

    text-align: center;

    letter-spacing: 2px;

    margin-bottom: 7px;
}

.welcome-mission-text {
    color: #CBD5E1;

    font-size: 14px;
    line-height: 1.6;

    text-align: center;

    margin-bottom: 18px;
}

.instructions-heading {
    color: #67E8F9;

    font-size: 12px;
    font-weight: 800;

    letter-spacing: 2px;

    text-align: center;

    margin-bottom: 12px;
}

.instruction-row {
    display: flex;
    align-items: center;

    gap: 14px;

    padding: 11px 14px;

    margin-bottom: 8px;

    border: 1px solid #29384C;
    border-radius: 9px;

    background: rgba(17, 24, 39, 0.90);
}

.instruction-number {
    display: flex;

    align-items: center;
    justify-content: center;

    width: 42px;
    height: 42px;

    flex-shrink: 0;

    border: 1px solid #155E75;
    border-radius: 8px;

    background: rgba(34, 211, 238, 0.08);

    color: #22D3EE;

    font-size: 18px;
    font-weight: 800;
}

.instruction-content {
    flex: 1;
    min-width: 0;
}

.instruction-title {
    color: #E2E8F0;

    font-size: 14px;
    font-weight: 700;

    margin-bottom: 3px;
}

.instruction-text {
    color: #94A3B8;

    font-size: 12px;
    line-height: 1.5;
}

.st-key-start_game_button button {
    min-height: 48px !important;

    font-size: 16px !important;
    font-weight: 800 !important;

    letter-spacing: 2px;

    background: linear-gradient(
        90deg,
        #155E75,
        #0E7490
    ) !important;

    border: 1px solid #22D3EE !important;

    color: #FFFFFF !important;

    box-shadow: 0 0 20px rgba(34, 211, 238, 0.16);
}


/* ==========================================================
   MAIN DASHBOARD
   ========================================================== */

.st-key-main_dashboard {
    width: 100%;
    min-width: 0;

    box-sizing: border-box;
}

.st-key-main_dashboard
[data-testid="stHorizontalBlock"] {
    align-items: flex-start;
}

.st-key-left_panel {
    width: 100%;
    min-width: 0;

    box-sizing: border-box;
}

.st-key-left_panel
[data-testid="stVerticalBlock"] {
    gap: 0.45rem !important;
}

.st-key-right_panel
[data-testid="stVerticalBlock"] {
    gap: 0.55rem !important;
}


/* ==========================================================
   SECTION HEADINGS
   ========================================================== */

.section-heading {
    color: var(--light-cyan);

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.8px;
    line-height: 1.5;

    margin: 0 0 3px;
}


/* ==========================================================
   RADIO BUTTONS
   ========================================================== */

.st-key-left_panel [role="radiogroup"] {
    width: 100%;

    display: flex;
    flex-direction: column;

    gap: 2px;

    padding: 6px 10px;

    box-sizing: border-box;

    border: 1px solid var(--border);
    border-radius: 9px;

    background: rgba(17, 24, 39, 0.85);
}

.st-key-left_panel [role="radiogroup"] label {
    width: 100%;

    margin: 0;
    padding: 1px 0;
}

.st-key-left_panel [role="radiogroup"] p {
    color: #E2E8F0;

    font-size: 13px;
    line-height: 1.4;
}


/* ==========================================================
   STRATEGY DESCRIPTION
   ========================================================== */

.strategy-description {
    width: 100%;

    box-sizing: border-box;

    background: rgba(17, 24, 39, 0.94);

    border: 1px solid var(--border);
    border-radius: 8px;

    padding: 8px 10px;
}

.strategy-description-title {
    font-size: 12px;
    font-weight: 700;

    line-height: 1.5;

    margin-bottom: 3px;
}

.strategy-description-text {
    color: #CBD5E1;

    font-size: 12px;
    line-height: 1.45;
}


/* ==========================================================
   SLIDER
   ========================================================== */

.st-key-left_panel [data-testid="stSlider"] {
    width: 100%;

    padding: 0 !important;
    margin: 0 !important;
}

.st-key-left_panel [data-testid="stWidgetLabel"] p {
    font-size: 12px;
}

.slider-help {
    color: var(--muted);

    font-size: 11px;
    line-height: 1.4;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {
    width: 100%;

    min-height: 35px;

    padding: 6px 10px;

    box-sizing: border-box;

    background: rgba(17, 24, 39, 0.96);

    border: 1px solid var(--border);
    border-radius: 8px;

    color: var(--light-cyan);

    font-weight: 600;

    transition:
        background 0.2s ease,
        border-color 0.2s ease;
}

.stButton > button p {
    font-size: 13px;
    line-height: 1.4;
}

.stButton > button[kind="primary"] {
    background: #155E75;

    border-color: var(--cyan);

    color: #FFFFFF;
}

.stButton > button:hover {
    background: #164E63;

    border-color: var(--cyan);

    color: #FFFFFF;
}

.stButton > button:disabled {
    opacity: 0.45;

    cursor: not-allowed;
}


/* ==========================================================
   MISSION CARD
   ========================================================== */

.mission-card {
    width: 100%;

    background: rgba(17, 24, 39, 0.78);

    border: 1px solid var(--border);
    border-radius: 8px;

    padding: 8px 10px;

    box-sizing: border-box;
}

.mission-title {
    color: var(--light-cyan);

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.6px;

    margin-bottom: 5px;
}

.mission-text {
    color: #A8BED3;

    font-size: 11px;
    line-height: 1.5;
}

.mission-target {
    color: #FBBF24;

    font-weight: 800;
}


/* ==========================================================
   STATISTIC CARDS
   ========================================================== */

.metric-grid {
    display: grid;

    grid-template-columns:
        repeat(5, minmax(0, 1fr));

    gap: 9px;

    width: 100%;
}

.metric-card {
    display: flex;
    flex-direction: column;

    justify-content: center;

    background: rgba(17, 24, 39, 0.95);

    border: 1px solid var(--border);
    border-radius: 10px;

    padding: 10px 12px;

    min-width: 0;
    min-height: 68px;

    box-sizing: border-box;
}

.metric-label {
    color: var(--muted);

    font-size: 9px;
    font-weight: 700;

    letter-spacing: 0.6px;
    line-height: 1.5;

    margin-bottom: 5px;
}

.metric-value {
    font-size: clamp(18px, 1.7vw, 25px);
    font-weight: 800;

    line-height: 1.2;

    overflow-wrap: anywhere;
}


/* ==========================================================
   GENERATION PROGRESS
   ========================================================== */

.progress-track {
    width: 100%;
    height: 5px;

    background: #1E293B;

    border-radius: 20px;

    overflow: hidden;

    margin-top: 9px;
}

.progress-fill {
    height: 100%;

    border-radius: 20px;

    transition: width 0.3s ease;
}


/* ==========================================================
   FITNESS LANDSCAPE
   ========================================================== */

.fitness-image {
    display: block;

    width: 100%;
    max-width: 100%;

    max-height: 39dvh;

    height: auto;

    object-fit: contain;

    background: #0B1120;

    border: 1px solid var(--border);
    border-radius: 10px;

    box-sizing: border-box;
}


/* ==========================================================
   TARGET STATUS
   ========================================================== */

.target-status {
    display: flex;

    justify-content: space-between;
    align-items: center;

    gap: 10px;

    padding: 8px 12px;

    border: 1px solid var(--border);
    border-radius: 8px;

    background: rgba(17, 24, 39, 0.90);

    font-size: 11px;
}

.target-status-label {
    color: #94A3B8;

    font-weight: 600;
}

.target-status-value {
    font-weight: 800;

    letter-spacing: 0.7px;
}


/* ==========================================================
   LIVE EVOLUTION FEEDBACK
   ========================================================== */

.feedback-box {
    width: 100%;

    background: rgba(17, 24, 39, 0.96);

    border: 1px solid var(--border);
    border-left: 4px solid var(--gold);

    border-radius: 9px;

    padding: 9px 12px;

    box-sizing: border-box;
}

.feedback-title {
    color: var(--gold);

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.8px;

    margin-bottom: 5px;
}

.feedback-text {
    color: var(--text);

    font-size: 12px;
    line-height: 1.5;

    overflow-wrap: break-word;
}

.feedback-success {
    border-left-color: #22C55E;
}

.feedback-success .feedback-title {
    color: #4ADE80;
}

.feedback-failed {
    border-left-color: #EF4444;
}

.feedback-failed .feedback-title {
    color: #F87171;
}


/* ==========================================================
   BOTTOM NAVIGATION
   ========================================================== */

.st-key-bottom_navigation {
    width: 100%;

    border-top: 1px solid var(--border);

    padding-top: 8px;

    margin-top: 3px;

    box-sizing: border-box;
}


/* ==========================================================
   DIALOG WINDOWS
   ========================================================== */

[data-testid="stDialog"] [role="dialog"] {
    background: #0B1120 !important;

    color: #E2E8F0;

    max-height: 90dvh;

    overflow-y: auto !important;
    overflow-x: hidden;

    border: 1px solid #29384C;
    border-radius: 16px;
}

[data-testid="stDialog"]
[data-testid="stVerticalBlock"] {
    gap: 0.75rem;
}


/* ==========================================================
   MISSION RESULT POP-UP
   ========================================================== */

.result-container {
    width: 100%;

    text-align: center;

    padding: 20px 15px;

    box-sizing: border-box;

    border-radius: 15px;
}

.result-success {
    border: 1px solid #22C55E;

    background:
        radial-gradient(
            ellipse at top,
            rgba(34, 197, 94, 0.12),
            transparent 70%
        ),
        #080D1C;

    box-shadow:
        0 0 35px rgba(34, 197, 94, 0.12);
}

.result-failed {
    border: 1px solid #EF4444;

    background:
        radial-gradient(
            ellipse at top,
            rgba(239, 68, 68, 0.12),
            transparent 70%
        ),
        #080D1C;

    box-shadow:
        0 0 35px rgba(239, 68, 68, 0.12);
}

.result-icon {
    font-size: 75px;

    line-height: 1.2;

    margin-bottom: 12px;

    animation: resultAppear 0.5s ease-out;
}

@keyframes resultAppear {
    from {
        opacity: 0;
        transform: scale(0.65);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

.result-title {
    font-size: clamp(27px, 4vw, 40px);

    font-weight: 900;

    letter-spacing: 3px;

    line-height: 1.2;

    margin-bottom: 12px;
}

.result-success .result-title {
    color: #4ADE80;

    text-shadow:
        0 0 24px rgba(34, 197, 94, 0.35);
}

.result-failed .result-title {
    color: #F87171;

    text-shadow:
        0 0 24px rgba(239, 68, 68, 0.35);
}

.result-description {
    color: #CBD5E1;

    font-size: 14px;
    line-height: 1.6;

    max-width: 580px;

    margin: 0 auto 20px;
}

.result-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 10px;

    margin-bottom: 18px;
}

.result-stat {
    background: #111827;

    border: 1px solid #29384C;
    border-radius: 10px;

    padding: 14px 8px;
}

.result-stat-label {
    color: #94A3B8;

    font-size: 10px;
    font-weight: 700;

    letter-spacing: 0.7px;

    margin-bottom: 7px;
}

.result-stat-value {
    color: #E2E8F0;

    font-size: 25px;
    font-weight: 800;
}

.result-strategy-label {
    color: #94A3B8;

    font-size: 10px;

    letter-spacing: 1.5px;

    margin-bottom: 5px;
}

.result-strategy {
    font-size: 19px;
    font-weight: 800;

    margin-bottom: 8px;
}

.result-distance {
    font-size: 13px;
    font-weight: 700;

    margin-bottom: 5px;
}

.result-reason {
    text-align: left;

    background: #111827;

    border: 1px solid #29384C;
    border-radius: 9px;

    padding: 14px;

    margin-top: 15px;
}

.result-reason-title {
    color: #FBBF24;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.3px;

    margin-bottom: 7px;
}

.result-reason-text {
    color: #CBD5E1;

    font-size: 13px;
    line-height: 1.6;
}


/* ==========================================================
   RESPONSIVE DESKTOP
   ========================================================== */

@media (min-width: 1200px)
and (max-height: 820px) {

    .block-container {
        padding-top: 0.65rem !important;
        padding-bottom: 0.5rem !important;
    }

    .hero {
        padding-bottom: 7px;
    }

    .hero-title {
        font-size: 30px;
    }

    .st-key-left_panel
    [data-testid="stVerticalBlock"] {
        gap: 0.3rem !important;
    }

    .strategy-description {
        padding: 6px 9px;
    }

    .strategy-description-text {
        font-size: 11px;
    }

    .metric-card {
        min-height: 62px;
        padding: 8px 10px;
    }

    .fitness-image {
        max-height: 35dvh;
    }

    .feedback-box {
        padding: 8px 10px;
    }

    .stButton > button {
        min-height: 32px;
    }

    .st-key-welcome_screen {
        margin-top: 0 !important;

        padding: 16px 25px !important;
    }

    .welcome-mountain {
        max-width: 350px;
    }
}


/* ==========================================================
   SMALL SCREENS
   ========================================================== */

@media (max-width: 1199px) {

    .block-container {
        padding: 1.2rem 1rem !important;
    }

    .metric-grid {
        grid-template-columns:
            repeat(3, minmax(0, 1fr));
    }

    .fitness-image {
        max-height: none;
    }

    .hero-title {
        font-size: 28px;
        letter-spacing: 3px;
    }
}

@media (max-width: 600px) {

    .hero-title {
        font-size: 23px;
        letter-spacing: 2px;
    }

    .hero-label,
    .hero-subtitle {
        letter-spacing: 1px;
    }

    .metric-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

    .st-key-welcome_screen {
        padding: 16px !important;
    }

    .welcome-title {
        font-size: 27px;
        letter-spacing: 2px;
    }

    .result-title {
        font-size: 26px;
        letter-spacing: 1px;
    }

    .result-stat-value {
        font-size: 19px;
    }

    .result-grid {
        gap: 5px;
    }

    .target-status {
        flex-wrap: wrap;
    }
}

</style>
"""

st.markdown(
    CSS.replace("__BACKGROUND__", background),
    unsafe_allow_html=True
)


# ============================================================
# 04. SIMULATION CONSTANTS
# ============================================================

MAX_GENERATIONS = 30

POPULATION_SIZE = 5

MIN_SIGMA = 0.5

MAX_SIGMA = 50.0

MIN_POSITION = 0

MAX_POSITION = 100

INITIAL_POSITION = 10

LOCAL_OPTIMUM = 27

GLOBAL_OPTIMUM = 79

TARGET_POSITION = GLOBAL_OPTIMUM

TARGET_FITNESS = 100.0

SIMULATION_VERSION = "exact_peak_v1"


STRATEGIES = {

    "Deterministic": {

        "icon": "⏱️",

        "color": "#22D3EE",

        "description": (
            "Step size decreases according to a "
            "predefined generation schedule."
        )

    },

    "Adaptive": {

        "icon": "⚡",

        "color": "#FBBF24",

        "description": (
            "Step size changes according to mutation "
            "success using the 1/5 Success Rule."
        )

    },

    "Self-Adaptive": {

        "icon": "🧬",

        "color": "#D946EF",

        "description": (
            "Each individual evolves its own "
            "mutation step size."
        )

    }

}


# ============================================================
# 05. FITNESS FUNCTION
# ============================================================

def fitness(x):

    return (

        25

        + 40 * np.exp(
            -((x - LOCAL_OPTIMUM) / 13) ** 2
        )

        + 75 * np.exp(
            -((x - GLOBAL_OPTIMUM) / 15) ** 2
        )

    )


# ============================================================
# 06. INITIALIZE APPLICATION STATE
# ============================================================

if "game_started" not in st.session_state:

    st.session_state.game_started = False


if "selected_strategy" not in st.session_state:

    st.session_state.selected_strategy = "Deterministic"


if "initial_sigma" not in st.session_state:

    st.session_state.initial_sigma = 15


if "active_dialog" not in st.session_state:

    st.session_state.active_dialog = None


# ============================================================
# 07. RESET SIMULATION
# ============================================================

def reset_simulation(strategy=None, initial_sigma=None):

    if strategy is None:

        strategy = st.session_state.selected_strategy

    if initial_sigma is None:

        initial_sigma = st.session_state.initial_sigma

    initial_sigma = float(initial_sigma)

    # Reset generation

    st.session_state.generation = 0

    # Create five individuals at position 10

    st.session_state.population = [

        (
            INITIAL_POSITION,
            initial_sigma
        )

        for _ in range(POPULATION_SIZE)

    ]

    # Reset shared step size

    st.session_state.sigma = initial_sigma

    # Reset histories

    st.session_state.history = [

        float(fitness(INITIAL_POSITION))

    ]

    st.session_state.sigma_history = [

        initial_sigma

    ]

    st.session_state.position_history = [

        INITIAL_POSITION

    ]

    st.session_state.distance_history = [

        abs(TARGET_POSITION - INITIAL_POSITION)

    ]

    st.session_state.success_history = [0.0]

    # Reset mutation details

    st.session_state.last_mutations = []

    # Reset mission status

    st.session_state.mission_success = False

    st.session_state.mission_failed = False

    st.session_state.game_finished = False

    st.session_state.success_generation = None

    st.session_state.result_shown = False

    st.session_state.active_dialog = None

    # Reset feedback

    st.session_state.feedback = (

        "Your population starts at position 10. "

        "Reach exactly position 79 within "

        "30 generations. Press Next Generation "

        "to begin."

    )

    # Store selected settings

    st.session_state.settings = (

        strategy,

        initial_sigma

    )

    st.session_state.simulation_version = (

        SIMULATION_VERSION

    )


# ============================================================
# 08. VALIDATE SIMULATION STATE
# ============================================================

def initialize_simulation():

    required_keys = [

        "generation",
        "population",
        "sigma",
        "history",
        "sigma_history",
        "position_history",
        "distance_history",
        "success_history",
        "last_mutations",
        "feedback",
        "settings",
        "mission_success",
        "mission_failed",
        "game_finished",
        "success_generation",
        "result_shown",
        "simulation_version"

    ]

    missing_state = any(

        key not in st.session_state

        for key in required_keys

    )

    if missing_state:

        reset_simulation()

        return

    # Prevent old continuous-position state
    # from being reused in the new game.

    if (

        st.session_state.simulation_version

        != SIMULATION_VERSION

    ):

        reset_simulation()

        return

    current_settings = (

        st.session_state.selected_strategy,

        float(st.session_state.initial_sigma)

    )

    if st.session_state.settings != current_settings:

        reset_simulation()

        return

    if len(st.session_state.population) != POPULATION_SIZE:

        reset_simulation()

        return

    generation = st.session_state.generation

    if not 0 <= generation <= MAX_GENERATIONS:

        reset_simulation()

        return

    expected_length = generation + 1

    history_keys = [

        "history",
        "sigma_history",
        "position_history",
        "distance_history",
        "success_history"

    ]

    invalid_history = any(

        len(st.session_state[key]) != expected_length

        for key in history_keys

    )

    if invalid_history:

        reset_simulation()

        return

    # All positions must be integers.

    invalid_position = any(

        not float(x).is_integer()

        or not MIN_POSITION <= x <= MAX_POSITION

        for x, _ in st.session_state.population

    )

    if invalid_position:

        reset_simulation()


initialize_simulation()


# ============================================================
# 09. MISSION STATUS HELPERS
# ============================================================

def get_best_individual():

    return st.session_state.population[0]


def get_best_position():

    best_x, _ = get_best_individual()

    return int(best_x)


def get_distance_from_target():

    return abs(

        TARGET_POSITION - get_best_position()

    )


def get_target_status(position):

    position = int(position)

    if position == TARGET_POSITION:

        return (

            "EXACT GLOBAL OPTIMUM",

            "#4ADE80"

        )

    elif position < TARGET_POSITION:

        return (

            "BELOW TARGET POSITION",

            "#FBBF24"

        )

    else:

        return (

            "OVERSHOT TARGET POSITION",

            "#F87171"

        )


def get_failure_reason(position):

    position = int(position)

    if abs(position - LOCAL_OPTIMUM) <= 5:

        return (

            "Trapped near the Local Optimum",

            "The population remained near the smaller "

            "mountain and did not reach the global peak. "

            "Try a different strategy or a larger initial "

            "mutation step size to encourage exploration."

        )

    elif position < TARGET_POSITION:

        return (

            "Undershot the Target",

            f"The best individual stopped at position "

            f"{position}, which is "

            f"{TARGET_POSITION - position} unit(s) "

            "before the exact Global Optimum. "

            "Try another parameter control strategy "

            "or initial mutation step size."

        )

    elif position > TARGET_POSITION:

        return (

            "Overshot the Target",

            f"The best individual stopped at position "

            f"{position}, which is "

            f"{position - TARGET_POSITION} unit(s) "

            "beyond the exact Global Optimum. "

            "Try a strategy that provides better "

            "refinement near the target."

        )

    return (

        "Target not reached",

        "Try a different strategy or initial step size."

    )


# ============================================================
# 10. EVOLUTION PROCESS
# ============================================================

def next_generation():

    # Do not evolve after winning or losing.

    if st.session_state.game_finished:

        return

    if st.session_state.generation >= MAX_GENERATIONS:

        return

    strategy, initial_sigma = st.session_state.settings

    population = list(

        st.session_state.population

    )

    sigma = float(

        st.session_state.sigma

    )

    previous_best_x = int(

        population[0][0]

    )

    offspring = []

    mutation_details = []

    successes = 0

    # --------------------------------------------------------
    # MUTATION
    # --------------------------------------------------------

    for i, (x, individual_sigma) in enumerate(population):

        x = int(x)

        individual_sigma = float(individual_sigma)

        # SELF-ADAPTIVE CONTROL

        if strategy == "Self-Adaptive":

            child_sigma = float(

                np.clip(

                    individual_sigma

                    * np.exp(

                        0.4 * np.random.normal()

                    ),

                    MIN_SIGMA,

                    MAX_SIGMA

                )

            )

        # DETERMINISTIC AND ADAPTIVE CONTROL

        else:

            child_sigma = sigma

        # Generate random mutation

        mutation = np.random.normal(

            0,

            child_sigma

        )

        # IMPORTANT:
        # Convert the new position to an integer.
        #
        # This allows an individual to reach
        # exactly position 79.

        child_x = int(

            np.clip(

                np.rint(x + mutation),

                MIN_POSITION,

                MAX_POSITION

            )

        )

        offspring.append(

            (
                child_x,
                child_sigma
            )

        )

        parent_fitness = float(fitness(x))

        child_fitness = float(fitness(child_x))

        improved = child_fitness > parent_fitness

        if improved:

            successes += 1

        mutation_details.append({

            "Individual": i + 1,

            "Parent Position": x,

            "Offspring Position": child_x,

            "Movement": child_x - x,

            "Step Size Used": round(child_sigma, 2),

            "Parent Fitness": round(parent_fitness, 2),

            "Offspring Fitness": round(child_fitness, 2),

            "Mutation Result": (

                "Improved"

                if improved

                else "Not Improved"

            )

        })

    # --------------------------------------------------------
    # SURVIVAL SELECTION
    # --------------------------------------------------------

    combined = population + offspring

    # Select according to fitness.
    # Keep the best five individuals.

    combined.sort(

        key=lambda individual: float(

            fitness(individual[0])

        ),

        reverse=True

    )

    new_population = combined[:POPULATION_SIZE]

    # Increase generation counter

    generation = st.session_state.generation + 1

    # Calculate success rate

    success_rate = successes / POPULATION_SIZE

    # --------------------------------------------------------
    # DETERMINISTIC CONTROL
    # --------------------------------------------------------

    if strategy == "Deterministic":

        new_sigma = max(

            MIN_SIGMA,

            initial_sigma * (

                1 - generation / MAX_GENERATIONS

            )

        )

        feedback = (

            f"Generation {generation}: "

            f"Step size decreased from "

            f"{sigma:.2f} to {new_sigma:.2f} "

            "according to the predefined schedule. "

            "Smaller steps encourage refinement."

        )

    # --------------------------------------------------------
    # ADAPTIVE CONTROL
    # --------------------------------------------------------

    elif strategy == "Adaptive":

        if success_rate > 0.2:

            new_sigma = min(

                MAX_SIGMA,

                sigma * 1.25

            )

            action = (

                "increased"

                if new_sigma > sigma

                else "maintained at the maximum"

            )

        elif success_rate < 0.2:

            new_sigma = max(

                MIN_SIGMA,

                sigma * 0.8

            )

            action = (

                "decreased"

                if new_sigma < sigma

                else "maintained at the minimum"

            )

        else:

            new_sigma = sigma

            action = "maintained"

        feedback = (

            f"Generation {generation}: "

            f"{successes}/{POPULATION_SIZE} mutations "

            f"were successful ({success_rate:.0%}). "

            f"Step size {action}: "

            f"{sigma:.2f} → {new_sigma:.2f}."

        )

    # --------------------------------------------------------
    # SELF-ADAPTIVE CONTROL
    # --------------------------------------------------------

    else:

        new_sigma = float(

            new_population[0][1]

        )

        feedback = (

            f"Generation {generation}: "

            "Each individual evolved its own step size. "

            f"The best surviving individual's "

            f"step size is {new_sigma:.2f}."

        )

    # --------------------------------------------------------
    # SYNCHRONIZE SHARED STEP SIZE
    # --------------------------------------------------------

    if strategy != "Self-Adaptive":

        new_population = [

            (
                int(x),
                float(new_sigma)
            )

            for x, _ in new_population

        ]

    # --------------------------------------------------------
    # CALCULATE BEST INDIVIDUAL
    # --------------------------------------------------------

    best_x = int(

        new_population[0][0]

    )

    best_fitness = float(

        fitness(best_x)

    )

    distance = abs(

        TARGET_POSITION - best_x

    )

    # --------------------------------------------------------
    # EXACT GLOBAL OPTIMUM CHECK
    # --------------------------------------------------------

    # No approximate fitness threshold.
    #
    # No tolerance range.
    #
    # No automatic snapping to position 79.
    #
    # An individual must reach exactly 79.

    mission_success = any(

        int(x) == TARGET_POSITION

        for x, _ in new_population

    )

    mission_failed = (

        generation >= MAX_GENERATIONS

        and not mission_success

    )

    game_finished = (

        mission_success

        or mission_failed

    )

    success_generation = (

        generation

        if mission_success

        else None

    )

    # --------------------------------------------------------
    # UPDATE FEEDBACK
    # --------------------------------------------------------

    feedback += (

        f" Best position: "

        f"{previous_best_x} → {best_x}. "

        f"Distance from target: {distance} unit(s)."

    )

    # --------------------------------------------------------
    # UPDATE SIMULATION STATE
    # --------------------------------------------------------

    st.session_state.population = new_population

    st.session_state.generation = generation

    st.session_state.sigma = float(new_sigma)

    st.session_state.feedback = feedback

    st.session_state.last_mutations = mutation_details

    st.session_state.mission_success = mission_success

    st.session_state.mission_failed = mission_failed

    st.session_state.game_finished = game_finished

    st.session_state.success_generation = success_generation

    # --------------------------------------------------------
    # UPDATE HISTORIES
    # --------------------------------------------------------

    st.session_state.history = (

        list(st.session_state.history)

        + [best_fitness]

    )

    st.session_state.sigma_history = (

        list(st.session_state.sigma_history)

        + [float(new_sigma)]

    )

    st.session_state.position_history = (

        list(st.session_state.position_history)

        + [best_x]

    )

    st.session_state.distance_history = (

        list(st.session_state.distance_history)

        + [distance]

    )

    st.session_state.success_history = (

        list(st.session_state.success_history)

        + [float(success_rate)]

    )

    # --------------------------------------------------------
    # OPEN MISSION RESULT
    # --------------------------------------------------------

    if game_finished:

        st.session_state.result_shown = False

        st.session_state.active_dialog = "result"


# ============================================================
# 11. GAME CONTROL CALLBACKS
# ============================================================

def handle_start_game():

    reset_simulation()

    st.session_state.game_started = True


def handle_settings_change():

    reset_simulation()


def handle_next_generation():

    if not st.session_state.game_finished:

        next_generation()


def handle_run_all():

    remaining_generations = (

        MAX_GENERATIONS

        - st.session_state.generation

    )

    for _ in range(remaining_generations):

        # Stop immediately if the exact
        # Global Optimum has been reached.

        if st.session_state.game_finished:

            break

        next_generation()


def handle_reset():

    reset_simulation()


def handle_play_again():

    reset_simulation()

    st.session_state.game_started = True


def handle_home():

    reset_simulation()

    st.session_state.game_started = False


def open_dialog(dialog_name):

    st.session_state.active_dialog = dialog_name


def close_dialog():

    st.session_state.active_dialog = None


# ============================================================
# 12. REUSABLE UI COMPONENTS
# ============================================================

def section_heading(text):

    st.markdown(

        f'<div class="section-heading">'

        f'{escape(text)}'

        f'</div>',

        unsafe_allow_html=True

    )


def metric_html(label, value, color):

    return (

        '<div class="metric-card">'

        '<div class="metric-label">'

        f'{escape(str(label))}'

        '</div>'

        f'<div class="metric-value" '

        f'style="color:{color};">'

        f'{escape(str(value))}'

        '</div>'

        '</div>'

    )


def result_metric_html(label, value, color="#E2E8F0"):

    return (

        '<div class="result-stat">'

        '<div class="result-stat-label">'

        f'{escape(str(label))}'

        '</div>'

        '<div class="result-stat-value" '

        f'style="color:{color};">'

        f'{escape(str(value))}'

        '</div>'

        '</div>'

    )


# ============================================================
# 13. WELCOME SCREEN
# ============================================================

def display_welcome_screen():

    with st.container(key="welcome_screen"):

        st.html("""
        <div class="welcome-label">
            EVOLUTIONARY COMPUTATION
        </div>

        <div class="welcome-title">
            FITNESS MOUNTAIN
        </div>

        <div class="welcome-subtitle">
            THE PARAMETER CONTROL CHALLENGE
        </div>

        <svg
            class="welcome-mountain"
            viewBox="0 0 430 115"
            xmlns="http://www.w3.org/2000/svg">

            <path
                d="M0 108 L95 42 L150 83 L275 10 L430 108 Z"
                fill="#22D3EE"
                fill-opacity="0.10"
            />

            <path
                d="M0 108 L95 42 L150 83 L275 10 L430 108"
                fill="none"
                stroke="#22D3EE"
                stroke-width="2"
            />

            <path
                d="M95 42 L110 108
                   M150 83 L175 108
                   M275 10 L230 108
                   M275 10 L320 108
                   M0 108 H430"
                stroke="#22D3EE"
                stroke-opacity="0.25"
                fill="none"
            />

            <circle
                cx="275"
                cy="10"
                r="10"
                fill="#FBBF24"
                opacity="0.20"
            />

            <circle
                cx="275"
                cy="10"
                r="4"
                fill="#FBBF24"
            />

            <text
                x="275"
                y="43"
                fill="#FBBF24"
                font-size="11"
                text-anchor="middle"
                font-weight="bold">
                GLOBAL OPTIMUM
            </text>

            <text
                x="95"
                y="27"
                fill="#94A3B8"
                font-size="9"
                text-anchor="middle">
                LOCAL OPTIMUM
            </text>

        </svg>

        <div class="welcome-mission">
            YOUR MISSION
        </div>

        <div class="welcome-mission-text">
            Reach the exact Global Optimum at
            <strong style="color:#FBBF24;">
                position 79
            </strong>
            within 30 generations.
            <br>
            Falling short or overshooting the target
            after 30 generations means mission failed.
        </div>

        <div class="instructions-heading">
            HOW TO PLAY
        </div>

        <div class="instruction-row">

            <div class="instruction-number">
                01
            </div>

            <div class="instruction-content">

                <div class="instruction-title">
                    Choose Your Strategy
                </div>

                <div class="instruction-text">
                    Select Deterministic, Adaptive
                    or Self-Adaptive Control.
                </div>

            </div>

        </div>

        <div class="instruction-row">

            <div class="instruction-number">
                02
            </div>

            <div class="instruction-content">

                <div class="instruction-title">
                    Set Your Step Size
                </div>

                <div class="instruction-text">
                    Large step sizes encourage exploration.
                    Small step sizes encourage refinement.
                </div>

            </div>

        </div>

        <div class="instruction-row">

            <div class="instruction-number">
                03
            </div>

            <div class="instruction-content">

                <div class="instruction-title">
                    Reach the Exact Peak
                </div>

                <div class="instruction-text">
                    Press Next Generation or Run All
                    to reach exactly position 79.
                </div>

            </div>

        </div>
        """)

        st.button(
            "▶ START GAME",
            type="primary",
            key="start_game_button",
            use_container_width=True,
            on_click=handle_start_game
        )

# ============================================================
# 14. APPLICATION HEADER
# ============================================================

def display_header():

    st.markdown(

        """
        <div class="hero">

            <div class="hero-label">
                EVOLUTIONARY COMPUTATION
            </div>

            <div class="hero-title">
                FITNESS MOUNTAIN
            </div>

            <div class="hero-subtitle">
                THE PARAMETER CONTROL CHALLENGE
            </div>

        </div>
        """,

        unsafe_allow_html=True

    )


# ============================================================
# 15. DISPLAY STATISTIC CARDS
# ============================================================

def display_metrics(strategy):

    generation = st.session_state.generation

    best_x = get_best_position()

    best_fitness = float(

        fitness(best_x)

    )

    distance = get_distance_from_target()

    sigma_label = (

        "BEST STEP SIZE (σ)"

        if strategy == "Self-Adaptive"

        else "NEXT STEP SIZE (σ)"

    )

    position_color = (

        "#4ADE80"

        if best_x == TARGET_POSITION

        else "#67E8F9"

    )

    distance_color = (

        "#4ADE80"

        if distance == 0

        else "#E879F9"

    )

    cards = [

        metric_html(

            "GENERATION",

            f"{generation}/{MAX_GENERATIONS}",

            "#67E8F9"

        ),

        metric_html(

            "BEST FITNESS",

            f"{best_fitness:.2f}",

            "#FBBF24"

        ),

        metric_html(

            sigma_label,

            f"{st.session_state.sigma:.2f}",

            "#E879F9"

        ),

        metric_html(

            "BEST POSITION",

            f"{best_x}",

            position_color

        ),

        metric_html(

            "DISTANCE TO TARGET",

            f"{distance}",

            distance_color

        )

    ]

    progress = min(

        100.0,

        generation / MAX_GENERATIONS * 100

    )

    if st.session_state.mission_success:

        progress_color = (

            "linear-gradient(90deg,#15803D,#4ADE80)"

        )

    elif st.session_state.mission_failed:

        progress_color = (

            "linear-gradient(90deg,#B91C1C,#F87171)"

        )

    else:

        progress_color = (

            "linear-gradient(90deg,#0891B2,#22D3EE)"

        )

    st.markdown(

        '<div class="metric-grid">'

        + "".join(cards)

        + '</div>'

        + '<div class="progress-track">'

        + '<div class="progress-fill" '

        + f'style="width:{progress:.2f}%;'

        + f'background:{progress_color};">'

        + '</div></div>',

        unsafe_allow_html=True

    )


# ============================================================
# 16. MATPLOTLIB THREAD LOCK
# ============================================================

@st.cache_resource
def get_plot_lock():

    return RLock()


# ============================================================
# 17. FITNESS LANDSCAPE GRAPH
# ============================================================

def display_fitness_landscape(accent):

    best_x = get_best_position()

    best_fitness = float(

        fitness(best_x)

    )

    x_values = np.linspace(

        MIN_POSITION,

        MAX_POSITION,

        1001

    )

    y_values = fitness(x_values)

    image_buffer = BytesIO()

    with get_plot_lock():

        fig, ax = plt.subplots(

            figsize=(12, 3.3),

            dpi=130

        )

        try:

            fig.patch.set_facecolor("#0B1120")

            ax.set_facecolor("#0B1120")

            # ------------------------------------------------
            # MOUNTAIN AREA
            # ------------------------------------------------

            ax.fill_between(

                x_values,

                y_values,

                color="#22D3EE",

                alpha=0.12

            )

            # ------------------------------------------------
            # NEON GLOW
            # ------------------------------------------------

            for width, alpha in [

                (12, 0.025),

                (8, 0.04),

                (5, 0.08)

            ]:

                ax.plot(

                    x_values,

                    y_values,

                    color="#22D3EE",

                    linewidth=width,

                    alpha=alpha

                )

            ax.plot(

                x_values,

                y_values,

                color="#22D3EE",

                linewidth=2

            )

            # ------------------------------------------------
            # EXACT TARGET LINE
            # ------------------------------------------------

            ax.axvline(

                TARGET_POSITION,

                color="#FBBF24",

                linestyle="--",

                linewidth=1.2,

                alpha=0.65,

                zorder=2

            )

            # ------------------------------------------------
            # POPULATION MEMBERS
            # ------------------------------------------------

            for x, individual_sigma in (

                st.session_state.population

            ):

                ax.scatter(

                    x,

                    fitness(x),

                    color="#38BDF8",

                    s=35,

                    alpha=0.85,

                    zorder=5

                )

            # ------------------------------------------------
            # BEST INDIVIDUAL
            # ------------------------------------------------

            best_color = (

                "#4ADE80"

                if st.session_state.mission_success

                else accent

            )

            for size, alpha in [

                (450, 0.05),

                (250, 0.10),

                (120, 0.18)

            ]:

                ax.scatter(

                    best_x,

                    best_fitness,

                    color=best_color,

                    s=size,

                    alpha=alpha,

                    zorder=6

                )

            ax.scatter(

                best_x,

                best_fitness,

                color=best_color,

                edgecolors="#FFFFFF",

                linewidths=1.2,

                s=75,

                zorder=7

            )

            # ------------------------------------------------
            # LOCAL OPTIMUM
            # ------------------------------------------------

            ax.annotate(

                "LOCAL OPTIMUM\nPosition 27",

                xy=(

                    LOCAL_OPTIMUM,

                    fitness(LOCAL_OPTIMUM)

                ),

                xytext=(LOCAL_OPTIMUM, 89),

                color="#CBD5E1",

                fontsize=9,

                ha="center",

                arrowprops=dict(

                    color="#94A3B8",

                    arrowstyle="->",

                    linewidth=1

                )

            )

            # ------------------------------------------------
            # GLOBAL OPTIMUM
            # ------------------------------------------------

            ax.scatter(

                GLOBAL_OPTIMUM,

                fitness(GLOBAL_OPTIMUM),

                marker="*",

                color="#FBBF24",

                s=180,

                zorder=8

            )

            ax.annotate(

                "GLOBAL OPTIMUM\nExact Target: 79",

                xy=(

                    GLOBAL_OPTIMUM,

                    fitness(GLOBAL_OPTIMUM)

                ),

                xytext=(GLOBAL_OPTIMUM, 123),

                color="#FBBF24",

                fontsize=9,

                fontweight="bold",

                ha="center",

                arrowprops=dict(

                    color="#FBBF24",

                    arrowstyle="->",

                    linewidth=1

                )

            )

            # ------------------------------------------------
            # BEST POSITION LABEL
            # ------------------------------------------------

            if best_x != TARGET_POSITION:

                ax.annotate(

                    f"x = {best_x}",

                    xy=(best_x, best_fitness),

                    xytext=(0, -19),

                    textcoords="offset points",

                    ha="center",

                    color=best_color,

                    fontsize=9,

                    fontweight="bold"

                )

            # ------------------------------------------------
            # AXIS FORMATTING
            # ------------------------------------------------

            ax.set_xlim(0, 100)

            ax.set_ylim(0, 135)

            ax.set_xticks(

                [0, 10, 20, 30, 40, 50, 60, 70, 79, 90, 100]

            )

            ax.set_xlabel(

                "Search Space — Candidate Position (x)",

                color="#94A3B8",

                fontsize=9,

                labelpad=7

            )

            ax.set_ylabel(

                "Fitness",

                color="#94A3B8",

                fontsize=9,

                labelpad=7

            )

            ax.tick_params(

                colors="#94A3B8",

                labelsize=8

            )

            ax.grid(

                color="#334155",

                linestyle="--",

                linewidth=0.5,

                alpha=0.5

            )

            for spine in ax.spines.values():

                spine.set_color("#26394C")

            # Highlight target tick

            for label in ax.get_xticklabels():

                if label.get_text() == str(TARGET_POSITION):

                    label.set_color("#FBBF24")

                    label.set_fontweight("bold")

            # ------------------------------------------------
            # GRAPH LEGEND
            # ------------------------------------------------

            legend_elements = [

                Line2D(

                    [0],

                    [0],

                    marker="o",

                    linestyle="None",

                    markerfacecolor="#38BDF8",

                    markeredgecolor="#38BDF8",

                    markersize=5,

                    label="Population members"

                ),

                Line2D(

                    [0],

                    [0],

                    marker="o",

                    linestyle="None",

                    markerfacecolor=best_color,

                    markeredgecolor="#FFFFFF",

                    markersize=6,

                    label="Best individual"

                ),

                Line2D(

                    [0],

                    [0],

                    marker="*",

                    linestyle="None",

                    markerfacecolor="#FBBF24",

                    markeredgecolor="#FBBF24",

                    markersize=9,

                    label="Exact global optimum"

                )

            ]

            fig.legend(

                handles=legend_elements,

                loc="lower center",

                bbox_to_anchor=(0.5, 0.025),

                ncol=3,

                frameon=False,

                fontsize=8,

                labelcolor="#94A3B8",

                columnspacing=2.0,

                handletextpad=0.5

            )

            fig.subplots_adjust(

                left=0.065,

                right=0.985,

                top=0.95,

                bottom=0.25

            )

            # ------------------------------------------------
            # SAVE GRAPH TO MEMORY
            # ------------------------------------------------

            fig.savefig(

                image_buffer,

                format="png",

                facecolor=fig.get_facecolor(),

                bbox_inches=None,

                pad_inches=0

            )

        finally:

            plt.close(fig)

    # Display the graph directly as a base64 image.
    # This avoids dependence on temporary media URLs
    # for the main fitness landscape.

    encoded_image = base64.b64encode(

        image_buffer.getvalue()

    ).decode("utf-8")

    image_buffer.close()

    st.markdown(

        f'<img class="fitness-image" '

        f'src="data:image/png;base64,{encoded_image}" '

        f'alt="Fitness landscape showing population '

        f'and exact global optimum at position 79">',

        unsafe_allow_html=True

    )


# ============================================================
# 18. TARGET STATUS
# ============================================================

def display_target_status():

    best_x = get_best_position()

    status, color = get_target_status(best_x)

    if st.session_state.mission_success:

        status = "MISSION COMPLETE"

        color = "#4ADE80"

    elif st.session_state.mission_failed:

        status = "MISSION FAILED"

        color = "#F87171"

    st.markdown(

        '<div class="target-status">'

        '<div class="target-status-label">'

        f'EXACT TARGET: '

        f'<strong style="color:#FBBF24;">'

        f'{TARGET_POSITION}</strong>'

        '</div>'

        '<div class="target-status-label">'

        f'CURRENT BEST: '

        f'<strong style="color:#E2E8F0;">'

        f'{best_x}</strong>'

        '</div>'

        f'<div class="target-status-value" '

        f'style="color:{color};">'

        f'{escape(status)}'

        '</div>'

        '</div>',

        unsafe_allow_html=True

    )


# ============================================================
# 19. LIVE EVOLUTION FEEDBACK
# ============================================================

def display_feedback():

    generation = st.session_state.generation

    best_x = get_best_position()

    distance = get_distance_from_target()

    feedback = st.session_state.feedback

    feedback_class = "feedback-box"

    feedback_title = "LIVE EVOLUTION FEEDBACK"

    # --------------------------------------------------------
    # MISSION COMPLETE
    # --------------------------------------------------------

    if st.session_state.mission_success:

        feedback_class += " feedback-success"

        feedback_title = "🏆 MISSION COMPLETE"

        feedback = (

            f"Exact Global Optimum reached at "

            f"Generation {generation}! "

            f"Position: {best_x}. "

            "Distance from target: 0. "

            "The simulation has stopped successfully."

        )

    # --------------------------------------------------------
    # MISSION FAILED
    # --------------------------------------------------------

    elif st.session_state.mission_failed:

        feedback_class += " feedback-failed"

        feedback_title = "MISSION FAILED"

        reason, _ = get_failure_reason(best_x)

        feedback = (

            f"All {MAX_GENERATIONS} generations used. "

            f"Best position: {best_x}. "

            f"Required position: {TARGET_POSITION}. "

            f"Distance from target: {distance}. "

            f"{reason}. Try again with different settings."

        )

    # --------------------------------------------------------
    # DISPLAY FEEDBACK
    # --------------------------------------------------------

    st.markdown(

        f'<div class="{feedback_class}">'

        '<div class="feedback-title">'

        f'{escape(feedback_title)}'

        '</div>'

        '<div class="feedback-text">'

        f'{escape(feedback)}'

        '</div>'

        '</div>',

        unsafe_allow_html=True

    )


# ============================================================
# 20. POP-UP: MISSION RESULT
# ============================================================

@st.dialog(

    "Mission Result",

    width="large",

    dismissible=False

)
def mission_result_dialog():

    generation = st.session_state.generation

    best_x = get_best_position()

    best_fitness = float(

        fitness(best_x)

    )

    distance = get_distance_from_target()

    strategy = st.session_state.settings[0]

    accent = STRATEGIES[strategy]["color"]

    success = st.session_state.mission_success

    st.session_state.result_shown = True

    # --------------------------------------------------------
    # MISSION COMPLETE
    # --------------------------------------------------------

    if success:

        result_class = "result-success"

        result_icon = "🏆"

        result_title = "MISSION COMPLETE!"

        result_color = "#4ADE80"

        description = (

            "Congratulations! You have reached "

            "the exact Global Optimum at position 79."

        )

        reason_html = (

            '<div class="result-reason">'

            '<div class="result-reason-title" '

            'style="color:#4ADE80;">'

            'TARGET SUCCESSFULLY REACHED'

            '</div>'

            '<div class="result-reason-text">'

            'Your population successfully reached '

            'the exact target position. '

            'The distance from the Global Optimum '

            'is zero. The simulation has stopped.'

            '</div>'

            '</div>'

        )

    # --------------------------------------------------------
    # MISSION FAILED
    # --------------------------------------------------------

    else:

        result_class = "result-failed"

        result_icon = "❌"

        result_title = "MISSION FAILED!"

        result_color = "#F87171"

        description = (

            "You did not reach the exact Global Optimum "

            "within 30 generations."

        )

        reason, advice = get_failure_reason(best_x)

        reason_html = (

            '<div class="result-reason">'

            '<div class="result-reason-title">'

            'WHY DID YOU FAIL?'

            '</div>'

            '<div class="result-reason-text">'

            f'<strong style="color:#F87171;">'

            f'{escape(reason)}'

            '</strong>'

            '<br><br>'

            f'{escape(advice)}'

            '</div>'

            '</div>'

        )

    # --------------------------------------------------------
    # RESULT STATISTICS
    # --------------------------------------------------------

    result_cards = [

        result_metric_html(

            "FINAL POSITION",

            best_x,

            result_color

        ),

        result_metric_html(

            "TARGET POSITION",

            TARGET_POSITION,

            "#FBBF24"

        ),

        result_metric_html(

            "GENERATIONS",

            f"{generation}/{MAX_GENERATIONS}",

            result_color

        ),

        result_metric_html(

            "BEST FITNESS",

            f"{best_fitness:.2f}",

            "#FBBF24"

        ),

        result_metric_html(

            "TARGET FITNESS",

            f"{TARGET_FITNESS:.2f}",

            "#FBBF24"

        ),

        result_metric_html(

            "DISTANCE TO TARGET",

            distance,

            result_color

        )

    ]

    st.markdown(

        f'<div class="result-container {result_class}">'

        f'<div class="result-icon">'

        f'{result_icon}'

        '</div>'

        f'<div class="result-title">'

        f'{escape(result_title)}'

        '</div>'

        '<div class="result-description">'

        f'{escape(description)}'

        '</div>'

        '<div class="result-grid">'

        + "".join(result_cards)

        + '</div>'

        + '<div class="result-strategy-label">'

        + 'PARAMETER CONTROL STRATEGY'

        + '</div>'

        + f'<div class="result-strategy" '

        + f'style="color:{accent};">'

        + f'{escape(strategy)} Control'

        + '</div>'

        + f'<div class="result-distance" '

        + f'style="color:{result_color};">'

        + f'Distance from target: {distance} unit(s)'

        + '</div>'

        + reason_html

        + '</div>',

        unsafe_allow_html=True

    )

    # --------------------------------------------------------
    # RESULT BUTTONS
    # --------------------------------------------------------

    button_label = (

        "↻ PLAY AGAIN"

        if success

        else "↻ TRY AGAIN"

    )

    if st.button(

        button_label,

        type="primary",

        use_container_width=True,

        key="result_play_again"

    ):

        handle_play_again()

        st.rerun()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(

            "📊 View Performance",

            use_container_width=True,

            key="result_performance"

        ):

            st.session_state.active_dialog = "performance"

            st.rerun()

    with col2:

        if st.button(

            "🏠 Main Menu",

            use_container_width=True,

            key="result_home"

        ):

            handle_home()

            st.rerun()

    if st.button(

        "Return to Dashboard",

        use_container_width=True,

        key="result_close"

    ):

        close_dialog()

        st.rerun()


# ============================================================
# 21. POP-UP: PERFORMANCE ANALYSIS
# ============================================================

@st.dialog(

    "Performance Analysis",

    width="large",

    dismissible=False

)
def performance_dialog():

    generation = st.session_state.generation

    best_fitness = st.session_state.history[-1]

    initial_fitness = st.session_state.history[0]

    improvement = best_fitness - initial_fitness

    best_x = get_best_position()

    distance = get_distance_from_target()

    current_strategy = st.session_state.settings[0]

    # --------------------------------------------------------
    # MISSION STATUS
    # --------------------------------------------------------

    if st.session_state.mission_success:

        st.success(

            "MISSION COMPLETE — Exact position 79 reached."

        )

    elif st.session_state.mission_failed:

        st.error(

            "MISSION FAILED — Exact target not reached."

        )

    else:

        st.info(

            "MISSION IN PROGRESS"

        )

    # --------------------------------------------------------
    # PERFORMANCE SUMMARY
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Generation",

        f"{generation}/{MAX_GENERATIONS}"

    )

    c2.metric(

        "Best Fitness",

        f"{best_fitness:.2f}"

    )

    c3.metric(

        "Fitness Improvement",

        f"{improvement:.2f}"

    )

    c4, c5, c6 = st.columns(3)

    c4.metric(

        "Best Position",

        best_x

    )

    c5.metric(

        "Target Position",

        TARGET_POSITION

    )

    c6.metric(

        "Distance to Target",

        distance

    )

    # --------------------------------------------------------
    # HISTORY DATAFRAME
    # --------------------------------------------------------

    history_df = pd.DataFrame({

        "Generation": list(

            range(

                len(st.session_state.history)

            )

        ),

        "Best Fitness": (

            st.session_state.history

        ),

        "Best Position": (

            st.session_state.position_history

        ),

        "Distance to Target": (

            st.session_state.distance_history

        ),

        "Step Size": (

            st.session_state.sigma_history

        ),

        "Mutation Success Rate (%)": [

            rate * 100

            for rate in st.session_state.success_history

        ]

    })

    # --------------------------------------------------------
    # BEST FITNESS HISTORY
    # --------------------------------------------------------

    st.subheader(

        "Best Fitness Progress"

    )

    st.line_chart(

        history_df,

        x="Generation",

        y="Best Fitness",

        color="#22D3EE",

        height=210

    )

    # --------------------------------------------------------
    # POSITION HISTORY
    # --------------------------------------------------------

    st.subheader(

        "Best Position Progress"

    )

    position_df = history_df[

        ["Generation", "Best Position"]

    ].copy()

    position_df["Target Position"] = TARGET_POSITION

    st.line_chart(

        position_df,

        x="Generation",

        y=[

            "Best Position",

            "Target Position"

        ],

        color=[

            "#22D3EE",

            "#FBBF24"

        ],

        height=210

    )

    st.caption(

        "The gold line represents the exact "

        "Global Optimum at position 79."

    )

    # --------------------------------------------------------
    # DISTANCE HISTORY
    # --------------------------------------------------------

    st.subheader(

        "Distance from Global Optimum"

    )

    st.line_chart(

        history_df,

        x="Generation",

        y="Distance to Target",

        color="#4ADE80",

        height=190

    )

    st.caption(

        "A distance of zero means the exact target "

        "has been reached."

    )

    # --------------------------------------------------------
    # STEP SIZE HISTORY
    # --------------------------------------------------------

    st.subheader(

        "Mutation Step Size Progress"

    )

    st.line_chart(

        history_df,

        x="Generation",

        y="Step Size",

        color="#D946EF",

        height=210

    )

    if current_strategy == "Self-Adaptive":

        st.caption(

            "The graph shows the best surviving "

            "individual's mutation step size."

        )

    else:

        st.caption(

            "The graph shows the shared mutation "

            "step size across generations."

        )

    # --------------------------------------------------------
    # ADAPTIVE SUCCESS RATE
    # --------------------------------------------------------

    if current_strategy == "Adaptive":

        st.subheader(

            "Mutation Success Rate"

        )

        if generation > 0:

            success_df = history_df.iloc[1:].copy()

            success_df["Success Threshold (%)"] = 20

            st.line_chart(

                success_df,

                x="Generation",

                y=[

                    "Mutation Success Rate (%)",

                    "Success Threshold (%)"

                ],

                color=[

                    "#FBBF24",

                    "#94A3B8"

                ],

                height=190

            )

        else:

            st.caption(

                "Start the simulation to collect "

                "mutation success data."

            )

        st.caption(

            "The 1/5 Success Rule uses "

            "a 20% mutation success threshold."

        )

    # --------------------------------------------------------
    # GENERATION HISTORY
    # --------------------------------------------------------

    with st.expander(

        "View Generation History"

    ):

        st.dataframe(

            history_df.round(2),

            use_container_width=True,

            hide_index=True

        )

    # --------------------------------------------------------
    # DIALOG BUTTONS
    # --------------------------------------------------------

    if st.session_state.game_finished:

        if st.button(

            "View Mission Result",

            type="primary",

            use_container_width=True,

            key="performance_result"

        ):

            st.session_state.active_dialog = "result"

            st.rerun()

    if st.button(

        "Close",

        key="close_performance",

        use_container_width=True

    ):

        close_dialog()

        st.rerun()


# ============================================================
# 22. POP-UP: POPULATION DETAILS
# ============================================================

@st.dialog(

    "Population Details",

    width="large",

    dismissible=False

)
def population_dialog():

    current_strategy = st.session_state.settings[0]

    st.caption(

        f"Generation {st.session_state.generation} "

        f"— {current_strategy} Control"

    )

    population_data = []

    for i, (x, individual_sigma) in enumerate(

        st.session_state.population

    ):

        x = int(x)

        if current_strategy == "Self-Adaptive":

            step_size = individual_sigma

        else:

            step_size = st.session_state.sigma

        if x == TARGET_POSITION:

            status = "Exact Global Optimum"

        elif i == 0:

            status = "Best Individual"

        else:

            status = "Surviving Individual"

        population_data.append({

            "Individual": i + 1,

            "Position": x,

            "Fitness": round(

                float(fitness(x)),

                2

            ),

            "Step Size": round(

                float(step_size),

                2

            ),

            "Distance to Target": abs(

                TARGET_POSITION - x

            ),

            "Status": status

        })

    population_df = pd.DataFrame(

        population_data

    )

    st.subheader(

        "Current Population"

    )

    st.dataframe(

        population_df,

        use_container_width=True,

        hide_index=True

    )

    st.caption(

        "The population contains the five "

        "fittest surviving individuals."

    )

    # --------------------------------------------------------
    # LATEST MUTATION DETAILS
    # --------------------------------------------------------

    if st.session_state.last_mutations:

        st.subheader(

            "Latest Mutation Results"

        )

        mutation_df = pd.DataFrame(

            st.session_state.last_mutations

        )

        st.dataframe(

            mutation_df,

            use_container_width=True,

            hide_index=True

        )

        successful_mutations = sum(

            row["Mutation Result"] == "Improved"

            for row in st.session_state.last_mutations

        )

        st.caption(

            f"Successful mutations: "

            f"{successful_mutations}/{POPULATION_SIZE}."

        )

    # --------------------------------------------------------
    # STRATEGY EXPLANATION
    # --------------------------------------------------------

    if current_strategy == "Self-Adaptive":

        st.info(

            "Each individual carries its own "

            "mutation step size. The parameter "

            "evolves together with the candidate solution."

        )

    else:

        st.info(

            "All individuals share the same mutation "

            "step size for the next generation."

        )

    if st.button(

        "Close",

        key="close_population",

        use_container_width=True

    ):

        close_dialog()

        st.rerun()


# ============================================================
# 23. POP-UP: LEARNING GUIDE
# ============================================================

@st.dialog(

    "Learning Guide",

    width="large",

    dismissible=False

)
def learning_dialog():

    tab1, tab2, tab3, tab4 = st.tabs([

        "Deterministic",

        "Adaptive",

        "Self-Adaptive",

        "Challenge"

    ])

    # --------------------------------------------------------
    # DETERMINISTIC CONTROL
    # --------------------------------------------------------

    with tab1:

        st.subheader(

            "Deterministic Control"

        )

        st.write(

            "The mutation step size changes according "

            "to a predefined generation schedule."

        )

        st.markdown(

            """
            - Does not use feedback from the search.
            - Large step sizes encourage exploration.
            - Small step sizes encourage refinement.
            """

        )

        st.latex(

            r"\sigma_t = "

            r"\max(0.5,\sigma_0(1-t/T))"

        )

        st.info(

            "The mutation step size gradually decreases "

            "as the generation increases."

        )

        st.markdown(

            """
            **Example**

            Initial step size = 15

            Generation 0 → 15.00

            Generation 1 → 14.50

            Generation 2 → 14.00
            """

        )

    # --------------------------------------------------------
    # ADAPTIVE CONTROL
    # --------------------------------------------------------

    with tab2:

        st.subheader(

            "Adaptive Control"

        )

        st.write(

            "The mutation step size changes based "

            "on feedback from the search process."

        )

        st.markdown(

            "**1/5 Success Rule**"

        )

        st.table([

            {

                "Success Rate": "Above 20%",

                "Action": "Increase step size by 25%"

            },

            {

                "Success Rate": "Equal to 20%",

                "Action": "Maintain step size"

            },

            {

                "Success Rate": "Below 20%",

                "Action": "Decrease step size by 20%"

            }

        ])

        st.info(

            "The algorithm adjusts its mutation "

            "step size based on the number of "

            "successful mutations."

        )

        st.markdown(

            """
            **Example**

            Initial step size = 15

            Successful mutations = 3 out of 5

            Success rate = 60%

            New step size = 18.75
            """

        )

    # --------------------------------------------------------
    # SELF-ADAPTIVE CONTROL
    # --------------------------------------------------------

    with tab3:

        st.subheader(

            "Self-Adaptive Control"

        )

        st.write(

            "Each individual carries its own "

            "mutation step size."

        )

        st.write(

            "The parameter evolves together with "

            "the candidate solution through mutation "

            "and survival selection."

        )

        st.latex(

            r"\sigma' = \sigma e^{0.4N(0,1)}"

        )

        st.info(

            "Different individuals may have "

            "different mutation step sizes."

        )

        st.table([

            {

                "Individual": "P1",

                "Example Step Size": 12.5

            },

            {

                "Individual": "P2",

                "Example Step Size": 18.7

            },

            {

                "Individual": "P3",

                "Example Step Size": 8.3

            },

            {

                "Individual": "P4",

                "Example Step Size": 22.1

            },

            {

                "Individual": "P5",

                "Example Step Size": 14.6

            }

        ])

        st.caption(

            "These values are illustrative examples."

        )

    # --------------------------------------------------------
    # GAME CHALLENGE
    # --------------------------------------------------------

    with tab4:

        st.subheader(

            "Your Mission"

        )

        st.write(

            f"Reach exactly position {TARGET_POSITION} "

            f"within {MAX_GENERATIONS} generations."

        )

        st.markdown(

            """
            **How to Play**

            1. Choose a parameter control strategy.
            2. Set the initial mutation step size.
            3. Press Next Generation or Run All.
            """

        )

        st.success(

            "MISSION COMPLETE: At least one surviving "

            "individual reaches exactly position 79 "

            "within 30 generations."

        )

        st.error(

            "MISSION FAILED: No individual reaches "

            "exactly position 79 after 30 generations."

        )

        st.table([

            {

                "Final Position": 27,

                "Result": "Failed — Local Optimum"

            },

            {

                "Final Position": 78,

                "Result": "Failed — Undershot"

            },

            {

                "Final Position": 79,

                "Result": "Mission Complete"

            },

            {

                "Final Position": 80,

                "Result": "Failed — Overshot"

            }

        ])

        st.markdown(

            """
            **Discussion**

            - Which strategy reached the exact peak?
            - How did the mutation step size change?
            - Did the population get trapped at the
              Local Optimum?
            - Which strategy reached the target
              in fewer generations?
            - How did the initial step size
              affect the final result?
            """

        )

        st.caption(

            "Positions are restricted to integers from "

            "0 to 100. Mutation step sizes remain "

            "continuous. Results may differ between "

            "attempts because mutation is random."

        )

    if st.button(

        "Close",

        key="close_learning",

        use_container_width=True

    ):

        close_dialog()

        st.rerun()


# ============================================================
# 24. MAIN DASHBOARD
# ============================================================

def display_dashboard():

    display_header()

    finished = st.session_state.game_finished

    # --------------------------------------------------------
    # MAIN LAYOUT
    # --------------------------------------------------------

    with st.container(

        key="main_dashboard"

    ):

        left, right = st.columns(

            [1, 3],

            gap="medium"

        )

        # ====================================================
        # LEFT CONTROL PANEL
        # ====================================================

        with left:

            with st.container(

                border=True,

                key="left_panel"

            ):

                section_heading(

                    "01 / CONTROL PANEL"

                )

                # --------------------------------------------
                # STRATEGY SELECTION
                # --------------------------------------------

                strategy = st.radio(

                    "Parameter Control Strategy",

                    options=list(

                        STRATEGIES.keys()

                    ),

                    format_func=lambda name: (

                        f'{STRATEGIES[name]["icon"]} {name}'

                    ),

                    key="selected_strategy",

                    disabled=finished,

                    on_change=handle_settings_change

                )

                accent = STRATEGIES[strategy]["color"]

                description = STRATEGIES[strategy][

                    "description"

                ]

                # --------------------------------------------
                # STRATEGY DESCRIPTION
                # --------------------------------------------

                st.markdown(

                    '<div class="strategy-description" '

                    f'style="border-left:3px solid {accent};">'

                    '<div class="strategy-description-title" '

                    f'style="color:{accent};">'

                    f'{escape(strategy)} Control'

                    '</div>'

                    '<div class="strategy-description-text">'

                    f'{escape(description)}'

                    '</div>'

                    '</div>',

                    unsafe_allow_html=True

                )

                # --------------------------------------------
                # INITIAL MUTATION STEP SIZE
                # --------------------------------------------

                st.slider(

                    "Initial Mutation Step Size (σ)",

                    min_value=1,

                    max_value=30,

                    step=1,

                    key="initial_sigma",

                    disabled=finished,

                    on_change=handle_settings_change

                )

                st.markdown(

                    '<div class="slider-help">'

                    'Large σ: exploration &nbsp;|&nbsp; '

                    'Small σ: refinement'

                    '</div>',

                    unsafe_allow_html=True

                )

                # --------------------------------------------
                # GAME CONTROLS
                # --------------------------------------------

                section_heading(

                    "02 / GAME CONTROLS"

                )

                st.button(

                    "▶ Next Generation",

                    type="primary",

                    disabled=finished,

                    use_container_width=True,

                    key="next_generation_button",

                    on_click=handle_next_generation

                )

                run_col, reset_col = st.columns(

                    2,

                    gap="small"

                )

                with run_col:

                    st.button(

                        "⏩ Run All",

                        disabled=finished,

                        use_container_width=True,

                        key="run_all_button",

                        on_click=handle_run_all

                    )

                with reset_col:

                    st.button(

                        "↻ Reset",

                        use_container_width=True,

                        key="reset_button",

                        on_click=handle_reset

                    )

                # --------------------------------------------
                # MISSION DESCRIPTION
                # --------------------------------------------

                st.markdown(

                    '<div class="mission-card">'

                    '<div class="mission-title">'

                    '03 / YOUR MISSION'

                    '</div>'

                    '<div class="mission-text">'

                    'Reach exactly '

                    '<span class="mission-target">'

                    'position 79'

                    '</span>'

                    ' within 30 generations. '

                    'A final position below or above '

                    '79 means mission failed.'

                    '</div>'

                    '</div>',

                    unsafe_allow_html=True

                )

                # --------------------------------------------
                # SHOW RESULT BUTTON
                # --------------------------------------------

                if finished:

                    st.button(

                        "🏁 View Mission Result",

                        type="primary",

                        use_container_width=True,

                        key="show_result_button",

                        on_click=open_dialog,

                        args=("result",)

                    )

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        with right:

            with st.container(

                key="right_panel"

            ):

                # --------------------------------------------
                # STATISTIC CARDS
                # --------------------------------------------

                display_metrics(

                    strategy

                )

                # --------------------------------------------
                # FITNESS LANDSCAPE
                # --------------------------------------------

                section_heading(

                    "04 / FITNESS LANDSCAPE"

                )

                display_fitness_landscape(

                    accent

                )

                # --------------------------------------------
                # TARGET STATUS
                # --------------------------------------------

                display_target_status()

                # --------------------------------------------
                # LIVE FEEDBACK
                # --------------------------------------------

                display_feedback()

    # ========================================================
    # BOTTOM NAVIGATION
    # ========================================================

    with st.container(

        key="bottom_navigation"

    ):

        p1, p2, p3, p4 = st.columns(

            [1, 1, 1, 0.7],

            gap="small"

        )

        with p1:

            st.button(

                "📊 Performance Analysis",

                use_container_width=True,

                key="performance_button",

                on_click=open_dialog,

                args=("performance",)

            )

        with p2:

            st.button(

                "🧬 Population Details",

                use_container_width=True,

                key="population_button",

                on_click=open_dialog,

                args=("population",)

            )

        with p3:

            st.button(

                "📖 Learning Guide",

                use_container_width=True,

                key="learning_button",

                on_click=open_dialog,

                args=("learning",)

            )

        with p4:

            st.button(

                "🏠 Main Menu",

                use_container_width=True,

                key="home_button",

                on_click=handle_home

            )


# ============================================================
# 25. APPLICATION ROUTING
# ============================================================

# Display the Welcome Screen before the game starts.

if not st.session_state.game_started:

    display_welcome_screen()

    st.stop()


# Display the game after Start Game is pressed.

display_dashboard()


# ============================================================
# 26. DIALOG ROUTING
# ============================================================

# Only one dialog can be opened during a script run.

active_dialog = st.session_state.active_dialog

if active_dialog == "result":

    if st.session_state.game_finished:

        mission_result_dialog()

    else:

        st.session_state.active_dialog = None

elif active_dialog == "performance":

    performance_dialog()

elif active_dialog == "population":

    population_dialog()

elif active_dialog == "learning":

    learning_dialog()


# ============================================================
# END OF APPLICATION
# ============================================================

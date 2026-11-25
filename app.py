
import streamlit as st
import numpy as np
import pandas as pd
import base64

from pathlib import Path
from html import escape


# ============================================================
# 01. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Fitness Mountain V6",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 02. GAME CONSTANTS
# ============================================================

GAME_VERSION = "FITNESS_MOUNTAIN_V6"

MAX_GENERATIONS = 30
POPULATION_SIZE = 5

INITIAL_POSITION = 10
LOCAL_OPTIMUM = 27
GLOBAL_OPTIMUM = 79

MIN_POSITION = 0
MAX_POSITION = 100

MIN_SIGMA = 0.5
MAX_SIGMA = 50.0

RANDOM_SEED = 44

POWERS = {
    "Deterministic": {
        "name": "TIME",
        "icon": "⏳",
        "color": "#22D3EE",
        "description": (
            "Your jump power becomes smaller "
            "as time passes."
        ),
        "default": 15
    },

    "Adaptive": {
        "name": "SMART",
        "icon": "⚡",
        "color": "#FBBF24",
        "description": (
            "Your jump power changes according "
            "to your team's performance."
        ),
        "default": 15
    },

    "Self-Adaptive": {
        "name": "EVOLVE",
        "icon": "🧬",
        "color": "#E879F9",
        "description": (
            "Every climber evolves their "
            "own jumping power."
        ),
        "default": 15
    },

    "Manual": {
        "name": "FREE PLAY",
        "icon": "🎮",
        "color": "#4ADE80",
        "description": (
            "Control your jump power and "
            "preview your next move."
        ),
        "default": 20
    }
}


# ============================================================
# 03. BACKGROUND
# ============================================================

@st.cache_data
def load_background():

    path = Path(__file__).parent / "background.jpg"

    if path.exists():

        return base64.b64encode(
            path.read_bytes()
        ).decode("utf-8")

    return ""


BACKGROUND = load_background()


# ============================================================
# 04. CSS — FULL SCREEN GAME INTERFACE
# ============================================================

CSS = """
<style>

:root {

    --cyan: #22D3EE;
    --gold: #FBBF24;
    --green: #4ADE80;
    --red: #F87171;
    --purple: #E879F9;

    --panel: #101827;
    --border: #29384C;
    --muted: #94A3B8;

    --scale: clamp(
        0.78px,
        0.135dvh,
        1.15px
    );
}


/* =========================================================
   FULL SCREEN
   ========================================================= */

html,
body,
#root,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {

    height: 100dvh !important;
    max-height: 100dvh !important;

    overflow: hidden !important;
    overscroll-behavior: none !important;
}

.stApp {

    background-color: #050A16;

    background-image:

        linear-gradient(
            rgba(5,10,22,0.85),
            rgba(5,10,22,0.94)
        ),

        url("data:image/jpeg;base64,__BACKGROUND__");

    background-position: center;
    background-size: cover;
    background-attachment: fixed;

    color: #E2E8F0;
}

[data-testid="stHeader"] {

    background: transparent;
    height: 25px;
}

[data-testid="stToolbar"],
[data-testid="stSidebar"],
#MainMenu,
footer {

    display: none !important;
}

.block-container {

    width: 100% !important;
    max-width: none !important;

    height: 100dvh !important;

    padding: 10px 24px 12px !important;

    margin: 0 auto !important;

    box-sizing: border-box;
    overflow: hidden !important;
}

.block-container >
[data-testid="stVerticalBlock"] {

    height: 100%;

    display: flex;
    flex-direction: column;

    gap: 8px !important;

    min-height: 0;
}

[data-testid="stVerticalBlock"] {

    gap: 6px !important;
}

[data-testid="stHorizontalBlock"] {

    gap: 12px !important;
}

[data-testid="stColumn"] {

    min-width: 0;
    min-height: 0;
}

[data-testid="stElementContainer"] {

    margin: 0 !important;
    padding: 0 !important;
}

.stMarkdown p {

    margin-bottom: 0;
}


/* =========================================================
   HEADER
   ========================================================= */

.hero {

    text-align: center;
    padding: 3px 0;
}

.hero-top {

    color: #22D3EE;

    font-size: calc(10 * var(--scale));
    font-weight: 800;
    letter-spacing: 5px;
}

.hero-title {

    color: #ECFEFF;

    font-size: calc(40 * var(--scale));
    font-weight: 900;

    line-height: 1.1;
    letter-spacing: 6px;

    margin: 5px 0;

    text-shadow:

        0 0 12px #0891B2,
        0 0 35px rgba(34,211,238,0.3);
}

.hero-subtitle {

    color: #94A3B8;

    font-size: calc(11 * var(--scale));

    letter-spacing: 4px;
    font-weight: 700;
}

.mode-badge {

    display: inline-block;

    padding: 4px 14px;

    margin-top: 5px;

    color: #67E8F9;

    background: rgba(34,211,238,0.08);

    border: 1px solid #155E75;
    border-radius: 30px;

    font-size: calc(10 * var(--scale));
    font-weight: 800;
    letter-spacing: 2px;
}


/* =========================================================
   MAIN MENU
   ========================================================= */

.st-key-welcome {

    width: 100%;
    max-width: 1000px;

    margin: auto !important;

    padding: 15px 25px !important;

    background: rgba(5,10,22,0.96);

    border: 1px solid #155E75;
    border-radius: 20px;

    box-shadow:

        0 0 50px rgba(34,211,238,0.12);
}

.mission-heading {

    text-align: center;

    color: #FBBF24;

    font-size: calc(24 * var(--scale));
    font-weight: 900;

    letter-spacing: 2px;
}

.mission-subtitle {

    text-align: center;

    color: #CBD5E1;

    font-size: calc(13 * var(--scale));
    line-height: 1.4;
}

.instructions {

    display: grid;

    grid-template-columns: repeat(3,1fr);

    gap: 10px;

    margin: 8px 0;
}

.instruction-card {

    background: #101827;

    border: 1px solid #29384C;
    border-radius: 12px;

    padding: 12px;

    text-align: center;
}

.instruction-icon {

    font-size: calc(27 * var(--scale));

    margin-bottom: 5px;
}

.instruction-title {

    color: #67E8F9;

    font-size: calc(14 * var(--scale));
    font-weight: 800;

    margin-bottom: 5px;
}

.instruction-text {

    color: #CBD5E1;

    font-size: calc(12 * var(--scale));
    line-height: 1.4;
}

.menu-card {

    background: #101827;

    border: 1px solid #29384C;
    border-radius: 12px;

    padding: 12px;

    min-height: 85px;

    text-align: center;
}

.menu-title {

    font-size: calc(18 * var(--scale));
    font-weight: 900;

    margin-bottom: 6px;
}

.menu-text {

    color: #CBD5E1;

    font-size: calc(12 * var(--scale));
    line-height: 1.4;
}


/* =========================================================
   GAME LAYOUT
   ========================================================= */

.st-key-game_area {

    flex: 1 1 auto;
    min-height: 0;
}

.section-title {

    color: #94A3B8;

    font-size: calc(11 * var(--scale));

    font-weight: 800;
    letter-spacing: 1.5px;

    margin: 2px 0;
}

.game-card {

    background: rgba(16,24,39,0.96);

    border: 1px solid #29384C;
    border-radius: 12px;

    padding: 10px 12px;
}

.card-title {

    color: #67E8F9;

    font-size: calc(13 * var(--scale));
    font-weight: 800;

    margin-bottom: 5px;
}

.card-text {

    color: #CBD5E1;

    font-size: calc(12 * var(--scale));
    line-height: 1.4;
}

.small-text {

    color: #94A3B8;

    font-size: calc(11 * var(--scale));
    line-height: 1.4;
}


/* =========================================================
   GAME STATISTICS
   ========================================================= */

.stats-grid {

    display: grid;

    grid-template-columns: repeat(3,1fr);

    gap: 10px;
}

.stat-card {

    background: rgba(16,24,39,0.96);

    border: 1px solid #29384C;
    border-radius: 12px;

    padding: 10px 12px;

    text-align: center;
}

.stat-label {

    color: #94A3B8;

    font-size: calc(11 * var(--scale));

    font-weight: 800;
    letter-spacing: 1px;
}

.stat-value {

    font-size: calc(33 * var(--scale));
    font-weight: 900;

    line-height: 1.2;

    margin-top: 4px;
}

.stat-description {

    color: #64748B;

    font-size: calc(10 * var(--scale));
}

.progress-track {

    height: 6px;

    background: #1E293B;

    border-radius: 20px;
    overflow: hidden;

    margin-top: 7px;
}

.progress-fill {

    height: 100%;

    background: linear-gradient(
        90deg,
        #0891B2,
        #22D3EE
    );

    border-radius: 20px;
}


/* =========================================================
   MOUNTAIN ARENA
   ========================================================= */

.arena {

    width: 100%;

    background: linear-gradient(
        180deg,
        #071322,
        #080D1C
    );

    border: 1px solid #164E63;
    border-radius: 14px;

    overflow: hidden;
}

.arena svg {

    display: block;

    width: 100%;
    height: 43dvh;

    max-height: 510px;
}

.practice-arena svg {

    height: 36dvh;
}

.welcome-arena svg {

    height: 23dvh;
    max-height: 230px;
}

.arena-top {

    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 8px 12px;

    color: #67E8F9;

    font-size: calc(11 * var(--scale));
    font-weight: 800;

    letter-spacing: 1px;

    border-bottom: 1px solid #164E63;
}

.live-dot {

    display: inline-block;

    width: 8px;
    height: 8px;

    margin-right: 5px;

    background: #4ADE80;

    border-radius: 50%;

    box-shadow: 0 0 10px #4ADE80;

    animation: pulse 1.5s infinite;
}

@keyframes pulse {

    0%,100% {
        opacity: 1;
    }

    50% {
        opacity: 0.35;
    }
}

.climber-glow {

    animation: pulse 2s infinite;
}

.jump-trail {

    stroke-dasharray: 8 7;

    animation: trail 1.2s linear infinite;
}

@keyframes trail {

    to {
        stroke-dashoffset: -30;
    }
}


/* =========================================================
   POWER CONTROLLER
   ========================================================= */

.power-card {

    background: #101827;

    border: 1px solid var(--power-color);
    border-radius: 12px;

    padding: 12px;

    text-align: center;

    box-shadow:
        0 0 18px rgba(34,211,238,0.06);
}

.power-icon {

    font-size: calc(32 * var(--scale));
    line-height: 1.2;
}

.power-name {

    color: var(--power-color);

    font-size: calc(23 * var(--scale));
    font-weight: 900;

    letter-spacing: 2px;
}

.power-type {

    color: #94A3B8;

    font-size: calc(11 * var(--scale));

    margin-bottom: 5px;
}

.power-description {

    color: #CBD5E1;

    font-size: calc(12 * var(--scale));
    line-height: 1.4;
}

.power-value {

    color: var(--power-color);

    font-size: calc(28 * var(--scale));
    font-weight: 900;

    margin-top: 5px;
}

.power-caption {

    color: #94A3B8;

    font-size: calc(10 * var(--scale));
    font-weight: 700;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton {

    padding: 0 !important;
    margin: 0 !important;
}

.stButton > button {

    width: 100%;

    min-height: calc(37 * var(--scale)) !important;

    padding: 5px 10px !important;

    background: #101827;

    color: #67E8F9;

    border: 1px solid #29384C;
    border-radius: 9px;

    font-weight: 800;
}

.stButton > button p {

    font-size: calc(12 * var(--scale));

    line-height: 1.2;

    margin: 0;
}

.stButton > button:hover {

    background: #164E63;

    color: #FFFFFF;

    border-color: #22D3EE;

    box-shadow:
        0 0 15px rgba(34,211,238,0.15);
}

.stButton > button[kind="primary"] {

    background: linear-gradient(
        135deg,
        #0E7490,
        #155E75
    );

    color: #FFFFFF;

    border-color: #22D3EE;
}

.stButton > button:disabled {

    opacity: 0.4;
}

.st-key-jump_button button {

    min-height: calc(50 * var(--scale)) !important;

    background: linear-gradient(
        135deg,
        #0891B2,
        #155E75
    ) !important;

    border: 1px solid #67E8F9 !important;

    box-shadow:
        0 0 18px rgba(34,211,238,0.22);
}

.st-key-jump_button button p {

    font-size: calc(17 * var(--scale));

    letter-spacing: 2px;
}

[data-testid="stWidgetLabel"] p {

    font-size: calc(12 * var(--scale));

    color: #E2E8F0;
}

[data-testid="stSlider"] {

    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stRadio"] {

    padding: 4px 8px;

    background: #101827;

    border: 1px solid #29384C;
    border-radius: 9px;
}

[data-testid="stRadio"] p {

    font-size: calc(12 * var(--scale));
}


/* =========================================================
   LIVE GAME HINT
   ========================================================= */

.hint-box {

    display: flex;

    align-items: center;

    gap: 12px;

    background: #101827;

    border: 1px solid #29384C;
    border-left: 4px solid var(--hint-color);

    border-radius: 10px;

    padding: 10px 12px;
}

.hint-icon {

    font-size: calc(25 * var(--scale));
    flex-shrink: 0;
}

.hint-title {

    color: var(--hint-color);

    font-size: calc(13 * var(--scale));

    font-weight: 900;

    margin-bottom: 3px;
}

.hint-text {

    color: #E2E8F0;

    font-size: calc(12 * var(--scale));
    line-height: 1.35;
}


/* =========================================================
   PRACTICE PREVIEW
   ========================================================= */

.preview-grid {

    display: grid;

    grid-template-columns: repeat(5,1fr);

    gap: 6px;
}

.preview-item {

    background: #101827;

    border: 1px solid #29384C;
    border-radius: 8px;

    padding: 6px;

    text-align: center;
}

.preview-name {

    color: #94A3B8;

    font-size: calc(10 * var(--scale));
}

.preview-position {

    font-size: calc(19 * var(--scale));
    font-weight: 900;
}


/* =========================================================
   FOOTER
   ========================================================= */

.st-key-bottom_navigation {

    flex: 0 0 auto;

    margin-top: auto !important;

    padding-top: 7px;

    border-top: 1px solid #29384C;
}


/* =========================================================
   POPUP DIALOGS
   ========================================================= */

[data-testid="stDialog"] {

    overflow: hidden !important;
}

[data-testid="stDialog"] [role="dialog"] {

    width: min(1000px,94vw) !important;

    max-width: 94vw !important;
    max-height: 94dvh !important;

    background: #080D1C !important;

    border: 1px solid #334155;
    border-radius: 18px;

    color: #E2E8F0;

    overflow: hidden !important;
}

[data-testid="stDialog"]
[role="dialog"] > div {

    overflow: hidden !important;
}

[data-testid="stDialog"]
[data-testid="stVerticalBlock"] {

    gap: 7px !important;
}

[data-testid="stDialog"] h2 {

    font-size: calc(22 * var(--scale));

    margin: 0;
}


/* =========================================================
   MISSION RESULT
   ========================================================= */

.result-box {

    background: #080D1C;

    border: 2px solid var(--result-color);
    border-radius: 15px;

    padding: 18px;

    text-align: center;
}

.result-icon {

    font-size: clamp(40px,10dvh,85px);

    line-height: 1.1;
}

.result-title {

    color: var(--result-color);

    font-size: clamp(28px,6dvh,55px);

    font-weight: 900;
    letter-spacing: 3px;

    margin: 8px 0;

    text-shadow:
        0 0 20px var(--result-color);
}

.result-stars {

    color: #FBBF24;

    font-size: clamp(24px,5dvh,45px);

    letter-spacing: 10px;

    margin: 8px 0;
}

.result-subtitle {

    color: #CBD5E1;

    font-size: calc(15 * var(--scale));

    margin-bottom: 12px;
}

.result-explanation {

    background: #101827;

    border: 1px solid #29384C;
    border-radius: 10px;

    padding: 12px;

    margin-top: 12px;

    text-align: left;
}

.result-explanation-title {

    color: var(--result-color);

    font-size: calc(15 * var(--scale));

    font-weight: 900;

    margin-bottom: 5px;
}


/* =========================================================
   STATIC TABLES
   ========================================================= */

.game-table {

    width: 100%;

    border-collapse: collapse;

    table-layout: fixed;

    background: #101827;

    font-size: calc(11 * var(--scale));

    color: #E2E8F0;
}

.game-table th {

    color: #67E8F9;

    background: #1E293B;

    padding: 7px 4px;

    border: 1px solid #334155;

    text-align: center;

    overflow-wrap: anywhere;
}

.game-table td {

    padding: 7px 4px;

    border: 1px solid #29384C;

    text-align: center;

    overflow-wrap: anywhere;
}

.guide-item {

    background: #101827;

    border: 1px solid #29384C;
    border-radius: 10px;

    padding: 12px;

    margin-bottom: 8px;
}


/* =========================================================
   SHORT LAPTOP SCREENS
   ========================================================= */

@media (max-height: 800px) {

    .block-container {

        padding: 6px 18px 8px !important;
    }

    [data-testid="stVerticalBlock"] {

        gap: 4px !important;
    }

    .hero-title {

        font-size: 32px;
    }

    .arena svg {

        height: 39dvh;
    }

    .practice-arena svg {

        height: 32dvh;
    }

    .welcome-arena svg {

        height: 20dvh;
    }

    .game-card,
    .power-card,
    .hint-box {

        padding: 7px 9px;
    }

    .stat-card {

        padding: 6px 8px;
    }

    .stat-value {

        font-size: 27px;
    }

    .power-icon {

        font-size: 24px;
    }

    .stButton > button {

        min-height: 30px !important;
    }

    .st-key-jump_button button {

        min-height: 40px !important;
    }

    .instruction-card,
    .menu-card {

        padding: 8px;
    }
}

@media (max-height: 650px) {

    :root {

        --scale: 0.78px;
    }

    .hero-title {

        font-size: 24px;
    }

    .hero-top,
    .hero-subtitle {

        font-size: 8px;
    }

    .arena svg {

        height: 33dvh;
    }

    .practice-arena svg {

        height: 26dvh;
    }

    .welcome-arena svg {

        height: 17dvh;
    }

    .power-card {

        padding: 5px 8px;
    }

    .power-icon {

        font-size: 18px;
    }

    .stButton > button {

        min-height: 25px !important;
    }

    .game-table td,
    .game-table th {

        padding: 4px 3px;
    }

    .result-box {

        padding: 10px;
    }
}

@media (max-width: 1100px) {

    .block-container {

        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    .stats-grid {

        gap: 5px;
    }

    .stat-value {

        font-size: 23px;
    }
}

</style>
"""

st.html(
    CSS.replace(
        "__BACKGROUND__",
        BACKGROUND
    )
)


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
# 06. SESSION STATE
# ============================================================

S = st.session_state

DEFAULT_STATE = {

    "version": GAME_VERSION,

    "screen": "menu",

    "game_mode": "Challenge",

    "strategy": "Deterministic",

    "initial_power": 15,

    "manual_power": 20.0,

    "active_dialog": None,

    "history_page": 0,

    "guide_topic": "How to Play",

    "completed_powers": [],

    "best_records": {}
}


if S.get("version") != GAME_VERSION:

    S.clear()


for key, value in DEFAULT_STATE.items():

    if key not in S:

        S[key] = value


# ============================================================
# 07. GAME HELPERS
# ============================================================

def get_strategy():

    if S.game_mode == "Practice":

        return "Manual"

    return S.strategy


def best_individual():

    return max(

        S.population,

        key=lambda item: float(
            fitness(item[0])
        )
    )


def best_position():

    return int(
        best_individual()[0]
    )


def display_position():

    if (
        S.finished
        and S.final_position is not None
    ):

        return int(
            S.final_position
        )

    return best_position()


def current_power():

    if (
        S.finished
        and S.final_sigma is not None
    ):

        return float(
            S.final_sigma
        )

    if S.game_mode == "Practice":

        return float(
            S.manual_power
        )

    return float(
        S.sigma
    )


def remaining_distance():

    return abs(
        GLOBAL_OPTIMUM - display_position()
    )


def moves_left():

    return max(
        0,
        MAX_GENERATIONS - S.generation
    )


def get_stars():

    if not S.won:

        return 0

    if S.generation <= 10:

        return 3

    if S.generation <= 20:

        return 2

    return 1


# ============================================================
# 08. RESET GAME
# ============================================================

def reset_game():

    strategy = get_strategy()

    if strategy == "Manual":

        initial_sigma = float(
            S.manual_power
        )

    else:

        initial_sigma = float(
            S.initial_power
        )

    S.settings = (
        strategy,
        initial_sigma
    )

    S.generation = 0

    S.population = [

        (
            INITIAL_POSITION,
            initial_sigma
        )

        for _ in range(
            POPULATION_SIZE
        )
    ]

    S.sigma = initial_sigma

    S.random_draws = np.random.default_rng(

        RANDOM_SEED

    ).normal(

        size=(
            MAX_GENERATIONS,
            2,
            POPULATION_SIZE
        )
    )

    S.finished = False
    S.won = False

    S.failure_type = None

    S.final_position = None
    S.final_sigma = None

    S.trigger_parent = None
    S.trigger_individual = None

    S.previous_position = INITIAL_POSITION

    S.last_mutations = []

    S.last_success_rate = None

    S.last_sigma_before = initial_sigma
    S.last_sigma_after = initial_sigma

    S.active_dialog = None

    S.history_page = 0

    S.hint_title = "YOUR ADVENTURE BEGINS!"

    S.hint_text = (
        "Escape the small mountain "
        "and reach the golden flag at 79."
    )

    S.hint_color = "#22D3EE"
    S.hint_icon = "🧭"

    S.power_feedback = (
        "Your power is ready."
    )

    S.history = [

        {
            "Turn": 0,

            "Position": INITIAL_POSITION,

            "Score": float(
                fitness(INITIAL_POSITION)
            ),

            "Sigma": initial_sigma,

            "Distance": (
                GLOBAL_OPTIMUM
                - INITIAL_POSITION
            ),

            "Success Rate": None,

            "Action": "Start"
        }
    ]


if "population" not in S:

    reset_game()


# ============================================================
# 09. GAME NAVIGATION
# ============================================================

def open_setup(mode):

    S.game_mode = mode

    S.screen = "setup"

    S.active_dialog = None

    if mode == "Practice":

        S.manual_power = 20.0

    else:

        S.strategy = "Deterministic"

        S.initial_power = 15


def start_game():

    reset_game()

    S.screen = "game"


def go_home():

    S.screen = "menu"

    S.active_dialog = None


def change_power():

    S.initial_power = int(

        POWERS[S.strategy]["default"]
    )


def restart_game():

    reset_game()

    S.screen = "game"


def open_dialog(name):

    S.active_dialog = name

    S.history_page = 0


def close_dialog():

    S.active_dialog = None


# ============================================================
# 10. MUTATION ENGINE
# ============================================================

def generate_mutations():

    if S.finished:

        return []

    if S.generation >= MAX_GENERATIONS:

        return []

    strategy, _ = S.settings

    draws = S.random_draws[
        S.generation
    ]

    mutations = []

    for i, (position, individual_sigma) in enumerate(
        S.population
    ):

        position = int(position)

        # ----------------------------------------------------
        # MANUAL CONTROL
        # ----------------------------------------------------

        if strategy == "Manual":

            child_sigma = float(
                S.manual_power
            )

        # ----------------------------------------------------
        # SELF-ADAPTIVE CONTROL
        # ----------------------------------------------------

        elif strategy == "Self-Adaptive":

            child_sigma = float(

                np.clip(

                    individual_sigma

                    * np.exp(
                        0.4 * draws[0, i]
                    ),

                    MIN_SIGMA,

                    MAX_SIGMA
                )
            )

        # ----------------------------------------------------
        # DETERMINISTIC / ADAPTIVE
        # ----------------------------------------------------

        else:

            child_sigma = float(
                S.sigma
            )

        # Gaussian mutation.
        # Movement may be positive or negative.

        movement = (
            child_sigma * draws[1, i]
        )

        # Round to integer positions.
        # Do not clamp to 79.
        # Overshooting must remain possible.

        child_position = int(

            np.clip(

                np.rint(
                    position + movement
                ),

                MIN_POSITION,

                MAX_POSITION
            )
        )

        parent_score = float(
            fitness(position)
        )

        child_score = float(
            fitness(child_position)
        )

        improved = (
            child_score > parent_score
        )

        if child_position > GLOBAL_OPTIMUM:

            result = "Overshoot"

        elif child_position == GLOBAL_OPTIMUM:

            result = "Exact Hit"

        elif improved:

            result = "Improved"

        else:

            result = "Not Improved"

        mutations.append({

            "individual": i + 1,

            "parent": position,

            "position": child_position,

            "sigma": child_sigma,

            "movement": (
                child_position - position
            ),

            "parent_score": parent_score,

            "child_score": child_score,

            "improved": improved,

            "result": result
        })

    return mutations


# ============================================================
# 11. SAVE PERFORMANCE HISTORY
# ============================================================

def save_history(action, success_rate=None):

    position = display_position()

    S.history.append({

        "Turn": S.generation,

        "Position": position,

        "Score": float(
            fitness(position)
        ),

        "Sigma": current_power(),

        "Distance": abs(
            GLOBAL_OPTIMUM - position
        ),

        "Success Rate": success_rate,

        "Action": action
    })


# ============================================================
# 12. MISSION RESULT ENGINE
# ============================================================

def finish_game(
    won,
    failure_type=None,
    trigger=None
):

    S.finished = True

    S.won = won

    S.failure_type = failure_type

    if trigger is not None:

        S.final_position = int(
            trigger["position"]
        )

        S.final_sigma = float(
            trigger["sigma"]
        )

        S.trigger_parent = int(
            trigger["parent"]
        )

        S.trigger_individual = int(
            trigger["individual"]
        )

    else:

        S.final_position = best_position()

        S.final_sigma = (

            float(S.manual_power)

            if S.game_mode == "Practice"

            else float(S.sigma)
        )

    if won:

        S.hint_title = (
            "PERFECT LANDING!"
        )

        S.hint_text = (
            "You reached the highest peak!"
        )

        S.hint_icon = "🏆"

        S.hint_color = "#4ADE80"

        if S.game_mode == "Challenge":

            strategy = S.settings[0]

            completed = list(
                S.completed_powers
            )

            if strategy not in completed:

                completed.append(
                    strategy
                )

            S.completed_powers = completed

            records = dict(
                S.best_records
            )

            previous = records.get(
                strategy
            )

            if (
                previous is None
                or S.generation < previous
            ):

                records[strategy] = (
                    S.generation
                )

            S.best_records = records

    else:

        S.hint_title = (
            "MISSION FAILED!"
        )

        S.hint_color = "#F87171"

        S.hint_icon = "⚠️"

        if failure_type == "OVERSHOOT":

            S.hint_text = (

                f"Climber {S.trigger_individual} "
                f"landed at {S.final_position}. "
                "The golden flag was at 79."
            )

        else:

            S.hint_text = (
                "You ran out of moves "
                "before reaching the golden flag."
            )

    S.active_dialog = "result"


# ============================================================
# 13. SHORT GAME HINTS
# ============================================================

def update_hint(previous_position):

    position = best_position()

    distance = (
        GLOBAL_OPTIMUM - position
    )

    if position >= 73:

        S.hint_title = "ALMOST THERE!"

        S.hint_text = (

            f"Only {distance} units left. "
            "Smaller jumps can improve precision."
        )

        S.hint_color = "#4ADE80"

        S.hint_icon = "🎯"

    elif position >= 60:

        S.hint_title = "THE FINAL CLIMB!"

        S.hint_text = (
            "You're getting closer. "
            "Watch out for overshooting!"
        )

        S.hint_color = "#FBBF24"

        S.hint_icon = "🚩"

    elif (
        abs(position - LOCAL_OPTIMUM) <= 5
        and position == previous_position
    ):

        S.hint_title = "TRAPPED AT THE SMALL PEAK!"

        S.hint_text = (
            "Your team needs enough jump power "
            "to explore beyond this mountain."
        )

        S.hint_color = "#FBBF24"

        S.hint_icon = "⛰️"

    elif position > previous_position:

        S.hint_title = "GREAT MOVE!"

        S.hint_text = (

            f"Your best climber moved "
            f"from {previous_position} "
            f"to {position}."
        )

        S.hint_color = "#4ADE80"

        S.hint_icon = "⚡"

    else:

        S.hint_title = "KEEP EXPLORING!"

        S.hint_text = (
            "Your team kept its strongest climbers. "
            "Try the next jump."
        )

        S.hint_color = "#22D3EE"

        S.hint_icon = "🧭"


# ============================================================
# 14. MAIN EVOLUTION ENGINE
# ============================================================

def jump():

    if S.finished:

        return

    if S.generation >= MAX_GENERATIONS:

        return

    strategy, initial_sigma = S.settings

    mutations = generate_mutations()

    if not mutations:

        return

    previous_position = best_position()

    old_sigma = current_power()

    S.previous_position = previous_position

    offspring = [

        (
            mutation["position"],
            mutation["sigma"]
        )

        for mutation in mutations
    ]

    successful_mutations = sum(

        mutation["improved"]

        for mutation in mutations
    )

    success_rate = (

        successful_mutations
        / POPULATION_SIZE
    )

    S.last_success_rate = success_rate

    S.last_mutations = mutations

    S.generation += 1

    # --------------------------------------------------------
    # A. FITNESS-BASED SURVIVAL SELECTION
    # --------------------------------------------------------

    combined = (

        list(S.population)
        + offspring
    )

    combined.sort(

        key=lambda item: float(
            fitness(item[0])
        ),

        reverse=True
    )

    new_population = combined[
        :POPULATION_SIZE
    ]

    # --------------------------------------------------------
    # B. PARAMETER CONTROL
    # --------------------------------------------------------

    if strategy == "Manual":

        new_sigma = float(
            S.manual_power
        )

        S.power_feedback = (

            f"Manual power: "
            f"{new_sigma:.1f}"
        )

    elif strategy == "Deterministic":

        # Predefined linear schedule.

        new_sigma = max(

            MIN_SIGMA,

            initial_sigma * (

                1 - (
                    S.generation
                    / MAX_GENERATIONS
                )
            )
        )

        S.power_feedback = (

            f"TIME power: "
            f"{old_sigma:.1f} → {new_sigma:.1f}. "
            "Power decreases with time."
        )

    elif strategy == "Adaptive":

        # 1/5 success rule.

        if success_rate > 0.2:

            new_sigma = min(

                MAX_SIGMA,

                old_sigma * 1.25
            )

            change = "increased"

        elif success_rate < 0.2:

            new_sigma = max(

                MIN_SIGMA,

                old_sigma * 0.8
            )

            change = "decreased"

        else:

            new_sigma = old_sigma

            change = "stayed the same"

        S.power_feedback = (

            f"{successful_mutations}/5 "
            f"climbers improved. "
            f"SMART power {change}."
        )

    else:

        # Self-adaptive sigma belongs
        # to each surviving individual.

        new_sigma = float(
            new_population[0][1]
        )

        S.power_feedback = (
            "EVOLVE power: the strongest "
            "climbers pass on their jump power."
        )

    if strategy != "Self-Adaptive":

        new_population = [

            (
                int(position),
                float(new_sigma)
            )

            for position, _ in new_population
        ]

    S.population = new_population

    S.sigma = new_sigma

    S.last_sigma_before = old_sigma

    S.last_sigma_after = new_sigma

    # --------------------------------------------------------
    # C. STRICT GAME RULES
    # --------------------------------------------------------

    overshoots = [

        mutation

        for mutation in mutations

        if (
            mutation["position"]
            > GLOBAL_OPTIMUM
        )
    ]

    exact_hits = [

        mutation

        for mutation in mutations

        if (
            mutation["position"]
            == GLOBAL_OPTIMUM
        )
    ]

    # Overshoot has priority.
    # Any offspring above 79 fails the mission.

    if overshoots:

        finish_game(

            won=False,

            failure_type="OVERSHOOT",

            trigger=overshoots[0]
        )

    elif exact_hits:

        finish_game(

            won=True,

            trigger=exact_hits[0]
        )

    elif S.generation >= MAX_GENERATIONS:

        finish_game(

            won=False,

            failure_type="UNDERSHOOT"
        )

    else:

        update_hint(
            previous_position
        )

    save_history(

        action="Jump",

        success_rate=success_rate
    )


# ============================================================
# 15. PRACTICE RETRY
# ============================================================

def retry_move():

    if S.finished:

        return

    if S.game_mode != "Practice":

        return

    if S.generation >= MAX_GENERATIONS:

        return

    S.generation += 1

    S.last_mutations = []

    S.last_success_rate = None

    S.previous_position = best_position()

    S.hint_title = "NEW MOVE AVAILABLE!"

    S.hint_text = (
        "You rejected the previous jump. "
        "One move has been used."
    )

    S.hint_icon = "🔄"

    S.hint_color = "#22D3EE"

    if S.generation >= MAX_GENERATIONS:

        finish_game(

            won=False,

            failure_type="UNDERSHOOT"
        )

    save_history(

        action="Retry",

        success_rate=None
    )


# ============================================================
# 16. MANUAL POWER PRESETS
# ============================================================

def set_manual_power(value):

    S.manual_power = float(value)


def set_initial_power(value):

    S.initial_power = int(value)


# ============================================================
# 17. HTML HELPERS
# ============================================================

def section_title(text):

    st.html(

        f'<div class="section-title">'
        f'{escape(text)}'
        f'</div>'
    )


def game_card(
    title,
    text,
    color="#67E8F9"
):

    st.html(f"""

    <div class="game-card">

        <div class="card-title"
             style="color:{color}">

            {escape(title)}

        </div>

        <div class="card-text">

            {escape(text)}

        </div>

    </div>

    """)


def static_table(dataframe):

    st.html(

        dataframe.to_html(

            index=False,

            escape=True,

            border=0,

            classes="game-table"
        )
    )


# ============================================================
# 18. HEADER
# ============================================================

def display_header(show_mode=False):

    mode_html = ""

    if show_mode:

        mode_html = f"""

        <div class="mode-badge">

            {escape(S.game_mode.upper())} MODE

        </div>

        """

    st.html(f"""

    <div class="hero">

        <div class="hero-top">

            EVOLUTIONARY COMPUTATION

        </div>

        <div class="hero-title">

            FITNESS MOUNTAIN

        </div>

        <div class="hero-subtitle">

            CONQUER THE PEAK

        </div>

        {mode_html}

    </div>

    """)


# ============================================================
# 19. SVG MOUNTAIN GAME ARENA
# ============================================================

def create_mountain_svg(
    welcome=False,
    preview=False
):

    width = 1000
    height = 370

    left = 45
    right = 955

    bottom = 325

    def sx(position):

        return (

            left

            + (
                float(position) / 100
            )

            * (right - left)
        )

    def sy(position):

        return (

            bottom

            - float(
                fitness(position)
            ) * 2.55
        )

    points = np.linspace(
        0,
        100,
        501
    )

    mountain_path = " ".join(

        (
            "M" if i == 0 else "L"
        )

        + f" {sx(x):.2f} {sy(x):.2f}"

        for i, x in enumerate(points)
    )

    fill_path = (

        mountain_path

        + f" L {right} {bottom}"

        + f" L {left} {bottom} Z"
    )

    target_x = sx(
        GLOBAL_OPTIMUM
    )

    target_y = sy(
        GLOBAL_OPTIMUM
    )

    local_x = sx(
        LOCAL_OPTIMUM
    )

    local_y = sy(
        LOCAL_OPTIMUM
    )

    # --------------------------------------------------------
    # BACKGROUND GRID
    # --------------------------------------------------------

    grid = ""

    for y in range(55, 326, 45):

        grid += f"""

        <line

            x1="{left}"

            y1="{y}"

            x2="{right}"

            y2="{y}"

            stroke="#1E293B"

            stroke-width="1"

            stroke-dasharray="4 8"

        />

        """

    # --------------------------------------------------------
    # AXIS LABELS
    # --------------------------------------------------------

    labels = ""

    for x in [

        0, 10, 20, 30, 40,
        50, 60, 70, 79, 90, 100
    ]:

        color = (

            "#FBBF24"

            if x == GLOBAL_OPTIMUM

            else "#94A3B8"
        )

        labels += f"""

        <text

            x="{sx(x)}"

            y="347"

            fill="{color}"

            font-size="13"

            font-weight="700"

            text-anchor="middle"

        >

            {x}

        </text>

        """

    # --------------------------------------------------------
    # CLIMBERS
    # --------------------------------------------------------

    climbers = ""

    if not welcome:

        position_counts = {}

        for i, (position, _) in enumerate(
            S.population
        ):

            position_counts[position] = (

                position_counts.get(
                    position,
                    0
                ) + 1
            )

        for position, count in position_counts.items():

            cx = sx(position)

            cy = sy(position)

            climbers += f"""

            <circle

                cx="{cx}"

                cy="{cy}"

                r="6"

                fill="#0891B2"

                stroke="#67E8F9"

                stroke-width="1.5"

            />

            """

            if count > 1:

                climbers += f"""

                <text

                    x="{cx + 12}"

                    y="{cy + 15}"

                    fill="#67E8F9"

                    font-size="11"

                    font-weight="700"

                >

                    ×{count}

                </text>

                """

    # --------------------------------------------------------
    # LAST JUMP TRAIL
    # --------------------------------------------------------

    trails = ""

    if (
        not welcome
        and S.last_mutations
    ):

        if (
            S.finished
            and S.trigger_parent is not None
        ):

            parent = S.trigger_parent

            child = display_position()

            color = (

                "#4ADE80"

                if S.won

                else "#F87171"
            )

        else:

            parent = S.previous_position

            child = best_position()

            color = "#22D3EE"

        if parent != child:

            x1 = sx(parent)

            y1 = sy(parent)

            x2 = sx(child)

            y2 = sy(child)

            middle_x = (
                x1 + x2
            ) / 2

            middle_y = max(

                12,

                min(y1, y2) - 85
            )

            trails = f"""

            <path

                class="jump-trail"

                d="M {x1} {y1}
                   Q {middle_x} {middle_y}
                     {x2} {y2}"

                fill="none"

                stroke="{color}"

                stroke-width="3"

                opacity="0.85"

            />

            <circle

                r="5"

                fill="{color}"

            >

                <animateMotion

                    dur="0.65s"

                    repeatCount="1"

                    fill="freeze"

                    path="M {x1} {y1}
                          Q {middle_x} {middle_y}
                            {x2} {y2}"

                />

            </circle>

            """

    # --------------------------------------------------------
    # PRACTICE MUTATION PREVIEW
    # --------------------------------------------------------

    preview_points = ""

    if (
        preview
        and not welcome
        and not S.finished
    ):

        mutations = generate_mutations()

        for mutation in mutations:

            position = mutation["position"]

            if position > GLOBAL_OPTIMUM:

                color = "#F87171"

            elif position == GLOBAL_OPTIMUM:

                color = "#4ADE80"

            else:

                color = "#FBBF24"

            preview_points += f"""

            <circle

                cx="{sx(position)}"

                cy="{sy(position)}"

                r="10"

                fill="none"

                stroke="{color}"

                stroke-width="2"

                stroke-dasharray="4 3"

            />

            """

    # --------------------------------------------------------
    # MAIN CLIMBER
    # --------------------------------------------------------

    position = (

        INITIAL_POSITION

        if welcome

        else display_position()
    )

    cx = sx(position)

    cy = sy(position)

    if not welcome and S.finished:

        player_color = (

            "#4ADE80"

            if S.won

            else "#F87171"
        )

    else:

        player_color = "#22D3EE"

    player_label = (

        "START"

        if welcome

        else f"BEST CLIMBER · {position}"
    )

    label_x = min(
        880,
        max(120, cx)
    )

    label_y = min(
        315,
        cy + 40
    )

    # Draw a simple vector climber.
    # No external image or asset required.

    player = f"""

    <circle

        class="climber-glow"

        cx="{cx}"

        cy="{cy - 13}"

        r="22"

        fill="{player_color}"

        opacity="0.13"

    />

    <g transform="translate({cx},{cy - 20})">

        <circle

            cx="0"

            cy="-11"

            r="6"

            fill="#F8FAFC"

        />

        <rect

            x="-6"

            y="-4"

            width="12"

            height="15"

            rx="4"

            fill="{player_color}"

        />

        <path

            d="M -4 0 L -13 7
               M 4 0 L 12 -5
               M -3 10 L -10 20
               M 3 10 L 9 20"

            stroke="#F8FAFC"

            stroke-width="4"

            stroke-linecap="round"

            fill="none"

        />

        <rect

            x="-11"

            y="-3"

            width="5"

            height="11"

            rx="2"

            fill="#FBBF24"

        />

    </g>

    <rect

        x="{label_x - 82}"

        y="{label_y - 15}"

        width="164"

        height="23"

        rx="6"

        fill="#0F172A"

        stroke="{player_color}"

        stroke-width="1"

    />

    <text

        x="{label_x}"

        y="{label_y}"

        fill="{player_color}"

        font-size="12"

        font-weight="800"

        text-anchor="middle"

    >

        {escape(player_label)}

    </text>

    """

    # --------------------------------------------------------
    # COMPLETE SVG
    # --------------------------------------------------------

    svg = f"""

    <svg

        xmlns="http://www.w3.org/2000/svg"

        viewBox="0 0 {width} {height}"

        preserveAspectRatio="xMidYMid meet"

    >

        <defs>

            <linearGradient

                id="mountainFill"

                x1="0"

                y1="0"

                x2="0"

                y2="1"

            >

                <stop

                    offset="0%"

                    stop-color="#155E75"

                    stop-opacity="0.85"

                />

                <stop

                    offset="100%"

                    stop-color="#071322"

                    stop-opacity="0.3"

                />

            </linearGradient>

            <linearGradient

                id="dangerFill"

                x1="0"

                y1="0"

                x2="1"

                y2="0"

            >

                <stop

                    offset="0%"

                    stop-color="#EF4444"

                    stop-opacity="0.04"

                />

                <stop

                    offset="100%"

                    stop-color="#EF4444"

                    stop-opacity="0.18"

                />

            </linearGradient>

        </defs>

        {grid}

        <rect

            x="{sx(79.5)}"

            y="20"

            width="{right - sx(79.5)}"

            height="{bottom - 20}"

            fill="url(#dangerFill)"

        />

        <text

            x="{sx(90)}"

            y="35"

            fill="#F87171"

            font-size="13"

            font-weight="800"

            text-anchor="middle"

        >

            DANGER ZONE

        </text>

        <path

            d="{fill_path}"

            fill="url(#mountainFill)"

        />

        <path

            d="{mountain_path}"

            stroke="#22D3EE"

            stroke-width="10"

            opacity="0.07"

            fill="none"

        />

        <path

            d="{mountain_path}"

            stroke="#22D3EE"

            stroke-width="3"

            fill="none"

        />

        <line

            x1="{left}"

            y1="{bottom}"

            x2="{right}"

            y2="{bottom}"

            stroke="#334155"

            stroke-width="1"

        />

        <circle

            cx="{local_x}"

            cy="{local_y}"

            r="6"

            fill="#94A3B8"

        />

        <text

            x="{local_x}"

            y="{local_y - 40}"

            fill="#CBD5E1"

            font-size="15"

            font-weight="800"

            text-anchor="middle"

        >

            SMALL PEAK

        </text>

        <text

            x="{local_x}"

            y="{local_y - 23}"

            fill="#94A3B8"

            font-size="11"

            text-anchor="middle"

        >

            Local Optimum · 27

        </text>

        <line

            x1="{target_x}"

            y1="{target_y}"

            x2="{target_x}"

            y2="{bottom}"

            stroke="#FBBF24"

            stroke-width="1.5"

            stroke-dasharray="5 6"

            opacity="0.65"

        />

        <line

            x1="{target_x}"

            y1="{target_y}"

            x2="{target_x}"

            y2="{target_y - 45}"

            stroke="#FBBF24"

            stroke-width="3"

        />

        <path

            d="M {target_x} {target_y - 45}

               L {target_x + 35} {target_y - 35}

               L {target_x} {target_y - 23} Z"

            fill="#FBBF24"

        />

        <text

            x="{target_x - 12}"

            y="{target_y - 47}"

            fill="#FBBF24"

            font-size="15"

            font-weight="900"

            text-anchor="end"

        >

            HIGHEST PEAK

        </text>

        <text

            x="{target_x - 12}"

            y="{target_y - 30}"

            fill="#FBBF24"

            font-size="11"

            text-anchor="end"

        >

            Global Optimum · 79

        </text>

        {trails}

        {climbers}

        {preview_points}

        {player}

        {labels}

        <text

            x="500"

            y="365"

            fill="#64748B"

            font-size="11"

            font-weight="700"

            text-anchor="middle"

        >

            MOUNTAIN POSITION

        </text>

    </svg>

    """

    return svg


# ============================================================
# 20. DISPLAY MOUNTAIN ARENA
# ============================================================

def display_arena(
    welcome=False,
    preview=False
):

    css_class = "arena"

    if welcome:

        css_class += " welcome-arena"

    elif S.game_mode == "Practice":

        css_class += " practice-arena"

    svg = create_mountain_svg(

        welcome=welcome,

        preview=preview
    )

    header = ""

    if not welcome:

        status = (

            "MISSION ENDED"

            if S.finished

            else "LIVE EXPEDITION"
        )

        header = f"""

        <div class="arena-top">

            <span>

                <span class="live-dot"></span>

                {status}

            </span>

            <span>

                TARGET: 79

            </span>

        </div>

        """

    st.html(f"""

    <div class="{css_class}">

        {header}

        {svg}

    </div>

    """)


# ============================================================
# 21. MAIN MENU
# ============================================================

def display_menu():

    with st.container(
        key="welcome"
    ):

        display_header()

        display_arena(
            welcome=True
        )

        st.html("""

        <div class="mission-heading">

            REACH THE GOLDEN FLAG!

        </div>

        <div class="mission-subtitle">

            Lead your team to the highest peak
            before you run out of moves.

        </div>

        <div class="instructions">

            <div class="instruction-card">

                <div class="instruction-icon">

                    ⚡

                </div>

                <div class="instruction-title">

                    01 · CHOOSE POWER

                </div>

                <div class="instruction-text">

                    Select how your team's
                    jump power will change.

                </div>

            </div>

            <div class="instruction-card">

                <div class="instruction-icon">

                    🧗

                </div>

                <div class="instruction-title">

                    02 · JUMP

                </div>

                <div class="instruction-text">

                    Set your starting power
                    and lead five climbers.

                </div>

            </div>

            <div class="instruction-card">

                <div class="instruction-icon">

                    🚩

                </div>

                <div class="instruction-title">

                    03 · HIT THE PEAK

                </div>

                <div class="instruction-text">

                    Land exactly at 79
                    within 30 moves.
                    Never overshoot!

                </div>

            </div>

        </div>

        """)

        left, right = st.columns(2)

        with left:

            st.html("""

            <div class="menu-card">

                <div class="menu-title"
                     style="color:#4ADE80">

                    🎮 PRACTICE MODE

                </div>

                <div class="menu-text">

                    Control your own jump power
                    and preview your next move.

                </div>

            </div>

            """)

            st.button(

                "START PRACTICE",

                key="menu_practice",

                type="primary",

                use_container_width=True,

                on_click=open_setup,

                args=("Practice",)
            )

        with right:

            st.html(f"""

            <div class="menu-card">

                <div class="menu-title"
                     style="color:#FBBF24">

                    🏆 CHALLENGE MODE

                </div>

                <div class="menu-text">

                    Master all three powers.

                    <br>

                    Completed:
                    {len(S.completed_powers)}/3

                </div>

            </div>

            """)

            st.button(

                "START CHALLENGE",

                key="menu_challenge",

                type="primary",

                use_container_width=True,

                on_click=open_setup,

                args=("Challenge",)
            )


# ============================================================
# 22. POWER CARD
# ============================================================

def display_power_card(
    strategy,
    sigma=None
):

    power = POWERS[strategy]

    value_html = ""

    if sigma is not None:

        value_html = f"""

        <div class="power-value">

            {sigma:.1f}

        </div>

        <div class="power-caption">

            CURRENT JUMP POWER (σ)

        </div>

        """

    st.html(f"""

    <div class="power-card"

         style="
            --power-color:{power['color']};
         ">

        <div class="power-icon">

            {power['icon']}

        </div>

        <div class="power-name">

            {power['name']}

        </div>

        <div class="power-type">

            {escape(strategy)} Control

        </div>

        <div class="power-description">

            {escape(power['description'])}

        </div>

        {value_html}

    </div>

    """)


# ============================================================
# 23. GAME SETUP SCREEN
# ============================================================

def display_setup():

    display_header(
        show_mode=True
    )

    left, right = st.columns(

        [1, 2.6]
    )

    with left:

        section_title(
            "CHOOSE YOUR POWER"
        )

        if S.game_mode == "Challenge":

            st.radio(

                "Power",

                options=[

                    "Deterministic",

                    "Adaptive",

                    "Self-Adaptive"
                ],

                format_func=lambda item: (

                    POWERS[item]["icon"]

                    + " "

                    + POWERS[item]["name"]

                    + " · "

                    + item
                ),

                key="strategy",

                label_visibility="collapsed",

                on_change=change_power
            )

            display_power_card(
                S.strategy
            )

            section_title(
                "STARTING JUMP POWER"
            )

            a, b, c = st.columns(3)

            with a:

                st.button(

                    "Small",

                    key="setup_small",

                    on_click=set_initial_power,

                    args=(5,)
                )

            with b:

                st.button(

                    "Medium",

                    key="setup_medium",

                    on_click=set_initial_power,

                    args=(15,)
                )

            with c:

                st.button(

                    "Large",

                    key="setup_large",

                    on_click=set_initial_power,

                    args=(30,)
                )

            st.slider(

                "Jump Power (σ)",

                min_value=1,

                max_value=30,

                step=1,

                key="initial_power"
            )

        else:

            display_power_card(
                "Manual"
            )

            st.slider(

                "Starting Jump Power (σ)",

                min_value=0.5,

                max_value=30.0,

                step=0.5,

                key="manual_power"
            )

        st.button(

            "▶ BEGIN ADVENTURE",

            key="begin_adventure",

            type="primary",

            use_container_width=True,

            on_click=start_game
        )

        st.button(

            "← MAIN MENU",

            key="setup_back",

            use_container_width=True,

            on_click=go_home
        )

    with right:

        display_arena(
            welcome=True
        )

        game_card(

            "YOUR MISSION",

            "Guide five climbers to position 79 "
            "within 30 moves. Any climber that "
            "lands beyond 79 ends the mission.",

            "#FBBF24"
        )

        if S.game_mode == "Challenge":

            strategy = S.strategy

            record = S.best_records.get(
                strategy
            )

            record_text = (

                f"Best record: {record} moves."

                if record is not None

                else "No winning record yet."
            )

            game_card(

                "POWER RECORD",

                record_text,

                "#4ADE80"
            )

        else:

            game_card(

                "PRACTICE TIP",

                "You can change your jump power "
                "at any time and see the proposed "
                "landing positions before jumping.",

                "#4ADE80"
            )


# ============================================================
# 24. GAME STATISTICS
# ============================================================

def stat_card(
    label,
    value,
    description,
    color
):

    return f"""

    <div class="stat-card">

        <div class="stat-label">

            {escape(str(label))}

        </div>

        <div class="stat-value"
             style="color:{color}">

            {escape(str(value))}

        </div>

        <div class="stat-description">

            {escape(str(description))}

        </div>

    </div>

    """


def display_stats():

    position = display_position()

    score = float(
        fitness(position)
    )

    distance = remaining_distance()

    left = moves_left()

    cards = [

        stat_card(

            "MOVES LEFT",

            left,

            f"Turn {S.generation}/30",

            "#22D3EE"
        ),

        stat_card(

            "FINAL SCORE"
            if S.finished
            else "HIGHEST SCORE",

            f"{score:.2f}",

            "Fitness",

            "#FBBF24"
        ),

        stat_card(

            "DISTANCE TO FLAG",

            distance,

            f"Position {position} / 79",

            "#4ADE80"
            if distance == 0
            else "#E879F9"
        )
    ]

    progress = (

        S.generation
        / MAX_GENERATIONS
        * 100
    )

    st.html(f"""

    <div class="stats-grid">

        {''.join(cards)}

    </div>

    <div class="progress-track">

        <div class="progress-fill"

             style="width:{progress}%">

        </div>

    </div>

    """)


# ============================================================
# 25. LIVE GAME HINT
# ============================================================

def display_hint():

    st.html(f"""

    <div class="hint-box"

         style="
            --hint-color:{S.hint_color};
         ">

        <div class="hint-icon">

            {S.hint_icon}

        </div>

        <div>

            <div class="hint-title">

                {escape(S.hint_title)}

            </div>

            <div class="hint-text">

                {escape(S.hint_text)}

            </div>

        </div>

    </div>

    """)


# ============================================================
# 26. PRACTICE MUTATION PREVIEW
# ============================================================

def display_preview():

    if S.finished:

        return

    mutations = generate_mutations()

    if not mutations:

        return

    cards = ""

    for mutation in mutations:

        position = mutation["position"]

        if position > GLOBAL_OPTIMUM:

            color = "#F87171"

        elif position == GLOBAL_OPTIMUM:

            color = "#4ADE80"

        else:

            color = "#FBBF24"

        cards += f"""

        <div class="preview-item">

            <div class="preview-name">

                CLIMBER {mutation['individual']}

            </div>

            <div class="preview-position"

                 style="color:{color}">

                {position}

            </div>

        </div>

        """

    overshoot = any(

        mutation["position"] > GLOBAL_OPTIMUM

        for mutation in mutations
    )

    exact_hit = any(

        mutation["position"] == GLOBAL_OPTIMUM

        for mutation in mutations
    )

    if overshoot:

        message = (
            "⚠ Danger! Reduce power or try another move."
        )

        color = "#F87171"

    elif exact_hit:

        message = (
            "✓ Perfect landing available! Press JUMP."
        )

        color = "#4ADE80"

    else:

        message = (
            "Adjust your power or take the next jump."
        )

        color = "#FBBF24"

    st.html(f"""

    <div class="section-title">

        NEXT LANDING PREVIEW

    </div>

    <div class="preview-grid">

        {cards}

    </div>

    <div style="

        color:{color};

        font-size:calc(12 * var(--scale));

        font-weight:700;

        padding:4px 0;

    ">

        {escape(message)}

    </div>

    """)


# ============================================================
# 27. PRACTICE CONTROLS
# ============================================================

def display_practice_controls():

    section_title(
        "YOUR POWER"
    )

    display_power_card(

        "Manual",

        current_power()
    )

    section_title(
        "CHOOSE JUMP POWER"
    )

    a, b, c = st.columns(3)

    with a:

        st.button(

            "Small",

            key="practice_small",

            disabled=S.finished,

            on_click=set_manual_power,

            args=(3.0,)
        )

    with b:

        st.button(

            "Medium",

            key="practice_medium",

            disabled=S.finished,

            on_click=set_manual_power,

            args=(15.0,)
        )

    with c:

        st.button(

            "Large",

            key="practice_large",

            disabled=S.finished,

            on_click=set_manual_power,

            args=(30.0,)
        )

    st.slider(

        "Jump Power (σ)",

        min_value=0.5,

        max_value=30.0,

        step=0.5,

        key="manual_power",

        disabled=S.finished
    )

    st.html("""

    <div class="small-text">

        Small power = finer movements.

        <br>

        Large power = wider exploration.

    </div>

    """)

    st.button(

        "⚡ JUMP",

        key="jump_button",

        type="primary",

        disabled=S.finished,

        use_container_width=True,

        on_click=jump
    )

    st.button(

        "🔄 TRY ANOTHER MOVE",

        key="retry_button",

        disabled=S.finished,

        use_container_width=True,

        on_click=retry_move
    )

    st.html("""

    <div class="small-text">

        Changing power is free.

        <br>

        Trying another move costs one turn.

    </div>

    """)

    st.button(

        "↻ RESTART",

        key="practice_restart",

        use_container_width=True,

        on_click=restart_game
    )


# ============================================================
# 28. CHALLENGE CONTROLS
# ============================================================

def display_challenge_controls():

    strategy = S.settings[0]

    section_title(
        "YOUR ACTIVE POWER"
    )

    display_power_card(

        strategy,

        current_power()
    )

    section_title(
        "POWER UPDATE"
    )

    game_card(

        "⚡ LIVE POWER EFFECT",

        S.power_feedback,

        POWERS[strategy]["color"]
    )

    st.button(

        "⚡ JUMP",

        key="jump_button",

        type="primary",

        disabled=S.finished,

        use_container_width=True,

        on_click=jump
    )

    st.button(

        "↻ RESTART",

        key="challenge_restart",

        use_container_width=True,

        on_click=restart_game
    )

    st.button(

        "CHANGE POWER",

        key="change_power_button",

        use_container_width=True,

        on_click=open_setup,

        args=("Challenge",)
    )

    game_card(

        "🚩 MISSION",

        "Land exactly at 79. "
        "Your selected power controls "
        "the jumps automatically.",

        "#FBBF24"
    )

    st.html("""

    <div class="small-text">

        Changing power starts a new mission.

        <br>

        Restart repeats the same challenge.

    </div>

    """)


# ============================================================
# 29. GAME FOOTER
# ============================================================

def display_navigation():

    with st.container(

        key="bottom_navigation"
    ):

        a, b, c, d = st.columns(4)

        with a:

            st.button(

                "📊 Your Progress",

                key="progress_button",

                use_container_width=True,

                on_click=open_dialog,

                args=("progress",)
            )

        with b:

            st.button(

                "🧗 Your Climbers",

                key="climbers_button",

                use_container_width=True,

                on_click=open_dialog,

                args=("climbers",)
            )

        with c:

            st.button(

                "📖 Game Guide",

                key="guide_button",

                use_container_width=True,

                on_click=open_dialog,

                args=("guide",)
            )

        with d:

            st.button(

                "🏠 Main Menu",

                key="home_button",

                use_container_width=True,

                on_click=go_home
            )


# ============================================================
# 30. MAIN GAME SCREEN
# ============================================================

def display_game():

    display_header(
        show_mode=True
    )

    with st.container(
        key="game_area"
    ):

        left, right = st.columns(

            [1, 3.2],

            gap="medium"
        )

        with left:

            if S.game_mode == "Practice":

                display_practice_controls()

            else:

                display_challenge_controls()

        with right:

            display_stats()

            display_arena(

                preview=(

                    S.game_mode == "Practice"
                )
            )

            if (

                S.game_mode == "Practice"

                and not S.finished
            ):

                display_preview()

            display_hint()

            if S.finished:

                st.button(

                    "VIEW MISSION RESULT",

                    key="view_result",

                    use_container_width=True,

                    on_click=open_dialog,

                    args=("result",)
                )

    display_navigation()


# ============================================================
# 31. MISSION RESULT POPUP
# ============================================================

@st.dialog(

    "Expedition Result",

    width="large",

    dismissible=False
)
def result_dialog():

    position = display_position()

    stars = get_stars()

    if S.won:

        title = "MISSION COMPLETE"

        color = "#4ADE80"

        icon = "🏆"

        subtitle = (

            f"You conquered the mountain "
            f"in {S.generation} moves!"
        )

        reason_title = "PERFECT LANDING"

        reason = (

            f"Climber {S.trigger_individual} "
            "reached exactly position 79. "
            "Your team successfully balanced "
            "exploration and precision."
        )

        lesson = (
            "Large jump power helps exploration. "
            "Smaller jump power helps refinement."
        )

    else:

        title = "MISSION FAILED"

        color = "#F87171"

        icon = "💥"

        subtitle = (
            "Your expedition has ended."
        )

        if S.failure_type == "OVERSHOOT":

            reason_title = "YOU OVERSHOT!"

            reason = (

                f"Climber {S.trigger_individual} "
                f"jumped from {S.trigger_parent} "
                f"to {position}. "
                f"The landing exceeded the flag "
                f"by {position - GLOBAL_OPTIMUM} units."
            )

            lesson = (
                "Try a smaller starting power "
                "or another power controller."
            )

        elif abs(
            position - LOCAL_OPTIMUM
        ) <= 5:

            reason_title = (
                "TRAPPED AT THE SMALL PEAK"
            )

            reason = (
                "Your team stayed near the smaller "
                "mountain and could not escape "
                "before time ran out."
            )

            lesson = (
                "Try stronger exploration or "
                "a different power controller."
            )

        else:

            reason_title = (
                "OUT OF MOVES"
            )

            reason = (

                f"You reached position {position}, "
                f"but the golden flag was still "
                f"{remaining_distance()} units away."
            )

            lesson = (
                "Try another starting power "
                "to improve your progress."
            )

    stars_html = (

        "★" * stars

        + "☆" * (3 - stars)
    )

    cards = [

        stat_card(

            "MOVES USED",

            S.generation,

            "Maximum 30",

            "#22D3EE"
        ),

        stat_card(

            "FINAL POSITION",

            position,

            "Target 79",

            color
        ),

        stat_card(

            "FINAL SCORE",

            f"{fitness(position):.2f}",

            "Fitness",

            "#FBBF24"
        )
    ]

    st.html(f"""

    <div class="result-box"

         style="--result-color:{color}">

        <div class="result-icon">

            {icon}

        </div>

        <div class="result-title">

            {title}

        </div>

        <div class="result-stars">

            {stars_html}

        </div>

        <div class="result-subtitle">

            {escape(subtitle)}

        </div>

        <div class="stats-grid">

            {''.join(cards)}

        </div>

        <div class="result-explanation">

            <div class="result-explanation-title">

                {escape(reason_title)}

            </div>

            <div class="card-text">

                {escape(reason)}

            </div>

            <div class="card-title"

                 style="

                    color:#FBBF24;

                    margin-top:10px;

                 ">

                NEXT STRATEGY

            </div>

            <div class="card-text">

                {escape(lesson)}

            </div>

        </div>

    </div>

    """)

    a, b, c = st.columns(3)

    with a:

        if st.button(

            "↻ PLAY AGAIN",

            key="result_retry",

            type="primary",

            use_container_width=True
        ):

            restart_game()

            st.rerun()

    with b:

        if st.button(

            "CHANGE POWER",

            key="result_change",

            use_container_width=True
        ):

            open_setup(
                S.game_mode
            )

            st.rerun()

    with c:

        if st.button(

            "VIEW GAME",

            key="result_close",

            use_container_width=True
        ):

            close_dialog()

            st.rerun()


# ============================================================
# 32. PERFORMANCE CHART
# ============================================================

def create_progress_chart(
    values,
    title,
    color,
    max_value=None
):

    width = 300
    height = 150

    left = 30
    right = 280

    top = 25
    bottom = 120

    values = [

        float(value)

        for value in values
    ]

    if not values:

        values = [0.0]

    maximum = (

        max_value

        if max_value is not None

        else max(1.0, max(values))
    )

    maximum = max(
        maximum,
        max(values),
        1.0
    )

    points = []

    for i, value in enumerate(values):

        x = (

            left

            + (
                i / max(1, len(values) - 1)
            )

            * (right - left)
        )

        y = (

            bottom

            - (
                value / maximum
            )

            * (bottom - top)
        )

        points.append(
            (x, y)
        )

    path = " ".join(

        (
            "M" if i == 0 else "L"
        )

        + f" {x:.2f} {y:.2f}"

        for i, (x, y) in enumerate(points)
    )

    dots = "".join(

        f'<circle cx="{x}" cy="{y}" '
        f'r="2.8" fill="{color}"/>'

        for x, y in points
    )

    return f"""

    <svg

        viewBox="0 0 {width} {height}"

        xmlns="http://www.w3.org/2000/svg"

        style="

            width:100%;

            height:22dvh;

            background:#101827;

            border:1px solid #29384C;

            border-radius:9px;

        "

    >

        <text

            x="150"

            y="16"

            fill="{color}"

            font-size="12"

            font-weight="800"

            text-anchor="middle"

        >

            {escape(title)}

        </text>

        <line

            x1="{left}"

            y1="{top}"

            x2="{left}"

            y2="{bottom}"

            stroke="#334155"

        />

        <line

            x1="{left}"

            y1="{bottom}"

            x2="{right}"

            y2="{bottom}"

            stroke="#334155"

        />

        <text

            x="25"

            y="{top + 4}"

            fill="#94A3B8"

            font-size="9"

            text-anchor="end"

        >

            {maximum:.0f}

        </text>

        <text

            x="25"

            y="{bottom + 4}"

            fill="#94A3B8"

            font-size="9"

            text-anchor="end"

        >

            0

        </text>

        <path

            d="{path}"

            stroke="{color}"

            stroke-width="2.5"

            fill="none"

        />

        {dots}

        <text

            x="150"

            y="140"

            fill="#94A3B8"

            font-size="10"

            text-anchor="middle"

        >

            Turn 0 → {len(values) - 1}

        </text>

    </svg>

    """


# ============================================================
# 33. PERFORMANCE ANALYSIS POPUP
# ============================================================

@st.dialog(

    "Your Progress — Performance Analysis",

    width="large",

    dismissible=False
)
def progress_dialog():

    dataframe = pd.DataFrame(
        S.history
    )

    a, b, c = st.columns(3)

    with a:

        st.html(

            create_progress_chart(

                dataframe["Score"],

                "FITNESS SCORE",

                "#22D3EE",

                max_value=100
            )
        )

    with b:

        st.html(

            create_progress_chart(

                dataframe["Sigma"],

                "JUMP POWER (σ)",

                "#E879F9"
            )
        )

    with c:

        st.html(

            create_progress_chart(

                dataframe["Distance"],

                "DISTANCE TO TARGET",

                "#FBBF24"
            )
        )

    section_title(
        "MOVE HISTORY"
    )

    page_size = 4

    total_pages = max(

        1,

        int(

            np.ceil(

                len(dataframe)
                / page_size
            )
        )
    )

    S.history_page = max(

        0,

        min(

            S.history_page,

            total_pages - 1
        )
    )

    start = (

        S.history_page
        * page_size
    )

    page = dataframe.iloc[

        start:start + page_size

    ].copy()

    page["Score"] = page[
        "Score"
    ].map(

        lambda value: f"{value:.2f}"
    )

    page["Sigma"] = page[
        "Sigma"
    ].map(

        lambda value: f"{value:.2f}"
    )

    page["Success Rate"] = page[
        "Success Rate"
    ].map(

        lambda value: (

            "—"

            if pd.isna(value)

            else f"{value:.0%}"
        )
    )

    static_table(page)

    left, middle, right = st.columns(

        [1, 2, 1]
    )

    with left:

        if st.button(

            "◀ Previous",

            key="progress_previous",

            disabled=S.history_page == 0
        ):

            S.history_page -= 1

            st.rerun(
                scope="fragment"
            )

    with middle:

        st.html(f"""

        <div class="small-text"

             style="

                text-align:center;

                padding:8px;

             ">

            Page {S.history_page + 1}
            of {total_pages}

        </div>

        """)

    with right:

        if st.button(

            "Next ▶",

            key="progress_next",

            disabled=(

                S.history_page
                >= total_pages - 1
            )
        ):

            S.history_page += 1

            st.rerun(
                scope="fragment"
            )

    if st.button(

        "CLOSE",

        key="close_progress",

        use_container_width=True
    ):

        close_dialog()

        st.rerun()


# ============================================================
# 34. POPULATION DETAILS POPUP
# ============================================================

@st.dialog(

    "Your Climbers — Population Details",

    width="large",

    dismissible=False
)
def climbers_dialog():

    section_title(
        "FIVE SURVIVING CLIMBERS"
    )

    population_data = []

    for i, (position, sigma) in enumerate(
        S.population
    ):

        population_data.append({

            "Climber": i + 1,

            "Position": position,

            "Fitness": (

                f"{fitness(position):.2f}"
            ),

            "Stored Sigma": (

                f"{sigma:.2f}"
            ),

            "Distance": abs(

                GLOBAL_OPTIMUM
                - position
            )
        })

    static_table(

        pd.DataFrame(
            population_data
        )
    )

    if (

        S.game_mode == "Practice"

        and not S.finished
    ):

        section_title(
            "NEXT PROPOSED JUMPS"
        )

        mutations = generate_mutations()

    else:

        section_title(
            "LAST FIVE MUTATIONS"
        )

        mutations = S.last_mutations

    if mutations:

        mutation_data = []

        for mutation in mutations:

            mutation_data.append({

                "Climber": (
                    mutation["individual"]
                ),

                "From": (
                    mutation["parent"]
                ),

                "Landing": (
                    mutation["position"]
                ),

                "Movement": (
                    mutation["movement"]
                ),

                "Sigma": (

                    f"{mutation['sigma']:.2f}"
                ),

                "Result": (
                    mutation["result"]
                )
            })

        static_table(

            pd.DataFrame(
                mutation_data
            )
        )

    else:

        st.html("""

        <div class="small-text">

            Take your first jump to see
            how the climbers evolve.

        </div>

        """)

    if st.button(

        "CLOSE",

        key="close_climbers",

        use_container_width=True
    ):

        close_dialog()

        st.rerun()


# ============================================================
# 35. GAME GUIDE CONTENT
# ============================================================

GUIDE_CONTENT = {

    "How to Play": [

        (

            "🚩 Your Mission",

            "Reach exactly position 79 within "
            "30 moves."
        ),

        (

            "⚡ Jump Power",

            "Sigma controls the scale of random "
            "movement. Larger sigma generally "
            "allows wider exploration."
        ),

        (

            "🧗 Your Team",

            "Five climbers generate five new "
            "candidates each turn. The five "
            "strongest individuals survive."
        ),

        (

            "⚠ Danger Zone",

            "Any offspring beyond position 79 "
            "fails the mission. This is a special "
            "game rule, not a standard rule "
            "of evolutionary algorithms."
        )
    ],

    "TIME — Deterministic": [

        (

            "⏳ Fixed Schedule",

            "Jump power decreases according "
            "to a predefined schedule."
        ),

        (

            "No Performance Feedback",

            "Power changes regardless of "
            "whether the climbers improve."
        ),

        (

            "Formula",

            "σ(t) = max(0.5, σ₀ × (1 − t/30))"
        )
    ],

    "SMART — Adaptive": [

        (

            "⚡ Performance Feedback",

            "The controller observes how many "
            "mutations improve their parent's "
            "fitness."
        ),

        (

            "More Than 20% Success",

            "Increase sigma by multiplying "
            "it by 1.25."
        ),

        (

            "Less Than 20% Success",

            "Decrease sigma by multiplying "
            "it by 0.8."
        ),

        (

            "Exactly 20% Success",

            "Keep sigma unchanged. This is "
            "the 1/5 success rule used in "
            "this simulation."
        )
    ],

    "EVOLVE — Self-Adaptive": [

        (

            "🧬 Individual Power",

            "Every climber carries its own "
            "sigma value."
        ),

        (

            "Power Mutation",

            "Sigma mutates before the "
            "climber's position mutates."
        ),

        (

            "Survival Selection",

            "The strongest individuals survive "
            "together with their associated "
            "sigma values."
        ),

        (

            "Formula",

            "σ′ = σ × exp(0.4 × N(0,1))"
        )
    ],

    "Practice Mode": [

        (

            "🎮 Free Control",

            "Change your jump power at any time "
            "without resetting your progress."
        ),

        (

            "Landing Preview",

            "Inspect all five proposed landing "
            "positions before jumping."
        ),

        (

            "Try Another Move",

            "Reject the current proposal and "
            "consume one turn to obtain a "
            "new random draw."
        )
    ],

    "Scoring and Rewards": [

        (

            "⭐ Three Stars",

            "Complete the mission in 10 moves "
            "or fewer."
        ),

        (

            "⭐ Two Stars",

            "Complete the mission in "
            "11 to 20 moves."
        ),

        (

            "⭐ One Star",

            "Complete the mission in "
            "21 to 30 moves."
        ),

        (

            "🏆 Power Master",

            "Win with TIME, SMART and EVOLVE "
            "to complete all three challenges."
        )
    ]
}


# ============================================================
# 36. LEARNING GUIDE POPUP
# ============================================================

@st.dialog(

    "Game Guide",

    width="large",

    dismissible=False
)
def guide_dialog():

    topic = st.selectbox(

        "Choose a topic",

        options=list(
            GUIDE_CONTENT.keys()
        ),

        key="guide_topic"
    )

    html = ""

    for title, text in GUIDE_CONTENT[topic]:

        html += f"""

        <div class="guide-item">

            <div class="card-title">

                {escape(title)}

            </div>

            <div class="card-text">

                {escape(text)}

            </div>

        </div>

        """

    st.html(html)

    if st.button(

        "BACK TO GAME",

        key="close_guide",

        use_container_width=True
    ):

        close_dialog()

        st.rerun()


# ============================================================
# 37. PRESERVE WIDGET STATE
# ============================================================

# Streamlit can remove widget state when a widget
# is not rendered on the current screen.
#
# Restore values from the active game settings
# before rendering the relevant widgets.

if S.screen == "game":

    active_strategy, active_initial = (
        S.settings
    )

    if S.game_mode == "Challenge":

        S.strategy = active_strategy

        S.initial_power = int(
            active_initial
        )

    else:

        # Keep the latest manual power
        # when the setup screen disappears.

        if "manual_power" not in S:

            S.manual_power = float(
                S.sigma
            )


# ============================================================
# 38. APPLICATION ROUTING
# ============================================================

if S.screen == "menu":

    display_menu()

elif S.screen == "setup":

    display_setup()

elif S.screen == "game":

    display_game()

    active_dialog = S.active_dialog

    if active_dialog == "result":

        result_dialog()

    elif active_dialog == "progress":

        progress_dialog()

    elif active_dialog == "climbers":

        climbers_dialog()

    elif active_dialog == "guide":

        guide_dialog()

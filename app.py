
import streamlit as st
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import base64

from pathlib import Path
from html import escape
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
# 02. CONSTANTS
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

RANDOM_SEED = 44

SIMULATION_VERSION = "fitness_mountain_v5"

STRATEGIES = {
    "Manual": {
        "color": "#4ADE80",
        "description": (
            "Adjust your step size and preview mutations "
            "before accepting the next generation."
        )
    },

    "Deterministic": {
        "color": "#22D3EE",
        "description": (
            "Step size decreases automatically according "
            "to a predefined generation schedule."
        )
    },

    "Adaptive": {
        "color": "#FBBF24",
        "description": (
            "Step size changes according to mutation "
            "success using the 1/5 Success Rule."
        )
    },

    "Self-Adaptive": {
        "color": "#E879F9",
        "description": (
            "Each individual evolves its own mutation "
            "step size through mutation and selection."
        )
    }
}


# ============================================================
# 03. BACKGROUND IMAGE
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


# ============================================================
# 04. GLOBAL CSS
# ============================================================

CSS = """
<style>

:root {
    --cyan: #22D3EE;
    --light-cyan: #67E8F9;
    --gold: #FBBF24;
    --purple: #E879F9;
    --green: #4ADE80;
    --red: #F87171;
    --muted: #94A3B8;
    --panel: #111827;
    --border: #29384C;
    --ui: clamp(0.82px, 0.135dvh, 1.25px);
}

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
    background-color: #080D1C;

    background-image:
        linear-gradient(
            rgba(5,10,25,0.87),
            rgba(5,10,25,0.87)
        ),
        url("data:image/jpeg;base64,__BACKGROUND__");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    color: #E2E8F0;
}

[data-testid="stHeader"] {
    background: transparent;
    height: 30px;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    width: 100% !important;
    max-width: none !important;

    height: 100dvh !important;

    padding: 10px 24px 12px !important;

    margin: 0 auto !important;

    overflow: hidden !important;
    box-sizing: border-box;
}

.block-container >
[data-testid="stVerticalBlock"] {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 0;
    gap: 8px !important;
}

[data-testid="stVerticalBlock"] {
    gap: 6px !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 14px !important;
}

[data-testid="stColumn"] {
    min-width: 0;
    min-height: 0;
}

[data-testid="stElementContainer"] {
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stWidgetLabel"] {
    min-height: 0 !important;
    margin-bottom: 0 !important;
}

[data-testid="stWidgetLabel"] p {
    color: #E2E8F0;
    font-size: calc(13 * var(--ui));
}

.stMarkdown p {
    margin-bottom: 0;
}


/* =========================================================
   HEADER
   ========================================================= */

.hero {
    text-align: center;
    padding: 2px 0 5px;
}

.hero-label {
    color: #22D3EE;
    font-size: calc(10 * var(--ui));
    font-weight: 800;
    letter-spacing: 5px;
}

.hero-title {
    color: #E0F2FE;
    font-size: calc(36 * var(--ui));
    font-weight: 900;
    letter-spacing: 6px;
    line-height: 1.15;
    margin: 4px 0;
    text-shadow: 0 0 24px #0891B2;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: calc(10 * var(--ui));
    letter-spacing: 3px;
}

.mode-label {
    display: inline-block;
    padding: 3px 12px;
    margin-top: 5px;
    border: 1px solid #155E75;
    border-radius: 20px;
    color: #67E8F9;
    background: rgba(34,211,238,0.08);
    font-size: calc(10 * var(--ui));
    font-weight: 800;
    letter-spacing: 1.5px;
}


/* =========================================================
   MAIN MENU
   ========================================================= */

.st-key-welcome_screen {
    width: 100%;
    max-width: 850px;

    margin: auto !important;
    padding: 18px 28px !important;

    background: rgba(8,13,28,0.97);

    border: 1px solid #164E63;
    border-radius: 18px;

    box-shadow: 0 0 45px rgba(34,211,238,0.12);

    box-sizing: border-box;
}

.welcome-mountain {
    display: block;
    width: 100%;
    height: 15dvh;
    max-height: 145px;
    object-fit: contain;
    margin: 0 auto;
}

.welcome-mission {
    color: #FBBF24;
    font-size: calc(19 * var(--ui));
    font-weight: 800;
    letter-spacing: 2px;
    text-align: center;
    margin: 4px 0;
}

.welcome-text {
    color: #CBD5E1;
    text-align: center;
    font-size: calc(13 * var(--ui));
    line-height: 1.4;
}

.instruction-row {
    display: flex;
    align-items: center;
    gap: 12px;

    background: #111827;
    border: 1px solid #29384C;
    border-radius: 9px;

    padding: 8px 12px;
    margin-bottom: 5px;
}

.instruction-number {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 32px;
    height: 32px;
    flex-shrink: 0;

    color: #22D3EE;
    background: rgba(34,211,238,0.08);

    border: 1px solid #155E75;
    border-radius: 8px;

    font-weight: 800;
}

.instruction-title {
    color: #E2E8F0;
    font-size: calc(13 * var(--ui));
    font-weight: 800;
}

.instruction-text {
    color: #94A3B8;
    font-size: calc(11 * var(--ui));
    line-height: 1.35;
}

.mode-card {
    min-height: 92px;
    padding: 10px 12px;

    background: #111827;
    border: 1px solid #29384C;
    border-radius: 10px;

    box-sizing: border-box;
}

.mode-card-title {
    font-size: calc(16 * var(--ui));
    font-weight: 800;
    margin-bottom: 5px;
}

.mode-card-text {
    font-size: calc(12 * var(--ui));
    color: #CBD5E1;
    line-height: 1.4;
}


/* =========================================================
   DASHBOARD
   ========================================================= */

.st-key-main_dashboard {
    flex: 1 1 auto;
    min-height: 0;
    width: 100%;
}

.section-heading {
    color: #67E8F9;
    font-size: calc(11 * var(--ui));
    font-weight: 800;
    letter-spacing: 1.6px;
    line-height: 1.3;
}

.panel-card {
    background: rgba(17,24,39,0.95);
    border: 1px solid #29384C;
    border-radius: 9px;
    padding: 8px 11px;
}

.panel-title {
    font-size: calc(12 * var(--ui));
    font-weight: 800;
    margin-bottom: 4px;
}

.panel-text {
    color: #CBD5E1;
    font-size: calc(12 * var(--ui));
    line-height: 1.4;
}

.small-text {
    color: #94A3B8;
    font-size: calc(11 * var(--ui));
    line-height: 1.35;
}


/* =========================================================
   RADIO BUTTONS
   ========================================================= */

.st-key-left_panel [role="radiogroup"] {
    display: flex;
    flex-direction: column;

    width: 100%;
    gap: 1px;

    padding: 7px 10px;

    background: rgba(17,24,39,0.95);
    border: 1px solid #29384C;
    border-radius: 9px;
}

.st-key-left_panel [role="radiogroup"] label {
    min-height: calc(24 * var(--ui));
    margin: 0 !important;
}

.st-key-left_panel [role="radiogroup"] p {
    font-size: calc(13 * var(--ui));
    color: #E2E8F0;
}


/* =========================================================
   SLIDER
   ========================================================= */

[data-testid="stSlider"] {
    margin: 0 !important;
    padding: 0 !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton {
    margin: 0 !important;
    padding: 0 !important;
}

.stButton > button {
    width: 100%;

    min-height: calc(34 * var(--ui)) !important;
    padding: 4px 9px !important;

    background: rgba(17,24,39,0.96);
    border: 1px solid #29384C;
    border-radius: 9px;

    color: #67E8F9;
    font-weight: 700;
}

.stButton > button p {
    font-size: calc(12 * var(--ui));
    line-height: 1.2;
    margin: 0;
}

.stButton > button[kind="primary"] {
    background: #155E75;
    border-color: #22D3EE;
    color: #FFFFFF;
}

.stButton > button:hover {
    background: #164E63;
    border-color: #22D3EE;
    color: #FFFFFF;
}

.stButton > button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

.metric-grid {
    display: grid;
    grid-template-columns: repeat(5,minmax(0,1fr));
    gap: 9px;
    width: 100%;
}

.metric-card {
    background: rgba(17,24,39,0.96);
    border: 1px solid #29384C;
    border-radius: 11px;

    padding: 9px 12px;
    min-height: calc(65 * var(--ui));

    display: flex;
    flex-direction: column;
    justify-content: center;

    box-sizing: border-box;
}

.metric-label {
    color: #94A3B8;
    font-size: calc(10 * var(--ui));
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 5px;
}

.metric-value {
    font-size: calc(27 * var(--ui));
    font-weight: 900;
    line-height: 1.1;
}

.progress-track {
    height: 5px;
    background: #1E293B;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 6px;
}

.progress-fill {
    height: 100%;
    border-radius: 10px;
}


/* =========================================================
   FITNESS LANDSCAPE
   ========================================================= */

.fitness-image {
    display: block;
    width: 100%;

    height: clamp(170px,36dvh,430px);

    object-fit: fill;

    background: #0B1120;
    border: 1px solid #29384C;
    border-radius: 12px;

    box-sizing: border-box;
}

.practice-image {
    height: clamp(150px,32dvh,390px);
}


/* =========================================================
   PHASE INDICATOR
   ========================================================= */

.phase-grid {
    display: grid;
    grid-template-columns: repeat(3,minmax(0,1fr));
    gap: 6px;
}

.phase-card {
    background: rgba(17,24,39,0.95);
    border: 1px solid #29384C;
    border-radius: 7px;

    text-align: center;
    padding: 6px 5px;

    color: #64748B;
    font-size: calc(10 * var(--ui));
    font-weight: 700;
}

.phase-active {
    border-color: var(--phase-color);
    color: var(--phase-color);
    background: rgba(34,211,238,0.06);
}


/* =========================================================
   STATUS AND FEEDBACK
   ========================================================= */

.target-status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;

    background: rgba(17,24,39,0.95);
    border: 1px solid #29384C;
    border-radius: 8px;

    padding: 8px 11px;

    font-size: calc(11 * var(--ui));
    font-weight: 700;
}

.feedback-box {
    background: rgba(17,24,39,0.96);
    border: 1px solid #29384C;
    border-left: 4px solid #FBBF24;
    border-radius: 9px;

    padding: 8px 12px;
}

.feedback-title {
    font-size: calc(11 * var(--ui));
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 4px;
}

.feedback-text {
    color: #E2E8F0;
    font-size: calc(12 * var(--ui));
    line-height: 1.35;
}

.preview-box {
    background: rgba(17,24,39,0.96);
    border: 1px solid #29384C;
    border-left: 4px solid #22D3EE;
    border-radius: 9px;
    padding: 8px 12px;
}

.preview-title {
    font-size: calc(11 * var(--ui));
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

.preview-value {
    font-size: calc(18 * var(--ui));
    font-weight: 900;
    line-height: 1.2;
}

.preview-text {
    color: #CBD5E1;
    font-size: calc(11 * var(--ui));
    line-height: 1.3;
}


/* =========================================================
   FOOTER
   ========================================================= */

.st-key-bottom_navigation {
    width: 100%;
    flex: 0 0 auto;
    margin-top: auto !important;

    padding-top: 8px;
    border-top: 1px solid #29384C;
}


/* =========================================================
   POP-UP DIALOGS
   ========================================================= */

[data-testid="stDialog"] {
    overflow: hidden !important;
}

[data-testid="stDialog"] [role="dialog"] {
    width: min(1000px,94vw) !important;
    max-width: 94vw !important;
    max-height: 92dvh !important;

    background: #0B1120 !important;
    color: #E2E8F0;

    border: 1px solid #29384C;
    border-radius: 16px;

    overflow: hidden !important;
    overscroll-behavior: none !important;
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
    font-size: calc(21 * var(--ui)) !important;
    margin: 0 !important;
}

[data-testid="stDialog"] p {
    font-size: calc(12 * var(--ui));
    line-height: 1.4;
}


/* =========================================================
   MISSION RESULT
   ========================================================= */

.result-container {
    width: 100%;
    text-align: center;

    padding: 16px;
    border-radius: 14px;

    background: #080D1C;
    box-sizing: border-box;
}

.result-success {
    border: 1px solid #22C55E;
    box-shadow: 0 0 35px rgba(34,197,94,0.15);
}

.result-failed {
    border: 1px solid #EF4444;
    box-shadow: 0 0 35px rgba(239,68,68,0.15);
}

.result-icon {
    font-size: clamp(35px,9dvh,75px);
    line-height: 1.1;
    margin-bottom: 6px;
}

.result-title {
    font-size: clamp(26px,5dvh,46px);
    font-weight: 900;
    letter-spacing: 3px;
    line-height: 1.2;
    margin-bottom: 8px;
}

.result-description {
    color: #CBD5E1;
    font-size: calc(14 * var(--ui));
    line-height: 1.4;
    margin-bottom: 12px;
}

.result-grid {
    display: grid;
    grid-template-columns: repeat(4,minmax(0,1fr));
    gap: 8px;
}

.result-stat {
    background: #111827;
    border: 1px solid #29384C;
    border-radius: 9px;
    padding: 10px;
}

.result-stat-label {
    color: #94A3B8;
    font-size: calc(10 * var(--ui));
    font-weight: 700;
}

.result-stat-value {
    color: #E2E8F0;
    font-size: calc(25 * var(--ui));
    font-weight: 900;
}

.result-reason {
    text-align: left;
    background: #111827;
    border: 1px solid #29384C;
    border-radius: 9px;
    padding: 10px 12px;
    margin-top: 10px;
}


/* =========================================================
   PERFORMANCE AND TABLES
   ========================================================= */

.analysis-image {
    display: block;
    width: 100%;
    height: 29dvh;
    max-height: 280px;
    object-fit: contain;

    background: #080D1C;
    border: 1px solid #29384C;
    border-radius: 9px;
}

.static-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;

    background: #111827;
    color: #E2E8F0;

    font-size: calc(11 * var(--ui));
}

.static-table th {
    color: #67E8F9;
    background: #1E293B;
    padding: 7px 4px;
    border: 1px solid #334155;
    text-align: center;
    overflow-wrap: anywhere;
}

.static-table td {
    padding: 7px 4px;
    border: 1px solid #29384C;
    text-align: center;
    overflow-wrap: anywhere;
}

.guide-card {
    background: #111827;
    border: 1px solid #29384C;
    border-radius: 10px;
    padding: 12px;
}

.guide-title {
    font-size: calc(20 * var(--ui));
    font-weight: 800;
    margin-bottom: 8px;
}

.guide-point {
    background: #080D1C;
    border-left: 3px solid #22D3EE;
    border-radius: 5px;

    color: #E2E8F0;
    font-size: calc(12 * var(--ui));
    line-height: 1.4;

    padding: 8px 10px;
    margin-bottom: 6px;
}


/* =========================================================
   SHORT DESKTOP / LAPTOP
   ========================================================= */

@media (max-height: 780px) {

    .block-container {
        padding: 7px 20px 8px !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 4px !important;
    }

    .hero-title {
        font-size: 30px;
    }

    .hero {
        padding-bottom: 3px;
    }

    .fitness-image {
        height: 34dvh;
    }

    .practice-image {
        height: 29dvh;
    }

    .metric-card {
        min-height: 53px;
        padding: 7px 10px;
    }

    .panel-card,
    .feedback-box,
    .preview-box {
        padding: 6px 9px;
    }

    .stButton > button {
        min-height: 29px !important;
    }

    .instruction-row {
        padding: 5px 9px;
    }

    .mode-card {
        min-height: 76px;
    }
}

@media (max-height: 650px) {

    :root {
        --ui: 0.8px;
    }

    .hero-title {
        font-size: 24px;
    }

    .hero-label,
    .hero-subtitle {
        font-size: 8px;
    }

    .fitness-image {
        height: 29dvh;
    }

    .practice-image {
        height: 25dvh;
    }

    .metric-card {
        min-height: 42px;
        padding: 5px 7px;
    }

    .stButton > button {
        min-height: 25px !important;
        padding: 2px 6px !important;
    }

    .welcome-mountain {
        max-height: 70px;
    }

    .static-table td,
    .static-table th {
        padding: 4px 3px;
    }
}

@media (max-width: 1100px) {

    .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    .metric-grid {
        gap: 5px;
    }

    .metric-card {
        padding: 6px;
    }

    .metric-label {
        font-size: 9px;
    }

    .metric-value {
        font-size: 20px;
    }
}

</style>
"""

st.html(
    CSS.replace(
        "__BACKGROUND__",
        background
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
    "game_started": False,
    "game_mode": "Practice",
    "selected_strategy": "Deterministic",
    "initial_sigma": 15,
    "manual_sigma": 20.0,
    "active_dialog": None,
    "history_page": 0,
    "guide_topic": "Manual Control"
}

for key, value in DEFAULT_STATE.items():

    if key not in S:
        S[key] = value


# ============================================================
# 07. RESET SIMULATION
# ============================================================

def reset_simulation():

    strategy = (
        "Manual"
        if S.game_mode == "Practice"
        else S.selected_strategy
    )

    sigma = float(
        S.manual_sigma
        if S.game_mode == "Practice"
        else S.initial_sigma
    )

    S.settings = (strategy, sigma)

    S.generation = 0

    S.population = [
        (INITIAL_POSITION, sigma)
        for _ in range(POPULATION_SIZE)
    ]

    S.sigma = sigma

    # Same random sequence after every reset.
    S.random_draws = np.random.default_rng(
        RANDOM_SEED
    ).normal(
        size=(
            MAX_GENERATIONS,
            2,
            POPULATION_SIZE
        )
    )

    S.history = [{
        "Generation": 0,
        "Position": INITIAL_POSITION,
        "Fitness": float(fitness(INITIAL_POSITION)),
        "Sigma": sigma,
        "Distance": TARGET_POSITION - INITIAL_POSITION,
        "Success Rate": None,
        "Action": "Start"
    }]

    S.last_mutations = []
    S.last_offspring = []

    S.game_finished = False
    S.mission_success = False
    S.mission_failed = False

    S.failure_type = None

    S.final_position = None
    S.final_sigma = None
    S.trigger_parent = None
    S.trigger_individual = None

    S.active_dialog = None
    S.history_page = 0

    S.feedback = (
        "Your population starts at position 10. "
        "Reach exactly position 79 within 30 turns."
    )

    S.simulation_version = SIMULATION_VERSION


if (
    S.get("simulation_version")
    != SIMULATION_VERSION
):

    reset_simulation()


# ============================================================
# 08. MISSION HELPERS
# ============================================================

def get_best_individual():

    return max(
        S.population,
        key=lambda individual: float(
            fitness(individual[0])
        )
    )


def get_best_position():

    return int(
        get_best_individual()[0]
    )


def get_display_position():

    if (
        S.game_finished
        and S.final_position is not None
    ):

        return int(S.final_position)

    return get_best_position()


def get_display_sigma():

    if (
        S.game_finished
        and S.final_sigma is not None
    ):

        return float(S.final_sigma)

    if S.game_mode == "Practice":

        return float(S.manual_sigma)

    return float(S.sigma)


def get_distance():

    return abs(
        TARGET_POSITION - get_display_position()
    )


def get_phase(position):

    if position < 45:

        return (
            "EXPLORATION",
            "#38BDF8",
            "Try a larger step size to escape "
            "the local optimum."
        )

    if position < 68:

        return (
            "TRANSITION",
            "#FBBF24",
            "Balance exploration with smaller "
            "movements toward the target."
        )

    return (
        "PRECISION",
        "#4ADE80",
        "Use smaller movements to reach "
        "position 79 without overshooting."
    )


def get_target_status():

    position = get_display_position()

    if position == TARGET_POSITION:

        return (
            "EXACT GLOBAL OPTIMUM",
            "#4ADE80"
        )

    if position > TARGET_POSITION:

        return (
            "OVERSHOT TARGET POSITION",
            "#F87171"
        )

    return (
        "BELOW TARGET POSITION",
        "#FBBF24"
    )


# ============================================================
# 09. MUTATION PREVIEW
# ============================================================

def generate_mutations():

    if S.game_finished:

        return []

    if S.generation >= MAX_GENERATIONS:

        return []

    strategy, _ = S.settings

    draws = S.random_draws[S.generation]

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
                S.manual_sigma
            )

        # ----------------------------------------------------
        # SELF-ADAPTIVE CONTROL
        # ----------------------------------------------------

        elif strategy == "Self-Adaptive":

            child_sigma = float(
                np.clip(
                    individual_sigma
                    * np.exp(0.4 * draws[0, i]),
                    MIN_SIGMA,
                    MAX_SIGMA
                )
            )

        # ----------------------------------------------------
        # DETERMINISTIC AND ADAPTIVE
        # ----------------------------------------------------

        else:

            child_sigma = float(
                S.sigma
            )

        movement = (
            child_sigma * draws[1, i]
        )

        # IMPORTANT:
        # Never restrict movement to position 79.
        # Overshooting must remain possible.

        child_position = int(
            np.clip(
                np.rint(position + movement),
                MIN_POSITION,
                MAX_POSITION
            )
        )

        parent_fitness = float(
            fitness(position)
        )

        child_fitness = float(
            fitness(child_position)
        )

        improved = (
            child_fitness > parent_fitness
        )

        if child_position > TARGET_POSITION:

            result = "OVERSHOOT"

        elif child_position == TARGET_POSITION:

            result = "EXACT HIT"

        else:

            result = "BELOW TARGET"

        mutations.append({
            "individual": i + 1,
            "parent": position,
            "position": child_position,
            "sigma": child_sigma,
            "movement": child_position - position,
            "parent_fitness": parent_fitness,
            "child_fitness": child_fitness,
            "improved": improved,
            "result": result
        })

    return mutations


# ============================================================
# 10. SAVE HISTORY
# ============================================================

def save_history(
    action,
    success_rate=None
):

    position = get_display_position()

    S.history.append({
        "Generation": S.generation,
        "Position": position,
        "Fitness": float(fitness(position)),
        "Sigma": get_display_sigma(),
        "Distance": abs(
            TARGET_POSITION - position
        ),
        "Success Rate": success_rate,
        "Action": action
    })


# ============================================================
# 11. FINISH MISSION
# ============================================================

def finish_mission(
    success,
    failure_type=None,
    trigger=None
):

    S.game_finished = True

    S.mission_success = success
    S.mission_failed = not success

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

        S.final_position = get_best_position()

        S.final_sigma = (
            float(S.manual_sigma)
            if S.game_mode == "Practice"
            else float(S.sigma)
        )

    S.active_dialog = "result"


# ============================================================
# 12. EVOLUTION PROCESS
# ============================================================

def next_generation():

    if S.game_finished:

        return

    if S.generation >= MAX_GENERATIONS:

        return

    strategy, initial_sigma = S.settings

    mutations = generate_mutations()

    if not mutations:

        return

    old_sigma = get_display_sigma()

    previous_position = get_best_position()

    offspring = [
        (
            mutation["position"],
            mutation["sigma"]
        )
        for mutation in mutations
    ]

    successes = sum(
        mutation["improved"]
        for mutation in mutations
    )

    success_rate = (
        successes / POPULATION_SIZE
    )

    S.generation += 1

    S.last_mutations = mutations
    S.last_offspring = offspring

    # --------------------------------------------------------
    # A. CHECK ALL OFFSPRING BEFORE SELECTION
    # --------------------------------------------------------

    overshoots = [
        mutation
        for mutation in mutations
        if mutation["position"] > TARGET_POSITION
    ]

    exact_hits = [
        mutation
        for mutation in mutations
        if mutation["position"] == TARGET_POSITION
    ]

    # --------------------------------------------------------
    # B. SURVIVAL SELECTION
    # --------------------------------------------------------

    combined = S.population + offspring

    combined.sort(
        key=lambda individual: float(
            fitness(individual[0])
        ),
        reverse=True
    )

    new_population = combined[:POPULATION_SIZE]

    # --------------------------------------------------------
    # C. PARAMETER CONTROL
    # --------------------------------------------------------

    if strategy == "Manual":

        new_sigma = float(
            S.manual_sigma
        )

        explanation = (
            f"Manual step size: {new_sigma:.2f}. "
            "The accepted mutations undergo "
            "fitness-based survival selection."
        )

    elif strategy == "Deterministic":

        new_sigma = max(
            MIN_SIGMA,
            initial_sigma * (
                1 - S.generation / MAX_GENERATIONS
            )
        )

        explanation = (
            f"Scheduled step size: "
            f"{old_sigma:.2f} → {new_sigma:.2f}."
        )

    elif strategy == "Adaptive":

        if success_rate > 0.2:

            new_sigma = min(
                MAX_SIGMA,
                old_sigma * 1.25
            )

            action = "Increase"

        elif success_rate < 0.2:

            new_sigma = max(
                MIN_SIGMA,
                old_sigma * 0.8
            )

            action = "Decrease"

        else:

            new_sigma = old_sigma
            action = "Maintain"

        explanation = (
            f"{successes}/{POPULATION_SIZE} "
            f"successful mutations "
            f"({success_rate:.0%}). "
            f"{action} sigma: "
            f"{old_sigma:.2f} → {new_sigma:.2f}."
        )

    else:

        new_sigma = float(
            new_population[0][1]
        )

        explanation = (
            "Each individual evolved its own sigma. "
            f"Best surviving sigma: {new_sigma:.2f}."
        )

    if strategy != "Self-Adaptive":

        new_population = [
            (int(position), float(new_sigma))
            for position, _ in new_population
        ]

    S.population = new_population
    S.sigma = new_sigma

    current_position = get_best_position()

    S.feedback = (
        f"Generation {S.generation}: "
        f"{explanation} "
        f"Best position: "
        f"{previous_position} → {current_position}."
    )

    # --------------------------------------------------------
    # D. OVERSHOOT = IMMEDIATE FAILURE
    # --------------------------------------------------------

    if overshoots:

        trigger = overshoots[0]

        finish_mission(
            success=False,
            failure_type="OVERSHOOT",
            trigger=trigger
        )

        S.feedback = (
            f"Individual {trigger['individual']} "
            f"moved from {trigger['parent']} "
            f"to {trigger['position']}. "
            f"Overshoot: "
            f"{trigger['position'] - TARGET_POSITION} "
            "unit(s). MISSION FAILED!"
        )

    # --------------------------------------------------------
    # E. EXACT POSITION 79 = SUCCESS
    # --------------------------------------------------------

    elif exact_hits:

        trigger = exact_hits[0]

        finish_mission(
            success=True,
            trigger=trigger
        )

        S.feedback = (
            f"Individual {trigger['individual']} "
            "reached exactly position 79. "
            "GLOBAL OPTIMUM REACHED!"
        )

    # --------------------------------------------------------
    # F. GENERATION LIMIT
    # --------------------------------------------------------

    elif S.generation >= MAX_GENERATIONS:

        finish_mission(
            success=False,
            failure_type="UNDERSHOOT"
        )

        S.feedback += (
            f" Maximum turns reached. "
            f"Remaining distance: {get_distance()}. "
            "MISSION FAILED!"
        )

    save_history(
        action="Mutation accepted",
        success_rate=success_rate
    )


# ============================================================
# 13. RETRY MUTATION — PRACTICE MODE
# ============================================================

def retry_mutation():

    if S.game_finished:

        return

    if S.game_mode != "Practice":

        return

    if S.generation >= MAX_GENERATIONS:

        return

    # Reject the current mutation preview.
    # The population remains unchanged.
    # One turn is consumed.

    S.generation += 1

    S.last_mutations = []
    S.last_offspring = []

    S.feedback = (
        "Mutation rejected. "
        "Your population remains unchanged. "
        "One turn has been consumed."
    )

    if S.generation >= MAX_GENERATIONS:

        finish_mission(
            success=False,
            failure_type="UNDERSHOOT"
        )

        S.feedback += (
            " No turns remaining. MISSION FAILED!"
        )

    save_history(
        action="Mutation rejected",
        success_rate=None
    )


# ============================================================
# 14. GAME CALLBACKS
# ============================================================

def start_game(mode):

    S.game_mode = mode
    S.game_started = True

    if mode == "Practice":

        S.manual_sigma = 20.0

    else:

        S.selected_strategy = "Deterministic"
        S.initial_sigma = 15

    reset_simulation()


def handle_settings_change():

    reset_simulation()


def handle_reset():

    reset_simulation()


def handle_run_all():

    if S.game_mode != "Challenge":

        return

    while (
        not S.game_finished
        and S.generation < MAX_GENERATIONS
    ):

        next_generation()


def handle_home():

    S.game_started = False
    S.active_dialog = None


def open_dialog(name):

    S.active_dialog = name
    S.history_page = 0


def close_dialog():

    S.active_dialog = None


def change_history_page(direction):

    S.history_page += direction


# ============================================================
# 15. REUSABLE UI COMPONENTS
# ============================================================

def section_heading(text):

    st.html(
        f'<div class="section-heading">'
        f'{escape(text)}</div>'
    )


def panel_card(
    title,
    text,
    color="#67E8F9"
):

    st.html(f"""
    <div class="panel-card">
        <div class="panel-title"
             style="color:{color}">
            {escape(title)}
        </div>
        <div class="panel-text">
            {escape(text)}
        </div>
    </div>
    """)


def metric_html(label, value, color):

    return f"""
    <div class="metric-card">
        <div class="metric-label">
            {escape(str(label))}
        </div>
        <div class="metric-value"
             style="color:{color}">
            {escape(str(value))}
        </div>
    </div>
    """


def static_table(dataframe):

    table = dataframe.to_html(
        index=False,
        escape=True,
        border=0,
        classes="static-table"
    )

    st.html(table)


# ============================================================
# 16. MATPLOTLIB HELPERS
# ============================================================

@st.cache_resource
def get_plot_lock():

    return RLock()


def figure_to_base64(fig):

    buffer = BytesIO()

    try:

        fig.savefig(
            buffer,
            format="png",
            dpi=140,
            facecolor=fig.get_facecolor()
        )

        buffer.seek(0)

        return base64.b64encode(
            buffer.read()
        ).decode("utf-8")

    finally:

        buffer.close()
        plt.close(fig)


def style_axis(ax):

    ax.set_facecolor("#0B1120")

    ax.tick_params(
        colors="#94A3B8",
        labelsize=9
    )

    for spine in ax.spines.values():

        spine.set_color("#29384C")

    ax.grid(
        True,
        color="#334155",
        alpha=0.25,
        linestyle="--"
    )


# ============================================================
# 17. WELCOME MOUNTAIN
# ============================================================

@st.cache_data
def create_welcome_mountain():

    with get_plot_lock():

        fig, ax = plt.subplots(
            figsize=(8, 2.2),
            facecolor="#080D1C"
        )

        ax.set_facecolor("#080D1C")

        x = np.linspace(0, 100, 500)
        y = fitness(x)

        ax.fill_between(
            x,
            20,
            y,
            color="#22D3EE",
            alpha=0.10
        )

        ax.plot(
            x,
            y,
            color="#22D3EE",
            linewidth=2.5
        )

        ax.scatter(
            LOCAL_OPTIMUM,
            fitness(LOCAL_OPTIMUM),
            color="#94A3B8",
            s=45
        )

        ax.scatter(
            GLOBAL_OPTIMUM,
            fitness(GLOBAL_OPTIMUM),
            marker="*",
            color="#FBBF24",
            s=220,
            zorder=5
        )

        ax.text(
            LOCAL_OPTIMUM,
            fitness(LOCAL_OPTIMUM) + 8,
            "LOCAL OPTIMUM",
            color="#94A3B8",
            fontsize=9,
            ha="center"
        )

        ax.text(
            GLOBAL_OPTIMUM,
            fitness(GLOBAL_OPTIMUM) + 10,
            "GLOBAL OPTIMUM · 79",
            color="#FBBF24",
            fontsize=10,
            fontweight="bold",
            ha="center"
        )

        ax.set_xlim(0, 100)
        ax.set_ylim(20, 125)

        ax.axis("off")

        fig.subplots_adjust(
            left=0.02,
            right=0.98,
            top=0.98,
            bottom=0.02
        )

        return figure_to_base64(fig)


# ============================================================
# 18. APPLICATION HEADER
# ============================================================

def display_header(show_mode=True):

    mode_html = ""

    if show_mode:

        mode_html = (
            f'<div class="mode-label">'
            f'{S.game_mode.upper()} MODE'
            f'</div>'
        )

    st.html(f"""
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

        {mode_html}
    </div>
    """)


# ============================================================
# 19. WELCOME SCREEN
# ============================================================

def display_welcome_screen():

    with st.container(
        key="welcome_screen"
    ):

        display_header(
            show_mode=False
        )

        mountain = create_welcome_mountain()

        st.html(f"""
        <img
            class="welcome-mountain"
            src="data:image/png;base64,{mountain}"
            alt="Fitness Mountain"
        >

        <div class="welcome-mission">
            REACH THE GLOBAL OPTIMUM
        </div>

        <div class="welcome-text">
            Land exactly on position 79 within
            30 turns without overshooting.
        </div>
        """)

        instructions = [

            (
                "01",
                "Choose Your Mode",
                "Learn with Practice Mode or test your "
                "strategy in Challenge Mode."
            ),

            (
                "02",
                "Control Your Step Size",
                "Use manual sigma or choose an automatic "
                "parameter control strategy."
            ),

            (
                "03",
                "Reach Position 79",
                "Hit the exact target to win. "
                "Overshooting or running out of turns fails."
            )
        ]

        html = ""

        for number, title, text in instructions:

            html += f"""
            <div class="instruction-row">

                <div class="instruction-number">
                    {number}
                </div>

                <div>
                    <div class="instruction-title">
                        {escape(title)}
                    </div>

                    <div class="instruction-text">
                        {escape(text)}
                    </div>
                </div>

            </div>
            """

        st.html(html)

        left, right = st.columns(2)

        with left:

            st.html("""
            <div class="mode-card">

                <div class="mode-card-title"
                     style="color:#4ADE80">
                    🎮 PRACTICE MODE
                </div>

                <div class="mode-card-text">
                    Adjust sigma, preview mutations,
                    accept or reject moves and learn
                    how to reach the target.
                </div>

            </div>
            """)

            st.button(
                "▶ START PRACTICE",
                key="start_practice",
                type="primary",
                use_container_width=True,
                on_click=start_game,
                args=("Practice",)
            )

        with right:

            st.html("""
            <div class="mode-card">

                <div class="mode-card-title"
                     style="color:#FBBF24">
                    🏆 CHALLENGE MODE
                </div>

                <div class="mode-card-text">
                    Choose Deterministic, Adaptive
                    or Self-Adaptive Control and
                    conquer the mountain.
                </div>

            </div>
            """)

            st.button(
                "▶ START CHALLENGE",
                key="start_challenge",
                type="primary",
                use_container_width=True,
                on_click=start_game,
                args=("Challenge",)
            )


# ============================================================
# 20. METRIC CARDS
# ============================================================

def display_metrics():

    position = get_display_position()

    sigma = get_display_sigma()

    fitness_value = float(
        fitness(position)
    )

    if S.mission_success:

        status_color = "#4ADE80"

    elif S.mission_failed:

        status_color = "#F87171"

    else:

        status_color = "#22D3EE"

    position_color = (
        "#F87171"
        if position > TARGET_POSITION
        else "#67E8F9"
    )

    cards = [

        metric_html(
            "GENERATION",
            f"{S.generation}/{MAX_GENERATIONS}",
            "#67E8F9"
        ),

        metric_html(
            "FINAL FITNESS"
            if S.game_finished
            else "BEST FITNESS",
            f"{fitness_value:.2f}",
            "#FBBF24"
        ),

        metric_html(
            "FINAL SIGMA"
            if S.game_finished
            else "CURRENT SIGMA",
            f"{sigma:.2f}",
            "#E879F9"
        ),

        metric_html(
            "FINAL POSITION"
            if S.game_finished
            else "BEST POSITION",
            position,
            position_color
        ),

        metric_html(
            "TARGET DISTANCE",
            get_distance(),
            "#4ADE80"
            if get_distance() == 0
            else "#E879F9"
        )
    ]

    progress = (
        S.generation / MAX_GENERATIONS * 100
    )

    st.html(f"""
    <div class="metric-grid">
        {''.join(cards)}
    </div>

    <div class="progress-track">

        <div class="progress-fill"
             style="
                 width:{progress}%;
                 background:{status_color};
             ">
        </div>

    </div>
    """)


# ============================================================
# 21. PHASE INDICATOR
# ============================================================

def display_phase_indicator():

    position = get_display_position()

    current_phase, _, _ = get_phase(
        position
    )

    phases = [

        (
            "EXPLORATION",
            "0–44",
            "#38BDF8"
        ),

        (
            "TRANSITION",
            "45–67",
            "#FBBF24"
        ),

        (
            "PRECISION",
            "68–79",
            "#4ADE80"
        )
    ]

    html = ""

    for phase, positions, color in phases:

        active = (
            "phase-active"
            if phase == current_phase
            and not S.game_finished
            else ""
        )

        html += f"""
        <div class="phase-card {active}"
             style="--phase-color:{color}">

            {phase} · {positions}

        </div>
        """

    st.html(f"""
    <div class="phase-grid">
        {html}
    </div>
    """)


# ============================================================
# 22. FITNESS LANDSCAPE
# ============================================================

def display_fitness_landscape():

    with get_plot_lock():

        fig, ax = plt.subplots(
            figsize=(13, 3.6),
            facecolor="#0B1120"
        )

        style_axis(ax)

        x = np.linspace(
            MIN_POSITION,
            MAX_POSITION,
            800
        )

        y = fitness(x)

        # ----------------------------------------------------
        # OVERSHOOT ZONE
        # ----------------------------------------------------

        ax.axvspan(
            TARGET_POSITION,
            MAX_POSITION,
            color="#EF4444",
            alpha=0.08
        )

        ax.text(
            90,
            117,
            "OVERSHOOT ZONE",
            color="#F87171",
            fontsize=9,
            fontweight="bold",
            ha="center"
        )

        # ----------------------------------------------------
        # MOUNTAIN GLOW
        # ----------------------------------------------------

        for width, alpha in [
            (9, 0.025),
            (6, 0.045),
            (4, 0.09)
        ]:

            ax.plot(
                x,
                y,
                color="#22D3EE",
                linewidth=width,
                alpha=alpha
            )

        ax.fill_between(
            x,
            20,
            y,
            color="#22D3EE",
            alpha=0.10
        )

        ax.plot(
            x,
            y,
            color="#22D3EE",
            linewidth=2.2,
            zorder=3
        )

        # ----------------------------------------------------
        # LOCAL OPTIMUM
        # ----------------------------------------------------

        ax.scatter(
            LOCAL_OPTIMUM,
            fitness(LOCAL_OPTIMUM),
            color="#94A3B8",
            s=55,
            zorder=5
        )

        ax.text(
            LOCAL_OPTIMUM,
            fitness(LOCAL_OPTIMUM) + 13,
            "LOCAL OPTIMUM\nPosition 27",
            color="#94A3B8",
            fontsize=9,
            fontweight="bold",
            ha="center"
        )

        # ----------------------------------------------------
        # GLOBAL OPTIMUM
        # ----------------------------------------------------

        ax.axvline(
            TARGET_POSITION,
            color="#FBBF24",
            linestyle="--",
            linewidth=1.2,
            alpha=0.8
        )

        ax.scatter(
            TARGET_POSITION,
            fitness(TARGET_POSITION),
            color="#FBBF24",
            marker="*",
            s=230,
            zorder=7
        )

        ax.text(
            TARGET_POSITION,
            113,
            "GLOBAL OPTIMUM\nPosition 79",
            color="#FBBF24",
            fontsize=10,
            fontweight="bold",
            ha="center"
        )

        # ----------------------------------------------------
        # CURRENT POPULATION
        # ----------------------------------------------------

        population_x = [
            position
            for position, _ in S.population
        ]

        ax.scatter(
            population_x,
            fitness(np.array(population_x)),
            s=50,
            color="#0891B2",
            edgecolors="#67E8F9",
            alpha=0.8,
            label="Population",
            zorder=6
        )

        # ----------------------------------------------------
        # PRACTICE MUTATION PREVIEW
        # ----------------------------------------------------

        if (
            S.game_mode == "Practice"
            and not S.game_finished
        ):

            mutations = generate_mutations()

            for i, mutation in enumerate(mutations):

                parent = mutation["parent"]
                child = mutation["position"]

                if child > TARGET_POSITION:

                    color = "#F87171"

                elif child == TARGET_POSITION:

                    color = "#4ADE80"

                else:

                    color = "#FBBF24"

                ax.annotate(
                    "",
                    xy=(
                        child,
                        fitness(child)
                    ),
                    xytext=(
                        parent,
                        fitness(parent)
                    ),
                    arrowprops={
                        "arrowstyle": "->",
                        "color": color,
                        "linestyle": "--",
                        "alpha": 0.65,
                        "connectionstyle": "arc3,rad=-0.12"
                    },
                    zorder=4
                )

                ax.scatter(
                    child,
                    fitness(child),
                    s=75,
                    facecolors="none",
                    edgecolors=color,
                    linewidths=1.6,
                    label=(
                        "Mutation Preview"
                        if i == 0
                        else None
                    ),
                    zorder=8
                )

        # ----------------------------------------------------
        # BEST / FINAL INDIVIDUAL
        # ----------------------------------------------------

        position = get_display_position()

        if S.mission_success:

            point_color = "#4ADE80"
            point_label = "EXACT HIT"

        elif S.mission_failed:

            point_color = "#F87171"

            point_label = (
                "OVERSHOOT"
                if position > TARGET_POSITION
                else "UNDERSHOOT"
            )

        else:

            point_color = "#22D3EE"
            point_label = "BEST"

        ax.scatter(
            position,
            fitness(position),
            s=110,
            color=point_color,
            edgecolors="#FFFFFF",
            linewidths=1.3,
            label=(
                "Final Position"
                if S.game_finished
                else "Best Individual"
            ),
            zorder=10
        )

        ax.vlines(
            position,
            20,
            fitness(position),
            colors=point_color,
            linestyles=":",
            alpha=0.6
        )

        ax.text(
            position,
            max(23, fitness(position) - 10),
            f"{point_label}: {position}",
            color=point_color,
            fontsize=9,
            fontweight="bold",
            ha="center"
        )

        # ----------------------------------------------------
        # FINAL OVERSHOOT MOVEMENT
        # ----------------------------------------------------

        if (
            S.failure_type == "OVERSHOOT"
            and S.trigger_parent is not None
        ):

            ax.annotate(
                "",
                xy=(
                    position,
                    fitness(position)
                ),
                xytext=(
                    S.trigger_parent,
                    fitness(S.trigger_parent)
                ),
                arrowprops={
                    "arrowstyle": "->",
                    "color": "#F87171",
                    "linewidth": 2,
                    "connectionstyle": "arc3,rad=-0.3"
                },
                zorder=9
            )

        ax.set_xlim(0, 100)
        ax.set_ylim(15, 125)

        ax.set_xticks(
            np.arange(0, 101, 10)
        )

        ax.set_xlabel(
            "POSITION (x)",
            color="#94A3B8",
            fontsize=10
        )

        ax.set_ylabel(
            "FITNESS",
            color="#94A3B8",
            fontsize=10
        )

        legend = ax.legend(
            loc="upper left",
            facecolor="#111827",
            edgecolor="#29384C",
            fontsize=8
        )

        for text in legend.get_texts():

            text.set_color("#CBD5E1")

        fig.subplots_adjust(
            left=0.055,
            right=0.98,
            top=0.94,
            bottom=0.16
        )

        image = figure_to_base64(fig)

    image_class = "fitness-image"

    if S.game_mode == "Practice":

        image_class += " practice-image"

    st.html(f"""
    <img
        class="{image_class}"
        src="data:image/png;base64,{image}"
        alt="Fitness landscape"
    >
    """)


# ============================================================
# 23. MUTATION PREVIEW PANEL
# ============================================================

def display_mutation_preview():

    if S.game_finished:

        return

    mutations = generate_mutations()

    if not mutations:

        return

    overshoots = [
        mutation
        for mutation in mutations
        if mutation["position"] > TARGET_POSITION
    ]

    exact_hits = [
        mutation
        for mutation in mutations
        if mutation["position"] == TARGET_POSITION
    ]

    candidates = ", ".join(
        str(mutation["position"])
        for mutation in mutations
    )

    if overshoots:

        color = "#F87171"

        title = "⚠ OVERSHOOT DETECTED"

        message = (
            "Reduce sigma or retry the mutation. "
            "Accepting this generation will fail the mission."
        )

    elif exact_hits:

        color = "#4ADE80"

        title = "✓ EXACT TARGET DETECTED"

        message = (
            "No offspring overshoots. "
            "Accept this generation to complete the mission."
        )

    else:

        color = "#FBBF24"

        title = "MUTATION PREVIEW"

        combined = S.population + [
            (
                mutation["position"],
                mutation["sigma"]
            )
            for mutation in mutations
        ]

        predicted_best = max(
            combined,
            key=lambda individual: float(
                fitness(individual[0])
            )
        )[0]

        message = (
            f"Predicted best survivor: {predicted_best}. "
            f"Target distance: "
            f"{abs(TARGET_POSITION - predicted_best)}."
        )

    st.html(f"""
    <div class="preview-box"
         style="border-left-color:{color}">

        <div class="preview-title"
             style="color:{color}">

            {escape(title)}

        </div>

        <div class="preview-value"
             style="color:{color}">

            Offspring: {escape(candidates)}

        </div>

        <div class="preview-text">

            {escape(message)}

        </div>

    </div>
    """)


# ============================================================
# 24. TARGET STATUS
# ============================================================

def display_target_status():

    status, color = get_target_status()

    distance = get_distance()

    st.html(f"""
    <div class="target-status">

        <span style="color:#94A3B8">
            TARGET: POSITION 79
        </span>

        <span style="color:{color}">
            {status}
        </span>

        <span style="color:#94A3B8">
            DISTANCE: {distance} UNIT(S)
        </span>

    </div>
    """)


# ============================================================
# 25. LIVE EVOLUTION FEEDBACK
# ============================================================

def display_feedback():

    if S.mission_success:

        color = "#4ADE80"

    elif S.mission_failed:

        color = "#F87171"

    else:

        color = "#FBBF24"

    st.html(f"""
    <div class="feedback-box"
         style="border-left-color:{color}">

        <div class="feedback-title"
             style="color:{color}">

            LIVE EVOLUTION FEEDBACK

        </div>

        <div class="feedback-text">

            {escape(S.feedback)}

        </div>

    </div>
    """)


# ============================================================
# 26. STRATEGIC HINT
# ============================================================

def display_strategic_hint():

    if S.game_finished:

        return

    position = get_best_position()

    phase, color, hint = get_phase(
        position
    )

    if S.game_mode == "Practice":

        if position < 45:

            recommendation = "Suggested σ: 15–30."

        elif position < 68:

            recommendation = "Suggested σ: 5–10."

        else:

            recommendation = "Suggested σ: 0.5–3."

        hint += " " + recommendation

    else:

        hint += (
            " Your selected strategy controls sigma "
            "automatically."
        )

    panel_card(
        f"STRATEGIC HINT · {phase}",
        hint,
        color
    )


# ============================================================
# 27. MISSION RESULT POP-UP
# ============================================================

def result_stat(label, value):

    return f"""
    <div class="result-stat">

        <div class="result-stat-label">
            {escape(str(label))}
        </div>

        <div class="result-stat-value">
            {escape(str(value))}
        </div>

    </div>
    """


@st.dialog(
    "Mission Result",
    width="large",
    dismissible=False
)
def mission_result_dialog():

    position = get_display_position()

    if S.mission_success:

        title = "MISSION COMPLETE"

        icon = "🏆"

        color = "#4ADE80"

        result_class = "result-success"

        description = (
            "Congratulations! You reached "
            "the exact Global Optimum."
        )

        reason_title = "GLOBAL OPTIMUM REACHED"

        reason = (
            f"Individual {S.trigger_individual} "
            f"landed exactly on position 79 "
            f"in generation {S.generation}. "
            "Your parameter control strategy "
            "successfully balanced exploration "
            "and precision."
        )

    else:

        title = "MISSION FAILED"

        icon = "✖"

        color = "#F87171"

        result_class = "result-failed"

        description = (
            "The population did not satisfy "
            "the mission objective."
        )

        if S.failure_type == "OVERSHOOT":

            reason_title = "OVERSHOOT"

            reason = (
                f"Individual {S.trigger_individual} "
                f"moved from {S.trigger_parent} "
                f"to {position}. "
                f"It exceeded the target by "
                f"{position - TARGET_POSITION} unit(s). "
                "Try a smaller mutation step size."
            )

        elif abs(position - LOCAL_OPTIMUM) <= 5:

            reason_title = "TRAPPED AT LOCAL OPTIMUM"

            reason = (
                "The population remained near "
                "the smaller mountain. "
                "Try stronger exploration or "
                "a different parameter control strategy."
            )

        else:

            reason_title = "UNDERSHOOT"

            reason = (
                f"All 30 turns have been consumed. "
                f"The final position is {position}, "
                f"which is {get_distance()} units "
                "away from the Global Optimum."
            )

    stats = "".join([

        result_stat(
            "GENERATION",
            f"{S.generation}/30"
        ),

        result_stat(
            "FINAL POSITION",
            position
        ),

        result_stat(
            "FINAL FITNESS",
            f"{fitness(position):.2f}"
        ),

        result_stat(
            "TARGET DISTANCE",
            get_distance()
        )
    ])

    strategy, _ = S.settings

    st.html(f"""
    <div class="result-container {result_class}">

        <div class="result-icon"
             style="color:{color}">
            {icon}
        </div>

        <div class="result-title"
             style="color:{color}">
            {title}
        </div>

        <div class="result-description">
            {escape(description)}
        </div>

        <div class="result-grid">
            {stats}
        </div>

        <div class="result-reason">

            <div class="panel-title"
                 style="color:{color}">

                {escape(reason_title)}

            </div>

            <div class="panel-text">

                {escape(reason)}

            </div>

        </div>

        <div class="small-text"
             style="margin-top:10px">

            {escape(S.game_mode)} Mode
            · {escape(strategy)} Control

        </div>

    </div>
    """)

    a, b, c = st.columns(3)

    with a:

        if st.button(
            "↻ PLAY AGAIN",
            key="result_play_again",
            type="primary",
            use_container_width=True
        ):

            reset_simulation()
            st.rerun()

    with b:

        if st.button(
            "VIEW DASHBOARD",
            key="result_close",
            use_container_width=True
        ):

            close_dialog()
            st.rerun()

    with c:

        if st.button(
            "🏠 MAIN MENU",
            key="result_home",
            use_container_width=True
        ):

            handle_home()
            st.rerun()


# ============================================================
# 28. PERFORMANCE ANALYSIS CHART
# ============================================================

def display_analysis_chart():

    dataframe = pd.DataFrame(
        S.history
    )

    with get_plot_lock():

        fig, axes = plt.subplots(
            1,
            3,
            figsize=(12, 3),
            facecolor="#080D1C"
        )

        charts = [

            (
                "Fitness",
                "#22D3EE",
                "Fitness Progress"
            ),

            (
                "Sigma",
                "#E879F9",
                "Mutation Step Size"
            ),

            (
                "Distance",
                "#FBBF24",
                "Target Distance"
            )
        ]

        for ax, (column, color, title) in zip(
            axes,
            charts
        ):

            style_axis(ax)

            ax.plot(
                dataframe["Generation"],
                dataframe[column],
                color=color,
                linewidth=2,
                marker="o",
                markersize=3
            )

            ax.set_title(
                title,
                color=color,
                fontsize=11,
                fontweight="bold"
            )

            ax.set_xlabel(
                "Generation",
                color="#94A3B8",
                fontsize=9
            )

            ax.set_xlim(
                0,
                max(1, S.generation)
            )

        fig.tight_layout(
            pad=1.8
        )

        image = figure_to_base64(fig)

    st.html(f"""
    <img
        class="analysis-image"
        src="data:image/png;base64,{image}"
        alt="Performance analysis"
    >
    """)


# ============================================================
# 29. PERFORMANCE ANALYSIS POP-UP
# ============================================================

@st.dialog(
    "Performance Analysis",
    width="large",
    dismissible=False
)
def performance_dialog():

    dataframe = pd.DataFrame(
        S.history
    )

    display_analysis_chart()

    section_heading(
        "GENERATION HISTORY"
    )

    page_size = 4

    total_pages = max(
        1,
        int(
            np.ceil(
                len(dataframe) / page_size
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

    start = S.history_page * page_size
    end = start + page_size

    page = dataframe.iloc[
        start:end
    ].copy()

    page["Fitness"] = page[
        "Fitness"
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
            key="history_previous",
            disabled=S.history_page == 0,
            use_container_width=True
        ):

            change_history_page(-1)
            st.rerun(scope="fragment")

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
            key="history_next",
            disabled=(
                S.history_page >= total_pages - 1
            ),
            use_container_width=True
        ):

            change_history_page(1)
            st.rerun(scope="fragment")

    if st.button(
        "CLOSE",
        key="close_performance",
        use_container_width=True
    ):

        close_dialog()
        st.rerun()


# ============================================================
# 30. POPULATION DETAILS POP-UP
# ============================================================

@st.dialog(
    "Population Details",
    width="large",
    dismissible=False
)
def population_dialog():

    section_heading(
        "CURRENT SURVIVING POPULATION"
    )

    population_data = []

    for i, (position, sigma) in enumerate(
        S.population
    ):

        population_data.append({

            "Individual": i + 1,

            "Position": position,

            "Fitness": (
                f"{fitness(position):.2f}"
            ),

            "Sigma": (
                f"{sigma:.2f}"
            ),

            "Distance": abs(
                TARGET_POSITION - position
            )
        })

    static_table(
        pd.DataFrame(population_data)
    )

    if (
        S.game_mode == "Practice"
        and not S.game_finished
    ):

        section_heading(
            "PROPOSED MUTATIONS"
        )

        mutations = generate_mutations()

    else:

        section_heading(
            "LAST GENERATION MUTATIONS"
        )

        mutations = S.last_mutations

    if mutations:

        mutation_data = []

        for mutation in mutations:

            mutation_data.append({

                "Individual": (
                    mutation["individual"]
                ),

                "Parent": mutation["parent"],

                "Offspring": (
                    mutation["position"]
                ),

                "Movement": (
                    mutation["movement"]
                ),

                "Sigma": (
                    f"{mutation['sigma']:.2f}"
                ),

                "Result": mutation["result"]
            })

        static_table(
            pd.DataFrame(mutation_data)
        )

    else:

        st.html("""
        <div class="small-text">
            No accepted mutations to display.
        </div>
        """)

    if st.button(
        "CLOSE",
        key="close_population",
        use_container_width=True
    ):

        close_dialog()
        st.rerun()


# ============================================================
# 31. LEARNING GUIDE CONTENT
# ============================================================

GUIDE_CONTENT = {

    "Manual Control": {

        "color": "#4ADE80",

        "description": (
            "Practice Mode allows you to manually "
            "adjust mutation step size before "
            "accepting a generation."
        ),

        "points": [

            "Large sigma encourages wider exploration.",

            "Small sigma allows more precise movement.",

            "Changing sigma does not consume a turn.",

            "Accept Mutation applies all five offspring.",

            "Retry Mutation rejects the proposal "
            "but consumes one turn."
        ],

        "example": (
            "If an offspring overshoots position 79, "
            "reduce sigma and inspect the new preview."
        )
    },

    "Deterministic Control": {

        "color": "#22D3EE",

        "description": (
            "The parameter follows a predefined "
            "schedule regardless of mutation performance."
        ),

        "points": [

            "Sigma starts at the selected initial value.",

            "Sigma decreases after every generation.",

            "The schedule does not use fitness feedback.",

            "Early generations encourage exploration.",

            "Later generations encourage refinement."
        ],

        "example": (
            "σ(t) = max(0.5, σ₀ × (1 − t/30))."
        )
    },

    "Adaptive Control": {

        "color": "#FBBF24",

        "description": (
            "The parameter changes using feedback "
            "from mutation performance."
        ),

        "points": [

            "Calculate the proportion of offspring "
            "that improve their parent's fitness.",

            "Success rate above 20%: multiply sigma by 1.25.",

            "Success rate below 20%: multiply sigma by 0.8.",

            "Success rate equal to 20%: maintain sigma.",

            "The adjustment is based on the 1/5 Success Rule."
        ],

        "example": (
            "Three successful mutations out of five "
            "give a 60% success rate. Sigma increases."
        )
    },

    "Self-Adaptive Control": {

        "color": "#E879F9",

        "description": (
            "Each individual carries its own "
            "mutation step size as part of its representation."
        ),

        "points": [

            "Every individual has a position and sigma.",

            "Sigma is mutated before position mutation.",

            "Different individuals may have different sigma.",

            "Fitness-based selection determines survivors.",

            "Successful individuals pass their sigma "
            "to subsequent generations."
        ],

        "example": (
            "σ′ = σ × exp(0.4 × N(0,1)). "
            "The new sigma controls position mutation."
        )
    },

    "Mission Rules": {

        "color": "#FBBF24",

        "description": (
            "The game uses an integer-position fitness "
            "landscape with a strict target at position 79."
        ),

        "points": [

            "The population starts at position 10.",

            "The local optimum is near position 27.",

            "Any offspring above position 79 "
            "causes immediate mission failure.",

            "An exact hit at position 79 wins "
            "if no offspring overshoots.",

            "Failure also occurs after 30 turns "
            "without reaching the target."
        ],

        "example": (
            "Position 78: continue. "
            "Position 79: win. "
            "Position 80: overshoot."
        )
    }
}


# ============================================================
# 32. LEARNING GUIDE POP-UP
# ============================================================

@st.dialog(
    "Learning Guide",
    width="large",
    dismissible=False
)
def learning_dialog():

    topic = st.selectbox(
        "Learning Topic",
        options=list(
            GUIDE_CONTENT.keys()
        ),
        key="guide_topic"
    )

    content = GUIDE_CONTENT[topic]

    points_html = "".join(

        f'<div class="guide-point">'
        f'{escape(point)}'
        f'</div>'

        for point in content["points"]
    )

    st.html(f"""
    <div class="guide-card">

        <div class="guide-title"
             style="color:{content['color']}">

            {escape(topic)}

        </div>

        <div class="panel-text"
             style="margin-bottom:10px">

            {escape(content['description'])}

        </div>

        {points_html}

        <div class="panel-card">

            <div class="panel-title"
                 style="color:#FBBF24">

                EXAMPLE

            </div>

            <div class="panel-text">

                {escape(content['example'])}

            </div>

        </div>

    </div>
    """)

    if st.button(
        "CLOSE",
        key="close_learning",
        use_container_width=True
    ):

        close_dialog()
        st.rerun()


# ============================================================
# 33. PRACTICE MODE CONTROL PANEL
# ============================================================

def display_practice_controls():

    section_heading(
        "01 / MANUAL PARAMETER CONTROL"
    )

    panel_card(
        "🎮 Practice Mode",
        STRATEGIES["Manual"]["description"],
        "#4ADE80"
    )

    section_heading(
        "02 / MUTATION STEP SIZE"
    )

    st.slider(
        "Mutation Step Size (σ)",
        min_value=0.5,
        max_value=30.0,
        step=0.5,
        key="manual_sigma",
        disabled=S.game_finished
    )

    st.html("""
    <div class="small-text">

        Small σ = precise movement.<br>
        Large σ = wider exploration.<br>
        Adjusting sigma does not reset the game.

    </div>
    """)

    section_heading(
        "03 / SIMULATION CONTROLS"
    )

    st.button(
        "✓ ACCEPT MUTATION",
        key="accept_mutation",
        type="primary",
        disabled=S.game_finished,
        use_container_width=True,
        on_click=next_generation
    )

    st.button(
        "↻ RETRY MUTATION",
        key="retry_mutation",
        disabled=S.game_finished,
        use_container_width=True,
        on_click=retry_mutation
    )

    st.button(
        "↺ RESET SIMULATION",
        key="practice_reset",
        use_container_width=True,
        on_click=handle_reset
    )

    display_strategic_hint()

    st.html("""
    <div class="panel-card">

        <div class="panel-title"
             style="color:#67E8F9">

            MISSION OBJECTIVE

        </div>

        <div class="small-text">

            Reach exactly
            <strong style="color:#FBBF24">
                POSITION 79
            </strong>
            within 30 turns.<br>

            <span style="color:#4ADE80">
                Exact hit = Mission Complete
            </span><br>

            <span style="color:#F87171">
                Overshoot = Immediate Failure
            </span>

        </div>

    </div>
    """)


# ============================================================
# 34. CHALLENGE MODE CONTROL PANEL
# ============================================================

def display_challenge_controls():

    section_heading(
        "01 / PARAMETER CONTROL"
    )

    strategy = st.radio(
        "Parameter Control",
        options=[
            "Deterministic",
            "Adaptive",
            "Self-Adaptive"
        ],
        key="selected_strategy",
        label_visibility="collapsed",
        on_change=handle_settings_change
    )

    strategy_info = STRATEGIES[strategy]

    panel_card(
        f"{strategy} Control",
        strategy_info["description"],
        strategy_info["color"]
    )

    section_heading(
        "02 / INITIAL STEP SIZE"
    )

    st.slider(
        "Mutation Step Size (σ)",
        min_value=1,
        max_value=30,
        step=1,
        key="initial_sigma",
        on_change=handle_settings_change
    )

    st.html("""
    <div class="small-text">

        Small σ = finer movements.<br>
        Large σ = wider exploration and overshoot risk.<br>
        Changing settings resets the mission.

    </div>
    """)

    section_heading(
        "03 / SIMULATION CONTROLS"
    )

    st.button(
        "▶ NEXT GENERATION",
        key="next_generation",
        type="primary",
        disabled=S.game_finished,
        use_container_width=True,
        on_click=next_generation
    )

    st.button(
        "⏩ RUN ALL GENERATIONS",
        key="run_all",
        disabled=S.game_finished,
        use_container_width=True,
        on_click=handle_run_all
    )

    st.button(
        "↺ RESET SIMULATION",
        key="challenge_reset",
        use_container_width=True,
        on_click=handle_reset
    )

    st.html("""
    <div class="panel-card">

        <div class="panel-title"
             style="color:#67E8F9">

            MISSION OBJECTIVE

        </div>

        <div class="small-text">

            Reach exactly
            <strong style="color:#FBBF24">
                POSITION 79
            </strong>
            within 30 generations.<br>

            <span style="color:#4ADE80">
                Exact hit = Mission Complete
            </span><br>

            <span style="color:#F87171">
                Overshoot = Immediate Failure
            </span><br>

            Reset repeats the same random challenge.

        </div>

    </div>
    """)


# ============================================================
# 35. MAIN DASHBOARD
# ============================================================

def display_dashboard():

    display_header()

    with st.container(
        key="main_dashboard"
    ):

        left, right = st.columns(
            [1, 3.05],
            gap="medium"
        )

        # ----------------------------------------------------
        # LEFT CONTROL PANEL
        # ----------------------------------------------------

        with left:

            with st.container(
                key="left_panel"
            ):

                if S.game_mode == "Practice":

                    display_practice_controls()

                else:

                    display_challenge_controls()

        # ----------------------------------------------------
        # RIGHT VISUALIZATION PANEL
        # ----------------------------------------------------

        with right:

            with st.container(
                key="right_panel"
            ):

                display_metrics()

                display_phase_indicator()

                section_heading(
                    "FITNESS LANDSCAPE"
                )

                display_fitness_landscape()

                display_target_status()

                if (
                    S.game_mode == "Practice"
                    and not S.game_finished
                ):

                    display_mutation_preview()

                display_feedback()

                if S.game_finished:

                    st.button(
                        "VIEW MISSION RESULT",
                        key="view_mission_result",
                        use_container_width=True,
                        on_click=open_dialog,
                        args=("result",)
                    )

    # --------------------------------------------------------
    # BOTTOM NAVIGATION
    # --------------------------------------------------------

    with st.container(
        key="bottom_navigation"
    ):

        a, b, c, d = st.columns(4)

        with a:

            st.button(
                "📊 Performance Analysis",
                key="performance_button",
                use_container_width=True,
                on_click=open_dialog,
                args=("performance",)
            )

        with b:

            st.button(
                "🧬 Population Details",
                key="population_button",
                use_container_width=True,
                on_click=open_dialog,
                args=("population",)
            )

        with c:

            st.button(
                "📖 Learning Guide",
                key="learning_button",
                use_container_width=True,
                on_click=open_dialog,
                args=("learning",)
            )

        with d:

            st.button(
                "🏠 Main Menu",
                key="main_menu_button",
                use_container_width=True,
                on_click=handle_home
            )


# ============================================================
# 36. APPLICATION ROUTING
# ============================================================

if not S.game_started:

    display_welcome_screen()

else:

    # Restore widget state when switching modes.
    # Streamlit may remove widget keys when hidden.

    if "selected_strategy" not in S:

        S.selected_strategy = (
            S.settings[0]
            if S.settings[0] != "Manual"
            else "Deterministic"
        )

    if "initial_sigma" not in S:

        S.initial_sigma = (
            int(S.settings[1])
            if S.settings[0] != "Manual"
            else 15
        )

    if "manual_sigma" not in S:

        S.manual_sigma = (
            float(S.sigma)
            if S.game_mode == "Practice"
            else 20.0
        )

    display_dashboard()

    active_dialog = S.active_dialog

    if active_dialog == "result":

        mission_result_dialog()

    elif active_dialog == "performance":

        performance_dialog()

    elif active_dialog == "population":

        population_dialog()

    elif active_dialog == "learning":

        learning_dialog()

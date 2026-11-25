
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


# ============================================================
# 03. GLOBAL CSS
# ============================================================

CSS = """
<style>

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

/* GLOBAL BACKGROUND */

.stApp {
    background-color: #080D1C;

    background-image:
        linear-gradient(
            rgba(5, 10, 25, 0.87),
            rgba(5, 10, 25, 0.87)
        ),
        url("data:image/jpeg;base64,__BACKGROUND__");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    color: #E2E8F0;
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
}

.block-container {
    max-width: 1800px;
    width: 100%;
    padding: 1rem 2rem 0.6rem !important;
    box-sizing: border-box;
}

.block-container > [data-testid="stVerticalBlock"] {
    gap: 0.55rem !important;
}

[data-testid="stColumn"] {
    min-width: 0;
}

[data-testid="stWidgetLabel"] p {
    color: #E2E8F0;
}


/* APPLICATION HEADER */

.hero {
    text-align: center;
    padding: 0 0 8px;
}

.hero-label {
    color: #22D3EE;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 5px;
    margin-bottom: 5px;
}

.hero-title {
    color: #E0F2FE;
    font-size: clamp(25px, 3vw, 34px);
    font-weight: 900;
    letter-spacing: 5px;
    line-height: 1.2;
    margin-bottom: 6px;
    text-shadow: 0 0 22px #0891B2;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 10px;
    letter-spacing: 3px;
}


/* WELCOME SCREEN */

.st-key-welcome_screen {
    width: 100%;
    max-width: 720px;

    margin: 0 auto !important;
    padding: 18px 26px !important;

    background: rgba(8, 13, 28, 0.96);

    border: 1px solid #164E63;
    border-radius: 18px;

    box-shadow:
        0 0 45px rgba(34, 211, 238, 0.10);

    box-sizing: border-box;
}

.st-key-welcome_screen
[data-testid="stVerticalBlock"] {
    gap: 0.4rem !important;
}

.welcome-label {
    color: #22D3EE;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 4px;
    text-align: center;
    margin-bottom: 8px;
}

.welcome-title {
    color: #E0F2FE;
    font-size: clamp(27px, 4vw, 38px);
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
    margin: 8px 0;
}

.welcome-mountain {
    display: block;
    width: 100%;
    max-width: 410px;
    max-height: 130px;
    object-fit: contain;
    margin: 0 auto;
}

.welcome-mission {
    color: #FBBF24;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 2px;
    text-align: center;
    margin: 4px 0 6px;
}

.welcome-mission-text {
    color: #CBD5E1;
    font-size: 13px;
    line-height: 1.5;
    text-align: center;
    margin-bottom: 12px;
}

.instructions-heading {
    color: #67E8F9;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-align: center;
    margin-bottom: 8px;
}

.instruction-row {
    display: flex;
    align-items: center;
    gap: 12px;

    padding: 8px 12px;
    margin-bottom: 6px;

    border: 1px solid #29384C;
    border-radius: 9px;

    background: rgba(17, 24, 39, 0.90);
}

.instruction-number {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 35px;
    height: 35px;
    flex-shrink: 0;

    border: 1px solid #155E75;
    border-radius: 8px;

    background: rgba(34, 211, 238, 0.08);

    color: #22D3EE;
    font-size: 15px;
    font-weight: 800;
}

.instruction-content {
    flex: 1;
    min-width: 0;
}

.instruction-title {
    color: #E2E8F0;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 2px;
}

.instruction-text {
    color: #94A3B8;
    font-size: 12px;
    line-height: 1.4;
}

.st-key-start_game_button button {
    min-height: 43px !important;

    font-size: 15px !important;
    font-weight: 800 !important;
    letter-spacing: 2px;

    background: linear-gradient(
        90deg,
        #155E75,
        #0E7490
    ) !important;

    border: 1px solid #22D3EE !important;
    color: #FFFFFF !important;

    box-shadow:
        0 0 20px rgba(34, 211, 238, 0.16);
}


/* MAIN DASHBOARD */

.st-key-main_dashboard {
    width: 100%;
    min-width: 0;
}

.st-key-left_panel
[data-testid="stVerticalBlock"] {
    gap: 0.4rem !important;
}

.st-key-right_panel
[data-testid="stVerticalBlock"] {
    gap: 0.5rem !important;
}

.section-heading {
    color: #67E8F9;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 3px;
}


/* RADIO BUTTONS */

.st-key-left_panel [role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 2px;

    padding: 6px 10px;

    border: 1px solid #29384C;
    border-radius: 9px;

    background: rgba(17, 24, 39, 0.85);
}

.st-key-left_panel [role="radiogroup"] label {
    margin: 0;
    padding: 1px 0;
}

.st-key-left_panel [role="radiogroup"] p {
    color: #E2E8F0;
    font-size: 13px;
}


/* STRATEGY DESCRIPTION */

.strategy-description {
    background: rgba(17, 24, 39, 0.94);
    border: 1px solid #29384C;
    border-radius: 8px;
    padding: 8px 10px;
}

.strategy-description-title {
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 3px;
}

.strategy-description-text {
    color: #CBD5E1;
    font-size: 12px;
    line-height: 1.45;
}


/* SLIDER */

.st-key-left_panel
[data-testid="stSlider"] {
    padding: 0 !important;
    margin: 0 !important;
}

.slider-help {
    color: #94A3B8;
    font-size: 11px;
    line-height: 1.4;
}


/* BUTTONS */

.stButton > button {
    width: 100%;
    min-height: 35px;

    padding: 6px 10px;

    background: rgba(17, 24, 39, 0.96);

    border: 1px solid #29384C;
    border-radius: 8px;

    color: #67E8F9;
    font-weight: 600;
}

.stButton > button p {
    font-size: 13px;
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
    opacity: 0.45;
    cursor: not-allowed;
}


/* MISSION CARD */

.mission-card {
    background: rgba(17, 24, 39, 0.78);
    border: 1px solid #29384C;
    border-radius: 8px;
    padding: 8px 10px;
}

.mission-title {
    color: #67E8F9;
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


/* METRIC CARDS */

.metric-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 9px;
    width: 100%;
}

.metric-card {
    display: flex;
    flex-direction: column;
    justify-content: center;

    background: rgba(17, 24, 39, 0.95);

    border: 1px solid #29384C;
    border-radius: 10px;

    padding: 10px 12px;

    min-width: 0;
    min-height: 65px;
}

.metric-label {
    color: #94A3B8;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.6px;
    margin-bottom: 5px;
}

.metric-value {
    font-size: clamp(18px, 1.7vw, 25px);
    font-weight: 800;
    line-height: 1.2;
    overflow-wrap: anywhere;
}


/* GENERATION PROGRESS */

.progress-track {
    width: 100%;
    height: 5px;

    background: #1E293B;
    border-radius: 20px;
    overflow: hidden;

    margin-top: 8px;
}

.progress-fill {
    height: 100%;
    border-radius: 20px;
    transition: width 0.3s ease;
}


/* FITNESS LANDSCAPE */

.fitness-image {
    display: block;
    width: 100%;
    max-width: 100%;
    max-height: 39dvh;

    height: auto;
    object-fit: contain;

    background: #0B1120;
    border: 1px solid #29384C;
    border-radius: 10px;
}


/* TARGET STATUS */

.target-status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;

    gap: 10px;
    padding: 8px 12px;

    border: 1px solid #29384C;
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


/* LIVE FEEDBACK */

.feedback-box {
    background: rgba(17, 24, 39, 0.96);

    border: 1px solid #29384C;
    border-left: 4px solid #FBBF24;
    border-radius: 9px;

    padding: 9px 12px;
}

.feedback-title {
    color: #FBBF24;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 5px;
}

.feedback-text {
    color: #E2E8F0;
    font-size: 12px;
    line-height: 1.5;
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


/* BOTTOM NAVIGATION */

.st-key-bottom_navigation {
    width: 100%;
    border-top: 1px solid #29384C;
    padding-top: 8px;
    margin-top: 3px;
}


/* DIALOG WINDOWS */

[data-testid="stDialog"] [role="dialog"] {
    background: #0B1120 !important;
    color: #E2E8F0;

    max-height: 90dvh;
    overflow-y: auto !important;

    border: 1px solid #29384C;
    border-radius: 16px;
}


/* MISSION RESULT POP-UP */

.result-container {
    width: 100%;
    text-align: center;
    padding: 24px 16px;
    border-radius: 15px;
    box-sizing: border-box;
}

.result-success {
    border: 1px solid #22C55E;

    background:
        radial-gradient(
            ellipse at top,
            rgba(34, 197, 94, 0.15),
            transparent 70%
        ),
        #080D1C;

    box-shadow:
        0 0 35px rgba(34, 197, 94, 0.15);
}

.result-failed {
    border: 1px solid #EF4444;

    background:
        radial-gradient(
            ellipse at top,
            rgba(239, 68, 68, 0.15),
            transparent 70%
        ),
        #080D1C;

    box-shadow:
        0 0 35px rgba(239, 68, 68, 0.15);
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
    font-size: clamp(27px, 4vw, 42px);
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
    margin-bottom: 20px;
}

.result-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
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
    margin-bottom: 7px;
}

.result-stat-value {
    color: #E2E8F0;
    font-size: 25px;
    font-weight: 800;
}

.result-strategy {
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 8px;
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


/* RESPONSIVE DESKTOP */

@media (min-width: 1200px) and (max-height: 820px) {

    .block-container {
        padding: 0.6rem 1.5rem !important;
    }

    .hero-title {
        font-size: 30px;
    }

    .metric-card {
        min-height: 58px;
        padding: 8px 10px;
    }

    .fitness-image {
        max-height: 35dvh;
    }

    .st-key-welcome_screen {
        padding: 14px 22px !important;
    }

    .welcome-mountain {
        max-height: 105px;
    }

    .st-key-left_panel
    [data-testid="stVerticalBlock"] {
        gap: 0.25rem !important;
    }

    .stButton > button {
        min-height: 32px;
    }
}


/* SMALL SCREENS */

@media (max-width: 1199px) {

    .block-container {
        padding: 1rem !important;
    }

    .metric-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .fitness-image {
        max-height: none;
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
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .st-key-welcome_screen {
        padding: 14px !important;
    }

    .welcome-title {
        font-size: 26px;
        letter-spacing: 2px;
    }

    .result-title {
        font-size: 26px;
        letter-spacing: 1px;
    }

    .result-stat-value {
        font-size: 19px;
    }
}

</style>
"""

st.html(
    CSS.replace("__BACKGROUND__", background)
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

SIMULATION_VERSION = "exact_peak_fixed_v2"


STRATEGIES = {

    "Deterministic": {
        "icon": "⏱️",
        "color": "#22D3EE",
        "description": (
            "Step size decreases according to "
            "a predefined generation schedule."
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
        "color": "#E879F9",
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

DEFAULT_STATE = {
    "game_started": False,
    "selected_strategy": "Deterministic",
    "initial_sigma": 15,
    "active_dialog": None
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# 07. RESET SIMULATION
# ============================================================

def reset_simulation(
    strategy=None,
    initial_sigma=None
):

    if strategy is None:
        strategy = st.session_state.selected_strategy

    if initial_sigma is None:
        initial_sigma = st.session_state.initial_sigma

    initial_sigma = float(initial_sigma)

    st.session_state.generation = 0

    st.session_state.population = [
        (INITIAL_POSITION, initial_sigma)
        for _ in range(POPULATION_SIZE)
    ]

    st.session_state.sigma = initial_sigma

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

    st.session_state.last_mutations = []

    st.session_state.mission_success = False
    st.session_state.mission_failed = False
    st.session_state.game_finished = False

    st.session_state.success_generation = None
    st.session_state.result_shown = False
    st.session_state.active_dialog = None

    st.session_state.feedback = (
        "Your population starts at position 10. "
        "Reach exactly position 79 within 30 generations. "
        "Press Next Generation to begin."
    )

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

    if any(
        key not in st.session_state
        for key in required_keys
    ):
        reset_simulation()
        return

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

    history_keys = [
        "history",
        "sigma_history",
        "position_history",
        "distance_history",
        "success_history"
    ]

    if any(
        len(st.session_state[key]) != generation + 1
        for key in history_keys
    ):
        reset_simulation()
        return

    if any(
        not float(x).is_integer()
        or not MIN_POSITION <= x <= MAX_POSITION
        for x, _ in st.session_state.population
    ):
        reset_simulation()


initialize_simulation()


# ============================================================
# 09. MISSION STATUS HELPERS
# ============================================================

def get_best_individual():

    return st.session_state.population[0]


def get_best_position():

    return int(get_best_individual()[0])


def get_distance_from_target():

    return abs(
        TARGET_POSITION - get_best_position()
    )


def get_target_status(position):

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

    return (
        "OVERSHOT TARGET POSITION",
        "#F87171"
    )


def get_failure_reason(position):

    if abs(position - LOCAL_OPTIMUM) <= 5:

        return (
            "Trapped near the Local Optimum",

            "The population remained near the smaller "
            "mountain. Try a larger initial step size "
            "or another strategy to encourage exploration."
        )

    elif position < TARGET_POSITION:

        return (
            "Undershot the Target",

            f"The best individual stopped at position "
            f"{position}, which is "
            f"{TARGET_POSITION - position} unit(s) "
            "before the exact Global Optimum."
        )

    elif position > TARGET_POSITION:

        return (
            "Overshot the Target",

            f"The best individual stopped at position "
            f"{position}, which is "
            f"{position - TARGET_POSITION} unit(s) "
            "beyond the exact Global Optimum."
        )

    return (
        "Target Not Reached",
        "Try another strategy or initial step size."
    )


# ============================================================
# 10. EVOLUTION PROCESS
# ============================================================

def next_generation():

    if st.session_state.game_finished:
        return

    if st.session_state.generation >= MAX_GENERATIONS:
        return

    strategy, initial_sigma = (
        st.session_state.settings
    )

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

        individual_sigma = float(
            individual_sigma
        )

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

        else:

            child_sigma = sigma

        mutation = np.random.normal(
            0,
            child_sigma
        )

        # Integer positions allow the population
        # to reach exactly position 79.

        child_x = int(
            np.clip(
                np.rint(x + mutation),
                MIN_POSITION,
                MAX_POSITION
            )
        )

        offspring.append(
            (child_x, child_sigma)
        )

        parent_fitness = float(
            fitness(x)
        )

        child_fitness = float(
            fitness(child_x)
        )

        improved = (
            child_fitness > parent_fitness
        )

        if improved:
            successes += 1

        mutation_details.append({

            "Individual": i + 1,

            "Parent Position": x,

            "Offspring Position": child_x,

            "Movement": child_x - x,

            "Step Size Used": round(
                child_sigma, 2
            ),

            "Parent Fitness": round(
                parent_fitness, 2
            ),

            "Offspring Fitness": round(
                child_fitness, 2
            ),

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

    combined.sort(
        key=lambda individual: float(
            fitness(individual[0])
        ),
        reverse=True
    )

    new_population = combined[:POPULATION_SIZE]

    generation = (
        st.session_state.generation + 1
    )

    success_rate = (
        successes / POPULATION_SIZE
    )


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

        action = (
            "decreased"
            if new_sigma < sigma
            else "remained at the minimum"
        )

        feedback = (
            f"Generation {generation}: "
            f"Step size {action} "
            f"({sigma:.2f} → {new_sigma:.2f}) "
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
                else "remained at the maximum"
            )

        elif success_rate < 0.2:

            new_sigma = max(
                MIN_SIGMA,
                sigma * 0.8
            )

            action = (
                "decreased"
                if new_sigma < sigma
                else "remained at the minimum"
            )

        else:

            new_sigma = sigma
            action = "remained unchanged"

        feedback = (
            f"Generation {generation}: "
            f"{successes}/{POPULATION_SIZE} mutations "
            f"improved fitness ({success_rate:.0%}). "
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
            f"The best surviving individual's step size "
            f"is {new_sigma:.2f}."
        )


    # --------------------------------------------------------
    # SYNCHRONIZE SHARED STEP SIZE
    # --------------------------------------------------------

    if strategy != "Self-Adaptive":

        new_population = [
            (int(x), float(new_sigma))
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

    # Position 78 = Not successful
    # Position 79 = Mission Complete
    # Position 80 = Not successful

    mission_success = (
        best_x == TARGET_POSITION
    )

    mission_failed = (
        generation >= MAX_GENERATIONS
        and not mission_success
    )

    game_finished = (
        mission_success or mission_failed
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

    if mission_success:

        feedback += (
            " Exact Global Optimum reached!"
        )

    elif mission_failed:

        feedback += (
            " Maximum generations reached "
            "without reaching the exact target."
        )


    # --------------------------------------------------------
    # UPDATE SIMULATION STATE
    # --------------------------------------------------------

    st.session_state.population = new_population
    st.session_state.generation = generation
    st.session_state.sigma = float(new_sigma)

    st.session_state.feedback = feedback

    st.session_state.last_mutations = (
        mutation_details
    )

    st.session_state.mission_success = (
        mission_success
    )

    st.session_state.mission_failed = (
        mission_failed
    )

    st.session_state.game_finished = (
        game_finished
    )

    st.session_state.success_generation = (
        success_generation
    )


    # --------------------------------------------------------
    # UPDATE HISTORIES
    # --------------------------------------------------------

    st.session_state.history.append(
        best_fitness
    )

    st.session_state.sigma_history.append(
        float(new_sigma)
    )

    st.session_state.position_history.append(
        best_x
    )

    st.session_state.distance_history.append(
        distance
    )

    st.session_state.success_history.append(
        float(success_rate)
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

    st.html(
        f'<div class="section-heading">'
        f'{escape(text)}'
        f'</div>'
    )


def metric_html(label, value, color):

    return f"""
    <div class="metric-card">
        <div class="metric-label">
            {escape(str(label))}
        </div>
        <div class="metric-value"
             style="color:{color};">
            {escape(str(value))}
        </div>
    </div>
    """


def result_metric_html(
    label,
    value,
    color="#E2E8F0"
):

    return f"""
    <div class="result-stat">
        <div class="result-stat-label">
            {escape(str(label))}
        </div>
        <div class="result-stat-value"
             style="color:{color};">
            {escape(str(value))}
        </div>
    </div>
    """


# ============================================================
# 13. MATPLOTLIB THREAD LOCK
# ============================================================

@st.cache_resource
def get_plot_lock():

    return RLock()


# ============================================================
# 14. WELCOME MOUNTAIN IMAGE
# ============================================================

# PNG image instead of inline SVG.
# Prevents SVG source code from appearing
# on the Welcome Screen.

@st.cache_data
def create_welcome_mountain():

    buffer = BytesIO()

    with get_plot_lock():

        fig, ax = plt.subplots(
            figsize=(6.5, 1.8),
            dpi=150
        )

        try:

            fig.patch.set_facecolor(
                "#080D1C"
            )

            ax.set_facecolor(
                "#080D1C"
            )

            x = np.linspace(
                0, 100, 1001
            )

            y = fitness(x)

            ax.fill_between(
                x,
                20,
                y,
                color="#22D3EE",
                alpha=0.10
            )

            for width, alpha in [
                (9, 0.04),
                (6, 0.07),
                (3, 0.15)
            ]:

                ax.plot(
                    x,
                    y,
                    color="#22D3EE",
                    linewidth=width,
                    alpha=alpha
                )

            ax.plot(
                x,
                y,
                color="#22D3EE",
                linewidth=2
            )

            local_y = float(
                fitness(LOCAL_OPTIMUM)
            )

            global_y = float(
                fitness(GLOBAL_OPTIMUM)
            )

            ax.scatter(
                LOCAL_OPTIMUM,
                local_y,
                color="#94A3B8",
                s=25,
                zorder=5
            )

            ax.scatter(
                GLOBAL_OPTIMUM,
                global_y,
                color="#FBBF24",
                s=180,
                alpha=0.12,
                zorder=5
            )

            ax.scatter(
                GLOBAL_OPTIMUM,
                global_y,
                color="#FBBF24",
                s=40,
                zorder=6
            )

            ax.text(
                LOCAL_OPTIMUM,
                local_y + 9,
                "LOCAL OPTIMUM",
                color="#94A3B8",
                fontsize=8,
                ha="center",
                fontweight="bold"
            )

            ax.text(
                GLOBAL_OPTIMUM,
                global_y + 9,
                "GLOBAL OPTIMUM",
                color="#FBBF24",
                fontsize=8,
                ha="center",
                fontweight="bold"
            )

            ax.text(
                GLOBAL_OPTIMUM,
                global_y - 17,
                "79",
                color="#FBBF24",
                fontsize=10,
                ha="center",
                fontweight="bold"
            )

            ax.set_xlim(0, 100)
            ax.set_ylim(20, 120)

            ax.axis("off")

            fig.subplots_adjust(
                left=0.02,
                right=0.98,
                top=0.98,
                bottom=0.02
            )

            fig.savefig(
                buffer,
                format="png",
                facecolor=fig.get_facecolor()
            )

        finally:

            plt.close(fig)

    encoded_image = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    buffer.close()

    return encoded_image


# ============================================================
# 15. WELCOME SCREEN
# ============================================================

def display_welcome_screen():

    mountain_image = (
        create_welcome_mountain()
    )

    with st.container(
        key="welcome_screen"
    ):

        st.html(f"""
        <div class="welcome-label">
            EVOLUTIONARY COMPUTATION
        </div>

        <div class="welcome-title">
            FITNESS MOUNTAIN
        </div>

        <div class="welcome-subtitle">
            THE PARAMETER CONTROL CHALLENGE
        </div>

        <img
            class="welcome-mountain"
            src="data:image/png;base64,{mountain_image}"
            alt="Fitness landscape with two mountain peaks"
        />

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
                    Press Next Generation or Run All.
                    Reach exactly position 79 to win.
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
# 16. APPLICATION HEADER
# ============================================================

def display_header():

    st.html("""
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
    """)


# ============================================================
# 17. DISPLAY STATISTIC CARDS
# ============================================================

def display_metrics(strategy):

    generation = (
        st.session_state.generation
    )

    best_x = get_best_position()

    best_fitness = float(
        fitness(best_x)
    )

    distance = (
        get_distance_from_target()
    )

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
            best_x,
            position_color
        ),

        metric_html(
            "DISTANCE TO TARGET",
            distance,
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

    cards_html = "".join(cards)

    st.html(f"""
    <div class="metric-grid">
        {cards_html}
    </div>

    <div class="progress-track">

        <div
            class="progress-fill"
            style="
                width:{progress:.2f}%;
                background:{progress_color};
            ">
        </div>

    </div>
    """)


# ============================================================
# 18. FITNESS LANDSCAPE GRAPH
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

    y_values = fitness(
        x_values
    )

    buffer = BytesIO()

    with get_plot_lock():

        fig, ax = plt.subplots(
            figsize=(12, 3.3),
            dpi=130
        )

        try:

            fig.patch.set_facecolor(
                "#0B1120"
            )

            ax.set_facecolor(
                "#0B1120"
            )


            # MOUNTAIN AREA

            ax.fill_between(
                x_values,
                20,
                y_values,
                color="#22D3EE",
                alpha=0.12
            )


            # NEON GLOW

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


            # EXACT TARGET LINE

            ax.axvline(
                TARGET_POSITION,
                color="#FBBF24",
                linestyle="--",
                linewidth=1.2,
                alpha=0.7
            )


            # LOCAL OPTIMUM

            local_y = float(
                fitness(LOCAL_OPTIMUM)
            )

            ax.scatter(
                LOCAL_OPTIMUM,
                local_y,
                color="#94A3B8",
                s=55,
                zorder=5
            )

            ax.annotate(
                "LOCAL OPTIMUM\nPosition 27",
                xy=(LOCAL_OPTIMUM, local_y),
                xytext=(LOCAL_OPTIMUM, local_y + 12),
                color="#94A3B8",
                fontsize=8,
                ha="center",
                fontweight="bold"
            )


            # GLOBAL OPTIMUM

            global_y = float(
                fitness(GLOBAL_OPTIMUM)
            )

            ax.scatter(
                GLOBAL_OPTIMUM,
                global_y,
                color="#FBBF24",
                marker="*",
                s=230,
                alpha=0.9,
                zorder=7
            )

            ax.annotate(
                "GLOBAL OPTIMUM\nPosition 79",
                xy=(GLOBAL_OPTIMUM, global_y),
                xytext=(GLOBAL_OPTIMUM, 113),
                color="#FBBF24",
                fontsize=9,
                ha="center",
                fontweight="bold"
            )


            # CURRENT POPULATION

            for index, (x, sigma) in enumerate(
                st.session_state.population
            ):

                if index == 0:
                    continue

                ax.scatter(
                    x,
                    float(fitness(x)),
                    color=accent,
                    s=50,
                    alpha=0.55,
                    edgecolors="#E2E8F0",
                    linewidths=0.5,
                    zorder=8,

                    label=(
                        "Population"
                        if index == 1
                        else None
                    )
                )


            # BEST INDIVIDUAL

            best_color = (
                "#4ADE80"
                if best_x == TARGET_POSITION
                else accent
            )

            ax.scatter(
                best_x,
                best_fitness,
                s=250,
                color=best_color,
                alpha=0.13,
                zorder=9
            )

            ax.scatter(
                best_x,
                best_fitness,
                s=90,
                color=best_color,
                edgecolors="#FFFFFF",
                linewidths=1.2,
                zorder=10,
                label="Best Individual"
            )

            ax.annotate(
                f"BEST: {best_x}",
                xy=(best_x, best_fitness),
                xytext=(0, -20),
                textcoords="offset points",
                color=best_color,
                fontsize=8,
                fontweight="bold",
                ha="center",
                zorder=11
            )


            # STARTING POSITION

            ax.axvline(
                INITIAL_POSITION,
                color="#64748B",
                linestyle=":",
                linewidth=1,
                alpha=0.5
            )


            # GRAPH FORMATTING

            ax.set_xlim(
                MIN_POSITION,
                MAX_POSITION
            )

            ax.set_ylim(15, 125)

            ax.set_xticks(
                np.arange(0, 101, 10)
            )

            ax.set_yticks(
                [20, 40, 60, 80, 100, 120]
            )

            ax.set_xlabel(
                "POSITION (x)",
                color="#94A3B8",
                fontsize=9
            )

            ax.set_ylabel(
                "FITNESS",
                color="#94A3B8",
                fontsize=9
            )

            ax.tick_params(
                colors="#94A3B8",
                labelsize=8
            )

            ax.grid(
                color="#334155",
                alpha=0.25,
                linestyle="--"
            )

            for spine in ax.spines.values():

                spine.set_color(
                    "#29384C"
                )

            legend = ax.legend(
                loc="upper left",
                fontsize=8,
                facecolor="#111827",
                edgecolor="#29384C"
            )

            for text in legend.get_texts():

                text.set_color(
                    "#CBD5E1"
                )

            fig.tight_layout(
                pad=1.1
            )

            fig.savefig(
                buffer,
                format="png",
                facecolor=fig.get_facecolor()
            )

        finally:

            plt.close(fig)


    # Encode PNG directly.
    # Avoids inline SVG and temporary image URLs.

    encoded_image = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    buffer.close()

    st.html(f"""
    <img
        class="fitness-image"
        src="data:image/png;base64,{encoded_image}"
        alt="Current population on the fitness landscape"
    />
    """)


# ============================================================
# 19. TARGET STATUS
# ============================================================

def display_target_status():

    best_x = get_best_position()

    distance = (
        get_distance_from_target()
    )

    status, color = (
        get_target_status(best_x)
    )

    st.html(f"""
    <div class="target-status">

        <span class="target-status-label">
            TARGET: POSITION 79
        </span>

        <span
            class="target-status-value"
            style="color:{color};">

            {status}

        </span>

        <span class="target-status-label">
            DISTANCE: {distance} UNIT(S)
        </span>

    </div>
    """)


# ============================================================
# 20. LIVE EVOLUTION FEEDBACK
# ============================================================

def display_feedback():

    css_class = "feedback-box"

    title = "LIVE EVOLUTION FEEDBACK"

    if st.session_state.mission_success:

        css_class += " feedback-success"
        title = "MISSION COMPLETE"

    elif st.session_state.mission_failed:

        css_class += " feedback-failed"
        title = "MISSION FAILED"

    feedback = escape(
        st.session_state.feedback
    )

    st.html(f"""
    <div class="{css_class}">

        <div class="feedback-title">
            {title}
        </div>

        <div class="feedback-text">
            {feedback}
        </div>

    </div>
    """)


# ============================================================
# 21. POP-UP: MISSION RESULT
# ============================================================

@st.dialog(
    "Mission Result",
    width="large",
    dismissible=False
)
def mission_result_dialog():

    success = (
        st.session_state.mission_success
    )

    generation = (
        st.session_state.generation
    )

    strategy = (
        st.session_state.settings[0]
    )

    best_x = get_best_position()

    best_fitness = float(
        fitness(best_x)
    )

    distance = (
        get_distance_from_target()
    )

    accent = STRATEGIES[strategy]["color"]

    if success:

        css_class = "result-success"

        icon = "🏆"

        title = "MISSION COMPLETE"

        description = (
            "Congratulations! Your population "
            "successfully reached the exact Global Optimum "
            f"at position 79 in {generation} generation(s)."
        )

        reason_title = "WHY YOU SUCCEEDED"

        reason_text = (
            "Your parameter control strategy and mutation "
            "process produced an individual at exactly "
            "position 79. The distance from the target "
            "is zero."
        )

        result_color = "#4ADE80"

    else:

        css_class = "result-failed"

        icon = "✖"

        title = "MISSION FAILED"

        description = (
            "The maximum number of generations "
            "has been reached without landing "
            "on the exact Global Optimum."
        )

        reason_title, reason_text = (
            get_failure_reason(best_x)
        )

        result_color = "#F87171"


    result_cards = "".join([

        result_metric_html(
            "GENERATIONS",
            f"{generation}/{MAX_GENERATIONS}"
        ),

        result_metric_html(
            "BEST POSITION",
            best_x,
            result_color
        ),

        result_metric_html(
            "BEST FITNESS",
            f"{best_fitness:.2f}",
            "#FBBF24"
        )
    ])


    st.html(f"""
    <div class="result-container {css_class}">

        <div
            class="result-icon"
            style="color:{result_color};">
            {icon}
        </div>

        <div class="result-title">
            {title}
        </div>

        <div class="result-description">
            {escape(description)}
        </div>

        <div class="result-grid">
            {result_cards}
        </div>

        <div style="
            color:#94A3B8;
            font-size:10px;
            letter-spacing:2px;
            margin-bottom:6px;
        ">
            PARAMETER CONTROL STRATEGY
        </div>

        <div
            class="result-strategy"
            style="color:{accent};">

            {escape(strategy)}

        </div>

        <div style="
            color:{result_color};
            font-size:14px;
            font-weight:700;
        ">
            DISTANCE FROM TARGET: {distance}
        </div>

        <div class="result-reason">

            <div class="result-reason-title">
                {escape(reason_title)}
            </div>

            <div class="result-reason-text">
                {escape(reason_text)}
            </div>

        </div>

    </div>
    """)

    st.session_state.result_shown = True

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "↻ PLAY AGAIN",
            type="primary",
            key="result_play_again",
            use_container_width=True
        ):

            handle_play_again()
            st.rerun()

    with col2:

        if st.button(
            "VIEW RESULTS",
            key="result_view_dashboard",
            use_container_width=True
        ):

            close_dialog()
            st.rerun()

    if st.button(
        "🏠 MAIN MENU",
        key="result_home",
        use_container_width=True
    ):

        handle_home()
        st.rerun()


# ============================================================
# 22. PERFORMANCE ANALYSIS CHART
# ============================================================

def display_analysis_chart(
    values,
    title,
    ylabel,
    color,
    target=None
):

    buffer = BytesIO()

    with get_plot_lock():

        fig, ax = plt.subplots(
            figsize=(9, 2.5),
            dpi=120
        )

        try:

            fig.patch.set_facecolor(
                "#0B1120"
            )

            ax.set_facecolor(
                "#0B1120"
            )

            generations = list(
                range(len(values))
            )

            ax.plot(
                generations,
                values,
                color=color,
                marker="o",
                markersize=3,
                linewidth=2
            )

            if target is not None:

                ax.axhline(
                    target,
                    color="#FBBF24",
                    linestyle="--",
                    linewidth=1,
                    label="Target"
                )

                legend = ax.legend(
                    facecolor="#111827",
                    edgecolor="#29384C",
                    fontsize=8
                )

                for text in legend.get_texts():

                    text.set_color(
                        "#E2E8F0"
                    )

            ax.set_title(
                title,
                color="#E2E8F0",
                fontsize=11,
                fontweight="bold"
            )

            ax.set_xlabel(
                "Generation",
                color="#94A3B8",
                fontsize=9
            )

            ax.set_ylabel(
                ylabel,
                color="#94A3B8",
                fontsize=9
            )

            ax.tick_params(
                colors="#94A3B8",
                labelsize=8
            )

            ax.set_xlim(
                0,
                max(1, len(values) - 1)
            )

            ax.grid(
                alpha=0.2,
                color="#64748B"
            )

            for spine in ax.spines.values():

                spine.set_color(
                    "#29384C"
                )

            fig.tight_layout()

            fig.savefig(
                buffer,
                format="png",
                facecolor=fig.get_facecolor()
            )

        finally:

            plt.close(fig)

    encoded_image = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    buffer.close()

    st.html(f"""
    <img
        src="data:image/png;base64,{encoded_image}"
        style="
            width:100%;
            border:1px solid #29384C;
            border-radius:10px;
        "
        alt="{escape(title)}"
    />
    """)


# ============================================================
# 23. POP-UP: PERFORMANCE ANALYSIS
# ============================================================

@st.dialog(
    "Performance Analysis",
    width="large",
    dismissible=False
)
def performance_dialog():

    strategy = (
        st.session_state.settings[0]
    )

    st.subheader(
        "Evolution Performance"
    )

    st.caption(
        f"Current strategy: {strategy}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Best Fitness",
        f"{fitness(get_best_position()):.2f}"
    )

    col2.metric(
        "Best Position",
        get_best_position()
    )

    col3.metric(
        "Distance to Target",
        get_distance_from_target()
    )

    if st.session_state.generation == 0:

        st.info(
            "Run at least one generation "
            "to observe evolutionary changes."
        )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([

        "Fitness",
        "Step Size",
        "Position",
        "Success Rate",
        "History"
    ])

    with tab1:

        display_analysis_chart(
            st.session_state.history,
            "Best Fitness by Generation",
            "Fitness",
            "#22D3EE",
            target=TARGET_FITNESS
        )

        st.caption(
            "Higher fitness indicates a better solution. "
            "Winning still requires the exact position 79."
        )

    with tab2:

        display_analysis_chart(
            st.session_state.sigma_history,
            "Mutation Step Size by Generation",
            "Step Size (σ)",
            "#E879F9"
        )

        st.caption(
            "For Self-Adaptive Control, this graph "
            "shows the best surviving individual's step size."
        )

    with tab3:

        display_analysis_chart(
            st.session_state.position_history,
            "Best Position by Generation",
            "Position",
            "#4ADE80",
            target=TARGET_POSITION
        )

        display_analysis_chart(
            st.session_state.distance_history,
            "Distance from Global Optimum",
            "Distance",
            "#FBBF24",
            target=0
        )

    with tab4:

        success_percentages = [

            rate * 100

            for rate in
            st.session_state.success_history
        ]

        display_analysis_chart(
            success_percentages,
            "Mutation Success Rate",
            "Success Rate (%)",
            "#FBBF24",
            target=20
        )

        st.caption(
            "The 20% reference represents the "
            "1/5 Success Rule used by Adaptive Control. "
            "Generation 0 has no mutations."
        )

    with tab5:

        history_df = pd.DataFrame({

            "Generation": list(
                range(
                    st.session_state.generation + 1
                )
            ),

            "Best Fitness": [
                round(v, 2)
                for v in st.session_state.history
            ],

            "Step Size": [
                round(v, 2)
                for v in st.session_state.sigma_history
            ],

            "Best Position":
                st.session_state.position_history,

            "Distance":
                st.session_state.distance_history,

            "Success Rate (%)": [
                round(v * 100, 2)
                for v in st.session_state.success_history
            ]
        })

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

    if st.button(
        "CLOSE",
        key="close_performance",
        use_container_width=True
    ):

        close_dialog()
        st.rerun()


# ============================================================
# 24. POP-UP: POPULATION DETAILS
# ============================================================

@st.dialog(
    "Population Details",
    width="large",
    dismissible=False
)
def population_dialog():

    st.subheader(
        "Current Population"
    )

    st.caption(
        f"Generation {st.session_state.generation} "
        f"of {MAX_GENERATIONS}"
    )

    rows = []

    for index, (x, sigma) in enumerate(
        st.session_state.population
    ):

        if x == TARGET_POSITION:

            status = "Global Optimum"

        elif index == 0:

            status = "Best Individual"

        else:

            status = "Surviving Individual"

        rows.append({

            "Rank": index + 1,

            "Position": int(x),

            "Fitness": round(
                float(fitness(x)),
                2
            ),

            "Step Size": round(
                float(sigma),
                2
            ),

            "Distance to Target": abs(
                TARGET_POSITION - x
            ),

            "Status": status
        })

    population_df = pd.DataFrame(
        rows
    )

    st.dataframe(
        population_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Latest Mutation Process"
    )

    if st.session_state.last_mutations:

        mutation_df = pd.DataFrame(
            st.session_state.last_mutations
        )

        st.dataframe(
            mutation_df,
            use_container_width=True,
            hide_index=True
        )

        improved_count = sum(

            row["Mutation Result"] == "Improved"

            for row in
            st.session_state.last_mutations
        )

        st.caption(
            f"{improved_count} out of "
            f"{POPULATION_SIZE} offspring "
            "improved their parent's fitness."
        )

    else:

        st.info(
            "No mutations have occurred yet. "
            "Press Next Generation to begin."
        )

    if st.button(
        "CLOSE",
        key="close_population",
        use_container_width=True
    ):

        close_dialog()
        st.rerun()


# ============================================================
# 25. POP-UP: LEARNING GUIDE
# ============================================================

@st.dialog(
    "Learning Guide",
    width="large",
    dismissible=False
)
def learning_dialog():

    st.subheader(
        "Understanding Parameter Control"
    )

    st.markdown("""
    Parameter control changes algorithm parameters
    during the evolutionary process.

    In this simulation, the controlled parameter
    is the mutation step size, **σ (sigma)**.

    The objective is to find the highest point
    of the fitness landscape.
    """)

    with st.expander(
        "⏱️ Deterministic Control",
        expanded=True
    ):

        st.markdown("""
        The step size decreases according to
        a predefined schedule.

        It does not depend on mutation success.

        **Example:** An initial step size of 15
        gradually decreases as generations progress.

        Large initial steps encourage exploration.
        Smaller later steps encourage refinement.
        """)

        st.latex(
            r"\sigma_g = "
            r"\max(0.5,\sigma_0(1-\frac{g}{30}))"
        )

    with st.expander(
        "⚡ Adaptive Control"
    ):

        st.markdown("""
        The step size changes according to feedback
        from mutation success.

        This simulation uses the 1/5 Success Rule.

        - Success rate above 20%: increase step size.
        - Success rate below 20%: decrease step size.
        - Success rate equal to 20%: maintain step size.

        The step size remains within 0.5 and 50.
        """)

    with st.expander(
        "🧬 Self-Adaptive Control"
    ):

        st.markdown("""
        Every individual carries its own mutation
        step size.

        During reproduction, both the position
        and the step size can evolve.

        Individuals with higher fitness are more
        likely to survive through selection.

        The step size is therefore evolved as
        part of the solution.
        """)

        st.latex(
            r"\sigma' = "
            r"\sigma \times e^{0.4N(0,1)}"
        )

        st.latex(
            r"x' = x + N(0,\sigma'^2)"
        )

        st.caption(
            "The new position is rounded to an integer "
            "and restricted to the range 0–100."
        )

    with st.expander(
        "⛰️ Local vs Global Optimum"
    ):

        st.markdown("""
        **Local Optimum — Position 27**

        A smaller peak that may trap the population.

        **Global Optimum — Position 79**

        The highest fitness position in the
        integer search space.

        A good parameter control strategy balances
        exploration and refinement.
        """)

    with st.expander(
        "🎯 Mission Rules"
    ):

        st.markdown("""
        Your population begins at position 10.

        You have a maximum of 30 generations
        to reach exactly position 79.

        | Best Position | Result |
        |---|---|
        | 78 | Target not reached |
        | 79 | Mission Complete |
        | 80 | Target not reached |

        If the exact target has not been reached
        by generation 30, the mission fails.

        Changing the strategy or initial step size
        starts a new simulation.

        Mutation is random, so identical settings
        can produce different results.
        """)

    if st.button(
        "CLOSE",
        key="close_learning",
        use_container_width=True
    ):

        close_dialog()
        st.rerun()


# ============================================================
# 26. MAIN DASHBOARD
# ============================================================

def display_dashboard():

    display_header()

    with st.container(
        key="main_dashboard"
    ):

        left_column, right_column = st.columns(
            [1, 3.2],
            gap="medium"
        )


        # ----------------------------------------------------
        # LEFT CONTROL PANEL
        # ----------------------------------------------------

        with left_column:

            with st.container(
                key="left_panel"
            ):

                section_heading(
                    "01 / PARAMETER CONTROL"
                )

                strategy = st.radio(

                    "Select Strategy",

                    options=list(
                        STRATEGIES.keys()
                    ),

                    key="selected_strategy",

                    on_change=handle_settings_change,

                    label_visibility="collapsed"
                )

                strategy_info = (
                    STRATEGIES[strategy]
                )

                accent = (
                    strategy_info["color"]
                )

                st.html(f"""
                <div class="strategy-description">

                    <div
                        class="strategy-description-title"
                        style="color:{accent};">

                        {strategy_info["icon"]}
                        {escape(strategy)} Control

                    </div>

                    <div class="strategy-description-text">

                        {escape(strategy_info["description"])}

                    </div>

                </div>
                """)


                # INITIAL STEP SIZE

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
                <div class="slider-help">

                    Small σ = finer movements.

                    <br>

                    Large σ = wider exploration.

                    <br>

                    Changing settings resets the mission.

                </div>
                """)


                # GAME CONTROLS

                section_heading(
                    "03 / SIMULATION CONTROLS"
                )

                st.button(

                    "▶ NEXT GENERATION",

                    type="primary",

                    key="next_generation_button",

                    use_container_width=True,

                    disabled=(
                        st.session_state.game_finished
                    ),

                    on_click=handle_next_generation
                )

                st.button(

                    "⏩ RUN ALL GENERATIONS",

                    key="run_all_button",

                    use_container_width=True,

                    disabled=(
                        st.session_state.game_finished
                    ),

                    on_click=handle_run_all
                )

                st.button(

                    "↻ RESET SIMULATION",

                    key="reset_button",

                    use_container_width=True,

                    on_click=handle_reset
                )

                if st.session_state.game_finished:

                    st.button(

                        "VIEW MISSION RESULT",

                        key="view_result_button",

                        use_container_width=True,

                        on_click=open_dialog,

                        args=("result",)
                    )


                # MISSION OBJECTIVE

                st.html("""
                <div class="mission-card">

                    <div class="mission-title">
                        MISSION OBJECTIVE
                    </div>

                    <div class="mission-text">

                        Reach exactly

                        <span class="mission-target">
                            POSITION 79
                        </span>

                        within 30 generations.

                        <br>

                        Target distance must be zero.

                    </div>

                </div>
                """)


        # ----------------------------------------------------
        # RIGHT DASHBOARD PANEL
        # ----------------------------------------------------

        with right_column:

            with st.container(
                key="right_panel"
            ):

                display_metrics(
                    strategy
                )

                section_heading(
                    "FITNESS LANDSCAPE"
                )

                display_fitness_landscape(
                    accent
                )

                display_target_status()

                display_feedback()


    # --------------------------------------------------------
    # BOTTOM NAVIGATION
    # --------------------------------------------------------

    with st.container(
        key="bottom_navigation"
    ):

        p1, p2, p3, p4 = st.columns(4)

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
# 27. APPLICATION ROUTING
# ============================================================

if not st.session_state.game_started:

    display_welcome_screen()

    st.stop()


display_dashboard()


# ============================================================
# 28. DIALOG ROUTING
# ============================================================

active_dialog = (
    st.session_state.active_dialog
)

if active_dialog == "result":

    if st.session_state.game_finished:

        mission_result_dialog()

    else:

        close_dialog()

elif active_dialog == "performance":

    performance_dialog()

elif active_dialog == "population":

    population_dialog()

elif active_dialog == "learning":

    learning_dialog()


# ============================================================
# END OF APPLICATION
# ============================================================

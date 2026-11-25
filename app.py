import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64

from pathlib import Path
from html import escape
from matplotlib.lines import Line2D


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
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="stAppViewContainer"] {
    min-height: 100dvh;
}

[data-testid="stMain"] {
    overflow-x: hidden;
}

.block-container {
    width: 100%;
    max-width: 1800px;

    padding: 1.1rem 2rem 0.75rem !important;

    box-sizing: border-box;
}

.block-container > [data-testid="stVerticalBlock"] {
    gap: 0.75rem !important;
}


/* ==========================================================
   APPLICATION HEADER
   ========================================================== */

.hero {
    display: block;

    width: 100%;

    text-align: center;

    padding: 0 0 18px;

    margin: 0;

    box-sizing: border-box;
}

.hero-label {
    color: var(--cyan);

    font-size: 10px;
    font-weight: 700;

    letter-spacing: 5px;
    line-height: 1.4;

    margin: 0 0 7px;
}

.hero-title {
    color: #E0F2FE;

    font-size: clamp(25px, 3vw, 34px);
    font-weight: 900;

    letter-spacing: 5px;
    line-height: 1.2;

    margin: 0 0 9px;

    text-shadow: 0 0 22px #0891B2;
}

.hero-subtitle {
    color: var(--muted);

    font-size: 10px;

    letter-spacing: 3px;
    line-height: 1.5;

    margin: 0;
}


/* ==========================================================
   MAIN DASHBOARD
   ========================================================== */

.st-key-main_dashboard {
    width: 100%;
    min-width: 0;

    margin-top: 6px;

    box-sizing: border-box;
}

.st-key-main_dashboard
[data-testid="stHorizontalBlock"] {
    align-items: flex-start;
}

.st-key-main_dashboard
[data-testid="stColumn"] {
    min-width: 0;
}


/* ==========================================================
   LEFT CONTROL PANEL
   ========================================================== */

.st-key-left_panel {
    width: 100%;
    min-width: 0;

    box-sizing: border-box;
}

.st-key-left_panel
[data-testid="stVerticalBlock"] {
    gap: 0.55rem !important;
}

.st-key-left_panel
[data-testid="stHorizontalBlock"] {
    gap: 0.65rem !important;
}

.st-key-left_panel
[data-testid="stVerticalBlockBorderWrapper"] {
    box-sizing: border-box;
}

.st-key-left_panel
[data-testid="stElementContainer"] {
    min-width: 0;
    flex-shrink: 0;
}


/* ==========================================================
   SECTION HEADINGS
   ========================================================== */

.section-heading {
    display: block;

    color: var(--light-cyan);

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.8px;
    line-height: 1.5;

    padding: 0;

    margin: 0 0 4px;
}

.control-label {
    display: block;

    color: var(--text);

    font-size: 12px;
    font-weight: 500;

    line-height: 1.5;

    margin: 0;
}


/* ==========================================================
   RADIO BUTTONS
   ========================================================== */

.st-key-left_panel
[data-testid="stRadio"] {
    width: 100% !important;
    max-width: 100%;

    background: transparent;

    border: none;

    padding: 0;
    margin: 0;
}

.st-key-left_panel
[role="radiogroup"] {
    width: 100% !important;

    display: flex;
    flex-direction: column;

    gap: 3px;

    box-sizing: border-box;

    padding: 6px 10px;

    border: 1px solid var(--border);
    border-radius: 9px;

    background: rgba(17, 24, 39, 0.85);
}

.st-key-left_panel
[role="radiogroup"] label {
    width: 100%;

    margin: 0;
    padding: 1px 0;
}

.st-key-left_panel
[role="radiogroup"] p {
    font-size: 13px;
    line-height: 1.4;
}


/* ==========================================================
   STRATEGY DESCRIPTION
   ========================================================== */

.strategy-description {
    display: block;

    width: 100%;

    box-sizing: border-box;

    background: rgba(17, 24, 39, 0.94);

    border: 1px solid var(--border);
    border-radius: 8px;

    padding: 9px 11px;

    margin: 0 0 4px;
}

.strategy-description-title {
    font-size: 12px;
    font-weight: 700;

    line-height: 1.5;

    margin-bottom: 4px;
}

.strategy-description-text {
    color: #CBD5E1;

    font-size: 12px;
    line-height: 1.5;

    overflow-wrap: break-word;
}


/* ==========================================================
   SLIDER
   ========================================================== */

.st-key-left_panel
[data-testid="stSlider"] {
    width: 100%;

    padding: 2px 0 0 !important;

    margin: 0 !important;
}

.st-key-left_panel
[data-testid="stWidgetLabel"] {
    margin-bottom: 4px;
}

.st-key-left_panel
[data-testid="stWidgetLabel"] p {
    font-size: 12px;
    line-height: 1.5;
}

.slider-help {
    display: block;

    color: var(--muted);

    font-size: 11px;
    line-height: 1.5;

    margin: 0 0 5px;
}


/* ==========================================================
   GAME CONTROL BUTTONS
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
   MISSION BOX
   ========================================================== */

.mission-card {
    display: block;

    width: 100%;

    background: rgba(17, 24, 39, 0.78);

    border: 1px solid var(--border);
    border-radius: 8px;

    padding: 9px 11px;

    box-sizing: border-box;

    margin: 3px 0 0;
}

.mission-title {
    color: var(--light-cyan);

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.6px;
    line-height: 1.5;

    margin-bottom: 5px;
}

.mission-text {
    color: #A8BED3;

    font-size: 11px;
    line-height: 1.5;

    overflow-wrap: break-word;
}


/* ==========================================================
   STATISTIC CARDS
   ========================================================== */

.metric-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 12px;

    width: 100%;
}

.metric-card {
    display: flex;
    flex-direction: column;

    justify-content: center;

    background: rgba(17, 24, 39, 0.95);

    border: 1px solid var(--border);
    border-radius: 10px;

    padding: 11px 13px;

    min-width: 0;
    min-height: 70px;

    box-sizing: border-box;
}

.metric-label {
    color: var(--muted);

    font-size: 10px;
    font-weight: 600;

    letter-spacing: 0.7px;
    line-height: 1.5;

    margin-bottom: 6px;
}

.metric-value {
    font-size: 25px;
    font-weight: 800;

    line-height: 1.2;
}


/* ==========================================================
   GENERATION PROGRESS BAR
   ========================================================== */

.progress-track {
    width: 100%;
    height: 6px;

    background: #1E293B;

    border-radius: 20px;

    overflow: hidden;

    margin-top: 10px;
    margin-bottom: 2px;
}

.progress-fill {
    height: 100%;

    background: linear-gradient(
        90deg,
        #0891B2,
        #22D3EE
    );

    border-radius: 20px;

    transition: width 0.3s ease;
}


/* ==========================================================
   RIGHT PANEL
   ========================================================== */

.st-key-right_panel {
    width: 100%;
    min-width: 0;

    box-sizing: border-box;
}

.st-key-right_panel
[data-testid="stVerticalBlock"] {
    gap: 0.65rem !important;
}


/* ==========================================================
   FITNESS LANDSCAPE
   ========================================================== */

.st-key-fitness_chart {
    width: 100%;
    min-width: 0;

    box-sizing: border-box;
}

.st-key-fitness_chart
[data-testid="stImage"] {
    width: 100%;

    margin: 0;
}

.st-key-fitness_chart
[data-testid="stImage"] img {
    display: block;

    width: 100% !important;
    max-width: 100%;

    height: auto !important;

    border: 1px solid var(--border);
    border-radius: 10px;

    box-sizing: border-box;

    object-fit: contain;
}


/* ==========================================================
   LIVE EVOLUTION FEEDBACK
   ========================================================== */

.feedback-box {
    display: block;

    width: 100%;

    background: rgba(17, 24, 39, 0.96);

    border: 1px solid var(--border);
    border-left: 4px solid var(--gold);

    border-radius: 9px;

    padding: 11px 13px;

    margin-top: 3px;

    box-sizing: border-box;
}

.feedback-title {
    color: var(--gold);

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.8px;
    line-height: 1.5;

    margin-bottom: 6px;
}

.feedback-text {
    color: var(--text);

    font-size: 12px;
    line-height: 1.5;

    overflow-wrap: break-word;
}


/* ==========================================================
   BOTTOM NAVIGATION
   ========================================================== */

.st-key-bottom_navigation {
    width: 100%;

    border-top: 1px solid var(--border);

    padding-top: 9px;

    margin: 4px 0 0;

    box-sizing: border-box;
}

.st-key-bottom_navigation
[data-testid="stHorizontalBlock"] {
    gap: 12px !important;
}

.st-key-bottom_navigation
.stButton > button {
    min-height: 36px;
}


/* ==========================================================
   SINGLE SCREEN DESKTOP
   ========================================================== */

@media (min-width: 1200px) and (min-height: 700px) {

    html,
    body {
        height: 100%;
        margin: 0;
    }

    .stApp {
        height: 100dvh;
        min-height: 100dvh;
    }

    [data-testid="stMain"] {
        height: 100dvh;

        overflow-y: auto;
        overflow-x: hidden;

        scrollbar-width: none;
        -ms-overflow-style: none;
    }

    [data-testid="stMain"]::-webkit-scrollbar {
        display: none;
        width: 0;
    }

    .block-container {
        padding-top: 0.85rem !important;
        padding-bottom: 0.65rem !important;

        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    .block-container >
    [data-testid="stVerticalBlock"] {
        gap: 0.65rem !important;
    }

    .hero {
        padding-bottom: 18px;
    }

    .hero-title {
        font-size: 32px;
    }

    .hero-label,
    .hero-subtitle {
        font-size: 9px;
    }

    .st-key-main_dashboard {
        margin-top: 6px;
    }

    .st-key-left_panel
    [data-testid="stVerticalBlock"] {
        gap: 0.45rem !important;
    }

    .st-key-right_panel
    [data-testid="stVerticalBlock"] {
        gap: 0.55rem !important;
    }

    .st-key-fitness_chart
    [data-testid="stImage"] img {
        max-height: 40dvh;
    }
}


/* ==========================================================
   COMPACT DESKTOP HEIGHT
   ========================================================== */

@media (min-width: 1200px) and (max-height: 820px) {

    .block-container {
        padding-top: 0.65rem !important;
        padding-bottom: 0.5rem !important;
    }

    .hero {
        padding-bottom: 14px;
    }

    .hero-title {
        font-size: 30px;

        margin-bottom: 7px;
    }

    .hero-label {
        margin-bottom: 5px;
    }

    .hero-subtitle {
        line-height: 1.5;
    }

    .st-key-main_dashboard {
        margin-top: 4px;
    }

    .section-heading {
        font-size: 10px;
        line-height: 1.5;

        margin-bottom: 3px;
    }

    .st-key-left_panel
    [data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }

    .st-key-left_panel
    [role="radiogroup"] {
        padding: 4px 9px;

        gap: 1px;
    }

    .st-key-left_panel
    [role="radiogroup"] p {
        font-size: 12px;
    }

    .strategy-description {
        padding: 7px 9px;

        margin-bottom: 3px;
    }

    .strategy-description-title {
        font-size: 11px;

        margin-bottom: 3px;
    }

    .strategy-description-text {
        font-size: 11px;
        line-height: 1.45;
    }

    .slider-help {
        font-size: 10px;

        margin-bottom: 3px;
    }

    .mission-card {
        padding: 7px 9px;
    }

    .mission-text {
        font-size: 10.5px;
        line-height: 1.45;
    }

    .metric-card {
        padding: 9px 12px;

        min-height: 65px;
    }

    .metric-value {
        font-size: 23px;
    }

    .feedback-box {
        padding: 9px 12px;
    }

    .stButton > button {
        min-height: 33px;

        padding: 5px 9px;
    }

    .st-key-fitness_chart
    [data-testid="stImage"] img {
        max-height: 38dvh;
    }

    .st-key-bottom_navigation {
        padding-top: 6px;

        margin-top: 2px;
    }
}


/* ==========================================================
   STATIC DESKTOP MODE

   Lock the main dashboard only when sufficient
   viewport space is available.
   ========================================================== */

@media (min-width: 1400px) and (min-height: 740px) {

    [data-testid="stMain"] {
        overflow-y: hidden !important;
        overflow-x: hidden !important;
    }

}


/* ==========================================================
   POP-UP WINDOWS
   ========================================================== */

[data-testid="stDialog"] [role="dialog"] {
    max-height: 90dvh;

    overflow-y: auto !important;
    overflow-x: hidden;
}

[data-testid="stDialog"]
[data-testid="stVerticalBlock"] {
    gap: 0.8rem;
}


/* ==========================================================
   RESPONSIVE SMALL SCREENS
   ========================================================== */

@media (max-width: 1199px) {

    [data-testid="stMain"] {
        overflow-y: auto !important;
    }

    .block-container {
        padding: 1.5rem 1rem !important;
    }

    .hero {
        padding-bottom: 16px;
    }

    .hero-title {
        font-size: 28px;
        letter-spacing: 3px;
    }

    .metric-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 8px;
    }

    .metric-value {
        font-size: 22px;
    }

}

@media (max-width: 600px) {

    .hero-title {
        font-size: 23px;
        letter-spacing: 2px;
    }

    .hero-label {
        letter-spacing: 2px;
    }

    .hero-subtitle {
        letter-spacing: 1px;
    }

    .hero {
        padding-bottom: 12px;
    }

    .metric-card {
        min-height: 65px;
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


STRATEGIES = {

    "Deterministic": {
        "icon": "⏱️",
        "color": "#22D3EE",
        "description": (
            "Step size changes according to a "
            "predefined generation schedule."
        )
    },

    "Adaptive": {
        "icon": "⚡",
        "color": "#FBBF24",
        "description": (
            "Step size changes based on mutation "
            "success using the 1/5 Success Rule."
        )
    },

    "Self-Adaptive": {
        "icon": "🧬",
        "color": "#D946EF",
        "description": (
            "Each individual evolves its own "
            "encoded mutation step size."
        )
    }

}


# ============================================================
# 05. FITNESS FUNCTION
# ============================================================

def fitness(x):

    return (
        25
        + 40 * np.exp(-((x - 27) / 13) ** 2)
        + 75 * np.exp(-((x - 79) / 15) ** 2)
    )


# ============================================================
# 06. RESET SIMULATION
# ============================================================

def reset_simulation(strategy, initial_sigma):

    st.session_state.generation = 0

    st.session_state.population = [
        (10.0, float(initial_sigma))
        for _ in range(POPULATION_SIZE)
    ]

    st.session_state.sigma = float(initial_sigma)

    st.session_state.history = [
        float(fitness(10.0))
    ]

    st.session_state.sigma_history = [
        float(initial_sigma)
    ]

    st.session_state.feedback = (
        "Ready to begin. Press Next Generation "
        "to start evolving your population."
    )

    st.session_state.settings = (
        strategy,
        initial_sigma
    )


# ============================================================
# 07. EVOLUTION PROCESS
# ============================================================

def next_generation(strategy, initial_sigma):

    if st.session_state.generation >= MAX_GENERATIONS:
        return

    population = st.session_state.population
    sigma = st.session_state.sigma

    offspring = []
    successes = 0

    # --------------------------------------------------------
    # MUTATION
    # --------------------------------------------------------

    for x, individual_sigma in population:

        if strategy == "Self-Adaptive":

            child_sigma = np.clip(
                individual_sigma
                * np.exp(0.4 * np.random.normal()),
                MIN_SIGMA,
                MAX_SIGMA
            )

        else:

            child_sigma = sigma

        child_x = np.clip(
            x + np.random.normal(0, child_sigma),
            0,
            100
        )

        offspring.append(
            (
                float(child_x),
                float(child_sigma)
            )
        )

        if fitness(child_x) > fitness(x):

            successes += 1

    # --------------------------------------------------------
    # SURVIVAL SELECTION
    # --------------------------------------------------------

    combined = population + offspring

    combined.sort(
        key=lambda individual: fitness(individual[0]),
        reverse=True
    )

    st.session_state.population = combined[
        :POPULATION_SIZE
    ]

    st.session_state.generation += 1

    generation = st.session_state.generation

    success_rate = successes / POPULATION_SIZE

    # --------------------------------------------------------
    # DETERMINISTIC CONTROL
    # --------------------------------------------------------

    if strategy == "Deterministic":

        new_sigma = max(
            MIN_SIGMA,
            initial_sigma
            * (1 - generation / MAX_GENERATIONS)
        )

        feedback = (
            f"Generation {generation}: "
            f"Step size changed from "
            f"{sigma:.2f} to {new_sigma:.2f} "
            "according to the predefined schedule."
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

            action = "increased"

        elif success_rate < 0.2:

            new_sigma = max(
                MIN_SIGMA,
                sigma * 0.8
            )

            action = "decreased"

        else:

            new_sigma = sigma
            action = "maintained"

        feedback = (
            f"Successful mutations: "
            f"{successes}/{POPULATION_SIZE} "
            f"({success_rate:.0%}). "
            f"Step size {action}: "
            f"{sigma:.2f} → {new_sigma:.2f}."
        )

    # --------------------------------------------------------
    # SELF-ADAPTIVE CONTROL
    # --------------------------------------------------------

    else:

        new_sigma = (
            st.session_state.population[0][1]
        )

        feedback = (
            "Individuals evolved their own "
            "mutation step sizes. "
            f"Best individual's step size: "
            f"{new_sigma:.2f}."
        )

    # --------------------------------------------------------
    # UPDATE SIMULATION STATE
    # --------------------------------------------------------

    st.session_state.sigma = float(new_sigma)

    st.session_state.feedback = feedback

    best_x = st.session_state.population[0][0]

    st.session_state.history.append(
        float(fitness(best_x))
    )

    st.session_state.sigma_history.append(
        float(new_sigma)
    )


# ============================================================
# 08. REUSABLE UI COMPONENTS
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


def display_metrics(strategy):

    generation = st.session_state.generation

    best_x = st.session_state.population[0][0]

    best_fitness = float(fitness(best_x))

    sigma_label = (
        "BEST σ"
        if strategy == "Self-Adaptive"
        else "NEXT STEP SIZE (σ)"
    )

    progress = (
        generation / MAX_GENERATIONS
    ) * 100

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
            f"{best_x:.2f}",
            "#67E8F9"
        )

    ]

    st.markdown(
        '<div class="metric-grid">'
        + "".join(cards)
        + '</div>'
        + '<div class="progress-track">'
        + f'<div class="progress-fill" '
          f'style="width:{progress:.2f}%;">'
        + '</div>'
        + '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 09. FITNESS LANDSCAPE GRAPH
# ============================================================

def display_fitness_landscape(accent):

    best_x = st.session_state.population[0][0]

    best_fitness = float(fitness(best_x))

    x_values = np.linspace(0, 100, 500)

    y_values = fitness(x_values)

    # --------------------------------------------------------
    # GRAPH CONFIGURATION
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 3.1),
        dpi=130
    )

    fig.patch.set_facecolor("#0B1120")

    ax.set_facecolor("#0B1120")

    # --------------------------------------------------------
    # MOUNTAIN AREA
    # --------------------------------------------------------

    ax.fill_between(
        x_values,
        y_values,
        color="#22D3EE",
        alpha=0.12
    )

    # --------------------------------------------------------
    # NEON GLOW EFFECT
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # POPULATION MEMBERS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # BEST INDIVIDUAL GLOW
    # --------------------------------------------------------

    for size, alpha in [

        (450, 0.05),
        (250, 0.10),
        (120, 0.18)

    ]:

        ax.scatter(
            best_x,
            best_fitness,
            color=accent,
            s=size,
            alpha=alpha,
            zorder=6
        )

    ax.scatter(
        best_x,
        best_fitness,
        color=accent,
        edgecolors="#FFFFFF",
        linewidths=1.2,
        s=75,
        zorder=7
    )

    # --------------------------------------------------------
    # LOCAL OPTIMUM
    # --------------------------------------------------------

    ax.annotate(
        "LOCAL OPTIMUM",
        xy=(27, fitness(27)),
        xytext=(27, 86),
        color="#CBD5E1",
        fontsize=9,
        ha="center",
        arrowprops=dict(
            color="#94A3B8",
            arrowstyle="->",
            linewidth=1
        )
    )

    # --------------------------------------------------------
    # GLOBAL OPTIMUM
    # --------------------------------------------------------

    ax.scatter(
        79,
        fitness(79),
        marker="*",
        color="#FBBF24",
        s=160,
        zorder=8
    )

    ax.annotate(
        "GLOBAL OPTIMUM",
        xy=(79, fitness(79)),
        xytext=(79, 118),
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

    # --------------------------------------------------------
    # AXIS FORMATTING
    # --------------------------------------------------------

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 130)

    ax.set_xlabel(
        "Search Space — Candidate Solution (x)",
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

    # --------------------------------------------------------
    # GRAPH LEGEND
    # --------------------------------------------------------

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
            markerfacecolor=accent,
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
            label="Global optimum"
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

    # --------------------------------------------------------
    # GRAPH SPACING
    # --------------------------------------------------------

    fig.subplots_adjust(
        left=0.065,
        right=0.985,
        top=0.95,
        bottom=0.26
    )

    with st.container(key="fitness_chart"):

        st.pyplot(
            fig,
            use_container_width=True,
            bbox_inches=None,
            pad_inches=0
        )

    plt.close(fig)


# ============================================================
# 10. LIVE EVOLUTION FEEDBACK
# ============================================================

def display_feedback():

    generation = st.session_state.generation

    best_x = st.session_state.population[0][0]

    best_fitness = float(fitness(best_x))

    feedback = st.session_state.feedback

    if best_fitness >= 99.9:

        feedback = (
            "🏆 Mission accomplished! "
            "Near-global optimum reached. "
            + feedback
        )

    elif generation >= MAX_GENERATIONS:

        feedback = (
            "Simulation completed. "
            "Try another strategy or step size. "
            + feedback
        )

    st.markdown(
        '<div class="feedback-box">'

        '<div class="feedback-title">'
        'LIVE EVOLUTION FEEDBACK'
        '</div>'

        '<div class="feedback-text">'
        f'{escape(feedback)}'
        '</div>'

        '</div>',

        unsafe_allow_html=True
    )


# ============================================================
# 11. POP-UP: PERFORMANCE ANALYSIS
# ============================================================

@st.dialog(
    "Performance Analysis",
    width="large"
)
def performance_dialog():

    st.subheader(
        "Best Fitness Progress"
    )

    st.line_chart(
        {
            "Best Fitness":
                st.session_state.history
        },
        color="#22D3EE",
        height=220
    )

    st.subheader(
        "Mutation Step Size Progress"
    )

    st.line_chart(
        {
            "Step Size":
                st.session_state.sigma_history
        },
        color="#D946EF",
        height=220
    )

    if (
        st.session_state.settings[0]
        == "Self-Adaptive"
    ):

        st.caption(
            "For Self-Adaptive Control, "
            "the graph shows the best "
            "individual's mutation step size."
        )

    else:

        st.caption(
            "The graph shows how the mutation "
            "step size changes across generations."
        )

    if st.button(
        "Close",
        key="close_performance",
        use_container_width=True
    ):

        st.rerun()


# ============================================================
# 12. POP-UP: POPULATION DETAILS
# ============================================================

@st.dialog(
    "Population Details",
    width="large"
)
def population_dialog():

    current_strategy = (
        st.session_state.settings[0]
    )

    population_data = []

    for i, (x, individual_sigma) in enumerate(
        st.session_state.population
    ):

        if current_strategy == "Self-Adaptive":

            step_size = individual_sigma

        else:

            step_size = st.session_state.sigma

        population_data.append(

            {
                "Individual": i + 1,

                "Position": round(x, 2),

                "Fitness": round(
                    float(fitness(x)),
                    2
                ),

                "Step Size": round(
                    step_size,
                    2
                )
            }

        )

    st.table(population_data)

    st.caption(
        "The population contains the five "
        "fittest surviving individuals."
    )

    if st.button(
        "Close",
        key="close_population",
        use_container_width=True
    ):

        st.rerun()


# ============================================================
# 13. POP-UP: LEARNING GUIDE
# ============================================================

@st.dialog(
    "Learning Guide",
    width="large"
)
def learning_dialog():

    tab1, tab2, tab3, tab4 = st.tabs(

        [
            "Deterministic",
            "Adaptive",
            "Self-Adaptive",
            "Challenge"
        ]

    )

    # --------------------------------------------------------
    # DETERMINISTIC CONTROL
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "Deterministic Control"
        )

        st.write(
            "Parameters change according to "
            "a predefined schedule."
        )

        st.markdown(
            """
- No feedback from the search.
- Large step sizes encourage exploration.
- Smaller step sizes encourage refinement.
            """
        )

        st.latex(
            r"\sigma_t = "
            r"\max(0.5,\sigma_0(1-t/T))"
        )

        st.info(
            "The mutation step size decreases "
            "as the generation increases."
        )

    # --------------------------------------------------------
    # ADAPTIVE CONTROL
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "Adaptive Control"
        )

        st.write(
            "Parameters change based on feedback "
            "from the search process."
        )

        st.markdown(
            "**1/5 Success Rule**"
        )

        st.table(

            [
                {
                    "Success Rate": "Above 20%",
                    "Action": "Increase step size"
                },

                {
                    "Success Rate": "Equal to 20%",
                    "Action": "Maintain step size"
                },

                {
                    "Success Rate": "Below 20%",
                    "Action": "Decrease step size"
                }
            ]

        )

        st.info(
            "The algorithm adjusts its mutation "
            "step size based on successful mutations."
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
            "the candidate solution through "
            "mutation and survival selection."
        )

        st.latex(
            r"\sigma' = \sigma e^{0.4N(0,1)}"
        )

        st.info(
            "Different individuals may have "
            "different mutation step sizes."
        )

    # --------------------------------------------------------
    # CHALLENGE
    # --------------------------------------------------------

    with tab4:

        st.subheader(
            "Your Mission"
        )

        st.write(
            "Reach a fitness value of at least "
            "99.9 within 30 generations."
        )

        st.markdown(
            """
1. Select a parameter control strategy.
2. Choose an initial mutation step size.
3. Run the simulation.
4. Observe the fitness and step size.
5. Repeat using another strategy.

**Discussion**

- Which strategy reached the highest peak?
- How did the mutation step size change?
- Did the population get trapped at a local optimum?
            """
        )

        st.caption(
            "Results may differ because mutation "
            "involves randomness."
        )

    if st.button(
        "Close",
        key="close_learning",
        use_container_width=True
    ):

        st.rerun()


# ============================================================
# 14. APPLICATION HEADER
# ============================================================

st.markdown(

    '<div class="hero">'

    '<div class="hero-label">'
    'EVOLUTIONARY COMPUTATION'
    '</div>'

    '<div class="hero-title">'
    'FITNESS MOUNTAIN'
    '</div>'

    '<div class="hero-subtitle">'
    'THE PARAMETER CONTROL CHALLENGE'
    '</div>'

    '</div>',

    unsafe_allow_html=True

)


# ============================================================
# 15. MAIN DASHBOARD LAYOUT
# ============================================================

with st.container(
    key="main_dashboard"
):

    left, right = st.columns(
        [1, 3],
        gap="medium"
    )

    # ========================================================
    # 16. LEFT CONTROL PANEL
    # ========================================================

    with left:

        with st.container(
            border=True,
            key="left_panel"
        ):

            # ------------------------------------------------
            # 01 / CONTROL PANEL
            # ------------------------------------------------

            section_heading(
                "01 / CONTROL PANEL"
            )

            # ------------------------------------------------
            # STRATEGY SELECTION
            # ------------------------------------------------

            strategy = st.radio(

                "Parameter Control Strategy",

                options=list(
                    STRATEGIES.keys()
                ),

                format_func=lambda name: (
                    f'{STRATEGIES[name]["icon"]} {name}'
                ),

                key="selected_strategy"

            )

            accent = STRATEGIES[strategy]["color"]

            description = STRATEGIES[strategy][
                "description"
            ]

            # ------------------------------------------------
            # STRATEGY DESCRIPTION
            # ------------------------------------------------

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

            # ------------------------------------------------
            # MUTATION STEP SIZE
            # ------------------------------------------------

            initial_sigma = st.slider(

                "Initial Mutation Step Size (σ)",

                min_value=1,

                max_value=30,

                value=15,

                step=1,

                key="initial_sigma"

            )

            st.markdown(

                '<div class="slider-help">'
                'Large σ: exploration &nbsp;|&nbsp; '
                'Small σ: refinement'
                '</div>',

                unsafe_allow_html=True

            )

            # ------------------------------------------------
            # INITIALIZE SESSION STATE
            # ------------------------------------------------

            settings = (
                strategy,
                initial_sigma
            )

            required_keys = [

                "generation",
                "population",
                "sigma",
                "history",
                "sigma_history",
                "feedback",
                "settings"

            ]

            missing_state = any(

                key not in st.session_state

                for key in required_keys

            )

            if (
                missing_state
                or st.session_state.get("settings") != settings
            ):

                reset_simulation(
                    strategy,
                    initial_sigma
                )

            finished = (
                st.session_state.generation
                >= MAX_GENERATIONS
            )

            # ------------------------------------------------
            # 02 / GAME CONTROLS
            # ------------------------------------------------

            section_heading(
                "02 / GAME CONTROLS"
            )

            # ------------------------------------------------
            # NEXT GENERATION
            # ------------------------------------------------

            if st.button(

                "▶ Next Generation",

                type="primary",

                disabled=finished,

                use_container_width=True,

                key="next_generation_button"

            ):

                next_generation(
                    strategy,
                    initial_sigma
                )

                st.rerun()

            # ------------------------------------------------
            # RUN ALL AND RESET
            # ------------------------------------------------

            run_col, reset_col = st.columns(
                2,
                gap="small"
            )

            with run_col:

                if st.button(

                    "⏩ Run All",

                    disabled=finished,

                    use_container_width=True,

                    key="run_all_button"

                ):

                    while (
                        st.session_state.generation
                        < MAX_GENERATIONS
                    ):

                        next_generation(
                            strategy,
                            initial_sigma
                        )

                    st.rerun()

            with reset_col:

                if st.button(

                    "↻ Reset",

                    use_container_width=True,

                    key="reset_button"

                ):

                    reset_simulation(
                        strategy,
                        initial_sigma
                    )

                    st.rerun()

            # ------------------------------------------------
            # 03 / YOUR MISSION
            # ------------------------------------------------

            st.markdown(

                '<div class="mission-card">'

                '<div class="mission-title">'
                '03 / YOUR MISSION'
                '</div>'

                '<div class="mission-text">'
                'Reach the highest fitness peak within '
                '30 generations. Compare how different '
                'strategies control mutation step size.'
                '</div>'

                '</div>',

                unsafe_allow_html=True

            )

    # ========================================================
    # 17. RIGHT PANEL
    # ========================================================

    with right:

        with st.container(
            key="right_panel"
        ):

            # ------------------------------------------------
            # STATISTIC CARDS
            # ------------------------------------------------

            display_metrics(
                strategy
            )

            # ------------------------------------------------
            # 04 / FITNESS LANDSCAPE
            # ------------------------------------------------

            section_heading(
                "04 / FITNESS LANDSCAPE"
            )

            display_fitness_landscape(
                accent
            )

            # ------------------------------------------------
            # LIVE EVOLUTION FEEDBACK
            # ------------------------------------------------

            display_feedback()


# ============================================================
# 18. BOTTOM NAVIGATION
# ============================================================

with st.container(
    key="bottom_navigation"
):

    p1, p2, p3 = st.columns(
        3,
        gap="medium"
    )

    # --------------------------------------------------------
    # PERFORMANCE ANALYSIS
    # --------------------------------------------------------

    with p1:

        if st.button(

            "📊 Performance Analysis",

            use_container_width=True,

            key="performance_button"

        ):

            performance_dialog()

    # --------------------------------------------------------
    # POPULATION DETAILS
    # --------------------------------------------------------

    with p2:

        if st.button(

            "🧬 Population Details",

            use_container_width=True,

            key="population_button"

        ):

            population_dialog()

    # --------------------------------------------------------
    # LEARNING GUIDE
    # --------------------------------------------------------

    with p3:

        if st.button(

            "📖 Learning Guide",

            use_container_width=True,

            key="learning_button"

        ):

            learning_dialog()


# ============================================================
# END OF APPLICATION
# ============================================================

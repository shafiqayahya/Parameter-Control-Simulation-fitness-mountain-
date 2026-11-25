
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64

from pathlib import Path
from html import escape


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Fitness Mountain",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# BACKGROUND IMAGE
# ==================================================

@st.cache_data
def load_background():

    path = Path(__file__).parent / "background.jpg"

    if path.exists():
        return base64.b64encode(
            path.read_bytes()
        ).decode()

    return ""


background = load_background()


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    f"""
<style>

.stApp {{
    background: #070B16;
    color: #E2E8F0;
}}

.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;

    background-image:
        linear-gradient(
            rgba(5, 10, 25, 0.86),
            rgba(5, 10, 25, 0.86)
        ),
        url("data:image/jpeg;base64,{background}");

    background-size: cover;
    background-position: center;
    filter: blur(4px);
    transform: scale(1.03);
    pointer-events: none;
    z-index: 0;
}}

[data-testid="stMain"] {{
    position: relative;
    z-index: 1;
    background: transparent;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stSidebar"] {{
    display: none;
}}

.block-container {{
    max-width: 1600px;
    padding-top: 2rem;
    padding-bottom: 1rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}}

[data-testid="stVerticalBlock"] {{
    gap: 0.5rem;
}}

[data-testid="stHorizontalBlock"] {{
    gap: 1rem;
}}


/* ==============================================
   HEADER
   ============================================== */

.hero {{
    text-align: center;
    padding-bottom: 14px;
}}

.hero-label {{
    color: #22D3EE;
    font-size: 10px;
    letter-spacing: 5px;
    font-weight: 700;
}}

.hero-title {{
    color: #E0F2FE;
    font-size: clamp(26px, 3vw, 38px);
    font-weight: 900;
    letter-spacing: 5px;
    line-height: 1.2;
    text-shadow: 0 0 22px #0891B2;
    margin: 5px 0;
}}

.hero-subtitle {{
    color: #94A3B8;
    font-size: 10px;
    letter-spacing: 3px;
}}


/* ==============================================
   SECTION LABEL
   ============================================== */

.section-label {{
    color: #67E8F9;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-top: 5px;
    margin-bottom: 5px;
}}


/* ==============================================
   CONTROL PANEL
   ============================================== */

[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: 12px;
}}

[data-testid="stRadio"] {{
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid #26394C;
    border-radius: 10px;
    padding: 8px 12px;
}}

[data-testid="stRadio"] label {{
    font-size: 13px;
}}

[data-testid="stRadio"] [role="radiogroup"] {{
    gap: 4px;
}}

.strategy-info {{
    background: rgba(15, 23, 42, 0.90);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 12px;
    line-height: 1.5;
    color: #CBD5E1;
    margin-bottom: 5px;
}}

[data-testid="stSlider"] {{
    padding-top: 4px;
    padding-bottom: 0;
}}


/* ==============================================
   STATISTIC CARDS
   ============================================== */

.metric-card {{
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid #26394C;
    border-radius: 12px;
    padding: 12px 16px;
    min-height: 78px;
    box-sizing: border-box;
}}

.metric-label {{
    color: #94A3B8;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.6px;
    margin-bottom: 7px;
}}

.metric-value {{
    font-size: 27px;
    font-weight: 800;
    line-height: 1.2;
}}


/* ==============================================
   BUTTONS
   ============================================== */

.stButton > button {{
    width: 100%;
    min-height: 36px;
    padding: 5px 12px;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid #334155;
    color: #67E8F9;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    transition: all 0.2s ease;
}}

.stButton > button[kind="primary"] {{
    background: #155E75;
    border-color: #22D3EE;
    color: #FFFFFF;
}}

.stButton > button:hover {{
    background: #164E63;
    border-color: #22D3EE;
    color: #FFFFFF;
    box-shadow: 0 0 10px #22D3EE33;
}}

.stButton > button:disabled {{
    opacity: 0.45;
    cursor: not-allowed;
}}


/* ==============================================
   FITNESS LANDSCAPE
   ============================================== */

[data-testid="stImage"] img {{
    border-radius: 12px;
    border: 1px solid #26394C;
}}

[data-testid="stProgress"] {{
    margin: 0;
}}


/* ==============================================
   LIVE FEEDBACK
   ============================================== */

.feedback-box {{
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid #334155;
    border-left: 4px solid #FBBF24;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 12px;
    line-height: 1.5;
    color: #E2E8F0;
    margin-top: 3px;
    margin-bottom: 5px;
}}

.feedback-title {{
    color: #FBBF24;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 6px;
}}


/* ==============================================
   MISSION
   ============================================== */

.mission {{
    color: #94A3B8;
    font-size: 11px;
    line-height: 1.5;
    padding: 3px 0;
}}

[data-testid="stCaptionContainer"] p {{
    color: #94A3B8;
    font-size: 11px;
    line-height: 1.4;
}}


/* ==============================================
   NAVIGATION
   ============================================== */

.navigation-divider {{
    border-top: 1px solid #26394C;
    margin: 6px 0 8px;
}}


/* ==============================================
   COMPACT DESKTOP
   ============================================== */

@media (max-height: 900px) {{

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 0.5rem;
    }}

    .hero {{
        padding-bottom: 8px;
    }}

    .hero-title {{
        font-size: 32px;
    }}

    [data-testid="stVerticalBlock"] {{
        gap: 0.35rem;
    }}

    .metric-card {{
        min-height: 68px;
        padding: 10px 14px;
    }}

    .metric-value {{
        font-size: 24px;
    }}

    .strategy-info {{
        padding: 8px 10px;
    }}

    .feedback-box {{
        padding: 9px 12px;
    }}

}}


/* ==============================================
   SMALLER SCREENS
   ============================================== */

@media (max-width: 900px) {{

    .block-container {{
        padding-left: 1rem;
        padding-right: 1rem;
    }}

    .hero-title {{
        font-size: 28px;
        letter-spacing: 3px;
    }}

    .metric-value {{
        font-size: 20px;
    }}

}}


/* ==================================================
   FINAL DASHBOARD SPACING FIX
   ================================================== */

/* MAIN CONTAINER */

.block-container {{
    max-width: 1600px;
    padding-top: 1.8rem !important;
    padding-bottom: 1rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}}


/* NORMALIZE COMPONENT SPACING */

[data-testid="stVerticalBlock"] {{
    gap: 0.65rem !important;
}}

[data-testid="stHorizontalBlock"] {{
    gap: 1rem !important;
    align-items: flex-start;
}}

[data-testid="stElementContainer"] {{
    min-height: 0;
    margin: 0 !important;
}}


/* HEADER */

.hero {{
    padding-top: 0;
    padding-bottom: 18px !important;
    margin-bottom: 6px;
}}

.hero-title {{
    font-size: 34px;
    line-height: 1.3;
    margin: 5px 0 8px;
}}

.hero-subtitle {{
    line-height: 1.5;
}}


/* SECTION LABELS */

.section-label {{
    display: block;
    font-size: 11px;
    line-height: 1.5;
    letter-spacing: 2px;
    font-weight: 700;
    padding: 0;
    margin: 2px 0 5px !important;
}}


/* LEFT CONTROL PANEL */

[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: 12px;
}}

[data-testid="stRadio"] {{
    display: block;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 10px 12px !important;
    margin: 0 !important;
}}

[data-testid="stRadio"] > div {{
    width: 100% !important;
}}

[data-testid="stRadio"] [role="radiogroup"] {{
    width: 100%;
    gap: 5px !important;
}}

[data-testid="stRadio"] label {{
    font-size: 13px;
    line-height: 1.5;
}}

[data-testid="stWidgetLabel"] {{
    margin-bottom: 5px !important;
}}


/* STRATEGY DESCRIPTION */

.strategy-info {{
    width: 100%;
    box-sizing: border-box;
    min-height: 0 !important;
    padding: 10px 12px !important;
    margin: 0 !important;
    line-height: 1.5;
    border-radius: 8px;
}}


/* MUTATION SLIDER */

[data-testid="stSlider"] {{
    width: 100%;
    padding-top: 2px !important;
    padding-bottom: 2px !important;
    margin: 0 !important;
}}

[data-testid="stSlider"] label {{
    line-height: 1.5;
}}


/* STATISTIC CARDS */

.metric-card {{
    width: 100%;
    min-height: 76px !important;
    height: auto;
    padding: 12px 15px !important;
    margin: 0 !important;
    box-sizing: border-box;
    background: rgba(15, 23, 42, 0.94);
    border: 1px solid #334155;
    border-radius: 10px;
}}

.metric-label {{
    font-size: 10px;
    line-height: 1.5;
    margin-bottom: 6px;
}}

.metric-value {{
    font-size: 25px !important;
    line-height: 1.25;
}}


/* GENERATION PROGRESS BAR */

[data-testid="stProgress"] {{
    padding-top: 3px !important;
    padding-bottom: 3px !important;
    margin: 0 !important;
}}


/* GAME BUTTONS */

.stButton {{
    width: 100%;
    margin: 0 !important;
}}

.stButton > button {{
    width: 100%;
    min-height: 36px !important;
    height: auto;
    padding: 7px 10px !important;
    margin: 0 !important;
    border-radius: 8px;
    font-size: 12px;
    line-height: 1.4;
}}

.stButton > button[kind="primary"] {{
    background: #155E75;
    border: 1px solid #22D3EE;
    color: #FFFFFF;
}}


/* FITNESS LANDSCAPE */

[data-testid="stImage"] {{
    width: 100%;
    margin: 0 !important;
    padding: 0 !important;
}}

[data-testid="stImage"] img {{
    display: block;
    max-width: 100%;
    border-radius: 10px;
    border: 1px solid #26394C;
}}


/* GRAPH LEGEND */

.graph-legend {{
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 6px 18px;
    font-size: 11px;
    line-height: 1.6;
    color: #94A3B8;
    padding: 4px 0;
    margin: 0;
    min-height: 24px;
    box-sizing: border-box;
}}

.graph-legend span {{
    display: inline-block;
    white-space: nowrap;
}}


/* LIVE EVOLUTION FEEDBACK */

.feedback-box {{
    display: block;
    width: 100%;
    height: auto;
    min-height: 60px;
    box-sizing: border-box;
    padding: 10px 14px !important;
    margin: 0 !important;
    background: rgba(15, 23, 42, 0.96);
    border: 1px solid #334155;
    border-left: 4px solid #FBBF24;
    border-radius: 10px;
    font-size: 12px;
    line-height: 1.5;
    overflow-wrap: anywhere;
}}

.feedback-title {{
    display: block;
    color: #FBBF24;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 700;
    line-height: 1.5;
    margin-bottom: 5px;
}}


/* MISSION */

.mission {{
    font-size: 11px;
    line-height: 1.6;
    padding: 0 0 3px;
    margin: 0;
    color: #94A3B8;
}}


/* CAPTION */

[data-testid="stCaptionContainer"] {{
    margin: 0 !important;
}}

[data-testid="stCaptionContainer"] p {{
    font-size: 11px;
    line-height: 1.5;
    margin: 0;
}}


/* BOTTOM NAVIGATION */

.navigation-divider {{
    border-top: 1px solid #26394C;
    margin: 8px 0 4px !important;
}}


/* RESPONSIVE DESKTOP */

@media (max-height: 900px) {{

    .block-container {{
        padding-top: 1.3rem !important;
        padding-bottom: 0.5rem !important;
    }}

    .hero {{
        padding-bottom: 10px !important;
        margin-bottom: 2px;
    }}

    [data-testid="stVerticalBlock"] {{
        gap: 0.5rem !important;
    }}

    .metric-card {{
        min-height: 68px !important;
        padding: 10px 14px !important;
    }}

    .metric-value {{
        font-size: 23px !important;
    }}

    .strategy-info {{
        padding: 8px 10px !important;
    }}

    .feedback-box {{
        padding: 9px 12px !important;
    }}

}}


/* RESPONSIVE SMALL SCREEN */

@media (max-width: 900px) {{

    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    .hero-title {{
        font-size: 26px;
        letter-spacing: 3px;
    }}

    .metric-value {{
        font-size: 20px !important;
    }}

}}

</style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# CONSTANTS
# ==================================================

MAX_GENERATIONS = 30
POPULATION_SIZE = 5

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


# ==================================================
# FITNESS FUNCTION
# ==================================================

def fitness(x):

    return (
        25
        + 40 * np.exp(-((x - 27) / 13) ** 2)
        + 75 * np.exp(-((x - 79) / 15) ** 2)
    )


# ==================================================
# RESET SIMULATION
# ==================================================

def reset_simulation(strategy, initial_sigma):

    st.session_state.generation = 0

    st.session_state.population = [
        (10.0, float(initial_sigma))
        for _ in range(POPULATION_SIZE)
    ]

    st.session_state.sigma = float(initial_sigma)

    st.session_state.history = [
        float(fitness(10))
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


# ==================================================
# EVOLUTION PROCESS
# ==================================================

def next_generation(strategy, initial_sigma):

    if st.session_state.generation >= MAX_GENERATIONS:
        return

    population = st.session_state.population
    sigma = st.session_state.sigma

    offspring = []
    successes = 0

    # ----------------------------------------------
    # MUTATION
    # ----------------------------------------------

    for x, individual_sigma in population:

        if strategy == "Self-Adaptive":

            child_sigma = np.clip(
                individual_sigma
                * np.exp(0.4 * np.random.normal()),
                0.5,
                50
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

    # ----------------------------------------------
    # SURVIVAL SELECTION
    # ----------------------------------------------

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

    # ----------------------------------------------
    # DETERMINISTIC CONTROL
    # ----------------------------------------------

    if strategy == "Deterministic":

        new_sigma = max(
            0.5,
            initial_sigma
            * (1 - generation / MAX_GENERATIONS)
        )

        feedback = (
            f"Generation {generation}: "
            f"Step size changed from "
            f"{sigma:.2f} to {new_sigma:.2f} "
            "according to the predefined schedule."
        )

    # ----------------------------------------------
    # ADAPTIVE CONTROL
    # ----------------------------------------------

    elif strategy == "Adaptive":

        if success_rate > 0.2:

            new_sigma = min(
                50,
                sigma * 1.25
            )

            action = "increased"

        elif success_rate < 0.2:

            new_sigma = max(
                0.5,
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

    # ----------------------------------------------
    # SELF-ADAPTIVE CONTROL
    # ----------------------------------------------

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

    st.session_state.sigma = float(new_sigma)

    st.session_state.feedback = feedback

    best_x = st.session_state.population[0][0]

    st.session_state.history.append(
        float(fitness(best_x))
    )

    st.session_state.sigma_history.append(
        float(new_sigma)
    )


# ==================================================
# REUSABLE UI COMPONENTS
# ==================================================

def section_label(text):

    st.markdown(
        f'<div class="section-label">'
        f'{escape(text)}'
        f'</div>',
        unsafe_allow_html=True
    )


def metric_card(label, value, color):

    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">'
        f'{escape(str(label))}'
        f'</div>'
        f'<div class="metric-value" '
        f'style="color:{color};">'
        f'{escape(str(value))}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ==================================================
# POP-UP: PERFORMANCE ANALYSIS
# ==================================================

@st.dialog("Performance Analysis", width="large")
def performance_dialog():

    st.subheader("Best Fitness Progress")

    st.line_chart(
        {
            "Best Fitness":
                st.session_state.history
        },
        color="#22D3EE",
        height=220
    )

    st.subheader("Mutation Step Size Progress")

    st.line_chart(
        {
            "Step Size":
                st.session_state.sigma_history
        },
        color="#D946EF",
        height=220
    )

    st.caption(
        "For Self-Adaptive Control, the graph "
        "shows the best individual's step size."
    )


# ==================================================
# POP-UP: POPULATION DETAILS
# ==================================================

@st.dialog("Population Details", width="large")
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
                    float(fitness(x)), 2
                ),
                "Step Size": round(
                    step_size, 2
                )
            }
        )

    st.table(population_data)

    st.caption(
        "The population contains the five "
        "fittest surviving individuals."
    )


# ==================================================
# POP-UP: LEARNING GUIDE
# ==================================================

@st.dialog("Learning Guide", width="large")
def learning_dialog():

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Deterministic",
            "Adaptive",
            "Self-Adaptive",
            "Challenge"
        ]
    )

    # ----------------------------------------------
    # DETERMINISTIC
    # ----------------------------------------------

    with tab1:

        st.subheader("Deterministic Control")

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

    # ----------------------------------------------
    # ADAPTIVE
    # ----------------------------------------------

    with tab2:

        st.subheader("Adaptive Control")

        st.write(
            "Parameters change based on feedback "
            "from the search process."
        )

        st.markdown("**1/5 Success Rule**")

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

    # ----------------------------------------------
    # SELF-ADAPTIVE
    # ----------------------------------------------

    with tab3:

        st.subheader("Self-Adaptive Control")

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

    # ----------------------------------------------
    # CHALLENGE
    # ----------------------------------------------

    with tab4:

        st.subheader("Your Mission")

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


# ==================================================
# HEADER
# ==================================================

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


# ==================================================
# SINGLE SCREEN LAYOUT
# ==================================================

left, right = st.columns(
    [1, 3],
    gap="medium"
)



# ==================================================
# LEFT PANEL — GAME CONTROLS
# ==================================================

with left:

    # ==============================================
    # 01 — CONTROL PANEL
    # ==============================================

    with st.container(border=True, key="control_panel"):

        section_label("01 / CONTROL PANEL")

        strategy = st.radio(
            "Parameter Control Strategy",
            options=list(STRATEGIES.keys()),
            format_func=lambda name: (
                f'{STRATEGIES[name]["icon"]} {name}'
            ),
            key="selected_strategy"
        )

        accent = STRATEGIES[strategy]["color"]

        description = STRATEGIES[strategy]["description"]

        st.markdown(
            f'<div class="strategy-info" '
            f'style="border-left:3px solid {accent};">'
            f'<strong style="color:{accent};">'
            f'{strategy} Control'
            f'</strong>'
            f'<div style="margin-top:5px;">'
            f'{description}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        initial_sigma = st.slider(
            "Initial Mutation Step Size (σ)",
            min_value=1,
            max_value=30,
            value=15
        )

        st.caption(
            "Large σ: exploration | "
            "Small σ: refinement"
        )

    # ==============================================
    # INITIALIZE SESSION
    # ==============================================

    settings = (
        strategy,
        initial_sigma
    )

    if (
        "generation" not in st.session_state
        or st.session_state.get("settings") != settings
        or "sigma_history" not in st.session_state
    ):

        reset_simulation(
            strategy,
            initial_sigma
        )

    finished = (
        st.session_state.generation >= MAX_GENERATIONS
    )

    # ==============================================
    # 02 — GAME CONTROLS
    # ==============================================

    with st.container(border=True, key="game_panel"):

        section_label("02 / GAME CONTROLS")

        if st.button(
            "▶ Next Generation",
            type="primary",
            disabled=finished,
            use_container_width=True
        ):

            next_generation(
                strategy,
                initial_sigma
            )

            st.rerun()

        run_col, reset_col = st.columns(2)

        with run_col:

            if st.button(
                "⏩ Run All",
                disabled=finished,
                use_container_width=True
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
                use_container_width=True
            ):

                reset_simulation(
                    strategy,
                    initial_sigma
                )

                st.rerun()

    # ==============================================
    # 03 — YOUR MISSION
    # ==============================================

    with st.container(border=True, key="mission_panel"):

        section_label("03 / YOUR MISSION")

        st.markdown(
            '<div class="mission">'
            'Reach the highest fitness peak within '
            '30 generations. Compare how different '
            'strategies control mutation step size.'
            '</div>',
            unsafe_allow_html=True
        )

# ==================================================
# RIGHT PANEL — GAME DISPLAY
# ==================================================

with right:

    best_x = st.session_state.population[0][0]

    best_fitness = float(
        fitness(best_x)
    )

    generation = st.session_state.generation

    # ----------------------------------------------
    # STATISTIC CARDS
    # ----------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        metric_card(
            "GENERATION",
            f"{generation}/{MAX_GENERATIONS}",
            "#67E8F9"
        )

    with m2:

        metric_card(
            "BEST FITNESS",
            f"{best_fitness:.2f}",
            "#FBBF24"
        )

    with m3:

        metric_card(
            "BEST σ"
            if strategy == "Self-Adaptive"
            else "NEXT STEP SIZE (σ)",
            f"{st.session_state.sigma:.2f}",
            "#E879F9"
        )

    with m4:

        metric_card(
            "BEST POSITION",
            f"{best_x:.2f}",
            "#67E8F9"
        )

    # ----------------------------------------------
    # GENERATION PROGRESS
    # ----------------------------------------------

    st.progress(
        generation / MAX_GENERATIONS
    )

    # ----------------------------------------------
    # FITNESS LANDSCAPE
    # ----------------------------------------------

    section_label("04 / FITNESS LANDSCAPE")

    x_values = np.linspace(
        0,
        100,
        500
    )

    y_values = fitness(x_values)

    fig, ax = plt.subplots(
        figsize=(12, 2.6),
        dpi=120
    )

    fig.patch.set_facecolor("#080F20")

    ax.set_facecolor("#080F20")

    # ----------------------------------------------
    # MOUNTAIN AREA
    # ----------------------------------------------

    ax.fill_between(
        x_values,
        y_values,
        color="#22D3EE",
        alpha=0.12
    )

    # ----------------------------------------------
    # NEON GLOW
    # ----------------------------------------------

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

    # ----------------------------------------------
    # POPULATION MEMBERS
    # ----------------------------------------------

    for x, individual_sigma in (
        st.session_state.population
    ):

        ax.scatter(
            x,
            fitness(x),
            color="#38BDF8",
            s=35,
            alpha=0.8,
            zorder=5
        )

    # ----------------------------------------------
    # BEST INDIVIDUAL GLOW
    # ----------------------------------------------

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
        edgecolors="white",
        linewidths=1.2,
        s=75,
        zorder=7
    )

    # ----------------------------------------------
    # LOCAL OPTIMUM
    # ----------------------------------------------

    ax.annotate(
        "LOCAL OPTIMUM",
        xy=(27, fitness(27)),
        xytext=(27, 86),
        color="#CBD5E1",
        fontsize=9,
        ha="center",
        arrowprops=dict(
            color="#94A3B8",
            arrowstyle="->"
        )
    )

    # ----------------------------------------------
    # GLOBAL OPTIMUM
    # ----------------------------------------------

    ax.scatter(
        79,
        fitness(79),
        marker="*",
        color="#FBBF24",
        s=150,
        zorder=4
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
            arrowstyle="->"
        )
    )

    # ----------------------------------------------
    # GRAPH FORMATTING
    # ----------------------------------------------

    ax.set_xlim(0, 100)

    ax.set_ylim(0, 128)

    ax.set_xlabel(
        "Search Space — Candidate Solution (x)",
        color="#94A3B8",
        fontsize=9
    )

    ax.set_ylabel(
        "Fitness",
        color="#94A3B8",
        fontsize=9
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

        spine.set_color("#1E3A4C")

    fig.tight_layout(pad=1.2)

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)

   
    # ----------------------------------------------
    # GRAPH LEGEND
    # ----------------------------------------------

    st.markdown(
        '<div class="graph-legend">'
        '<span>'
        '<b style="color:#38BDF8;">●</b> '
        'Population members'
        '</span>'
        '<span>'
        f'<b style="color:{accent};">◉</b> '
        'Best individual'
        '</span>'
        '<span>'
        '<b style="color:#FBBF24;">★</b> '
        'Global optimum'
        '</span>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # ----------------------------------------------
    # LIVE EVOLUTION FEEDBACK
    # ----------------------------------------------

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
        f'{escape(feedback)}'
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# BOTTOM NAVIGATION
# ==================================================

st.markdown(
    '<div class="navigation-divider"></div>',
    unsafe_allow_html=True
)

p1, p2, p3 = st.columns(3)

with p1:

    if st.button(
        "📊 Performance Analysis",
        use_container_width=True
    ):

        performance_dialog()

with p2:

    if st.button(
        "🧬 Population Details",
        use_container_width=True
    ):

        population_dialog()

with p3:

    if st.button(
        "📖 Learning Guide",
        use_container_width=True
    ):

        learning_dialog()

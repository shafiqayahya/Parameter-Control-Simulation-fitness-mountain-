
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
# BACKGROUND
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
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;

        background-image:
            linear-gradient(
                rgba(5, 10, 25, 0.85),
                rgba(5, 10, 25, 0.85)
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
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 0.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}

    [data-testid="stVerticalBlock"] {{
        gap: 0.45rem;
    }}

    [data-testid="stHorizontalBlock"] {{
        gap: 1rem;
    }}

    /* HEADER */

    .hero {{
        text-align: center;
        padding: 0 0 8px;
    }}

    .hero-label {{
        color: #22D3EE;
        font-size: 10px;
        letter-spacing: 5px;
        font-weight: 600;
    }}

    .hero-title {{
        color: #E0F2FE;
        font-size: clamp(26px, 3vw, 40px);
        font-weight: 900;
        letter-spacing: 4px;
        line-height: 1.2;
        text-shadow: 0 0 22px #0891B2;
        margin: 4px 0;
    }}

    .hero-subtitle {{
        color: #94A3B8;
        font-size: 11px;
        letter-spacing: 2px;
    }}

    /* SECTION TITLE */

    .section-label {{
        color: #67E8F9;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 4px 0;
    }}

    /* CONTROL PANEL */

    .strategy-info {{
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 12px;
        line-height: 1.5;
        color: #CBD5E1;
        min-height: 70px;
    }}

    [data-testid="stRadio"] label {{
        font-size: 14px;
    }}

    /* STATISTICS */

    [data-testid="stMetric"] {{
        background: rgba(15, 23, 42, 0.90);
        border: 1px solid #164E63;
        border-radius: 10px;
        padding: 10px 14px;
        min-height: 75px;
    }}

    [data-testid="stMetricValue"] {{
        color: #67E8F9;
        font-size: 26px;
        font-weight: 700;
    }}

    [data-testid="stMetricLabel"] {{
        color: #CBD5E1;
    }}

    [data-testid="stMetricLabel"] p {{
        font-size: 11px;
    }}

    /* BUTTONS */

    .stButton > button {{
        width: 100%;
        min-height: 36px;
        padding: 5px 12px;
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid #22D3EE;
        color: #67E8F9;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
    }}

    .stButton > button:hover {{
        background: #164E63;
        border-color: #67E8F9;
        color: white;
        box-shadow: 0 0 12px #0891B255;
    }}

    .stButton > button[kind="primary"] {{
        background: #155E75;
        color: white;
    }}

    .stButton > button:disabled {{
        opacity: 0.45;
        cursor: not-allowed;
    }}

    /* FEEDBACK */

    .feedback-box {{
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid #334155;
        border-left: 4px solid #FBBF24;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 12px;
        line-height: 1.5;
        color: #E2E8F0;
    }}

    .feedback-title {{
        color: #FBBF24;
        font-size: 10px;
        letter-spacing: 2px;
        font-weight: 700;
        margin-bottom: 5px;
    }}

    .mission {{
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.5;
        padding: 4px 0;
    }}

    [data-testid="stCaptionContainer"] p {{
        font-size: 11px;
    }}

    [data-testid="stProgress"] {{
        margin: 0;
    }}

    [data-testid="stImage"] img {{
        border-radius: 10px;
    }}

    /* SMALLER SCREENS */

    @media (max-width: 900px) {{
        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}

        .hero-title {{
            font-size: 28px;
        }}
    }}

    
/* ==================================================
   FINAL UI REFINEMENT
   ================================================== */

.block-container {{
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}}

/* HEADER SPACING */

.hero {{
    padding-bottom: 14px;
}}

.hero-title {{
    font-size: 36px;
    letter-spacing: 5px;
    margin: 5px 0;
}}

.hero-subtitle {{
    font-size: 10px;
    letter-spacing: 3px;
}}

/* GENERAL SPACING */

[data-testid="stVerticalBlock"] {{
    gap: 0.55rem;
}}

[data-testid="stHorizontalBlock"] {{
    gap: 1rem;
}}

/* SECTION LABEL */

.section-label {{
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 6px;
    margin-bottom: 5px;
}}

/* CONTROL PANEL */

[data-testid="stRadio"] {{
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid #26394C;
    border-radius: 10px;
    padding: 10px 14px;
}}

[data-testid="stRadio"] label {{
    font-size: 13px;
}}

[data-testid="stRadio"] [role="radiogroup"] {{
    gap: 6px;
}}

.strategy-info {{
    min-height: 0;
    padding: 10px 14px;
    margin-bottom: 5px;
    background: rgba(15, 23, 42, 0.88);
    border-radius: 8px;
    line-height: 1.5;
}}

/* SLIDER */

[data-testid="stSlider"] {{
    padding-top: 5px;
    padding-bottom: 0;
}}

/* STATISTIC CARDS */

[data-testid="stMetric"] {{
    background: rgba(15, 23, 42, 0.90);
    border: 1px solid #26394C;
    border-radius: 12px;
    padding: 12px 16px;
    min-height: 78px;
}}

[data-testid="stMetricLabel"] p {{
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.5px;
    color: #94A3B8;
}}

[data-testid="stMetricValue"] {{
    font-size: 27px;
    font-weight: 700;
    line-height: 1.2;
}}

/* BEST FITNESS */

[data-testid="stHorizontalBlock"]
> [data-testid="stColumn"]:nth-child(2)
[data-testid="stMetricValue"] {{
    color: #FBBF24;
}}

/* MUTATION STEP SIZE */

[data-testid="stHorizontalBlock"]
> [data-testid="stColumn"]:nth-child(3)
[data-testid="stMetricValue"] {{
    color: #E879F9;
}}

/* GAME BUTTONS */

.stButton > button {{
    min-height: 36px;
    border-radius: 8px;
    border: 1px solid #334155;
    background: rgba(15, 23, 42, 0.95);
    color: #CBD5E1;
    font-size: 12px;
    font-weight: 600;
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
    box-shadow: 0 0 10px #22D3EE22;
}}

/* FITNESS LANDSCAPE */

[data-testid="stImage"] img {{
    border-radius: 12px;
    border: 1px solid #26394C;
}}

/* LIVE FEEDBACK */

.feedback-box {{
    padding: 12px 16px;
    border-radius: 10px;
    margin-top: 3px;
    margin-bottom: 8px;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid #334155;
    border-left: 3px solid #FBBF24;
}}

.feedback-title {{
    font-size: 10px;
    letter-spacing: 2px;
    margin-bottom: 6px;
}}

/* MISSION */

.mission {{
    font-size: 11px;
    line-height: 1.5;
    color: #94A3B8;
}}

/* CAPTIONS */

[data-testid="stCaptionContainer"] p {{
    color: #94A3B8;
    font-size: 11px;
    line-height: 1.4;
}}

/* COMPACT DESKTOP HEIGHT */

@media (max-height: 900px) {{

    .block-container {{
        padding-top: 1rem;
        padding-bottom: 0.5rem;
    }}

    .hero {{
        padding-bottom: 8px;
    }}

    .hero-title {{
        font-size: 32px;
    }}

    [data-testid="stVerticalBlock"] {{
        gap: 0.4rem;
    }}

    [data-testid="stMetric"] {{
        min-height: 68px;
        padding: 10px 14px;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 24px;
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
        "description":
            "Step size changes according to a "
            "predefined generation schedule."
    },

    "Adaptive": {
        "icon": "⚡",
        "color": "#FBBF24",
        "description":
            "Step size changes based on mutation "
            "success using the 1/5 Success Rule."
    },

    "Self-Adaptive": {
        "icon": "🧬",
        "color": "#D946EF",
        "description":
            "Each individual evolves its own "
            "encoded mutation step size."
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

    # Mutation

    for x, individual_sigma in population:

        if strategy == "Self-Adaptive":

            child_sigma = np.clip(
                individual_sigma *
                np.exp(0.4 * np.random.normal()),
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
            (float(child_x), float(child_sigma))
        )

        if fitness(child_x) > fitness(x):
            successes += 1

    # Survival selection

    combined = population + offspring

    combined.sort(
        key=lambda individual:
            fitness(individual[0]),
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
            initial_sigma *
            (1 - generation / MAX_GENERATIONS)
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

            new_sigma = min(50, sigma * 1.25)
            action = "increased"

        elif success_rate < 0.2:

            new_sigma = max(0.5, sigma * 0.8)
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

    st.table([
        {
            "Individual": i + 1,

            "Position": round(x, 2),

            "Fitness": round(
                float(fitness(x)), 2
            ),

            "Step Size": round(
                individual_sigma
                if current_strategy == "Self-Adaptive"
                else st.session_state.sigma,
                2
            )
        }

        for i, (x, individual_sigma)
        in enumerate(st.session_state.population)
    ])

    st.caption(
        "The population contains the five "
        "fittest surviving individuals."
    )

# ==================================================
# POP-UP: LEARNING GUIDE
# ==================================================

@st.dialog("Learning Guide", width="large")
def learning_dialog():

    tab1, tab2, tab3, tab4 = st.tabs([
        "Deterministic",
        "Adaptive",
        "Self-Adaptive",
        "Challenge"
    ])

    with tab1:

        st.markdown("""
        ### Deterministic Control

        Parameters change according to a
        predefined schedule.

        - No feedback from the search.
        - Large step sizes encourage exploration.
        - Smaller step sizes encourage refinement.
        """)

        st.latex(
            r"\sigma_t = "
            r"\max(0.5,\sigma_0(1-t/T))"
        )

    with tab2:

        st.markdown("""
        ### Adaptive Control

        Parameters change based on feedback
        from the search process.

        **1/5 Success Rule**
        """)

        st.table([
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
        ])

    with tab3:

        st.markdown("""
        ### Self-Adaptive Control

        Each individual carries its own
        mutation step size.

        The parameter evolves together with
        the candidate solution through mutation
        and survival selection.
        """)

        st.latex(
            r"\sigma' = \sigma e^{0.4N(0,1)}"
        )

    with tab4:

        st.markdown("""
        ### Your Mission

        Reach a fitness value of at least 99.9
        within 30 generations.

        1. Select a parameter control strategy.
        2. Choose an initial mutation step size.
        3. Run the simulation.
        4. Observe the fitness and step size.
        5. Repeat using another strategy.

        **Discussion**

        - Which strategy reached the highest peak?
        - How did the mutation step size change?
        - Did the population get trapped at
          a local optimum?

        Results may differ because mutation
        involves randomness.
        """)

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

with left, st.container(border=True):

    st.markdown(
        '<div class="section-label">'
        '01 / CONTROL PANEL'
        '</div>',
        unsafe_allow_html=True
    )

    strategy = st.radio(
        "Parameter Control Strategy",

        options=list(STRATEGIES.keys()),

        format_func=lambda name:
            f'{STRATEGIES[name]["icon"]} {name}',

        key="selected_strategy"
    )

    accent = STRATEGIES[strategy]["color"]

    description = STRATEGIES[strategy]["description"]

    st.markdown(
        f'<div class="strategy-info" '
        f'style="border-left:3px solid {accent};">'
        f'<strong style="color:{accent};">'
        f'{strategy} Control'
        f'</strong><br>'
        f'{description}'
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
        "Large σ: exploration | Small σ: refinement"
    )

    # Initialize or reset when settings change

    settings = (strategy, initial_sigma)

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
        st.session_state.generation
        >= MAX_GENERATIONS
    )

    st.markdown(
        '<div class="section-label">'
        '02 / GAME CONTROLS'
        '</div>',
        unsafe_allow_html=True
    )

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

    st.markdown(
        '<div class="section-label">'
        '03 / YOUR MISSION'
        '</div>'
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

    best_fitness = float(fitness(best_x))

    generation = st.session_state.generation

    # ----------------------------------------------
    # STATISTICS
    # ----------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "GENERATION",
        f"{generation}/30"
    )

    m2.metric(
        "BEST FITNESS",
        f"{best_fitness:.2f}"
    )

    m3.metric(
        "BEST σ"
        if strategy == "Self-Adaptive"
        else "NEXT STEP SIZE (σ)",
        f"{st.session_state.sigma:.2f}"
    )

    m4.metric(
        "BEST POSITION",
        f"{best_x:.2f}"
    )

    st.progress(
        generation / MAX_GENERATIONS
    )

    # ----------------------------------------------
    # FITNESS LANDSCAPE
    # ----------------------------------------------

    st.markdown(
        '<div class="section-label">'
        '04 / FITNESS LANDSCAPE'
        '</div>',
        unsafe_allow_html=True
    )

    x_values = np.linspace(0, 100, 500)

    y_values = fitness(x_values)

   fig, ax = plt.subplots(
    figsize=(12, 2.8),
    dpi=120
    )

    fig.patch.set_facecolor("#080F20")

    ax.set_facecolor("#080F20")

    # Mountain area

    ax.fill_between(
        x_values,
        y_values,
        color="#22D3EE",
        alpha=0.12
    )

    # Neon glow

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

    # Population members

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

    # Best individual glow

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

    # Local optimum

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

    # Global optimum

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

    st.caption(
        "● Population members  |  "
        "◉ Best individual  |  "
        "★ Global optimum"
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
# BOTTOM NAVIGATION — POP-UP BUTTONS
# ==================================================

st.markdown(
    '<div style="border-top:1px solid #26394C;'
    'margin:6px 0 8px;"></div>',
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

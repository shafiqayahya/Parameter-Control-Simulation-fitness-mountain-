
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64
from pathlib import Path

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
# BACKGROUND AND CUSTOM UI
# ==================================================

image_path = Path(__file__).parent / "background.jpg"

encoded = ""

if image_path.exists():
    encoded = base64.b64encode(
        image_path.read_bytes()
    ).decode()

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: #070B16;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(
                rgba(5, 10, 25, 0.92),
                rgba(5, 10, 25, 0.92)
            ),
            url("data:image/jpeg;base64,{encoded}");
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

    .block-container {{
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    [data-testid="stSidebar"] {{
        display: none;
    }}

    .hero {{
        text-align: center;
        padding: 25px 10px 30px;
    }}

    .hero-label {{
        color: #22D3EE;
        font-size: 12px;
        letter-spacing: 5px;
        font-weight: 600;
    }}

    .hero-title {{
        font-size: clamp(32px, 6vw, 60px);
        font-weight: 900;
        letter-spacing: 4px;
        color: #E0F2FE;
        text-shadow: 0 0 25px #0891B2;
        margin: 8px 0;
    }}

    .hero-subtitle {{
        color: #94A3B8;
        font-size: 14px;
        letter-spacing: 3px;
    }}

    .mission {{
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #164E63;
        border-left: 4px solid #22D3EE;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 22px;
        color: #CBD5E1;
    }}

    .section-label {{
        color: #67E8F9;
        font-size: 12px;
        letter-spacing: 3px;
        font-weight: 700;
        margin-top: 18px;
        margin-bottom: 12px;
    }}

    .strategy-card {{
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 10px;
        text-align: center;
        min-height: 120px;
    }}

    .strategy-icon {{
        font-size: 28px;
        margin-bottom: 8px;
    }}

    .strategy-title {{
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 6px;
    }}

    .strategy-description {{
        color: #94A3B8;
        font-size: 12px;
    }}

    [data-testid="stMetric"] {{
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(34, 211, 238, 0.25);
        border-radius: 12px;
        padding: 18px;
        min-height: 110px;
    }}

    [data-testid="stMetricValue"] {{
        color: #67E8F9;
        font-weight: 700;
    }}

    [data-testid="stMetricLabel"] {{
        color: #CBD5E1;
    }}

    .stButton > button {{
        width: 100%;
        min-height: 48px;
        background: #101827;
        border: 1px solid #22D3EE;
        color: #67E8F9;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.2s;
    }}

    .stButton > button:hover {{
        background: #164E63;
        border-color: #67E8F9;
        color: white;
        box-shadow: 0 0 15px #0891B255;
    }}

    .stButton > button:disabled {{
        opacity: 0.4;
    }}

    [data-testid="stExpander"] {{
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #334155;
        border-radius: 12px;
    }}

    .feedback-box {{
        background: rgba(15, 23, 42, 0.90);
        border: 1px solid #334155;
        border-left: 4px solid #FBBF24;
        border-radius: 10px;
        padding: 18px;
        color: #E2E8F0;
        margin-bottom: 15px;
    }}

    .footer {{
        text-align: center;
        color: #64748B;
        font-size: 11px;
        letter-spacing: 2px;
        padding: 25px 0;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# HEADER
# ==================================================

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

    <div class="mission">
        <strong style="color:#67E8F9;">
            YOUR MISSION
        </strong><br>
        Evolve your population and reach the highest
        fitness peak. Explore how different parameter
        control strategies influence the search
        for an optimal solution.
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# FITNESS FUNCTION
# ==================================================

def fitness(x):
    return (
        25
        + 40 * np.exp(-((x - 27) / 13) ** 2)
        + 75 * np.exp(-((x - 79) / 15) ** 2)
    )


MAX_GENERATIONS = 30
POPULATION_SIZE = 5

# ==================================================
# STRATEGY SELECTION
# ==================================================

st.markdown(
    '<div class="section-label">'
    '01 / SELECT YOUR STRATEGY</div>',
    unsafe_allow_html=True
)

strategies = {
    "Deterministic": {
        "icon": "⏱️",
        "color": "#22D3EE",
        "description": "Time-based control"
    },
    "Adaptive": {
        "icon": "⚡",
        "color": "#FBBF24",
        "description": "Feedback-based control"
    },
    "Self-Adaptive": {
        "icon": "🧬",
        "color": "#D946EF",
        "description": "Evolution-based control"
    }
}

if "strategy" not in st.session_state:
    st.session_state.strategy = "Deterministic"

columns = st.columns(3)

for column, (name, details) in zip(
    columns, strategies.items()
):

    with column:

        selected = st.session_state.strategy == name

        border = (
            details["color"]
            if selected
            else "#334155"
        )

        st.markdown(
            f"""
            <div class="strategy-card"
                 style="border-color:{border};">

                <div class="strategy-icon">
                    {details["icon"]}
                </div>

                <div class="strategy-title"
                     style="color:{details["color"]};">
                    {name}
                </div>

                <div class="strategy-description">
                    {details["description"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Selected" if selected else "Select",
            key=f"select_{name}",
            disabled=selected,
            use_container_width=True
        ):
            st.session_state.strategy = name
            st.rerun()

strategy = st.session_state.strategy
accent = strategies[strategy]["color"]

descriptions = {
    "Deterministic":
        "The mutation step size decreases according "
        "to a predefined generation schedule.",

    "Adaptive":
        "The mutation step size changes based on "
        "search feedback using the 1/5 Success Rule.",

    "Self-Adaptive":
        "Each individual carries its own mutation "
        "step size, which evolves with its solution."
}

st.info(descriptions[strategy])

# ==================================================
# SIMULATION SETTINGS
# ==================================================

st.markdown(
    '<div class="section-label">'
    '02 / CONFIGURE YOUR PARAMETER</div>',
    unsafe_allow_html=True
)

initial_sigma = st.slider(
    "Initial Mutation Step Size (σ)",
    min_value=1,
    max_value=30,
    value=15
)

st.caption(
    "Large step size = broader exploration. "
    "Small step size = local refinement."
)

settings = (strategy, initial_sigma)

# ==================================================
# RESET SIMULATION
# ==================================================

def reset_simulation():

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
        "to evolve your population."
    )

    st.session_state.settings = settings


if (
    "generation" not in st.session_state
    or st.session_state.get("settings") != settings
    or "sigma_history" not in st.session_state
):
    reset_simulation()

# ==================================================
# EVOLUTION PROCESS
# ==================================================

def next_generation():

    if st.session_state.generation >= MAX_GENERATIONS:
        return

    population = st.session_state.population
    sigma = st.session_state.sigma

    offspring = []
    successes = 0

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
        key=lambda individual: fitness(individual[0]),
        reverse=True
    )

    st.session_state.population = combined[
        :POPULATION_SIZE
    ]

    st.session_state.generation += 1

    generation = st.session_state.generation
    success_rate = successes / POPULATION_SIZE

    # Deterministic Control

    if strategy == "Deterministic":

        new_sigma = max(
            0.5,
            initial_sigma *
            (1 - generation / MAX_GENERATIONS)
        )

        feedback = (
            f"Generation {generation}: "
            f"Mutation step size changed from "
            f"{sigma:.2f} to {new_sigma:.2f} "
            "according to the predefined schedule."
        )

    # Adaptive Control

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
            f"Mutation step size {action} "
            f"from {sigma:.2f} to {new_sigma:.2f}."
        )

    # Self-Adaptive Control

    else:

        new_sigma = st.session_state.population[0][1]

        feedback = (
            "Individuals mutated their own encoded "
            "step sizes. Fitter individuals survived "
            "together with their strategy parameters. "
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
# GAME CONTROLS
# ==================================================

st.markdown(
    '<div class="section-label">'
    '03 / EVOLUTION CHALLENGE</div>',
    unsafe_allow_html=True
)

finished = (
    st.session_state.generation >= MAX_GENERATIONS
)

b1, b2, b3 = st.columns(3)

with b1:

    if st.button(
        "▶ Next Generation",
        disabled=finished,
        use_container_width=True
    ):
        next_generation()
        st.rerun()

with b2:

    if st.button(
        "⏩ Run All",
        disabled=finished,
        use_container_width=True
    ):
        while (
            st.session_state.generation
            < MAX_GENERATIONS
        ):
            next_generation()

        st.rerun()

with b3:

    if st.button(
        "↻ Reset Simulation",
        use_container_width=True
    ):
        reset_simulation()
        st.rerun()

# ==================================================
# GAME STATISTICS
# ==================================================

best_x = st.session_state.population[0][0]
best_fitness = float(fitness(best_x))

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "GENERATION",
    f"{st.session_state.generation}/30"
)

m2.metric(
    "BEST FITNESS",
    f"{best_fitness:.2f}"
)

m3.metric(
    "BEST INDIVIDUAL σ"
    if strategy == "Self-Adaptive"
    else "NEXT STEP SIZE (σ)",
    f"{st.session_state.sigma:.2f}"
)

m4.metric(
    "BEST POSITION",
    f"{best_x:.2f}"
)

st.progress(
    st.session_state.generation / MAX_GENERATIONS
)

# ==================================================
# FITNESS LANDSCAPE
# ==================================================

st.markdown(
    '<div class="section-label">'
    '04 / FITNESS LANDSCAPE</div>',
    unsafe_allow_html=True
)

x_values = np.linspace(0, 100, 500)
y_values = fitness(x_values)

fig, ax = plt.subplots(figsize=(11, 4.2))

fig.patch.set_facecolor("#080F20")
ax.set_facecolor("#080F20")

# Mountain fill

ax.fill_between(
    x_values,
    y_values,
    color="#22D3EE",
    alpha=0.12
)

# Neon glow effect

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

# Population

for x, individual_sigma in st.session_state.population:

    ax.scatter(
        x,
        fitness(x),
        color="#38BDF8",
        s=45,
        alpha=0.85,
        zorder=5
    )

# Best individual glow

for size, alpha in [
    (650, 0.04),
    (350, 0.08),
    (180, 0.15)
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
    s=95,
    zorder=7,
    label="Best Individual"
)

# Local optimum

ax.annotate(
    "LOCAL OPTIMUM",
    xy=(27, fitness(27)),
    xytext=(27, 82),
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
    s=180,
    zorder=4
)

ax.annotate(
    "GLOBAL OPTIMUM",
    xy=(79, fitness(79)),
    xytext=(79, 116),
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
ax.set_ylim(0, 125)

ax.set_xlabel(
    "Search Space — Candidate Solution (x)",
    color="#94A3B8",
    labelpad=10
)

ax.set_ylabel(
    "Fitness Value",
    color="#94A3B8"
)

ax.tick_params(
    colors="#94A3B8",
    labelsize=9
)

ax.grid(
    color="#334155",
    linestyle="--",
    linewidth=0.5,
    alpha=0.5
)

for spine in ax.spines.values():
    spine.set_color("#1E3A4C")

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

st.caption(
    "Blue dots: population members  |  "
    "Highlighted dot: best individual  |  "
    "Gold star: global optimum"
)

# ==================================================
# LIVE FEEDBACK
# ==================================================

st.markdown(
    f"""
    <div class="feedback-box">

        <strong style="
            color:#FBBF24;
            letter-spacing:2px;
            font-size:12px;
        ">
            LIVE EVOLUTION FEEDBACK
        </strong>

        <br><br>

        {st.session_state.feedback}

    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# CHALLENGE RESULT
# ==================================================

if best_fitness >= 99.9:

    st.success(
        "🏆 MISSION ACCOMPLISHED! "
        "Your population has reached a "
        "near-global optimum."
    )

elif st.session_state.generation >= MAX_GENERATIONS:

    st.warning(
        "Simulation completed. Try another "
        "strategy or initial step size and "
        "compare the results."
    )

# ==================================================
# PERFORMANCE ANALYSIS
# ==================================================

with st.expander("📊 View Performance Analysis"):

    st.subheader("Fitness Progress")

    st.line_chart(
        {"Best Fitness": st.session_state.history},
        color="#22D3EE"
    )

    st.subheader("Mutation Step Size Progress")

    st.line_chart(
        {
            "Step Size":
            st.session_state.sigma_history
        },
        color="#D946EF"
    )

    st.caption(
        "For Self-Adaptive Control, the step size "
        "graph shows the best individual's parameter."
    )

# ==================================================
# POPULATION DETAILS
# ==================================================

with st.expander("🧬 View Population Details"):

    st.table([
        {
            "Individual": i + 1,
            "Position": round(x, 2),
            "Fitness": round(float(fitness(x)), 2),
            "Step Size": round(
                individual_sigma
                if strategy == "Self-Adaptive"
                else st.session_state.sigma,
                2
            )
        }
        for i, (x, individual_sigma)
        in enumerate(st.session_state.population)
    ])

# ==================================================
# LEARNING MATERIAL
# ==================================================

with st.expander("📖 Learning Guide"):

    st.markdown("""
    ### Deterministic Control

    Parameters change according to a predefined
    schedule without feedback from the search.

    ### Adaptive Control

    Parameters change based on search feedback.

    **1/5 Success Rule:**

    | Success Rate | Action |
    |---|---|
    | Above 20% | Increase step size |
    | Equal to 20% | Maintain step size |
    | Below 20% | Decrease step size |

    ### Self-Adaptive Control

    Each individual carries its own mutation
    step size in its chromosome.

    The parameter evolves together with the
    candidate solution through mutation and
    survival selection.

    ### Exploration vs Exploitation

    - Large mutation step size encourages
      broader exploration.
    - Small mutation step size encourages
      local refinement.

    ### Local vs Global Optimum

    - Local optimum: A solution better than
      nearby solutions.
    - Global optimum: The best solution
      within the entire search space.

    ### Try This Challenge

    1. Select Deterministic Control.
    2. Set the initial step size to 5.
    3. Press Run All and observe the result.
    4. Repeat using Adaptive Control.
    5. Repeat using Self-Adaptive Control.
    6. Compare fitness and step size progress.

    Results may differ between runs because
    mutation involves randomness.
    """)

# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        FITNESS MOUNTAIN
        &nbsp; | &nbsp;
        INTERACTIVE LEARNING SIMULATION
        <br><br>
        PARAMETER CONTROL IN EVOLUTIONARY ALGORITHMS
    </div>
    """,
    unsafe_allow_html=True
)


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Fitness Mountain",
    page_icon="⛰️",
    layout="wide"
)

st.title("⛰️ Fitness Mountain")
st.caption("Interactive Parameter Control Learning Simulator")

st.write(
    "Explore how different parameter control strategies "
    "influence the search for an optimal solution."
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

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Simulation Settings")

strategy = st.sidebar.radio(
    "Parameter Control Strategy",
    [
        "Deterministic",
        "Adaptive",
        "Self-Adaptive"
    ]
)

initial_sigma = st.sidebar.slider(
    "Initial Mutation Step Size (σ)",
    min_value=1,
    max_value=30,
    value=15
)

MAX_GENERATIONS = 30
POPULATION_SIZE = 5

descriptions = {
    "Deterministic":
        "Step size changes according to a predefined "
        "generation schedule without feedback.",

    "Adaptive":
        "Step size changes based on search performance "
        "using the 1/5 Success Rule.",

    "Self-Adaptive":
        "Each individual carries its own mutation "
        "step size, which evolves with its solution."
}

st.sidebar.info(descriptions[strategy])

# ==================================================
# SESSION STATE
# ==================================================

settings = (strategy, initial_sigma)

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

    st.session_state.feedback = (
        "Press Next Generation to begin."
    )

    st.session_state.settings = settings


if (
    "generation" not in st.session_state
    or st.session_state.get("settings") != settings
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

        # Self-adaptive parameter mutation
        if strategy == "Self-Adaptive":

            child_sigma = np.clip(
                individual_sigma *
                np.exp(0.4 * np.random.normal()),
                0.5,
                50
            )

        else:
            child_sigma = sigma

        # Gaussian mutation
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

    # ----------------------------------------------
    # DETERMINISTIC CONTROL
    # ----------------------------------------------

    if strategy == "Deterministic":

        new_sigma = max(
            0.5,
            initial_sigma *
            (1 - generation / MAX_GENERATIONS)
        )

        st.session_state.feedback = (
            f"Generation {generation}: "
            f"Step size changes from {sigma:.2f} "
            f"to {new_sigma:.2f} according to "
            "the predefined schedule."
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

        st.session_state.feedback = (
            f"Success rate: {success_rate:.0%}. "
            f"Step size {action} from "
            f"{sigma:.2f} to {new_sigma:.2f}."
        )

    # ----------------------------------------------
    # SELF-ADAPTIVE CONTROL
    # ----------------------------------------------

    else:

        new_sigma = st.session_state.population[0][1]

        st.session_state.feedback = (
            "Individuals mutate their own step sizes. "
            "Fitter solutions survive together with "
            "their encoded parameters."
        )

    st.session_state.sigma = float(new_sigma)

    best_x = st.session_state.population[0][0]

    st.session_state.history.append(
        float(fitness(best_x))
    )

# ==================================================
# CONTROL BUTTONS
# ==================================================

col1, col2, col3 = st.columns(3)

finished = (
    st.session_state.generation >= MAX_GENERATIONS
)

with col1:

    if st.button(
        "Next Generation",
        use_container_width=True,
        disabled=finished
    ):
        next_generation()

with col2:

    if st.button(
        "Run All",
        use_container_width=True,
        disabled=finished
    ):
        while (
            st.session_state.generation
            < MAX_GENERATIONS
        ):
            next_generation()

with col3:

    if st.button(
        "Reset",
        use_container_width=True
    ):
        reset_simulation()

# ==================================================
# PERFORMANCE METRICS
# ==================================================

best_x = st.session_state.population[0][0]
best_fitness = fitness(best_x)

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Generation",
    f"{st.session_state.generation}/30"
)

m2.metric(
    "Best Fitness",
    f"{best_fitness:.2f}"
)

m3.metric(
    "Mutation Step Size (σ)",
    f"{st.session_state.sigma:.2f}"
)

m4.metric(
    "Best Position",
    f"{best_x:.2f}"
)

# ==================================================
# FITNESS MOUNTAIN
# ==================================================

st.subheader("Fitness Landscape")

x_values = np.linspace(0, 100, 500)
y_values = fitness(x_values)

fig, ax = plt.subplots(figsize=(10, 4))

fig.patch.set_facecolor("#0E1117")
ax.set_facecolor("#0E1117")

ax.fill_between(
    x_values,
    y_values,
    color="#14B8A6",
    alpha=0.20
)

ax.plot(
    x_values,
    y_values,
    color="#2DD4BF",
    linewidth=2.5
)

# Population positions
for x, individual_sigma in st.session_state.population:

    ax.scatter(
        x,
        fitness(x),
        color="#38BDF8",
        s=60,
        zorder=4
    )

# Best individual
ax.scatter(
    best_x,
    best_fitness,
    color="#FBBF24",
    edgecolors="white",
    s=150,
    zorder=5,
    label="Best Individual"
)

ax.annotate(
    "Local Optimum",
    xy=(27, fitness(27)),
    xytext=(27, 78),
    color="white",
    ha="center",
    arrowprops=dict(color="white", arrowstyle="->")
)

ax.annotate(
    "Global Optimum",
    xy=(79, fitness(79)),
    xytext=(79, 115),
    color="#FBBF24",
    ha="center",
    arrowprops=dict(
        color="#FBBF24",
        arrowstyle="->"
    )
)

ax.set_xlim(0, 100)
ax.set_ylim(0, 125)

ax.set_xlabel(
    "Candidate Solution (x)",
    color="white"
)

ax.set_ylabel(
    "Fitness Value",
    color="white"
)

ax.tick_params(colors="white")
ax.grid(alpha=0.15)

for spine in ax.spines.values():
    spine.set_color("#475569")

st.pyplot(fig)
plt.close(fig)

st.caption(
    "Blue dots represent individuals. "
    "The yellow dot represents the best individual."
)

# ==================================================
# SIMULATION FEEDBACK
# ==================================================

st.subheader("Simulation Feedback")

st.info(st.session_state.feedback)

if best_fitness >= 99.9:

    st.success(
        "Challenge completed! The population has "
        "reached a near-global optimum."
    )

elif st.session_state.generation >= MAX_GENERATIONS:

    st.warning(
        "Simulation completed. Try another strategy "
        "or initial step size to compare the results."
    )

# ==================================================
# FITNESS HISTORY
# ==================================================

st.subheader("Fitness Progress")

st.line_chart(
    {"Best Fitness": st.session_state.history}
)

# ==================================================
# POPULATION DETAILS
# ==================================================

with st.expander("View Population Details"):

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

with st.expander("Understanding Parameter Control"):

    st.markdown("""
    ### Deterministic Control
    Parameters change according to a predefined
    schedule without feedback from the search.

    ### Adaptive Control
    Parameters change based on search feedback.

    **1/5 Success Rule:**
    - Success rate > 20%: Increase step size.
    - Success rate = 20%: Maintain step size.
    - Success rate < 20%: Decrease step size.

    ### Self-Adaptive Control
    Parameters are encoded within individuals
    and evolve through mutation and selection.

    ### Exploration and Exploitation
    - Large step size encourages broader exploration.
    - Small step size encourages local refinement.

    ### Local and Global Optimum
    - Local optimum: A solution better than nearby solutions.
    - Global optimum: The best solution in the search space.
    """)

st.divider()

st.caption(
    "Educational Simulation | "
    "Parameter Control in Evolutionary Algorithms"
)

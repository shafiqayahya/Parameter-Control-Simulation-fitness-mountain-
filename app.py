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


/* =========================================================
   FIXED SCREEN — NO SCROLL
   ========================================================= */

html,
body,
#root {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden !important;
    overscroll-behavior: none !important;
}

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

    height: 100dvh !important;
    max-height: 100dvh !important;

    overflow: hidden !important;
}

[data-testid="stHeader"] {
    background: transparent;
    height: 30px;
}

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    height: 100dvh !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
    overscroll-behavior: none !important;
}

.block-container {
    width: 100% !important;
    max-width: 1800px !important;

    height: 100dvh !important;
    max-height: 100dvh !important;

    padding: 10px 24px !important;
    margin: 0 auto !important;

    box-sizing: border-box;
    overflow: hidden !important;
}

.block-container >
[data-testid="stVerticalBlock"] {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 0;
    gap: 6px !important;
}

[data-testid="stVerticalBlock"] {
    gap: 6px !important;
}

[data-testid="stElementContainer"] {
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 14px !important;
}

[data-testid="stColumn"] {
    min-width: 0;
    min-height: 0;
}

[data-testid="stWidgetLabel"] p {
    color: #E2E8F0;
    font-size: 12px;
}

[data-testid="stWidgetLabel"] {
    min-height: 0 !important;
    margin-bottom: 0 !important;
}


/* =========================================================
   APPLICATION HEADER
   ========================================================= */

.hero {
    text-align: center;
    padding: 0 0 4px;
}

.hero-label {
    color: #22D3EE;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 4px;
    margin-bottom: 3px;
}

.hero-title {
    color: #E0F2FE;
    font-size: clamp(24px, 4dvh, 34px);
    font-weight: 900;
    letter-spacing: 5px;
    line-height: 1.1;
    margin-bottom: 4px;
    text-shadow: 0 0 22px #0891B2;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 9px;
    letter-spacing: 3px;
}


/* =========================================================
   WELCOME SCREEN
   ========================================================= */

.st-key-welcome_screen {
    width: 100%;
    max-width: 720px;

    margin: auto !important;
    padding: 16px 24px !important;

    background: rgba(8, 13, 28, 0.96);

    border: 1px solid #164E63;
    border-radius: 18px;

    box-shadow:
        0 0 45px rgba(34, 211, 238, 0.10);

    box-sizing: border-box;
}

.welcome-label {
    color: #22D3EE;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 4px;
    text-align: center;
    margin-bottom: 6px;
}

.welcome-title {
    color: #E0F2FE;
    font-size: clamp(25px, 4dvh, 38px);
    font-weight: 900;
    letter-spacing: 4px;
    line-height: 1.2;
    text-align: center;
    text-shadow: 0 0 24px #0891B2;
}

.welcome-subtitle {
    color: #94A3B8;
    font-size: 10px;
    letter-spacing: 2px;
    text-align: center;
    margin: 6px 0;
}

.welcome-mountain {
    display: block;
    width: 100%;
    max-width: 440px;
    height: 15dvh;
    max-height: 115px;
    object-fit: contain;
    margin: 0 auto;
}

.welcome-mission {
    color: #FBBF24;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 2px;
    text-align: center;
    margin: 4px 0;
}

.welcome-mission-text {
    color: #CBD5E1;
    font-size: 12px;
    line-height: 1.4;
    text-align: center;
    margin-bottom: 8px;
}

.instructions-heading {
    color: #67E8F9;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-align: center;
    margin-bottom: 6px;
}

.instruction-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 10px;
    margin-bottom: 5px;
    border: 1px solid #29384C;
    border-radius: 9px;
    background: rgba(17, 24, 39, 0.90);
}

.instruction-number {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 32px;
    height: 32px;
    flex-shrink: 0;

    border: 1px solid #155E75;
    border-radius: 8px;

    background: rgba(34, 211, 238, 0.08);
    color: #22D3EE;

    font-size: 14px;
    font-weight: 800;
}

.instruction-content {
    flex: 1;
    min-width: 0;
}

.instruction-title {
    color: #E2E8F0;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 2px;
}

.instruction-text {
    color: #94A3B8;
    font-size: 11px;
    line-height: 1.35;
}

.st-key-start_game_button button {
    min-height: 38px !important;
    font-weight: 800 !important;
    letter-spacing: 2px;

    background: linear-gradient(
        90deg,
        #155E75,
        #0E7490
    ) !important;

    border: 1px solid #22D3EE !important;
    color: #FFFFFF !important;
}


/* =========================================================
   MAIN DASHBOARD
   ========================================================= */

.st-key-main_dashboard {
    width: 100%;
    min-width: 0;
    min-height: 0;
    flex: 1 1 auto;
}

.st-key-left_panel
[data-testid="stVerticalBlock"],

.st-key-right_panel
[data-testid="stVerticalBlock"] {
    gap: 6px !important;
}

.section-heading {
    color: #67E8F9;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    line-height: 1.2;
    margin: 0;
}


/* =========================================================
   RADIO BUTTONS
   ========================================================= */

.st-key-left_panel [role="radiogroup"] {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 0;
    padding: 5px 9px;
    border: 1px solid #29384C;
    border-radius: 9px;
    background: rgba(17, 24, 39, 0.85);
    box-sizing: border-box;
}

.st-key-left_panel [role="radiogroup"] label {
    margin: 0 !important;
    padding: 0 !important;
    min-height: 23px;
}

.st-key-left_panel [role="radiogroup"] p {
    color: #E2E8F0;
    font-size: 12px;
    line-height: 1.2;
}


/* =========================================================
   STRATEGY DESCRIPTION
   ========================================================= */

.strategy-description {
    background: rgba(17, 24, 39, 0.94);
    border: 1px solid #29384C;
    border-radius: 8px;
    padding: 7px 10px;
}

.strategy-description-title {
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 3px;
}

.strategy-description-text {
    color: #CBD5E1;
    font-size: 11px;
    line-height: 1.35;
}


/* =========================================================
   SLIDER
   ========================================================= */

.st-key-left_panel
[data-testid="stSlider"] {
    padding: 0 !important;
    margin: 0 !important;
}

.slider-help {
    color: #94A3B8;
    font-size: 10px;
    line-height: 1.35;
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
    min-height: 32px !important;
    padding: 4px 8px !important;
    margin: 0 !important;

    background: rgba(17, 24, 39, 0.96);
    border: 1px solid #29384C;
    border-radius: 8px;

    color: #67E8F9;
    font-weight: 600;
}

.stButton > button p {
    font-size: 12px;
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
    opacity: 0.45;
    cursor: not-allowed;
}


/* =========================================================
   MISSION OBJECTIVE
   ========================================================= */

.mission-card {
    background: rgba(17, 24, 39, 0.78);
    border: 1px solid #29384C;
    border-radius: 8px;
    padding: 7px 10px;
}

.mission-title {
    color: #67E8F9;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.6px;
    margin-bottom: 4px;
}

.mission-text {
    color: #A8BED3;
    font-size: 10px;
    line-height: 1.4;
}

.mission-target {
    color: #FBBF24;
    font-weight: 800;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

.metric-grid {
    display: grid;
    grid-template-columns:
        repeat(5, minmax(0, 1fr));
    gap: 8px;
    width: 100%;
}

.metric-card {
    display: flex;
    flex-direction: column;
    justify-content: center;

    background: rgba(17, 24, 39, 0.95);
    border: 1px solid #29384C;
    border-radius: 10px;

    padding: 7px 10px;
    min-width: 0;
    min-height: 56px;

    box-sizing: border-box;
}

.metric-label {
    color: #94A3B8;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
}

.metric-value {
    font-size: clamp(18px, 2.8dvh, 25px);
    font-weight: 800;
    line-height: 1.1;
}


/* =========================================================
   PROGRESS BAR
   ========================================================= */

.progress-track {
    width: 100%;
    height: 4px;
    background: #1E293B;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 5px;
}

.progress-fill {
    height: 100%;
    border-radius: 20px;
    transition: width 0.3s ease;
}


/* =========================================================
   FITNESS LANDSCAPE
   ========================================================= */

.fitness-image {
    display: block;
    width: 100%;

    height: clamp(150px, 35dvh, 330px);

    object-fit: contain;

    background: #0B1120;
    border: 1px solid #29384C;
    border-radius: 10px;
    box-sizing: border-box;
}


/* =========================================================
   TARGET STATUS
   ========================================================= */

.target-status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 6px;

    padding: 7px 10px;

    border: 1px solid #29384C;
    border-radius: 8px;

    background: rgba(17, 24, 39, 0.90);
    font-size: 10px;
}

.target-status-label {
    color: #94A3B8;
    font-weight: 600;
}

.target-status-value {
    font-weight: 800;
    letter-spacing: 0.7px;
}


/* =========================================================
   LIVE FEEDBACK
   ========================================================= */

.feedback-box {
    background: rgba(17, 24, 39, 0.96);
    border: 1px solid #29384C;
    border-left: 4px solid #FBBF24;
    border-radius: 9px;
    padding: 8px 10px;
}

.feedback-title {
    color: #FBBF24;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 4px;
}

.feedback-text {
    color: #E2E8F0;
    font-size: 11px;
    line-height: 1.4;
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


/* =========================================================
   BOTTOM NAVIGATION
   ========================================================= */

.st-key-bottom_navigation {
    width: 100%;
    flex: 0 0 auto;
    border-top: 1px solid #29384C;
    padding-top: 7px;
    margin-top: auto !important;
}

.st-key-bottom_navigation
[data-testid="stHorizontalBlock"] {
    gap: 10px !important;
}


/* =========================================================
   FIXED POP-UP DIALOGS
   ========================================================= */

[data-testid="stDialog"] {
    overflow: hidden !important;
    overscroll-behavior: none !important;
}

[data-testid="stDialog"] [role="dialog"] {
    width: min(1050px, 94vw) !important;
    max-width: 94vw !important;
    max-height: 92dvh !important;

    overflow: hidden !important;
    overscroll-behavior: none !important;

    background: #0B1120 !important;
    color: #E2E8F0;

    border: 1px solid #29384C;
    border-radius: 16px;
    box-sizing: border-box;
}

[data-testid="stDialog"]
[role="dialog"] > div {
    overflow: hidden !important;
}

[data-testid="stDialog"]
[data-testid="stVerticalBlock"] {
    gap: 6px !important;
}

[data-testid="stDialog"]
[data-testid="stElementContainer"] {
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stDialog"] h1,
[data-testid="stDialog"] h2,
[data-testid="stDialog"] h3 {
    font-size: 19px !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stDialog"] p {
    font-size: 12px;
    line-height: 1.4;
}

[data-testid="stDialog"]
.stButton > button {
    min-height: 32px !important;
    padding: 4px 10px !important;
}


/* =========================================================
   MISSION RESULT
   ========================================================= */

.result-container {
    width: 100%;
    text-align: center;
    padding: 12px 16px;
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
    font-size: clamp(35px, 8dvh, 65px);
    line-height: 1.1;
    margin-bottom: 5px;
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
    font-size: clamp(24px, 4.8dvh, 42px);
    font-weight: 900;
    letter-spacing: 3px;
    line-height: 1.2;
    margin-bottom: 6px;
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
    font-size: 12px;
    line-height: 1.4;
    margin-bottom: 10px;
}

.result-grid {
    display: grid;
    grid-template-columns:
        repeat(4, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 10px;
}

.result-stat {
    background: #111827;
    border: 1px solid #29384C;
    border-radius: 10px;
    padding: 8px;
}

.result-stat-label {
    color: #94A3B8;
    font-size: 9px;
    font-weight: 700;
    margin-bottom: 4px;
}

.result-stat-value {
    color: #E2E8F0;
    font-size: 23px;
    font-weight: 800;
}

.result-strategy {
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 4px;
}

.result-reason {
    text-align: left;
    background: #111827;
    border: 1px solid #29384C;
    border-radius: 9px;
    padding: 8px 12px;
    margin-top: 8px;
}

.result-reason-title {
    color: #FBBF24;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.3px;
    margin-bottom: 4px;
}

.result-reason-text {
    color: #CBD5E1;
    font-size: 12px;
    line-height: 1.4;
}


/* =========================================================
   PERFORMANCE ANALYSIS
   ========================================================= */

.analysis-image {
    display: block;
    width: 100%;
    height: 29dvh;
    max-height: 260px;
    object-fit: contain;

    background: #080D1C;
    border: 1px solid #29384C;
    border-radius: 9px;
}

.dialog-description {
    color: #94A3B8;
    font-size: 11px;
    line-height: 1.4;
    margin: 3px 0;
}

.dialog-heading {
    color: #67E8F9;
    font-size: 13px;
    font-weight: 800;
    margin: 4px 0;
}


/* =========================================================
   STATIC TABLES — NO SCROLL
   ========================================================= */

.static-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;

    background: #111827;
    border: 1px solid #29384C;
    color: #E2E8F0;

    font-size: 11px;
}

.static-table th {
    background: #1E293B;
    color: #67E8F9;
    font-weight: 700;
    padding: 7px 4px;
    border-bottom: 1px solid #334155;
    text-align: center;
    overflow-wrap: anywhere;
}

.static-table td {
    padding: 7px 4px;
    border-bottom: 1px solid #29384C;
    text-align: center;
    overflow-wrap: anywhere;
}

.static-table tbody tr:nth-child(even) {
    background: rgba(30, 41, 59, 0.4);
}

.table-page {
    color: #94A3B8;
    font-size: 11px;
    text-align: center;
    padding: 4px;
}


/* =========================================================
   LEARNING GUIDE
   ========================================================= */

.guide-card {
    background: #111827;
    border: 1px solid #29384C;
    border-radius: 10px;
    padding: 14px;
    margin: 4px 0;
}

.guide-title {
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 8px;
}

.guide-description {
    color: #CBD5E1;
    font-size: 13px;
    line-height: 1.5;
    margin-bottom: 10px;
}

.guide-point {
    background: #080D1C;
    border-left: 3px solid #22D3EE;
    border-radius: 5px;
    color: #E2E8F0;
    font-size: 12px;
    line-height: 1.4;
    padding: 8px 10px;
    margin-bottom: 6px;
}

.guide-example {
    background: rgba(251, 191, 36, 0.06);
    border: 1px solid #854D0E;
    border-radius: 8px;
    padding: 8px 10px;
    color: #FBBF24;
    font-size: 12px;
    line-height: 1.4;
}


/* =========================================================
   COMPACT LAPTOP SCREEN
   ========================================================= */

@media (max-height: 800px) {

    .block-container {
        padding: 8px 20px !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 4px !important;
    }

    .hero-title {
        font-size: 27px;
    }

    .hero-label,
    .hero-subtitle {
        font-size: 8px;
    }

    .metric-card {
        min-height: 48px;
        padding: 6px 9px;
    }

    .metric-value {
        font-size: 21px;
    }

    .fitness-image {
        height: 33dvh;
    }

    .stButton > button {
        min-height: 29px !important;
        padding: 3px 7px !important;
    }

    .strategy-description,
    .mission-card,
    .feedback-box {
        padding: 6px 8px;
    }

    .result-container {
        padding: 10px 12px;
    }

    .guide-card {
        padding: 10px;
    }

    .guide-point {
        padding: 6px 8px;
        margin-bottom: 4px;
    }
}


/* =========================================================
   SHORT DESKTOP SCREEN
   ========================================================= */

@media (max-height: 650px) {

    .block-container {
        padding: 5px 16px !important;
    }

    .hero-title {
        font-size: 23px;
    }

    .hero-label,
    .hero-subtitle {
        font-size: 7px;
    }

    .fitness-image {
        height: 29dvh;
    }

    .metric-card {
        min-height: 42px;
        padding: 4px 7px;
    }

    .metric-value {
        font-size: 18px;
    }

    .st-key-left_panel
    [data-testid="stVerticalBlock"] {
        gap: 3px !important;
    }

    .st-key-left_panel
    [role="radiogroup"] label {
        min-height: 19px;
    }

    .stButton > button {
        min-height: 26px !important;
    }

    .welcome-mountain {
        max-height: 75px;
    }

    .instruction-row {
        padding: 4px 8px;
        margin-bottom: 3px;
    }

    .result-icon {
        font-size: 36px;
    }

    .result-title {
        font-size: 25px;
    }

    .result-stat-value {
        font-size: 19px;
    }

    .static-table td,
    .static-table th {
        padding: 4px 3px;
    }

    .guide-title {
        font-size: 16px;
    }

    .guide-description,
    .guide-point,
    .guide-example {
        font-size: 11px;
    }
}


/* =========================================================
   NARROW SCREEN
   ========================================================= */

@media (max-width: 1100px) {

    .block-container {
        padding: 8px 12px !important;
    }

    .metric-grid {
        gap: 4px;
    }

    .metric-card {
        padding: 5px;
    }

    .metric-label {
        font-size: 8px;
    }

    .metric-value {
        font-size: 18px;
    }

    .target-status {
        font-size: 9px;
    }
}


/* =========================================================
   MOBILE FALLBACK
   ========================================================= */

@media (max-width: 767px) {

    html,
    body,
    #root,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        height: auto !important;
        max-height: none !important;
        overflow-y: auto !important;
    }

    .block-container {
        height: auto !important;
        max-height: none !important;
        overflow: visible !important;
    }

    .metric-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

    [data-testid="stDialog"] [role="dialog"],
    [data-testid="stDialog"] [role="dialog"] > div {
        overflow-y: auto !important;
    }
}

/* =========================================================
   FULL SCREEN RESPONSIVE DASHBOARD
   ========================================================= */

@media (min-width: 1100px) and (min-height: 680px) {

    :root {
        --ui-scale: clamp(0.9px, 0.14dvh, 1.4px);
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
    }

    /* MAIN SCREEN */

    .block-container {
        width: 100% !important;
        max-width: none !important;

        height: 100dvh !important;

        padding: 12px 24px 16px !important;

        box-sizing: border-box;
        overflow: hidden !important;
    }

    .block-container >
    [data-testid="stVerticalBlock"] {
        display: flex !important;
        flex-direction: column !important;

        height: 100% !important;
        min-height: 0 !important;

        gap: 10px !important;
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .hero {
        padding: 2px 0 10px;
    }

    .hero-label {
        font-size: calc(10 * var(--ui-scale));
        letter-spacing: 5px;
        margin-bottom: 5px;
    }

    .hero-title {
        font-size: calc(36 * var(--ui-scale));
        letter-spacing: 6px;
        line-height: 1.1;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: calc(10 * var(--ui-scale));
        letter-spacing: 4px;
    }


    /* =====================================================
       MAIN DASHBOARD
       ===================================================== */

    .st-key-main_dashboard {
        flex: 1 1 auto !important;
        min-height: 0 !important;
        width: 100% !important;
    }

    .st-key-main_dashboard
    [data-testid="stHorizontalBlock"] {
        gap: 18px !important;
    }

    .st-key-left_panel
    [data-testid="stVerticalBlock"],

    .st-key-right_panel
    [data-testid="stVerticalBlock"] {
        gap: 8px !important;
    }

    .section-heading {
        font-size: calc(11 * var(--ui-scale));
        letter-spacing: 1.6px;
        line-height: 1.3;
    }


    /* =====================================================
       PARAMETER CONTROL
       ===================================================== */

    .st-key-left_panel [role="radiogroup"] {
        width: 100% !important;
        padding: 9px 12px !important;
        gap: 3px !important;
    }

    .st-key-left_panel
    [role="radiogroup"] label {
        min-height: calc(25 * var(--ui-scale));
    }

    .st-key-left_panel
    [role="radiogroup"] p {
        font-size: calc(13 * var(--ui-scale));
        line-height: 1.3;
    }

    .strategy-description {
        padding: 10px 12px;
        border-radius: 10px;
    }

    .strategy-description-title {
        font-size: calc(12 * var(--ui-scale));
        margin-bottom: 5px;
    }

    .strategy-description-text {
        font-size: calc(12 * var(--ui-scale));
        line-height: 1.4;
    }


    /* =====================================================
       INITIAL STEP SIZE
       ===================================================== */

    [data-testid="stWidgetLabel"] p {
        font-size: calc(13 * var(--ui-scale));
    }

    .st-key-left_panel
    [data-testid="stSlider"] {
        padding: 2px 0 !important;
    }

    .slider-help {
        font-size: calc(11 * var(--ui-scale));
        line-height: 1.4;
    }


    /* =====================================================
       SIMULATION BUTTONS
       ===================================================== */

    .stButton > button {
        min-height: calc(35 * var(--ui-scale)) !important;

        padding: 6px 12px !important;

        border-radius: 9px;
    }

    .stButton > button p {
        font-size: calc(12 * var(--ui-scale));
        font-weight: 600;
        line-height: 1.2;
    }


    /* =====================================================
       MISSION OBJECTIVE
       ===================================================== */

    .mission-card {
        padding: 10px 12px;
        border-radius: 10px;
    }

    .mission-title {
        font-size: calc(10 * var(--ui-scale));
        margin-bottom: 6px;
    }

    .mission-text {
        font-size: calc(11 * var(--ui-scale));
        line-height: 1.5;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    .metric-grid {
        grid-template-columns:
            repeat(5, minmax(0, 1fr));

        gap: 10px;
    }

    .metric-card {
        min-height: calc(68 * var(--ui-scale));

        padding: 10px 14px;

        border-radius: 12px;
    }

    .metric-label {
        font-size: calc(10 * var(--ui-scale));
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: calc(28 * var(--ui-scale));
        line-height: 1.1;
    }

    .progress-track {
        height: 5px;
        margin-top: 6px;
    }


    /* =====================================================
       FITNESS LANDSCAPE
       ===================================================== */

    .fitness-image {
        display: block;

        width: 100% !important;

        height: clamp(220px, 40dvh, 480px) !important;

        max-height: none !important;

        object-fit: fill !important;

        border-radius: 12px;

        box-sizing: border-box;
    }


    /* =====================================================
       TARGET STATUS
       ===================================================== */

    .target-status {
        min-height: 35px;

        padding: 8px 12px;

        border-radius: 9px;

        font-size: calc(11 * var(--ui-scale));
    }


    /* =====================================================
       LIVE EVOLUTION FEEDBACK
       ===================================================== */

    .feedback-box {
        padding: 10px 14px;

        min-height: 60px;

        border-radius: 10px;
    }

    .feedback-title {
        font-size: calc(11 * var(--ui-scale));
        margin-bottom: 6px;
    }

    .feedback-text {
        font-size: calc(12 * var(--ui-scale));
        line-height: 1.4;
    }


    /* =====================================================
       BOTTOM NAVIGATION
       ===================================================== */

    .st-key-bottom_navigation {
        width: 100% !important;

        flex: 0 0 auto !important;

        margin-top: auto !important;

        padding-top: 10px !important;
        padding-bottom: 4px !important;
    }

    .st-key-bottom_navigation
    [data-testid="stHorizontalBlock"] {
        gap: 12px !important;
    }

    .st-key-bottom_navigation
    .stButton > button {
        min-height: calc(38 * var(--ui-scale)) !important;
    }


    /* =====================================================
       WELCOME SCREEN
       ===================================================== */

    .st-key-welcome_screen {
        max-width: 850px;

        padding: 22px 30px !important;
    }

    .welcome-title {
        font-size: calc(40 * var(--ui-scale));
    }

    .welcome-subtitle {
        font-size: calc(11 * var(--ui-scale));
    }

    .welcome-mountain {
        height: 17dvh;
        max-height: 160px;
        max-width: 550px;
    }

    .welcome-mission {
        font-size: calc(19 * var(--ui-scale));
    }

    .welcome-mission-text {
        font-size: calc(13 * var(--ui-scale));
    }

    .instruction-row {
        padding: 10px 14px;
    }

    .instruction-title {
        font-size: calc(13 * var(--ui-scale));
    }

    .instruction-text {
        font-size: calc(12 * var(--ui-scale));
    }

}


/* =========================================================
   SHORT LAPTOP SCREEN
   ========================================================= */

@media (min-width: 1100px) and (max-height: 780px) {

    .block-container {
        padding: 8px 22px 10px !important;
    }

    .hero {
        padding-bottom: 5px;
    }

    .hero-title {
        font-size: 32px;
    }

    .st-key-left_panel
    [data-testid="stVerticalBlock"],

    .st-key-right_panel
    [data-testid="stVerticalBlock"] {
        gap: 5px !important;
    }

    .fitness-image {
        height: 37dvh !important;
    }

    .metric-card {
        min-height: 58px;
        padding: 8px 12px;
    }

    .metric-value {
        font-size: 25px;
    }

    .strategy-description,
    .mission-card,
    .feedback-box {
        padding: 7px 10px;
    }

    .stButton > button {
        min-height: 32px !important;
    }

    .feedback-box {
        min-height: 0;
    }

    .st-key-bottom_navigation {
        padding-top: 6px !important;
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

SIMULATION_VERSION = "exact_peak_overshoot_v4"

HISTORY_PAGE_SIZE = 5


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

    "active_dialog": None,

    "history_page": 0
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

        strategy = (
            st.session_state.selected_strategy
        )

    if initial_sigma is None:

        initial_sigma = (
            st.session_state.initial_sigma
        )

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

    st.session_state.last_offspring = []

    st.session_state.mission_success = False

    st.session_state.mission_failed = False

    st.session_state.game_finished = False

    st.session_state.success_generation = None

    st.session_state.failure_generation = None

    st.session_state.failure_type = None

    st.session_state.final_position = None

    st.session_state.final_sigma = None

    st.session_state.trigger_individual = None

    st.session_state.trigger_parent_position = None

    st.session_state.overshoot_count = 0

    st.session_state.result_shown = False

    st.session_state.active_dialog = None

    st.session_state.history_page = 0

    st.session_state.feedback = (

        "Your population starts at position 10. "
        "Reach exactly position 79 to win. "
        "Overshooting the target causes immediate failure."
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
        "last_offspring",
        "feedback",
        "settings",
        "mission_success",
        "mission_failed",
        "game_finished",
        "success_generation",
        "failure_generation",
        "failure_type",
        "final_position",
        "final_sigma",
        "trigger_individual",
        "trigger_parent_position",
        "overshoot_count",
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

    if len(
        st.session_state.population
    ) != POPULATION_SIZE:

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

    return max(

        st.session_state.population,

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
        st.session_state.game_finished

        and st.session_state.final_position is not None
    ):

        return int(
            st.session_state.final_position
        )

    return get_best_position()


def get_display_sigma():

    if (
        st.session_state.game_finished

        and st.session_state.final_sigma is not None
    ):

        return float(
            st.session_state.final_sigma
        )

    return float(
        st.session_state.sigma
    )


def get_distance_from_target():

    return abs(
        TARGET_POSITION - get_display_position()
    )


def get_target_status(position):

    if position == TARGET_POSITION:

        return (
            "EXACT GLOBAL OPTIMUM",
            "#4ADE80"
        )

    if position < TARGET_POSITION:

        return (
            "BELOW TARGET POSITION",
            "#FBBF24"
        )

    return (
        "OVERSHOT TARGET POSITION",
        "#F87171"
    )


def get_failure_reason(position):

    if st.session_state.failure_type == "OVERSHOOT":

        parent = (
            st.session_state.trigger_parent_position
        )

        individual = (
            st.session_state.trigger_individual
        )

        return (

            "OVERSHOOT — TARGET EXCEEDED",

            f"Individual {individual} moved from "
            f"position {parent} to position {position}. "
            f"It exceeded the target by "
            f"{position - TARGET_POSITION} unit(s). "
            "Try a smaller initial step size or a "
            "strategy that encourages refinement."
        )

    if abs(position - LOCAL_OPTIMUM) <= 5:

        return (

            "TRAPPED NEAR THE LOCAL OPTIMUM",

            "The population remained near the smaller "
            "mountain until the generation limit. "
            "Try a larger initial step size to "
            "encourage exploration."
        )

    return (

        "UNDERSHOOT — TARGET NOT REACHED",

        f"The best individual stopped at position "
        f"{position}, which is "
        f"{TARGET_POSITION - position} unit(s) "
        "before the Global Optimum. "
        "Try a different parameter combination."
    )


# ============================================================
# 10. EVOLUTION PROCESS
# ============================================================

def next_generation():

    # --------------------------------------------------------
    # STOP IF MISSION HAS ENDED
    # --------------------------------------------------------

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

    previous_best_x = get_best_position()

    generation = (
        st.session_state.generation + 1
    )

    offspring = []

    mutation_details = []

    exact_hits = []

    overshoot_hits = []

    successes = 0


    # ========================================================
    # A. MUTATION
    # ========================================================

    for i, (x, individual_sigma) in enumerate(population):

        x = int(x)

        individual_sigma = float(
            individual_sigma
        )

        # ----------------------------------------------------
        # SELF-ADAPTIVE MUTATION STEP SIZE
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # RANDOM MUTATION MOVEMENT
        # ----------------------------------------------------

        mutation = np.random.normal(

            0,

            child_sigma
        )


        # IMPORTANT:
        # Position is limited to 0–100, NOT 0–79.
        # This allows genuine overshooting.

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


        # ====================================================
        # B. CHECK EXACT HIT AND OVERSHOOT
        # BEFORE SURVIVAL SELECTION
        # ====================================================

        if child_x == TARGET_POSITION:

            target_result = "EXACT HIT"

            exact_hits.append({

                "individual": i + 1,

                "parent": x,

                "position": child_x,

                "sigma": child_sigma
            })

        elif child_x > TARGET_POSITION:

            target_result = "OVERSHOOT"

            overshoot_hits.append({

                "individual": i + 1,

                "parent": x,

                "position": child_x,

                "sigma": child_sigma
            })

        else:

            target_result = "BELOW TARGET"


        mutation_details.append({

            "Individual": i + 1,

            "Parent": x,

            "Offspring": child_x,

            "Movement": child_x - x,

            "Sigma": round(child_sigma, 2),

            "Parent Fitness": round(
                parent_fitness, 2
            ),

            "Offspring Fitness": round(
                child_fitness, 2
            ),

            "Fitness Result": (

                "Improved"

                if improved

                else "Not Improved"
            ),

            "Target Result": target_result
        })


    # ========================================================
    # C. MUTATION SUCCESS RATE
    # ========================================================

    success_rate = (
        successes / POPULATION_SIZE
    )


    # ========================================================
    # D. SURVIVAL SELECTION
    # ========================================================

    combined = population + offspring

    combined.sort(

        key=lambda individual: float(
            fitness(individual[0])
        ),

        reverse=True
    )

    new_population = combined[:POPULATION_SIZE]


    # ========================================================
    # E. PARAMETER CONTROL
    # ========================================================

    if strategy == "Deterministic":

        new_sigma = max(

            MIN_SIGMA,

            initial_sigma * (
                1 - generation / MAX_GENERATIONS
            )
        )

        feedback = (

            f"Generation {generation}: "
            f"Deterministic step size "
            f"{sigma:.2f} → {new_sigma:.2f}. "
            "Step size decreases according to "
            "the predefined schedule."
        )


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

            action = "remained unchanged"

        if new_sigma == sigma:

            action = "remained unchanged"

        feedback = (

            f"Generation {generation}: "
            f"{successes}/{POPULATION_SIZE} successful "
            f"mutations ({success_rate:.0%}). "
            f"Step size {action}: "
            f"{sigma:.2f} → {new_sigma:.2f}."
        )


    else:

        new_sigma = float(
            new_population[0][1]
        )

        feedback = (

            f"Generation {generation}: "
            "Each individual evolved its own "
            "mutation step size. "
            f"Best surviving sigma: {new_sigma:.2f}."
        )


    # --------------------------------------------------------
    # SYNCHRONIZE SHARED SIGMA
    # --------------------------------------------------------

    if strategy != "Self-Adaptive":

        new_population = [

            (int(x), float(new_sigma))

            for x, _ in new_population
        ]


    # ========================================================
    # F. CALCULATE BEST SURVIVING INDIVIDUAL
    # ========================================================

    best_x = int(
        new_population[0][0]
    )

    best_fitness = float(
        fitness(best_x)
    )

    distance = abs(
        TARGET_POSITION - best_x
    )


    # ========================================================
    # G. EXACT PEAK MISSION RULES
    # ========================================================

    mission_success = False

    mission_failed = False

    failure_type = None

    final_position = None

    final_sigma = None

    trigger_individual = None

    trigger_parent_position = None


    # --------------------------------------------------------
    # RULE 1:
    # EXACT POSITION 79 = MISSION COMPLETE
    # --------------------------------------------------------

    if exact_hits:

        winning_individual = exact_hits[0]

        mission_success = True

        final_position = TARGET_POSITION

        final_sigma = float(
            winning_individual["sigma"]
        )

        trigger_individual = (
            winning_individual["individual"]
        )

        trigger_parent_position = (
            winning_individual["parent"]
        )

        feedback += (

            f" Individual {trigger_individual} "
            f"landed exactly at position "
            f"{TARGET_POSITION}. "
            "MISSION COMPLETE!"
        )


    # --------------------------------------------------------
    # RULE 2:
    # ANY OFFSPRING ABOVE 79 = IMMEDIATE FAILURE
    # IF NO OFFSPRING HIT 79
    # --------------------------------------------------------

    elif overshoot_hits:

        # Use the first overshooting offspring
        # as the individual responsible for failure.

        failed_individual = overshoot_hits[0]

        mission_failed = True

        failure_type = "OVERSHOOT"

        final_position = int(
            failed_individual["position"]
        )

        final_sigma = float(
            failed_individual["sigma"]
        )

        trigger_individual = (
            failed_individual["individual"]
        )

        trigger_parent_position = (
            failed_individual["parent"]
        )

        overshoot_distance = (
            final_position - TARGET_POSITION
        )

        feedback += (

            f" Individual {trigger_individual} "
            f"jumped from position "
            f"{trigger_parent_position} "
            f"to {final_position}. "

            f"Overshoot: {overshoot_distance} unit(s). "

            "MISSION FAILED!"
        )


    # --------------------------------------------------------
    # RULE 3:
    # GENERATION 30 WITHOUT EXACT HIT = UNDERSHOOT
    # --------------------------------------------------------

    elif generation >= MAX_GENERATIONS:

        mission_failed = True

        failure_type = "UNDERSHOOT"

        final_position = best_x

        final_sigma = float(
            new_population[0][1]
        )

        feedback += (

            f" Maximum generations reached. "
            f"Final position: {best_x}. "
            f"Remaining distance: {distance}. "
            "MISSION FAILED!"
        )


    # --------------------------------------------------------
    # RULE 4:
    # BELOW 79 AND GENERATIONS REMAIN = CONTINUE
    # --------------------------------------------------------

    else:

        feedback += (

            f" Best position: "
            f"{previous_best_x} → {best_x}. "

            f"Distance to target: "
            f"{distance} unit(s)."
        )


    game_finished = (
        mission_success or mission_failed
    )


    # ========================================================
    # H. UPDATE SIMULATION STATE
    # ========================================================

    st.session_state.population = new_population

    st.session_state.generation = generation

    st.session_state.sigma = float(new_sigma)

    st.session_state.feedback = feedback

    st.session_state.last_mutations = (
        mutation_details
    )

    st.session_state.last_offspring = offspring

    st.session_state.mission_success = (
        mission_success
    )

    st.session_state.mission_failed = (
        mission_failed
    )

    st.session_state.game_finished = (
        game_finished
    )

    st.session_state.failure_type = failure_type

    st.session_state.final_position = (
        final_position
    )

    st.session_state.final_sigma = final_sigma

    st.session_state.trigger_individual = (
        trigger_individual
    )

    st.session_state.trigger_parent_position = (
        trigger_parent_position
    )

    st.session_state.overshoot_count += len(
        overshoot_hits
    )

    st.session_state.success_generation = (

        generation

        if mission_success

        else None
    )

    st.session_state.failure_generation = (

        generation

        if mission_failed

        else None
    )


    # ========================================================
    # I. UPDATE HISTORIES
    # ========================================================

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


    # ========================================================
    # J. OPEN MISSION RESULT POP-UP
    # ========================================================

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

    if dialog_name == "performance":

        st.session_state.history_page = 0


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


def display_static_table(dataframe):

    table_html = dataframe.to_html(

        index=False,

        border=0,

        classes="static-table",

        escape=True
    )

    st.html(table_html)


# ============================================================
# 13. MATPLOTLIB THREAD LOCK
# ============================================================

@st.cache_resource
def get_plot_lock():

    return RLock()


def figure_to_base64(fig):

    with BytesIO() as buffer:

        fig.savefig(

            buffer,

            format="png",

            facecolor=fig.get_facecolor(),

            dpi=130
        )

        return base64.b64encode(

            buffer.getvalue()

        ).decode("utf-8")


# ============================================================
# 14. WELCOME MOUNTAIN IMAGE
# ============================================================

@st.cache_data
def create_welcome_mountain():

    with get_plot_lock():

        fig, ax = plt.subplots(

            figsize=(6.5, 1.8),

            dpi=150
        )

        try:

            fig.patch.set_facecolor("#080D1C")

            ax.set_facecolor("#080D1C")

            x = np.linspace(0, 100, 1001)

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

                s=30,

                zorder=5
            )

            ax.scatter(

                GLOBAL_OPTIMUM,

                global_y,

                color="#FBBF24",

                marker="*",

                s=160,

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

            ax.set_ylim(20, 125)

            ax.axis("off")

            fig.subplots_adjust(

                left=0.02,

                right=0.98,

                top=0.98,

                bottom=0.02
            )

            return figure_to_base64(fig)

        finally:

            plt.close(fig)


# ============================================================
# 15. WELCOME SCREEN
# ============================================================

def display_welcome_screen():

    mountain_image = create_welcome_mountain()

    with st.container(key="welcome_screen"):

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
            alt="Fitness Mountain"
        />

        <div class="welcome-mission">
            EXACT PEAK CHALLENGE
        </div>

        <div class="welcome-mission-text">

            Reach exactly
            <strong style="color:#FBBF24;">
                POSITION 79
            </strong>

            within 30 generations.

            <br>

            Too far or not far enough?
            Your mission fails.

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
                    Set Your Initial Step Size
                </div>

                <div class="instruction-text">

                    Small steps refine your position.
                    Large steps explore further but
                    may overshoot.

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

                    Run generations to land exactly
                    at 79. Overshooting or running
                    out of generations causes failure.

                </div>

            </div>

        </div>

        """)

        st.button(

            "▶ START GAME",

            key="start_game_button",

            type="primary",

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
# 17. METRIC CARDS
# ============================================================

def display_metrics(strategy):

    generation = st.session_state.generation

    position = get_display_position()

    position_fitness = float(
        fitness(position)
    )

    distance = get_distance_from_target()

    sigma = get_display_sigma()

    if st.session_state.game_finished:

        position_label = "FINAL POSITION"

        fitness_label = "FINAL FITNESS"

        sigma_label = "FINAL SIGMA"

    else:

        position_label = "BEST POSITION"

        fitness_label = "BEST FITNESS"

        sigma_label = (

            "BEST SIGMA"

            if strategy == "Self-Adaptive"

            else "CURRENT SIGMA"
        )

    if position == TARGET_POSITION:

        position_color = "#4ADE80"

        distance_color = "#4ADE80"

    elif position > TARGET_POSITION:

        position_color = "#F87171"

        distance_color = "#F87171"

    else:

        position_color = "#67E8F9"

        distance_color = "#E879F9"

    cards = [

        metric_html(

            "GENERATION",

            f"{generation}/{MAX_GENERATIONS}",

            "#67E8F9"
        ),

        metric_html(

            fitness_label,

            f"{position_fitness:.2f}",

            "#FBBF24"
        ),

        metric_html(

            sigma_label,

            f"{sigma:.2f}",

            "#E879F9"
        ),

        metric_html(

            position_label,

            position,

            position_color
        ),

        metric_html(

            "TARGET DISTANCE",

            distance,

            distance_color
        )
    ]

    progress = min(

        100,

        generation / MAX_GENERATIONS * 100
    )

    cards_html = "".join(cards)

    progress_color = (

        "#4ADE80"

        if st.session_state.mission_success

        else "#F87171"

        if st.session_state.mission_failed

        else STRATEGIES[strategy]["color"]
    )

    st.html(f"""

    <div class="metric-grid">

        {cards_html}

    </div>

    <div class="progress-track">

        <div
            class="progress-fill"
            style="
                width:{progress}%;
                background:{progress_color};
            "
        ></div>

    </div>

    """)


# ============================================================
# 18. FITNESS LANDSCAPE
# ============================================================

def display_fitness_landscape(accent):

    display_x = get_display_position()

    display_fitness = float(
        fitness(display_x)
    )

    population = st.session_state.population

    offspring = st.session_state.last_offspring

    x_values = np.linspace(
        MIN_POSITION,
        MAX_POSITION,
        1001
    )

    y_values = fitness(x_values)

    with get_plot_lock():

        fig, ax = plt.subplots(

            figsize=(12, 3.1),

            dpi=130
        )

        try:

            fig.patch.set_facecolor("#0B1120")

            ax.set_facecolor("#0B1120")


            # ------------------------------------------------
            # OVERSHOOT DANGER ZONE
            # ------------------------------------------------

            ax.axvspan(

                TARGET_POSITION,

                MAX_POSITION,

                color="#EF4444",

                alpha=0.07,

                zorder=0
            )


            # ------------------------------------------------
            # FITNESS CURVE
            # ------------------------------------------------

            ax.fill_between(

                x_values,

                20,

                y_values,

                color="#22D3EE",

                alpha=0.10
            )

            for width, alpha in [

                (10, 0.025),

                (6, 0.05),

                (3, 0.15)
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
            # LOCAL OPTIMUM
            # ------------------------------------------------

            local_y = float(
                fitness(LOCAL_OPTIMUM)
            )

            ax.scatter(

                LOCAL_OPTIMUM,

                local_y,

                color="#94A3B8",

                s=45,

                zorder=6
            )

            ax.annotate(

                "LOCAL OPTIMUM\nPosition 27",

                xy=(
                    LOCAL_OPTIMUM,
                    local_y
                ),

                xytext=(
                    LOCAL_OPTIMUM,
                    local_y + 12
                ),

                ha="center",

                color="#94A3B8",

                fontsize=8,

                fontweight="bold"
            )


            # ------------------------------------------------
            # GLOBAL OPTIMUM
            # ------------------------------------------------

            global_y = float(
                fitness(GLOBAL_OPTIMUM)
            )

            ax.axvline(

                TARGET_POSITION,

                color="#FBBF24",

                linestyle="--",

                linewidth=1.1,

                alpha=0.75
            )

            ax.scatter(

                GLOBAL_OPTIMUM,

                global_y,

                color="#FBBF24",

                marker="*",

                s=170,

                zorder=7
            )

            ax.annotate(

                "GLOBAL OPTIMUM\nPosition 79",

                xy=(
                    GLOBAL_OPTIMUM,
                    global_y
                ),

                xytext=(
                    GLOBAL_OPTIMUM,
                    global_y + 11
                ),

                ha="center",

                color="#FBBF24",

                fontsize=8,

                fontweight="bold"
            )

            ax.text(

                90,

                116,

                "OVERSHOOT ZONE",

                color="#F87171",

                fontsize=7,

                ha="center",

                fontweight="bold"
            )


            # ------------------------------------------------
            # SURVIVING POPULATION
            # ------------------------------------------------

            population_x = [

                individual[0]

                for individual in population
            ]

            population_y = [

                float(fitness(x))

                for x in population_x
            ]

            ax.scatter(

                population_x,

                population_y,

                color=accent,

                s=45,

                alpha=0.65,

                edgecolors="#E2E8F0",

                linewidths=0.5,

                label="Population",

                zorder=8
            )


            # ------------------------------------------------
            # SHOW ALL OVERSHOOTING OFFSPRING
            # EVEN IF REJECTED BY SURVIVAL SELECTION
            # --------------------------------------------------------

            overshoot_positions = [

                x

                for x, _ in offspring

                if x > TARGET_POSITION
            ]

            if overshoot_positions:

                ax.scatter(

                    overshoot_positions,

                    [
                        float(fitness(x))
                        for x in overshoot_positions
                    ],

                    color="#F87171",

                    marker="X",

                    s=70,

                    edgecolors="#FFFFFF",

                    linewidths=0.6,

                    label="Overshoot",

                    zorder=9
                )


            # ------------------------------------------------
            # CURRENT OR FINAL POSITION
            # ------------------------------------------------

            if st.session_state.mission_success:

                marker_color = "#4ADE80"

                marker_label = "Exact Hit"

                position_text = "EXACT HIT: 79"

            elif st.session_state.mission_failed:

                marker_color = "#F87171"

                marker_label = "Final Position"

                if (
                    st.session_state.failure_type
                    == "OVERSHOOT"
                ):

                    position_text = (
                        f"OVERSHOOT: {display_x}"
                    )

                else:

                    position_text = (
                        f"UNDERSHOOT: {display_x}"
                    )

            else:

                marker_color = accent

                marker_label = "Best Individual"

                position_text = (
                    f"BEST: {display_x}"
                )


            ax.scatter(

                display_x,

                display_fitness,

                color=marker_color,

                s=250,

                alpha=0.12,

                zorder=10
            )

            ax.scatter(

                display_x,

                display_fitness,

                color=marker_color,

                s=85,

                edgecolors="#FFFFFF",

                linewidths=1.2,

                label=marker_label,

                zorder=11
            )

            ax.vlines(

                display_x,

                20,

                display_fitness,

                color=marker_color,

                linestyle=":",

                linewidth=1,

                alpha=0.7
            )

            ax.annotate(

                position_text,

                xy=(
                    display_x,
                    display_fitness
                ),

                xytext=(

                    display_x,

                    max(
                        24,
                        display_fitness - 12
                    )
                ),

                color=marker_color,

                fontsize=8,

                fontweight="bold",

                ha="center"
            )


            # ------------------------------------------------
            # SHOW FAILED MUTATION MOVEMENT
            # ------------------------------------------------

            if (

                st.session_state.failure_type
                == "OVERSHOOT"

                and st.session_state.trigger_parent_position
                is not None
            ):

                parent_x = (
                    st.session_state.trigger_parent_position
                )

                parent_y = float(
                    fitness(parent_x)
                )

                ax.annotate(

                    "",

                    xy=(
                        display_x,
                        display_fitness
                    ),

                    xytext=(
                        parent_x,
                        parent_y
                    ),

                    arrowprops={

                        "arrowstyle": "->",

                        "color": "#F87171",

                        "linewidth": 1.5,

                        "connectionstyle": "arc3,rad=-0.25"
                    },

                    zorder=9
                )


            # ------------------------------------------------
            # GRAPH STYLING
            # ------------------------------------------------

            ax.set_xlim(0, 100)

            ax.set_ylim(15, 125)

            ax.set_xticks(
                np.arange(0, 101, 10)
            )

            ax.set_yticks(
                np.arange(20, 121, 20)
            )

            ax.set_xlabel(

                "POSITION (x)",

                color="#94A3B8",

                fontsize=8
            )

            ax.set_ylabel(

                "FITNESS",

                color="#94A3B8",

                fontsize=8
            )

            ax.tick_params(

                colors="#94A3B8",

                labelsize=7
            )

            ax.grid(

                True,

                color="#334155",

                linestyle="--",

                linewidth=0.5,

                alpha=0.35
            )

            for spine in ax.spines.values():

                spine.set_color("#29384C")

            legend = ax.legend(

                loc="upper left",

                fontsize=7,

                facecolor="#111827",

                edgecolor="#29384C"
            )

            for text in legend.get_texts():

                text.set_color("#CBD5E1")

            fig.subplots_adjust(

                left=0.07,

                right=0.98,

                top=0.94,

                bottom=0.17
            )

            encoded_image = figure_to_base64(fig)

        finally:

            plt.close(fig)

    st.html(f"""

    <img
        class="fitness-image"
        src="data:image/png;base64,{encoded_image}"
        alt="Current fitness landscape"
    />

    """)


# ============================================================
# 19. TARGET STATUS
# ============================================================

def display_target_status():

    position = get_display_position()

    distance = get_distance_from_target()

    status, color = get_target_status(
        position
    )

    if position > TARGET_POSITION:

        distance_label = (
            f"OVERSHOOT: {distance} UNIT(S)"
        )

    elif position == TARGET_POSITION:

        distance_label = "DISTANCE: 0"

    else:

        distance_label = (
            f"DISTANCE: {distance} UNIT(S)"
        )

    st.html(f"""

    <div class="target-status">

        <div class="target-status-label">

            TARGET: POSITION {TARGET_POSITION}

        </div>

        <div class="target-status-value"
             style="color:{color};">

            {escape(status)}

        </div>

        <div class="target-status-label">

            {escape(distance_label)}

        </div>

    </div>

    """)


# ============================================================
# 20. LIVE EVOLUTION FEEDBACK
# ============================================================

def display_feedback():

    feedback_class = ""

    if st.session_state.mission_success:

        feedback_class = "feedback-success"

    elif st.session_state.mission_failed:

        feedback_class = "feedback-failed"

    st.html(f"""

    <div class="feedback-box {feedback_class}">

        <div class="feedback-title">

            LIVE EVOLUTION FEEDBACK

        </div>

        <div class="feedback-text">

            {escape(st.session_state.feedback)}

        </div>

    </div>

    """)


# ============================================================
# 21. MISSION RESULT POP-UP
# ============================================================

@st.dialog(

    "Mission Result",

    width="large",

    dismissible=False
)
def mission_result_dialog():

    success = st.session_state.mission_success

    strategy = st.session_state.settings[0]

    generation = st.session_state.generation

    final_x = get_display_position()

    final_fitness = float(
        fitness(final_x)
    )

    final_sigma = get_display_sigma()

    distance = get_distance_from_target()


    # --------------------------------------------------------
    # SUCCESS RESULT
    # --------------------------------------------------------

    if success:

        result_class = "result-success"

        icon = "🏆"

        title = "MISSION COMPLETE"

        color = "#4ADE80"

        description = (

            "Congratulations! You landed exactly "
            "at the Global Optimum."
        )

        reason_title = "EXACT GLOBAL OPTIMUM REACHED"

        reason = (

            f"Individual "
            f"{st.session_state.trigger_individual} "
            f"moved from position "
            f"{st.session_state.trigger_parent_position} "
            f"to exactly position {TARGET_POSITION} "
            f"in generation {generation}. "
            "Target distance is zero."
        )


    # --------------------------------------------------------
    # FAILED RESULT
    # --------------------------------------------------------

    else:

        result_class = "result-failed"

        icon = "❌"

        title = "MISSION FAILED"

        color = "#F87171"

        if (

            st.session_state.failure_type
            == "OVERSHOOT"
        ):

            description = (

                "You overshot the Global Optimum! "
                "Your mission has ended immediately."
            )

        else:

            description = (

                "You reached the generation limit "
                "without landing exactly at position 79."
            )

        reason_title, reason = get_failure_reason(
            final_x
        )


    result_cards = "".join([

        result_metric_html(

            "FINAL POSITION",

            final_x,

            color
        ),

        result_metric_html(

            "FINAL FITNESS",

            f"{final_fitness:.2f}",

            "#FBBF24"
        ),

        result_metric_html(

            "GENERATION",

            f"{generation}/{MAX_GENERATIONS}",

            "#67E8F9"
        ),

        result_metric_html(

            "TARGET DISTANCE",

            distance,

            color
        )
    ])

    st.html(f"""

    <div class="result-container {result_class}">

        <div class="result-icon">

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

        <div class="result-strategy"
             style="color:{STRATEGIES[strategy]['color']};">

            {escape(strategy)} Control

        </div>

        <div class="dialog-description">

            Initial Step Size:
            {st.session_state.settings[1]:.2f}

            &nbsp; | &nbsp;

            Final Step Size:
            {final_sigma:.2f}

        </div>

        <div class="result-reason">

            <div class="result-reason-title">

                {escape(reason_title)}

            </div>

            <div class="result-reason-text">

                {escape(reason)}

            </div>

        </div>

    </div>

    """)

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(

            "↻ PLAY AGAIN",

            key="result_play_again",

            type="primary",

            use_container_width=True
        ):

            handle_play_again()

            st.rerun()

    with col2:

        if st.button(

            "📊 PERFORMANCE ANALYSIS",

            key="result_performance",

            use_container_width=True
        ):

            open_dialog("performance")

            st.rerun()

    with col3:

        if st.button(

            "CLOSE",

            key="result_close",

            use_container_width=True
        ):

            close_dialog()

            st.rerun()


# ============================================================
# 22. PERFORMANCE ANALYSIS CHART
# ============================================================

def display_analysis_chart(

    values,

    title,

    ylabel,

    color,

    target=None,

    show_final_position=False
):

    generations = list(
        range(len(values))
    )

    with get_plot_lock():

        fig, ax = plt.subplots(

            figsize=(10, 2.6),

            dpi=130
        )

        try:

            fig.patch.set_facecolor("#080D1C")

            ax.set_facecolor("#080D1C")

            ax.plot(

                generations,

                values,

                color=color,

                linewidth=2,

                marker="o",

                markersize=3,

                label="Best surviving population"
            )

            ax.fill_between(

                generations,

                values,

                color=color,

                alpha=0.08
            )

            if target is not None:

                ax.axhline(

                    target,

                    color="#FBBF24",

                    linestyle="--",

                    linewidth=1,

                    label=f"Target: {target}"
                )

            if (

                show_final_position

                and st.session_state.game_finished

                and st.session_state.final_position
                is not None
            ):

                final_x = (
                    st.session_state.final_position
                )

                final_color = (

                    "#4ADE80"

                    if st.session_state.mission_success

                    else "#F87171"
                )

                ax.scatter(

                    st.session_state.generation,

                    final_x,

                    color=final_color,

                    marker="X",

                    s=100,

                    label="Mission final position",

                    zorder=8
                )

            ax.set_title(

                title,

                color="#E2E8F0",

                fontsize=10,

                fontweight="bold"
            )

            ax.set_xlabel(

                "Generation",

                color="#94A3B8",

                fontsize=8
            )

            ax.set_ylabel(

                ylabel,

                color="#94A3B8",

                fontsize=8
            )

            ax.set_xlim(
                0,
                max(1, len(values) - 1)
            )

            ax.tick_params(

                colors="#94A3B8",

                labelsize=7
            )

            ax.grid(

                True,

                color="#334155",

                linestyle="--",

                linewidth=0.5,

                alpha=0.4
            )

            for spine in ax.spines.values():

                spine.set_color("#29384C")

            if (

                target is not None

                or show_final_position
            ):

                legend = ax.legend(

                    fontsize=7,

                    facecolor="#111827",

                    edgecolor="#29384C"
                )

                for text in legend.get_texts():

                    text.set_color("#CBD5E1")

            fig.tight_layout(
                pad=1.2
            )

            encoded_image = figure_to_base64(fig)

        finally:

            plt.close(fig)

    st.html(f"""

    <img
        class="analysis-image"
        src="data:image/png;base64,{encoded_image}"
        alt="{escape(title)}"
    />

    """)


# ============================================================
# 23. HISTORY TABLE WITH PAGINATION
# ============================================================

def display_history_table():

    history_df = pd.DataFrame({

        "Generation": list(

            range(
                len(st.session_state.history)
            )
        ),

        "Best Fitness": [

            round(value, 2)

            for value in st.session_state.history
        ],

        "Best Position": (

            st.session_state.position_history
        ),

        "Step Size": [

            round(value, 2)

            for value in st.session_state.sigma_history
        ],

        "Distance": (

            st.session_state.distance_history
        ),

        "Success Rate": [

            f"{value:.0%}"

            for value in st.session_state.success_history
        ]
    })

    total_records = len(history_df)

    total_pages = max(

        1,

        int(
            np.ceil(
                total_records / HISTORY_PAGE_SIZE
            )
        )
    )

    page = max(

        0,

        min(

            st.session_state.history_page,

            total_pages - 1
        )
    )

    st.session_state.history_page = page

    start = page * HISTORY_PAGE_SIZE

    end = min(

        start + HISTORY_PAGE_SIZE,

        total_records
    )

    display_static_table(

        history_df.iloc[start:end]
    )

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col1:

        st.button(

            "◀ Previous",

            key="history_previous",

            disabled=(page == 0),

            use_container_width=True,

            on_click=change_history_page,

            args=(-1,)
        )

    with col2:

        st.html(f"""

        <div class="table-page">

            Page {page + 1} of {total_pages}

        </div>

        """)

    with col3:

        st.button(

            "Next ▶",

            key="history_next",

            disabled=(
                page >= total_pages - 1
            ),

            use_container_width=True,

            on_click=change_history_page,

            args=(1,)
        )


def change_history_page(direction):

    st.session_state.history_page += direction


# ============================================================
# 24. PERFORMANCE ANALYSIS POP-UP
# ============================================================

@st.dialog(

    "Performance Analysis",

    width="large",

    dismissible=False
)
def performance_dialog():

    strategy = st.session_state.settings[0]

    best_x = get_best_position()

    best_fitness = float(
        fitness(best_x)
    )

    final_x = get_display_position()

    generation = st.session_state.generation

    if st.session_state.mission_success:

        mission_status = "COMPLETE"

        status_color = "#4ADE80"

    elif st.session_state.mission_failed:

        mission_status = (

            st.session_state.failure_type
        )

        status_color = "#F87171"

    else:

        mission_status = "IN PROGRESS"

        status_color = "#FBBF24"

    cards = "".join([

        result_metric_html(

            "GENERATION",

            generation,

            "#67E8F9"
        ),

        result_metric_html(

            "BEST FITNESS",

            f"{best_fitness:.2f}",

            "#FBBF24"
        ),

        result_metric_html(

            "CURRENT / FINAL POSITION",

            final_x,

            "#67E8F9"
        ),

        result_metric_html(

            "MISSION STATUS",

            mission_status,

            status_color
        )
    ])

    st.html(f"""

    <div class="result-grid">

        {cards}

    </div>

    <div class="dialog-description">

        Strategy: {escape(strategy)} Control

        &nbsp; | &nbsp;

        Initial Sigma:
        {st.session_state.settings[1]:.2f}

        &nbsp; | &nbsp;

        Overshooting Offspring:
        {st.session_state.overshoot_count}

    </div>

    """)

    analysis_tab = st.radio(

        "Analysis Type",

        [

            "Fitness",

            "Step Size",

            "Position",

            "Success Rate",

            "History"
        ],

        horizontal=True,

        key="analysis_tab",

        label_visibility="collapsed"
    )

    if analysis_tab == "Fitness":

        display_analysis_chart(

            st.session_state.history,

            "Best Surviving Fitness",

            "Fitness",

            "#FBBF24",

            target=TARGET_FITNESS
        )

        st.html("""

        <div class="dialog-description">

            Shows how the fitness of the best
            surviving individual changes over time.

        </div>

        """)

    elif analysis_tab == "Step Size":

        display_analysis_chart(

            st.session_state.sigma_history,

            "Mutation Step Size",

            "Sigma",

            "#E879F9"
        )

        st.html("""

        <div class="dialog-description">

            Shows how the selected parameter
            control strategy changes mutation
            step size.

        </div>

        """)

    elif analysis_tab == "Position":

        display_analysis_chart(

            st.session_state.position_history,

            "Position Towards Global Optimum",

            "Position",

            "#22D3EE",

            target=TARGET_POSITION,

            show_final_position=True
        )

        st.html("""

        <div class="dialog-description">

            The gold line represents position 79.
            The final mission marker also shows
            an overshooting offspring, even if
            it was rejected during selection.

        </div>

        """)

    elif analysis_tab == "Success Rate":

        display_analysis_chart(

            [

                value * 100

                for value in
                st.session_state.success_history
            ],

            "Mutation Improvement Rate",

            "Success Rate (%)",

            "#4ADE80",

            target=20
        )

        st.html("""

        <div class="dialog-description">

            The 20% reference line represents
            the threshold used by Adaptive Control.

        </div>

        """)

    else:

        display_history_table()

    if st.button(

        "CLOSE",

        key="close_performance",

        use_container_width=True
    ):

        close_dialog()

        st.rerun()


# ============================================================
# 25. POPULATION DETAILS POP-UP
# ============================================================

@st.dialog(

    "Population Details",

    width="large",

    dismissible=False
)
def population_dialog():

    generation = st.session_state.generation

    strategy = st.session_state.settings[0]

    st.html(f"""

    <div class="dialog-description">

        Generation: {generation}

        &nbsp; | &nbsp;

        Population Size: {POPULATION_SIZE}

        &nbsp; | &nbsp;

        Strategy: {escape(strategy)}

    </div>

    """)

    population_view = st.radio(

        "Population View",

        [

            "Surviving Population",

            "Latest Mutations"
        ],

        horizontal=True,

        key="population_view",

        label_visibility="collapsed"
    )


    # --------------------------------------------------------
    # SURVIVING POPULATION
    # --------------------------------------------------------

    if population_view == "Surviving Population":

        rows = []

        for i, (x, sigma) in enumerate(

            st.session_state.population
        ):

            if x == TARGET_POSITION:

                status = "Exact Hit"

            elif x > TARGET_POSITION:

                status = "Overshoot"

            else:

                status = "Below Target"

            rows.append({

                "Individual": i + 1,

                "Position": int(x),

                "Fitness": round(
                    float(fitness(x)), 2
                ),

                "Sigma": round(sigma, 2),

                "Distance": abs(
                    TARGET_POSITION - x
                ),

                "Status": status
            })

        display_static_table(

            pd.DataFrame(rows)
        )

        st.html("""

        <div class="dialog-description">

            These individuals were retained
            through fitness-based survival selection.

            The offspring responsible for mission
            failure may not be part of this population.

        </div>

        """)


    # --------------------------------------------------------
    # LATEST MUTATIONS
    # --------------------------------------------------------

    else:

        if not st.session_state.last_mutations:

            st.info(

                "Run the first generation to view "
                "mutation details."
            )

        else:

            mutation_df = pd.DataFrame(

                st.session_state.last_mutations
            )

            display_static_table(

                mutation_df[[

                    "Individual",

                    "Parent",

                    "Offspring",

                    "Movement",

                    "Sigma",

                    "Target Result"
                ]]
            )

            st.html("""

            <div class="dialog-description">

                EXACT HIT = position 79.

                <br>

                OVERSHOOT = position greater than 79.

                <br>

                BELOW TARGET = position less than 79.

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
# 26. LEARNING GUIDE CONTENT
# ============================================================

LEARNING_CONTENT = {

    "Game Rules": {

        "title": "Exact Peak Challenge",

        "color": "#FBBF24",

        "description": (

            "Your objective is to evolve a population "
            "that lands exactly at position 79."
        ),

        "points": [

            "All five individuals begin at position 10.",

            "An offspring at exactly 79 completes "
            "the mission.",

            "An offspring above 79 causes immediate "
            "failure unless another offspring hits 79 "
            "in the same generation.",

            "Remaining below 79 after generation 30 "
            "causes mission failure."
        ],

        "example": (

            "Position 78 → 79: Mission Complete. "
            "Position 78 → 83: Mission Failed."
        )
    },

    "Deterministic": {

        "title": "Deterministic Parameter Control",

        "color": "#22D3EE",

        "description": (

            "The mutation step size follows a "
            "predefined schedule."
        ),

        "points": [

            "The initial step size is selected "
            "by the player.",

            "Step size decreases as the generation "
            "number increases.",

            "Larger early steps encourage exploration.",

            "Smaller later steps encourage refinement."
        ],

        "example": (

            "With initial sigma 30, the step size "
            "becomes 29 after generation 1 and "
            "15 after generation 15."
        )
    },

    "Adaptive": {

        "title": "Adaptive Parameter Control",

        "color": "#FBBF24",

        "description": (

            "The mutation step size changes according "
            "to the success rate of recent mutations."
        ),

        "points": [

            "Success rate above 20%: "
            "increase sigma by 25%.",

            "Success rate below 20%: "
            "decrease sigma by 20%.",

            "Success rate equal to 20%: "
            "keep sigma unchanged.",

            "Larger sigma may increase the chance "
            "of overshooting the target."
        ],

        "example": (

            "If three out of five mutations improve "
            "fitness, the success rate is 60%. "
            "Sigma 20 increases to 25."
        )
    },

    "Self-Adaptive": {

        "title": "Self-Adaptive Parameter Control",

        "color": "#E879F9",

        "description": (

            "Each individual carries its own mutation "
            "step size as part of its representation."
        ),

        "points": [

            "Each individual starts with the selected "
            "initial sigma.",

            "Sigma itself undergoes mutation.",

            "Individuals can evolve different "
            "mutation step sizes.",

            "Fitness-based selection determines "
            "which individuals and sigmas survive."
        ],

        "example": (

            "Individual 1 may evolve sigma 8 while "
            "Individual 2 evolves sigma 25. "
            "Their mutation movements can therefore "
            "have different magnitudes."
        )
    },

    "Step Size": {

        "title": "Mutation Step Size (Sigma)",

        "color": "#67E8F9",

        "description": (

            "Sigma controls the spread of random "
            "mutation movements."
        ),

        "points": [

            "Small sigma produces generally "
            "smaller movements.",

            "Large sigma produces a wider range "
            "of possible movements.",

            "Large movements can escape a local "
            "optimum but may overshoot.",

            "Small movements can refine a solution "
            "but may become trapped."
        ],

        "example": (

            "At position 75, a movement of +4 "
            "wins the mission. A movement of +10 "
            "overshoots to position 85."
        )
    }
}


# ============================================================
# 27. LEARNING GUIDE POP-UP
# ============================================================

@st.dialog(

    "Learning Guide",

    width="large",

    dismissible=False
)
def learning_dialog():

    selected_topic = st.radio(

        "Learning Topic",

        list(
            LEARNING_CONTENT.keys()
        ),

        horizontal=True,

        key="learning_topic",

        label_visibility="collapsed"
    )

    content = LEARNING_CONTENT[
        selected_topic
    ]

    points_html = "".join([

        f"""

        <div class="guide-point">

            {escape(point)}

        </div>

        """

        for point in content["points"]
    ])

    st.html(f"""

    <div class="guide-card">

        <div class="guide-title"
             style="color:{content['color']};">

            {escape(content['title'])}

        </div>

        <div class="guide-description">

            {escape(content['description'])}

        </div>

        {points_html}

        <div class="guide-example">

            <strong>Example:</strong>

            {escape(content['example'])}

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
# 28. MAIN DASHBOARD
# ============================================================

def display_dashboard():

    display_header()

    with st.container(key="main_dashboard"):

        left_column, right_column = st.columns(

            [1, 3.2],

            gap="medium"
        )


        # ====================================================
        # LEFT CONTROL PANEL
        # ====================================================

        with left_column:

            with st.container(key="left_panel"):

                section_heading(

                    "01 / PARAMETER CONTROL"
                )

                strategy = st.radio(

                    "Parameter Control Strategy",

                    list(STRATEGIES.keys()),

                    key="selected_strategy",

                    label_visibility="collapsed",

                    on_change=handle_settings_change
                )

                strategy_info = STRATEGIES[
                    strategy
                ]

                st.html(f"""

                <div class="strategy-description">

                    <div
                        class="strategy-description-title"
                        style="
                            color:{strategy_info['color']};
                        "
                    >

                        {strategy_info['icon']}

                        {escape(strategy)} Control

                    </div>

                    <div class="strategy-description-text">

                        {escape(strategy_info['description'])}

                    </div>

                </div>

                """)


                # --------------------------------------------
                # INITIAL STEP SIZE
                # --------------------------------------------

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

                    Large σ = wider exploration
                    and overshoot risk.

                    <br>

                    Changing settings resets the mission.

                </div>

                """)


                # --------------------------------------------
                # SIMULATION CONTROLS
                # --------------------------------------------

                section_heading(

                    "03 / SIMULATION CONTROLS"
                )

                st.button(

                    "▶ NEXT GENERATION",

                    key="next_generation_button",

                    type="primary",

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

                    key="reset_simulation_button",

                    use_container_width=True,

                    on_click=handle_reset
                )


                # --------------------------------------------
                # MISSION OBJECTIVE
                # --------------------------------------------

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

                        <span style="color:#4ADE80;">
                            Exact hit = Mission Complete
                        </span>

                        <br>

                        <span style="color:#F87171;">
                            Overshoot = Immediate Failure
                        </span>

                    </div>

                </div>

                """)


        # ====================================================
        # RIGHT VISUALIZATION PANEL
        # ====================================================

        with right_column:

            with st.container(key="right_panel"):

                display_metrics(strategy)

                section_heading(

                    "FITNESS LANDSCAPE"
                )

                display_fitness_landscape(

                    STRATEGIES[strategy]["color"]
                )

                display_target_status()

                display_feedback()

                if st.session_state.game_finished:

                    st.button(

                        "VIEW MISSION RESULT",

                        key="view_result_button",

                        use_container_width=True,

                        on_click=open_dialog,

                        args=("result",)
                    )


    # ========================================================
    # BOTTOM NAVIGATION
    # ========================================================

    with st.container(key="bottom_navigation"):

        p1, p2, p3, p4 = st.columns(4)

        with p1:

            st.button(

                "📊 Performance Analysis",

                key="performance_button",

                use_container_width=True,

                on_click=open_dialog,

                args=("performance",)
            )

        with p2:

            st.button(

                "🧬 Population Details",

                key="population_button",

                use_container_width=True,

                on_click=open_dialog,

                args=("population",)
            )

        with p3:

            st.button(

                "📖 Learning Guide",

                key="learning_button",

                use_container_width=True,

                on_click=open_dialog,

                args=("learning",)
            )

        with p4:

            st.button(

                "🏠 Main Menu",

                key="main_menu_button",

                use_container_width=True,

                on_click=handle_home
            )


# ============================================================
# 29. APPLICATION ROUTING
# ============================================================

if not st.session_state.game_started:

    display_welcome_screen()

else:

    display_dashboard()

    active_dialog = st.session_state.active_dialog

    if active_dialog == "result":

        mission_result_dialog()

    elif active_dialog == "performance":

        performance_dialog()

    elif active_dialog == "population":

        population_dialog()

    elif active_dialog == "learning":

        learning_dialog()

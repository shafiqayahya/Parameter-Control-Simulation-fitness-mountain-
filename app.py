
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
   GLOBAL BACKGROUND
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
    height: 32px;

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

    padding: 12px 24px !important;

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


[data-testid="stHtml"] {

    margin: 0 !important;

}


/* =========================================================
   APPLICATION HEADER
   ========================================================= */

.hero {

    text-align: center;

    padding: 0 0 5px;
    margin: 0;

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

    font-size: clamp(25px, 4dvh, 34px);

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


.st-key-welcome_screen
[data-testid="stVerticalBlock"] {

    gap: 6px !important;

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
    max-width: 410px;

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
   GENERATION PROGRESS
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

    height: clamp(170px, 37dvh, 340px);

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
   NO VERTICAL OR HORIZONTAL SCROLL
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


[data-testid="stDialog"] h1 {

    font-size: 23px !important;

    margin: 0 !important;

    padding: 0 !important;

}


[data-testid="stDialog"] h2 {

    font-size: 19px !important;

    margin: 0 !important;

    padding: 0 !important;

}


[data-testid="stDialog"] h3 {

    font-size: 16px !important;

    margin: 0 !important;

    padding: 0 !important;

}


[data-testid="stDialog"] p {

    font-size: 12px;

    line-height: 1.4;

}


[data-testid="stDialog"]
[data-baseweb="tab-list"] {

    gap: 8px !important;

    overflow: hidden !important;

}


[data-testid="stDialog"]
[data-baseweb="tab"] {

    padding: 5px 10px !important;

    min-height: 32px !important;

}


[data-testid="stDialog"]
[data-testid="stMetricValue"] {

    font-size: 23px !important;

}


[data-testid="stDialog"]
.stButton > button {

    min-height: 32px !important;

    padding: 4px 10px !important;

}


/* =========================================================
   MISSION RESULT POP-UP
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


.analysis-image-small {

    height: 26dvh;

    max-height: 220px;

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
   STATIC TABLES
   NO INTERNAL TABLE SCROLL
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

    .block-container >
    [data-testid="stVerticalBlock"],

    .st-key-left_panel
    [data-testid="stVerticalBlock"],

    .st-key-right_panel
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

        height: 34dvh;

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
   SHORT DESKTOP VIEWPORT
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

        height: 30dvh;

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

    .st-key-left_panel [role="radiogroup"] label {

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
   SMALL DEVICE FALLBACK
   Preserve access to controls on narrow mobile devices.
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

SIMULATION_VERSION = "exact_peak_fixed_v3"

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

    st.session_state.mission_success = False

    st.session_state.mission_failed = False

    st.session_state.game_finished = False

    st.session_state.success_generation = None

    st.session_state.result_shown = False

    st.session_state.active_dialog = None

    st.session_state.history_page = 0

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

        individual_sigma = float(individual_sigma)

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

        parent_fitness = float(fitness(x))

        child_fitness = float(fitness(child_x))

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

            "The best surviving individual's step size "

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

    best_x = int(new_population[0][0])

    best_fitness = float(fitness(best_x))

    distance = abs(TARGET_POSITION - best_x)


    # --------------------------------------------------------
    # EXACT GLOBAL OPTIMUM CHECK
    # --------------------------------------------------------

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

    st.session_state.last_mutations = mutation_details

    st.session_state.mission_success = mission_success

    st.session_state.mission_failed = mission_failed

    st.session_state.game_finished = game_finished

    st.session_state.success_generation = success_generation


    # --------------------------------------------------------
    # UPDATE HISTORIES
    # --------------------------------------------------------

    st.session_state.history.append(best_fitness)

    st.session_state.sigma_history.append(
        float(new_sigma)
    )

    st.session_state.position_history.append(best_x)

    st.session_state.distance_history.append(distance)

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

            local_y = float(fitness(LOCAL_OPTIMUM))

            global_y = float(fitness(GLOBAL_OPTIMUM))

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
            alt="Fitness landscape"
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

    generation = st.session_state.generation

    best_x = get_best_position()

    best_fitness = float(fitness(best_x))

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

    best_fitness = float(fitness(best_x))

    x_values = np.linspace(

        MIN_POSITION,

        MAX_POSITION,

        1001

    )

    y_values = fitness(x_values)

    with get_plot_lock():

        fig, ax = plt.subplots(

            figsize=(12, 3.4),

            dpi=130

        )

        try:

            fig.patch.set_facecolor("#0B1120")

            ax.set_facecolor("#0B1120")


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

            local_y = float(fitness(LOCAL_OPTIMUM))

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

                fontsize=9,

                ha="center",

                fontweight="bold"

            )


            # GLOBAL OPTIMUM

            global_y = float(fitness(GLOBAL_OPTIMUM))

            ax.scatter(

                GLOBAL_OPTIMUM,

                global_y,

                color="#FBBF24",

                marker="*",

                s=230,

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

                fontsize=9,

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

                spine.set_color("#29384C")

            legend = ax.legend(

                loc="upper left",

                fontsize=8,

                facecolor="#111827",

                edgecolor="#29384C"

            )

            for text in legend.get_texts():

                text.set_color("#CBD5E1")

            fig.subplots_adjust(

                left=0.065,

                right=0.985,

                top=0.96,

                bottom=0.16

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

    best_x = get_best_position()

    distance = get_distance_from_target()

    status, color = get_target_status(best_x)

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

            DISTANCE: {distance} UNIT(S)

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
# 21. POP-UP: MISSION RESULT
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

    best_x = get_best_position()

    best_fitness = float(fitness(best_x))

    distance = get_distance_from_target()

    if success:

        result_class = "result-success"

        icon = "🏆"

        title = "MISSION COMPLETE"

        color = "#4ADE80"

        description = (

            "Congratulations! You reached the "
            "exact Global Optimum."

        )

        reason_title = "WHY YOU SUCCEEDED"

        reason = (

            f"Your population reached exactly position "
            f"{TARGET_POSITION} in generation {generation}. "
            "The distance from the target is zero."

        )

    else:

        result_class = "result-failed"

        icon = "❌"

        title = "MISSION FAILED"

        color = "#F87171"

        description = (

            "The population did not reach the "
            "exact Global Optimum within 30 generations."

        )

        reason_title, reason = get_failure_reason(best_x)

    result_cards = "".join([

        result_metric_html(

            "FINAL POSITION",

            best_x,

            color

        ),

        result_metric_html(

            "BEST FITNESS",

            f"{best_fitness:.2f}",

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
            {st.session_state.sigma:.2f}

        </div>

        <div class="result-reason">

            <div class="result-reason-title">

                {escape(reason_title.upper())}

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

            "📊 VIEW RESULTS",

            key="result_view_results",

            use_container_width=True

        ):

            st.session_state.result_shown = True

            open_dialog("performance")

            st.rerun()

    with col3:

        if st.button(

            "🏠 MAIN MENU",

            key="result_main_menu",

            use_container_width=True

        ):

            handle_home()

            st.rerun()


# ============================================================
# 22. ANALYSIS CHART
# ============================================================

def display_analysis_chart(

    values,

    title,

    ylabel,

    color,

    target=None,

    compact=False

):

    generations = list(range(len(values)))

    figure_size = (

        (5.5, 2.5)

        if compact

        else (10, 2.6)

    )

    with get_plot_lock():

        fig, ax = plt.subplots(

            figsize=figure_size,

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

                markersize=3

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

                    alpha=0.8,

                    label=f"Target: {target}"

                )

                legend = ax.legend(

                    fontsize=8,

                    facecolor="#111827",

                    edgecolor="#29384C"

                )

                for text in legend.get_texts():

                    text.set_color("#E2E8F0")

            ax.set_title(

                title,

                color="#E2E8F0",

                fontsize=10,

                fontweight="bold",

                pad=8

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

            if ylabel == "Success Rate (%)":

                ax.set_ylim(-5, 105)

            ax.tick_params(

                colors="#94A3B8",

                labelsize=8

            )

            ax.grid(

                color="#334155",

                linestyle="--",

                alpha=0.3

            )

            for spine in ax.spines.values():

                spine.set_color("#29384C")

            fig.tight_layout(pad=1.2)

            encoded_image = figure_to_base64(fig)

        finally:

            plt.close(fig)

    image_class = (

        "analysis-image analysis-image-small"

        if compact

        else "analysis-image"

    )

    st.html(f"""

    <img
        class="{image_class}"
        src="data:image/png;base64,{encoded_image}"
        alt="{escape(title)}"
    />

    """)


# ============================================================
# 23. PAGINATED HISTORY TABLE
# ============================================================

def display_history_table():

    history_df = pd.DataFrame({

        "Generation": list(

            range(len(st.session_state.history))

        ),

        "Best Fitness": [

            f"{value:.2f}"

            for value in st.session_state.history

        ],

        "Step Size": [

            f"{value:.2f}"

            for value in st.session_state.sigma_history

        ],

        "Position": st.session_state.position_history,

        "Distance": st.session_state.distance_history,

        "Success Rate": [

            f"{value:.0%}"

            for value in st.session_state.success_history

        ]

    })

    total_records = len(history_df)

    total_pages = max(

        1,

        (total_records + HISTORY_PAGE_SIZE - 1)

        // HISTORY_PAGE_SIZE

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

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:

        st.button(

            "◀ PREVIOUS",

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

            <br>

            Records {start + 1}–{end}
            of {total_records}

        </div>

        """)

    with col3:

        st.button(

            "NEXT ▶",

            key="history_next",

            disabled=(page >= total_pages - 1),

            use_container_width=True,

            on_click=change_history_page,

            args=(1,)

        )


def change_history_page(direction):

    st.session_state.history_page += direction


# ============================================================
# 24. POP-UP: PERFORMANCE ANALYSIS
# ============================================================

@st.dialog(

    "Performance Analysis",

    width="large",

    dismissible=False

)
def performance_dialog():

    strategy = st.session_state.settings[0]

    best_x = get_best_position()

    best_fitness = float(fitness(best_x))

    distance = get_distance_from_target()

    generation = st.session_state.generation

    cards = "".join([

        result_metric_html(

            "STRATEGY",

            strategy,

            STRATEGIES[strategy]["color"]

        ),

        result_metric_html(

            "BEST FITNESS",

            f"{best_fitness:.2f}",

            "#FBBF24"

        ),

        result_metric_html(

            "GENERATION",

            f"{generation}/{MAX_GENERATIONS}",

            "#67E8F9"

        ),

        result_metric_html(

            "DISTANCE",

            distance,

            "#4ADE80" if distance == 0 else "#E879F9"

        )

    ])

    st.html(f"""

    <div class="result-grid">

        {cards}

    </div>

    """)

    analysis_tab = st.radio(

        "Analysis View",

        [

            "Fitness",

            "Step Size",

            "Position",

            "Success Rate",

            "History"

        ],

        horizontal=True,

        label_visibility="collapsed",

        key="analysis_view"

    )


    # --------------------------------------------------------
    # FITNESS ANALYSIS
    # --------------------------------------------------------

    if analysis_tab == "Fitness":

        display_analysis_chart(

            st.session_state.history,

            "Best Fitness by Generation",

            "Fitness",

            "#22D3EE",

            target=TARGET_FITNESS

        )

        st.html("""

        <div class="dialog-description">

            Higher fitness indicates a better solution.
            The population retains its best surviving
            individuals after every generation.

        </div>

        """)


    # --------------------------------------------------------
    # STEP SIZE ANALYSIS
    # --------------------------------------------------------

    elif analysis_tab == "Step Size":

        display_analysis_chart(

            st.session_state.sigma_history,

            "Mutation Step Size by Generation",

            "Step Size",

            "#E879F9"

        )

        st.html(f"""

        <div class="dialog-description">

            Initial step size:
            {st.session_state.settings[1]:.2f}

            &nbsp; | &nbsp;

            Current step size:
            {st.session_state.sigma:.2f}

        </div>

        """)


    # --------------------------------------------------------
    # POSITION ANALYSIS
    # TWO CHARTS SIDE BY SIDE
    # --------------------------------------------------------

    elif analysis_tab == "Position":

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            display_analysis_chart(

                st.session_state.position_history,

                "Best Position",

                "Position",

                "#4ADE80",

                target=TARGET_POSITION,

                compact=True

            )

        with chart_col2:

            display_analysis_chart(

                st.session_state.distance_history,

                "Distance from Global Optimum",

                "Distance",

                "#FBBF24",

                target=0,

                compact=True

            )

        st.html("""

        <div class="dialog-description">

            Mission success requires the best position
            to reach exactly 79 and the target distance
            to become zero.

        </div>

        """)


    # --------------------------------------------------------
    # SUCCESS RATE ANALYSIS
    # --------------------------------------------------------

    elif analysis_tab == "Success Rate":

        success_percentages = [

            value * 100

            for value in st.session_state.success_history

        ]

        display_analysis_chart(

            success_percentages,

            "Successful Mutations by Generation",

            "Success Rate (%)",

            "#FBBF24",

            target=20 if strategy == "Adaptive" else None

        )

        st.html("""

        <div class="dialog-description">

            A successful mutation produces an offspring
            with higher fitness than its parent.

            Generation 0 represents the initial population.

        </div>

        """)


    # --------------------------------------------------------
    # PAGINATED HISTORY
    # --------------------------------------------------------

    elif analysis_tab == "History":

        display_history_table()


    # --------------------------------------------------------
    # CLOSE BUTTON
    # --------------------------------------------------------

    if st.button(

        "CLOSE",

        key="close_performance",

        use_container_width=True

    ):

        close_dialog()

        st.rerun()


# ============================================================
# 25. POP-UP: POPULATION DETAILS
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

        Generation {generation}/{MAX_GENERATIONS}

        &nbsp; | &nbsp;

        Population Size: {POPULATION_SIZE}

        &nbsp; | &nbsp;

        Strategy: {escape(strategy)}

    </div>

    """)

    population_view = st.radio(

        "Population View",

        [

            "Current Population",

            "Latest Mutation"

        ],

        horizontal=True,

        label_visibility="collapsed",

        key="population_view"

    )


    # --------------------------------------------------------
    # CURRENT POPULATION
    # --------------------------------------------------------

    if population_view == "Current Population":

        population_rows = []

        for index, (x, sigma) in enumerate(

            st.session_state.population

        ):

            population_rows.append({

                "Individual": index + 1,

                "Position": int(x),

                "Fitness": f"{fitness(x):.2f}",

                "Step Size": f"{sigma:.2f}",

                "Distance": abs(

                    TARGET_POSITION - int(x)

                ),

                "Status": (

                    "Best Individual"

                    if index == 0

                    else "Survivor"

                )

            })

        population_df = pd.DataFrame(population_rows)

        display_static_table(population_df)

        st.html("""

        <div class="guide-example">

            The five individuals with the highest fitness
            survive to the next generation.

        </div>

        """)


    # --------------------------------------------------------
    # LATEST MUTATION PROCESS
    # --------------------------------------------------------

    elif population_view == "Latest Mutation":

        if not st.session_state.last_mutations:

            st.html("""

            <div class="guide-card">

                <div class="guide-title"
                     style="color:#22D3EE;">

                    No Mutation Yet

                </div>

                <div class="guide-description">

                    Press Next Generation to generate
                    offspring and observe the mutation
                    process.

                </div>

            </div>

            """)

        else:

            mutation_df = pd.DataFrame(

                st.session_state.last_mutations

            )

            mutation_df = mutation_df.rename(

                columns={

                    "Individual": "ID",

                    "Parent Position": "Parent",

                    "Offspring Position": "Offspring",

                    "Movement": "Move",

                    "Step Size Used": "Sigma",

                    "Parent Fitness": "Parent Fitness",

                    "Offspring Fitness": "Child Fitness",

                    "Mutation Result": "Result"

                }

            )

            display_static_table(mutation_df)

            improved_count = sum(

                row["Mutation Result"] == "Improved"

                for row in st.session_state.last_mutations

            )

            success_rate = (

                improved_count / POPULATION_SIZE

            )

            st.html(f"""

            <div class="guide-example">

                Successful mutations:
                {improved_count}/{POPULATION_SIZE}

                &nbsp; | &nbsp;

                Success rate: {success_rate:.0%}

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

    "Deterministic": {

        "title": "⏱️ Deterministic Control",

        "color": "#22D3EE",

        "description": (

            "The mutation step size changes according "
            "to a predefined schedule."

        ),

        "points": [

            "The step size decreases as generations increase.",

            "The adjustment does not depend on mutation success.",

            "Large initial steps encourage exploration, "
            "while smaller later steps encourage refinement."

        ],

        "example": (

            "Formula: σ = max(0.5, initial σ × "
            "(1 − generation / 30))."

        )

    },

    "Adaptive": {

        "title": "⚡ Adaptive Control",

        "color": "#FBBF24",

        "description": (

            "The mutation step size changes according "
            "to feedback from mutation success."

        ),

        "points": [

            "Success rate above 20%: increase step size by 25%.",

            "Success rate below 20%: decrease step size by 20%.",

            "Success rate exactly 20%: maintain the current step size."

        ],

        "example": (

            "Example: If 3 out of 5 mutations improve fitness, "
            "the success rate is 60%. A step size of 15 "
            "increases to 18.75."

        )

    },

    "Self-Adaptive": {

        "title": "🧬 Self-Adaptive Control",

        "color": "#E879F9",

        "description": (

            "Each individual carries and evolves "
            "its own mutation step size."

        ),

        "points": [

            "Every individual has its own position and sigma.",

            "During mutation, sigma and position evolve together.",

            "Survival selection retains individuals "
            "with higher fitness and their associated sigma."

        ],

        "example": (

            "Formula: offspring σ = parent σ × exp(0.4 × N(0,1)), "
            "bounded between 0.5 and 50."

        )

    },

    "Optimum": {

        "title": "⛰️ Local vs Global Optimum",

        "color": "#67E8F9",

        "description": (

            "The fitness landscape contains two "
            "important mountain peaks."

        ),

        "points": [

            "Local Optimum: position 27. "
            "A smaller peak that may trap the population.",

            "Global Optimum: position 79. "
            "The highest integer-position fitness.",

            "Exploration helps escape local optima, "
            "while refinement helps reach the exact peak."

        ],

        "example": (

            "A fitness value close to 100 does not "
            "automatically mean the exact target has been reached."

        )

    },

    "Mission Rules": {

        "title": "🎯 Mission Rules",

        "color": "#4ADE80",

        "description": (

            "Your objective is to reach exactly position 79 "
            "within a maximum of 30 generations."

        ),

        "points": [

            "Position 79: Mission Complete immediately.",

            "Position below or above 79: continue searching "
            "while generations remain.",

            "Generation 30 without position 79: Mission Failed."

        ],

        "example": (

            "Position 78 = distance 1. "
            "Position 80 = distance 1. "
            "Only position 79 has distance 0."

        )

    }

}


# ============================================================
# 27. POP-UP: LEARNING GUIDE
# ============================================================

@st.dialog(

    "Learning Guide",

    width="large",

    dismissible=False

)
def learning_dialog():

    st.html("""

    <div class="dialog-description">

        Understand how parameter control affects
        the evolutionary search process.

    </div>

    """)

    selected_topic = st.radio(

        "Learning Topic",

        list(LEARNING_CONTENT.keys()),

        horizontal=True,

        label_visibility="collapsed",

        key="learning_topic"

    )

    content = LEARNING_CONTENT[selected_topic]

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

            [1, 3.3],

            gap="medium"

        )


        # ====================================================
        # LEFT CONTROL PANEL
        # ====================================================

        with left_column:

            with st.container(key="left_panel"):


                # --------------------------------------------
                # PARAMETER CONTROL
                # --------------------------------------------

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

                strategy_info = STRATEGIES[strategy]

                accent = strategy_info["color"]

                st.html(f"""

                <div class="strategy-description">

                    <div
                        class="strategy-description-title"
                        style="color:{accent};"
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

                    Large σ = wider exploration.

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

                    disabled=st.session_state.game_finished,

                    on_click=handle_next_generation

                )

                st.button(

                    "⏩ RUN ALL GENERATIONS",

                    key="run_all_button",

                    use_container_width=True,

                    disabled=st.session_state.game_finished,

                    on_click=handle_run_all

                )

                st.button(

                    "↻ RESET SIMULATION",

                    key="reset_simulation_button",

                    use_container_width=True,

                    on_click=handle_reset

                )

                if st.session_state.game_finished:

                    st.button(

                        "🏆 VIEW MISSION RESULT",

                        key="view_result_button",

                        use_container_width=True,

                        on_click=open_dialog,

                        args=("result",)

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

                        Target distance must be zero.

                    </div>

                </div>

                """)


        # ====================================================
        # RIGHT MONITORING PANEL
        # ====================================================

        with right_column:

            with st.container(key="right_panel"):

                strategy = st.session_state.settings[0]

                accent = STRATEGIES[strategy]["color"]


                # --------------------------------------------
                # METRIC CARDS
                # --------------------------------------------

                display_metrics(strategy)


                # --------------------------------------------
                # FITNESS LANDSCAPE
                # --------------------------------------------

                section_heading(

                    "FITNESS LANDSCAPE"

                )

                display_fitness_landscape(accent)


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

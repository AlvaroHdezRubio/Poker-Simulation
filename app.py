# ============================================================
# POKER LAB BY ÁLVARO HDEZ
# Calculadora visual de probabilidades de Texas Hold'em
# ============================================================

import base64
import random
from pathlib import Path

import streamlit as st
from treys import Card, Evaluator


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Poker Lab by Álvaro Hdez",
    page_icon="♠️",
    layout="centered"
)


# ============================================================
# 2. CARGAR LA IMAGEN DEL JOKER
# ============================================================

def image_b64(image_path):
    """
    Convierte joker.png a Base64 para utilizarlo
    como imagen decorativa.
    """

    path = Path(image_path)

    if not path.exists():
        return None

    return base64.b64encode(
        path.read_bytes()
    ).decode("utf-8")


JOKER_IMAGE = image_b64("joker.png")


# ============================================================
# 3. ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>

    /* Ocultar la cabecera superior de Streamlit */

    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        display: none !important;
    }

    header[data-testid="stHeader"] {
        height: 0 !important;
        min-height: 0 !important;
    }

    .stAppViewContainer {
        padding-top: 0 !important;
    }


    /* Fondo verde tipo tapete */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #176b45 0%,
                #0d5638 35%,
                #073b29 75%,
                #052d20 100%
            );

        color: #ffffff;
    }


    /* Contenedor principal */

    .block-container {
        position: relative;
        z-index: 5;

        width: 100%;
        max-width: 920px;

        padding-top: 0.60rem !important;
        padding-bottom: 1rem !important;
    }


    /* ======================================================
       CABECERA CORPORATIVA
       ====================================================== */

    .brand-header {
        position: relative;
        z-index: 20;

        margin: 0 0 0.90rem 0;
        padding: 0;
    }

    .brand-main {
        display: flex;
        align-items: center;

        gap: 0.42rem;

        font-size: 1.78rem;
        font-weight: 900;
        line-height: 1.05;

        background:
            linear-gradient(
                180deg,
                #fff2a8 0%,
                #f2c24f 42%,
                #d99a16 100%
            );

        -webkit-background-clip: text;
        background-clip: text;

        color: transparent;

        text-shadow:
            0 2px 4px rgba(0, 0, 0, 0.72),
            0 0 16px rgba(242, 194, 79, 0.22);
    }

    .brand-symbol {
        color: #f2c24f;
        -webkit-text-fill-color: #f2c24f;

        filter:
            drop-shadow(
                0 2px 2px rgba(0, 0, 0, 0.55)
            );
    }

    .brand-signature {
        display: block;

        margin-top: 0.42rem;
        margin-left: 2rem;

        color: rgba(255, 255, 255, 0.90);

        font-size: 0.66rem;
        font-weight: 700;
        line-height: 1.30;
        letter-spacing: 0.13rem;
    }


    /* ======================================================
       PANEL PRINCIPAL
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(2, 31, 21, 0.86),
                rgba(4, 52, 34, 0.72)
            );

        border:
            1px solid rgba(229, 169, 35, 0.46) !important;

        border-radius: 14px !important;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.28);
    }


    /* Títulos de sección */

    .section-title {
        color: #ffffff !important;

        font-size: 0.90rem;
        font-weight: 800;

        letter-spacing: 0.05rem;
        text-transform: uppercase;

        margin-top: 0.50rem;
        margin-bottom: 0.30rem;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.85);
    }


    /* Etiquetas Carta 1, Flop 1, etc. */

    .card-position-label {
        display: block;

        width: 100%;

        color: #ffffff !important;

        font-size: 0.70rem;
        font-weight: 750;
        line-height: 1.15;

        text-align: center;

        margin: 0;
        padding: 0 0 0.28rem 0;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 1);
    }


    /* ======================================================
       CARTAS PRINCIPALES
       ====================================================== */

    div[data-testid="stPopover"] > button {
        position: relative !important;

        width: 100% !important;
        min-height: 5.40rem !important;

        padding: 0.20rem !important;

        background:
            linear-gradient(
                145deg,
                #fffef8 0%,
                #f5f1e5 67%,
                #ddd6c7 100%
            ) !important;

        color: #111111 !important;

        border:
            2px solid rgba(255, 255, 255, 0.94) !important;

        border-radius: 9px !important;

        box-shadow:
            0 5px 10px rgba(0, 0, 0, 0.40),
            inset 0 0 10px rgba(0, 0, 0, 0.08) !important;

        overflow: hidden !important;

        transition:
            transform 0.12s ease,
            border-color 0.12s ease,
            box-shadow 0.12s ease !important;
    }


    /* Marco interior de la carta */

    div[data-testid="stPopover"] > button::after {
        content: "";

        position: absolute;

        top: 5px;
        right: 5px;
        bottom: 5px;
        left: 5px;

        border:
            1px solid rgba(25, 35, 28, 0.17);

        border-radius: 6px;

        pointer-events: none;
    }


    /* Centrar el valor y el palo */

    div[data-testid="stPopover"] > button
    [data-testid="stMarkdownContainer"] {
        position: relative !important;
        z-index: 5 !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        width: 100% !important;
        height: 100% !important;
    }


    div[data-testid="stPopover"] > button
    [data-testid="stMarkdownContainer"] p {
        color: #111111 !important;

        font-size: 1.50rem !important;
        font-weight: 850 !important;
        line-height: 1 !important;

        margin: 0 !important;

        opacity: 1 !important;
    }


    div[data-testid="stPopover"] > button
    [data-testid="stMarkdownContainer"] span {
        font-size: 1.50rem !important;
        font-weight: 850 !important;
        line-height: 1 !important;

        opacity: 1 !important;
    }


    div[data-testid="stPopover"] > button:hover {
        transform: translateY(-2px);

        border-color: #e5a923 !important;

        box-shadow:
            0 8px 15px rgba(0, 0, 0, 0.46) !important;
    }


    /* ======================================================
       SELECTOR DE CARTAS
       ====================================================== */

    .picker-title {
        color: #ffffff !important;

        font-size: 0.90rem;
        font-weight: 800;

        margin-bottom: 0.30rem;
    }


    div[data-testid="stPopoverBody"] button {
        width: 100% !important;
        min-width: 0 !important;
        min-height: 2.25rem !important;

        padding: 0.05rem !important;

        background-color: #f8f6ee !important;

        border:
            1px solid rgba(40, 45, 40, 0.25) !important;

        border-radius: 6px !important;

        color: #111111 !important;
    }


    div[data-testid="stPopoverBody"] button
    [data-testid="stMarkdownContainer"] p {
        color: #111111 !important;

        font-size: 0.76rem !important;
        font-weight: 800 !important;

        margin: 0 !important;
    }


    div[data-testid="stPopoverBody"] button
    [data-testid="stMarkdownContainer"] span {
        font-size: 0.76rem !important;
        font-weight: 800 !important;
    }


    div[data-testid="stPopoverBody"] button:hover {
        background-color: #fff5c9 !important;
        border-color: #e5a923 !important;
    }


    div[data-testid="stPopoverBody"] button:disabled {
        background-color: #aeb4b0 !important;

        opacity: 0.40 !important;
    }


    /* ======================================================
       ETIQUETAS DE CONTROLES
       ====================================================== */

    [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;

        font-size: 0.78rem !important;
        font-weight: 700 !important;

        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.70);
    }


    /* Número de jugadores */

    [data-testid="stNumberInput"] input {
        min-height: 2.40rem;

        background-color: #f7f8f7 !important;
        color: #17231d !important;

        font-size: 1rem;
        font-weight: 800;

        text-align: center;
    }


    [data-testid="stNumberInput"] button {
        min-height: 2.40rem;

        color: #ffffff !important;
        background-color: #073b29 !important;
    }


    [data-testid="stNumberInput"] button:hover {
        background-color: #0e6946 !important;
    }


    /* Selector de simulaciones */

    div[data-baseweb="select"] > div {
        min-height: 2.40rem;

        background-color: #f7f8f7;

        border-radius: 8px;
    }


    div[data-baseweb="select"] span {
        color: #17231d !important;
        font-weight: 650;
    }


    /* Botones */

    div[data-testid="stButton"] button {
        min-height: 2.40rem;

        border-radius: 8px;

        font-weight: 750;
    }


    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #e5a923;

        color: #172016;

        border: 1px solid #ffd46d;
    }


    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #f2bd3e;
    }


    div[data-testid="stButton"] button[kind="secondary"] {
        background-color:
            rgba(3, 42, 27, 0.88);

        color: #ffffff;

        border:
            1px solid rgba(255, 255, 255, 0.45);
    }


    /* ======================================================
       RESULTADOS
       ====================================================== */

    .results-grid {
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 0.35rem;

        margin-top: 0.30rem;
        margin-bottom: 0.40rem;
    }


    .result-card {
        padding: 0.55rem 0.15rem;

        background-color:
            rgba(2, 26, 18, 0.92);

        border-radius: 9px;

        text-align: center;
    }


    .result-win {
        border:
            1px solid rgba(85, 190, 77, 0.60);
    }


    .result-tie {
        border:
            1px solid rgba(229, 169, 35, 0.65);
    }


    .result-loss {
        border:
            1px solid rgba(220, 62, 55, 0.65);
    }


    .result-label {
        color:
            rgba(255, 255, 255, 0.72);

        font-size: 0.58rem;
        font-weight: 750;

        text-transform: uppercase;
    }


    .result-value {
        margin-top: 0.14rem;

        font-size: 1.15rem;
        font-weight: 850;
    }


    .win-value {
        color: #61c854;
    }


    .tie-value {
        color: #e5a923;
    }


    .loss-value {
        color: #ed514a;
    }


    /* Resumen debajo de los resultados */

    .hand-summary {
        margin-top: 0.45rem;
        margin-bottom: 0.15rem;

        padding: 0.50rem 0.65rem;

        background-color:
            rgba(2, 28, 19, 0.86);

        border:
            1px solid rgba(229, 169, 35, 0.45);

        border-radius: 10px;

        color: #ffffff;

        font-size: 0.78rem;
        line-height: 1.50;
    }


    /* Textos inferiores */

    [data-testid="stCaptionContainer"] p {
        color:
            rgba(255, 255, 255, 0.74) !important;
    }


    hr {
        border-color:
            rgba(255, 255, 255, 0.16);
    }


    /* ======================================================
       JOKER INTEGRADO CON EL TAPETE
       ====================================================== */

    .joker-background {
        position: fixed;

        z-index: 0;

        pointer-events: none;

        right: -25px;
        bottom: 0;

        width: 415px;
        height: 96vh;

        background-position: right bottom;
        background-repeat: no-repeat;
        background-size: contain;

        opacity: 0.34;

        -webkit-mask-image:
            linear-gradient(
                to right,
                transparent 0%,
                rgba(0, 0, 0, 0.10) 12%,
                rgba(0, 0, 0, 0.65) 36%,
                black 58%
            );

        mask-image:
            linear-gradient(
                to right,
                transparent 0%,
                rgba(0, 0, 0, 0.10) 12%,
                rgba(0, 0, 0, 0.65) 36%,
                black 58%
            );

        filter:
            saturate(0.88)
            contrast(1.04)
            brightness(0.82);
    }


    /* ======================================================
       VERSIÓN MÓVIL
       ====================================================== */

    @media screen and (max-width: 640px) {

        .block-container {
            width: 100% !important;
            max-width: 100% !important;

            padding-top: 0.28rem !important;
            padding-left: 0.32rem !important;
            padding-right: 0.32rem !important;
            padding-bottom: 0.70rem !important;
        }


        .brand-header {
            margin-bottom: 0.60rem;
        }


        .brand-main {
            font-size: 1.24rem;
        }


        .brand-signature {
            margin-top: 0.34rem;
            margin-left: 1.50rem;

            font-size: 0.46rem;
            line-height: 1.40;
            letter-spacing: 0.085rem;
        }


        .section-title {
            font-size: 0.66rem;

            margin-top: 0.32rem;
            margin-bottom: 0.20rem;
        }


        .card-position-label {
            font-size: 0.49rem;

            padding-bottom: 0.16rem;
        }


        div[data-testid="stPopover"] > button {
            min-height: 3.60rem !important;

            border-radius: 6px !important;
        }


        div[data-testid="stPopover"] > button
        [data-testid="stMarkdownContainer"] p,
        div[data-testid="stPopover"] > button
        [data-testid="stMarkdownContainer"] span {
            font-size: 0.88rem !important;
        }


        div[data-testid="stPopoverBody"] button {
            min-height: 2.10rem !important;
        }


        div[data-testid="stPopoverBody"] button
        [data-testid="stMarkdownContainer"] p,
        div[data-testid="stPopoverBody"] button
        [data-testid="stMarkdownContainer"] span {
            font-size: 0.68rem !important;
        }


        [data-testid="stWidgetLabel"] p {
            font-size: 0.64rem !important;
        }


        [data-testid="stNumberInput"] input,
        [data-testid="stNumberInput"] button,
        div[data-baseweb="select"] > div {
            min-height: 2.25rem !important;
        }


        div[data-testid="stButton"] button {
            min-height: 2.25rem;

            font-size: 0.74rem;
        }


        .results-grid {
            gap: 0.20rem;
        }


        .result-card {
            padding: 0.42rem 0.06rem;
        }


        .result-label {
            font-size: 0.47rem;
        }


        .result-value {
            font-size: 0.90rem;
        }


        .hand-summary {
            padding: 0.40rem 0.48rem;

            font-size: 0.68rem;
        }


        .joker-background {
            width: 145px;
            height: 50vh;

            right: -30px;
            bottom: 0;

            opacity: 0.09;

            -webkit-mask-image:
                linear-gradient(
                    to right,
                    transparent 0%,
                    rgba(0, 0, 0, 0.18) 28%,
                    black 68%
                );

            mask-image:
                linear-gradient(
                    to right,
                    transparent 0%,
                    rgba(0, 0, 0, 0.18) 28%,
                    black 68%
                );

            filter:
                saturate(0.80)
                contrast(1.02)
                brightness(0.82);
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. MOSTRAR EL JOKER SIN CAPA ADICIONAL
# ============================================================

if JOKER_IMAGE:

    st.markdown(
        (
            '<div class="joker-background" '
            'style="background-image:'
            f'url(data:image/png;base64,{JOKER_IMAGE})'
            '">'
            '</div>'
        ),
        unsafe_allow_html=True
    )


# ============================================================
# 5. BARAJA
# ============================================================

DISPLAY_RANKS = "AKQJT98765432"
SUITS = "shdc"

EVALUATOR = Evaluator()


FULL_DECK = [
    rank + suit
    for suit in SUITS
    for rank in DISPLAY_RANKS
]


RANK_NAMES = {
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "T": "10",
    "J": "J",
    "Q": "Q",
    "K": "K",
    "A": "A"
}


SUIT_SYMBOLS = {
    "s": "♠",
    "h": "♥",
    "d": "♦",
    "c": "♣"
}


def card_visual_name(card):
    """
    Convierte una carta al formato visual.
    """

    if card is None:
        return "＋"

    rank = RANK_NAMES[card[0]]
    suit = SUIT_SYMBOLS[card[1]]

    return f"{rank} {suit}"


def card_picker_label(card):
    """
    Genera la etiqueta coloreada de una carta.
    """

    if card is None:
        return ':color[＋]{foreground="#374151"}'

    text = card_visual_name(card)

    if card[1] in ("h", "d"):
        color = "#d62828"
    else:
        color = "#111111"

    return (
        f':color[{text}]'
        f'{{foreground="{color}"}}'
    )


# ============================================================
# 6. ESTADO DE LA APLICACIÓN
# ============================================================

CARD_SLOTS = [
    "hero_card_1",
    "hero_card_2",
    "flop_card_1",
    "flop_card_2",
    "flop_card_3",
    "turn_card",
    "river_card"
]


DEFAULT_STATE = {
    "hero_card_1": "Kh",
    "hero_card_2": "Ks",
    "flop_card_1": None,
    "flop_card_2": None,
    "flop_card_3": None,
    "turn_card": None,
    "river_card": None,
    "active_players": 6,
    "simulations": 25000,
    "calculation_result": None,
    "calculation_summary": None
}


for state_key, default_value in DEFAULT_STATE.items():

    if state_key not in st.session_state:
        st.session_state[state_key] = default_value


def clear_result():
    """
    Borra el resultado anterior.
    """

    st.session_state["calculation_result"] = None
    st.session_state["calculation_summary"] = None


def select_card(slot_key, card):
    """
    Guarda una carta seleccionada.
    """

    st.session_state[slot_key] = card

    clear_result()


def reset_hand():
    """
    Restaura la mano inicial.
    """

    for state_key, default_value in DEFAULT_STATE.items():
        st.session_state[state_key] = default_value


def used_cards_except(current_slot):
    """
    Devuelve las cartas utilizadas en otras posiciones.
    """

    return {
        st.session_state[slot]
        for slot in CARD_SLOTS
        if (
            slot != current_slot
            and st.session_state[slot] is not None
        )
    }


# ============================================================
# 7. SELECTOR VISUAL DE CARTAS
# ============================================================

def render_card_grid(
    slot_key,
    unavailable_cards
):
    """
    Muestra la baraja en filas de seis cartas.
    """

    for start in range(
        0,
        len(FULL_DECK),
        6
    ):

        row_cards = FULL_DECK[
            start:start + 6
        ]

        columns = st.columns(6)

        for column, card in zip(
            columns,
            row_cards
        ):

            with column:

                st.button(
                    card_picker_label(card),
                    key=f"choose_{slot_key}_{card}",
                    disabled=(
                        card in unavailable_cards
                    ),
                    use_container_width=True,
                    on_click=select_card,
                    args=(slot_key, card)
                )


def card_picker(
    slot_key,
    position_label,
    allow

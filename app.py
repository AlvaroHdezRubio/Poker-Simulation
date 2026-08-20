# ============================================================
# POKER LAB BY ALVARO HDEZ
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

def load_image_as_base64(image_path):
    """
    Convierte joker.png en texto Base64 para utilizarlo
    como imagen decorativa dentro del fondo.
    """

    path = Path(image_path)

    # Si la imagen no existe, la aplicación continúa funcionando.
    if not path.exists():
        return None

    with path.open("rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# joker.png debe estar en el mismo nivel que app.py.
JOKER_IMAGE = load_image_as_base64("joker.png")


# ============================================================
# 3. ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>

    /* ------------------------------------------------------
       OCULTAR CABECERA DE STREAMLIT
       ------------------------------------------------------ */

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


    /* ------------------------------------------------------
       FONDO GENERAL
       ------------------------------------------------------ */

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


    /* ------------------------------------------------------
       CONTENEDOR PRINCIPAL
       ------------------------------------------------------ */

    .block-container {
        position: relative;
        z-index: 5;

        width: 100%;
        max-width: 920px;

        padding-top: 0.70rem !important;
        padding-bottom: 1rem !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.34rem;
    }


    /* ------------------------------------------------------
       CABECERA CORPORATIVA
       ------------------------------------------------------ */

    .brand-header {
        position: relative;
        z-index: 20;

        margin: 0 0 0.75rem 0;
        padding: 0;
    }

    .brand-main {
        display: flex;
        align-items: center;

        gap: 0.45rem;

        color: #ffffff;

        font-size: 1.80rem;
        font-weight: 850;
        line-height: 1;

        text-shadow:
            0 2px 4px rgba(0, 0, 0, 0.80),
            0 0 14px rgba(255, 180, 40, 0.28);
    }

    .brand-symbol {
        color: #e8ad25;

        filter:
            drop-shadow(
                0 2px 2px rgba(0, 0, 0, 0.55)
            );
    }

    .brand-signature {
        margin-top: 0.30rem;
        margin-left: 2.05rem;

        color: rgba(255, 255, 255, 0.86);

        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.14rem;
    }


    /* ------------------------------------------------------
       PANEL PRINCIPAL
       ------------------------------------------------------ */

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
            0 10px 28px rgba(0, 0, 0, 0.28),
            inset 0 0 24px rgba(255, 255, 255, 0.025);
    }


    /* ------------------------------------------------------
       TÍTULOS DE SECCIÓN
       ------------------------------------------------------ */

    .section-title {
        position: relative;
        z-index: 15;

        display: block;

        color: #ffffff !important;

        font-size: 0.92rem;
        font-weight: 800;

        letter-spacing: 0.055rem;
        text-transform: uppercase;

        margin-top: 0.60rem;
        margin-bottom: 0.32rem;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.82);
    }


    /* ------------------------------------------------------
       NOMBRES DE LAS POSICIONES
       ------------------------------------------------------ */

    .card-position-label {
        position: relative;
        z-index: 20;

        display: block;

        width: 100%;

        color: #ffffff !important;

        font-size: 0.72rem;
        font-weight: 750;
        line-height: 1.2;

        text-align: center;

        /*
        El padding inferior crea una separación real
        entre el título y el naipe.
        */
        margin: 0;
        padding-top: 0.08rem;
        padding-bottom: 0.52rem;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.95);
    }


    /* El contenedor Markdown de la etiqueta no debe
       tener márgenes negativos */
    div[data-testid="stMarkdownContainer"]:has(
        .card-position-label
    ) {
        margin: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
    }


    /* ------------------------------------------------------
       CARTAS FÍSICAS
       ------------------------------------------------------ */

    div[data-testid="stPopover"] > button {
        position: relative !important;

        width: 100% !important;
        min-height: 6rem !important;

        padding: 0.30rem !important;

        background:
            linear-gradient(
                145deg,
                #fffef8 0%,
                #f5f1e5 67%,
                #ddd6c7 100%
            ) !important;

        color: #151915 !important;

        border:
            2px solid rgba(255, 255, 255, 0.94) !important;

        border-radius: 9px !important;

        box-shadow:
            0 5px 10px rgba(0, 0, 0, 0.40),
            inset 0 0 10px rgba(0, 0, 0, 0.08) !important;

        overflow: hidden !important;

        transition:
            transform 0.12s ease,
            box-shadow 0.12s ease,
            border-color 0.12s ease !important;
    }


    /* Marco interior del naipe */
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


    /* Contenedor del texto de la carta */
    div[data-testid="stPopover"] > button
    [data-testid="stMarkdownContainer"] {
        position: relative !important;
        z-index: 5 !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        width: 100% !important;
        height: 100% !important;

        opacity: 1 !important;
    }


    /*
    Texto normal utilizado por picas y tréboles.
    Se fuerza color oscuro para que no herede el blanco
    general de la página.
    */
    div[data-testid="stPopover"] > button
    [data-testid="stMarkdownContainer"] p {
        position: relative !important;
        z-index: 6 !important;

        color: #151915 !important;

        font-size: 1.68rem !important;
        font-weight: 850 !important;
        line-height: 1 !important;

        margin: 0 !important;

        opacity: 1 !important;
    }


    /*
    Texto coloreado de corazones y diamantes.
    Streamlit introduce el color dentro de un span.
    */
    div[data-testid="stPopover"] > button
    [data-testid="stMarkdownContainer"] span {
        position: relative !important;
        z-index: 6 !important;

        font-size: 1.68rem !important;
        font-weight: 850 !important;
        line-height: 1 !important;

        opacity: 1 !important;
    }


    div[data-testid="stPopover"] > button:hover {
        transform: translateY(-2px);

        border-color: #e5a923 !important;

        box-shadow:
            0 8px 15px rgba(0, 0, 0, 0.47),
            inset 0 0 10px rgba(0, 0, 0, 0.08) !important;
    }


    /* ------------------------------------------------------
       BARAJA DESPLEGADA
       ------------------------------------------------------ */

    .picker-title {
        color: #ffffff !important;

        font-size: 1rem;
        font-weight: 800;

        margin-bottom: 0.45rem;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.85);
    }

    .suit-title {
        color: #ffffff !important;

        font-size: 0.82rem;
        font-weight: 750;

        margin-top: 0.50rem;
        margin-bottom: 0.18rem;

        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.75);
    }


    /* Botones individuales dentro de la baraja */
    div[data-testid="stPopoverBody"] button {
        min-height: 2.30rem !important;

        padding: 0.12rem !important;

        background-color: #f8f6ee !important;

        border:
            1px solid rgba(40, 45, 40, 0.24) !important;

        border-radius: 6px !important;

        color: #121712 !important;

        font-size: 0.88rem !important;
        font-weight: 800 !important;
    }


    /* Picas y tréboles dentro de la baraja */
    div[data-testid="stPopoverBody"] button p {
        color: #121712 !important;

        font-size: 0.88rem !important;
        font-weight: 800 !important;

        opacity: 1 !important;
    }


    /* Corazones y diamantes dentro de la baraja */
    div[data-testid="stPopoverBody"] button span {
        font-size: 0.88rem !important;
        font-weight: 800 !important;

        opacity: 1 !important;
    }


    div[data-testid="stPopoverBody"] button:hover {
        background-color: #fff8da !important;
        border-color: #e5a923 !important;
    }


    div[data-testid="stPopoverBody"] button:disabled {
        background-color: #aeb4b0 !important;
        color: #6a6e6b !important;

        opacity: 0.45 !important;
    }


    /* ------------------------------------------------------
       ETIQUETAS DE CONTROLES
       ------------------------------------------------------ */

    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;

        font-size: 0.82rem !important;
        font-weight: 700 !important;

        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.70);
    }


    /* ------------------------------------------------------
       SELECTOR DE JUGADORES
       ------------------------------------------------------ */

    [data-testid="stNumberInput"] input {
        min-height: 2.55rem;

        background-color: #f7f8f7 !important;
        color: #17231d !important;

        font-size: 1rem;
        font-weight: 800;

        text-align: center;
    }

    [data-testid="stNumberInput"] button {
        min-height: 2.55rem;

        color: #ffffff !important;
        background-color: #073b29 !important;

        border-color:
            rgba(255, 255, 255, 0.35) !important;
    }

    [data-testid="stNumberInput"] button:hover {
        background-color: #0e6946 !important;
    }


    /* ------------------------------------------------------
       SELECTOR DE SIMULACIONES
       ------------------------------------------------------ */

    div[data-baseweb="select"] > div {
        min-height: 2.55rem;

        background-color: #f7f8f7;

        border:
            1px solid rgba(255, 255, 255, 0.35);

        border-radius: 8px;
    }

    div[data-baseweb="select"] span {
        color: #17231d !important;
        font-weight: 650;
    }


    /* ------------------------------------------------------
       BOTONES GENERALES
       ------------------------------------------------------ */

    div[data-testid="stButton"] button {
        min-height: 2.50rem;

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
        color: #101710;
    }

    div[data-testid="stButton"] button[kind="secondary"] {
        background-color:
            rgba(3, 42, 27, 0.88);

        color: #ffffff;

        border:
            1px solid rgba(255, 255, 255, 0.45);
    }


    /* ------------------------------------------------------
       RESUMEN DE LA MANO
       ------------------------------------------------------ */

    .hand-summary {
        margin-top: 0.70rem;

        padding: 0.62rem 0.78rem;

        background-color:
            rgba(2, 28, 19, 0.84);

        border:
            1px solid rgba(229, 169, 35, 0.42);

        border-radius: 10px;

        color: #ffffff;

        font-size: 0.84rem;
        line-height: 1.58;

        box-shadow:
            0 5px 15px rgba(0, 0, 0, 0.24);
    }

    .hand-summary strong {
        color: #ffffff;
    }


    /* ------------------------------------------------------
       TARJETAS DE RESULTADOS
       ------------------------------------------------------ */

    .results-grid {
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 0.55rem;

        margin-top: 0.38rem;
        margin-bottom: 0.35rem;
    }

    .result-card {
        padding: 0.70rem 0.35rem;

        background-color:
            rgba(2, 26, 18, 0.90);

        border-radius: 9px;

        text-align: center;

        box-shadow:
            0 5px 14px rgba(0, 0, 0, 0.27);
    }

    .result-win {
        border:
            1px solid rgba(85, 190, 77, 0.58);
    }

    .result-tie {
        border:
            1px solid rgba(229, 169, 35, 0.62);
    }

    .result-loss {
        border:
            1px solid rgba(220, 62, 55, 0.62);
    }

    .result-label {
        color:
            rgba(255, 255, 255, 0.72);

        font-size: 0.68rem;
        font-weight: 750;

        letter-spacing: 0.04rem;
        text-transform: uppercase;
    }

    .result-value {
        margin-top: 0.20rem;

        font-size: 1.45rem;
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


    /* ------------------------------------------------------
       PIE DE PÁGINA
       ------------------------------------------------------ */

    [data-testid="stCaptionContainer"] p {
        color:
            rgba(255, 255, 255, 0.78) !important;
    }

    hr {
        border-color:
            rgba(255, 255, 255, 0.17);

        margin-top: 0.70rem;
        margin-bottom: 0.35rem;
    }


    /* ------------------------------------------------------
       JOKER DECORATIVO
       ------------------------------------------------------ */

    .joker-background {
        position: fixed;

        z-index: 0;

        pointer-events: none;

        right: 0;
        bottom: 0;

        width: 390px;
        height: 100vh;

        background-position: right center;
        background-repeat: no-repeat;
        background-size: cover;

        opacity: 0.28;

        -webkit-mask-image:
            linear-gradient(
                to right,
                transparent 0%,
                rgba(0, 0, 0, 0.18) 25%,
                black 68%
            );

        mask-image:
            linear-gradient(
                to right,
                transparent 0%,
                rgba(0, 0, 0, 0.18) 25%,
                black 68%
            );
    }


    /* ------------------------------------------------------
       VERSIÓN MÓVIL
       ------------------------------------------------------ */

    @media screen and (max-width: 640px) {

        .block-container {
            width: 100% !important;
            max-width: 100% !important;

            padding-top: 0.50rem !important;
            padding-left: 0.42rem !important;
            padding-right: 0.42rem !important;
            padding-bottom: 0.80rem !important;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.23rem;
        }

        .brand-header {
            margin-bottom: 0.42rem;
        }

        .brand-main {
            font-size: 1.38rem;
        }

        .brand-signature {
            margin-top: 0.18rem;
            margin-left: 1.75rem;

            font-size: 0.56rem;
            letter-spacing: 0.10rem;
        }

        .section-title {
            font-size: 0.74rem;

            margin-top: 0.45rem;
            margin-bottom: 0.20rem;
        }

        .card-position-label {
            position: relative !important;
            z-index: 20 !important;

            display: block !important;

            width: 100% !important;

            color: #ffffff !important;

            font-size: 0.58rem !important;
            font-weight: 750 !important;
            line-height: 1.15 !important;

            text-align: center !important;

            margin: 0 !important;

            padding-top: 0.04rem !important;
            padding-bottom: 0.40rem !important;

            text-shadow:
                0 1px 3px rgba(0, 0, 0, 0.95) !important;
        }

        /* Cartas adaptadas a móvil */
        div[data-testid="stPopover"] > button {
            min-height: 4.60rem !important;

            padding: 0.10rem !important;

            border-radius: 7px !important;
        }

        /* Picas y tréboles */
        div[data-testid="stPopover"] > button
        [data-testid="stMarkdownContainer"] p {
            color: #151915 !important;

            font-size: 1.08rem !important;

            opacity: 1 !important;
        }

        /* Corazones y diamantes */
        div[data-testid="stPopover"] > button
        [data-testid="stMarkdownContainer"] span {
            font-size: 1.08rem !important;

            opacity: 1 !important;
        }

        div[data-testid="stPopoverBody"] button {
            min-height: 2.25rem !important;

            font-size: 0.76rem !important;
        }

        div[data-testid="stPopoverBody"] button p,
        div[data-testid="stPopoverBody"] button span {
            font-size: 0.76rem !important;
        }

        [data-testid="stWidgetLabel"] p {
            font-size: 0.72rem !important;
        }

        [data-testid="stNumberInput"] input,
        [data-testid="stNumberInput"] button,
        div[data-baseweb="select"] > div {
            min-height: 2.42rem !important;
        }

        div[data-testid="stButton"] button {
            min-height: 2.42rem;

            font-size: 0.82rem;
        }

        .hand-summary {
            padding: 0.48rem 0.58rem;

            font-size: 0.76rem;
            line-height: 1.48;
        }

        .results-grid {
            gap: 0.30rem;
        }

        .result-card {
            padding: 0.52rem 0.14rem;
        }

        .result-label {
            font-size: 0.56rem;
        }

        .result-value {
            font-size: 1.05rem;
        }

        .joker-background {
            width: 150px;
            height: 55vh;

            right: -28px;
            bottom: 0;

            opacity: 0.07;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. MOSTRAR EL JOKER
# ============================================================

if JOKER_IMAGE:

    st.markdown(
        f"""
        <div
            class="joker-background"
            style="
                background-image:
                    linear-gradient(
                        to left,
                        rgba(5, 45, 31, 0.04),
                        rgba(5, 45, 31, 0.50)
                    ),
                    url('data:image/png;base64,{JOKER_IMAGE}');
            "
        ></div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 5. BARAJA Y EVALUADOR
# ============================================================

# Orden interno de los valores.
RANKS = "23456789TJQKA"

# Orden visual dentro del selector.
DISPLAY_RANKS = "AKQJT98765432"

# Palos.
SUITS = "shdc"

EVALUATOR = Evaluator()


def create_deck():
    """
    Crea una baraja completa de 52 cartas.
    """

    return [
        rank + suit
        for rank in RANKS
        for suit in SUITS
    ]


FULL_DECK = create_deck()


# ============================================================
# 6. NOMBRES VISUALES
# ============================================================

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


SUIT_NAMES = {
    "s": "Picas ♠",
    "h": "Corazones ♥",
    "d": "Diamantes ♦",
    "c": "Tréboles ♣"
}


def card_visual_name(card):
    """
    Texto normal utilizado en el resumen de la mano.
    """

    if card is None:
        return "＋"

    rank = RANK_NAMES[card[0]]
    suit = SUIT_SYMBOLS[card[1]]

    return f"{rank} {suit}"


def card_picker_label(card):
    """
    Etiqueta utilizada dentro de los naipes.

    Corazones y diamantes aparecen en rojo.
    Picas y tréboles utilizan texto normal oscuro.
    """

    if card is None:
        return "＋"

    rank = RANK_NAMES[card[0]]
    suit = SUIT_SYMBOLS[card[1]]

    # Corazones y diamantes en rojo.
    if card[1] in ("h", "d"):
        return f":red[{rank} {suit}]"

    # Picas y tréboles como texto normal.
    # El CSS fuerza este texto a color oscuro.
    return f"{rank} {suit}"


# ============================================================
# 7. ESTADO DE LA APLICACIÓN
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
    Elimina el resultado anterior cuando cambia la mano.
    """

    st.session_state["calculation_result"] = None
    st.session_state["calculation_summary"] = None


def select_card(slot_key, card):
    """
    Guarda una carta dentro de una posición concreta.
    """

    st.session_state[slot_key] = card

    clear_result()


def reset_hand():
    """
    Restaura todos los valores iniciales.
    """

    for state_key, default_value in DEFAULT_STATE.items():
        st.session_state[state_key] = default_value


def used_cards_except(current_slot):
    """
    Obtiene las cartas utilizadas en el resto de posiciones.
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
# 8. SELECTOR VISUAL DE CARTAS
# ============================================================

def card_picker(
    slot_key,
    position_label,
    allow_empty=False
):
    """
    Muestra un naipe interactivo.

    Al pulsar el naipe se abre la baraja completa.
    """

    selected_card = st.session_state[slot_key]

    trigger_label = card_picker_label(
        selected_card
    )

    # Nombre de la posición.
    st.markdown(
        (
            '<div class="card-position-label">'
            f'{position_label}'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    # Carta física que abre la baraja.
    with st.popover(
        trigger_label,
        use_container_width=True,
        key=f"picker_{slot_key}"
    ):

        st.markdown(
            (
                '<div class="picker-title">'
                f'Seleccionar {position_label}'
                '</div>'
            ),
            unsafe_allow_html=True
        )

        # Flop, turn y river pueden quedar vacíos.
        if allow_empty:

            st.button(
                "＋ Sin carta",
                key=f"clear_{slot_key}",
                use_container_width=True,
                on_click=select_card,
                args=(slot_key, None)
            )

        unavailable_cards = used_cards_except(
            slot_key
        )

        # Mostramos la baraja organizada por palos.
        for suit in SUITS:

            st.markdown(
                (
                    '<div class="suit-title">'
                    f'{SUIT_NAMES[suit]}'
                    '</div>'
                ),
                unsafe_allow_html=True
            )

            suit_cards = [
                rank + suit
                for rank in DISPLAY_RANKS
            ]

            # Primera fila del palo.
            first_row = suit_cards[:7]
            first_columns = st.columns(7)

            for column, card in zip(
                first_columns,
                first_row
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

            # Segunda fila del palo.
            second_row = suit_cards[7:]
            second_columns = st.columns(6)

            for column, card in zip(
                second_columns,
                second_row
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

        st.caption(
            "Las cartas utilizadas en otras posiciones "
            "aparecen desactivadas."
        )

    return selected_card


# ============================================================
# 9. VALIDACIÓN
# ============================================================

def validate_inputs(
    hero_cards,
    board_cards,
    num_players
):
    """
    Comprueba cartas, mesa y número de jugadores.
    """

    if len(hero_cards) != 2:
        raise ValueError(
            "Debes seleccionar dos cartas propias."
        )

    if None in hero_cards:
        raise ValueError(
            "Tus dos cartas deben estar seleccionadas."
        )

    if len(board_cards) not in (0, 3, 4, 5):
        raise ValueError(
            "Debes introducir las tres cartas "
            "del flop juntas."
        )

    if num_players < 2 or num_players > 10:
        raise ValueError(
            "Debe haber entre 2 y 10 jugadores activos."
        )

    all_known_cards = hero_cards + board_cards

    if len(all_known_cards) != len(
        set(all_known_cards)
    ):
        raise ValueError(
            "Hay cartas repetidas."
        )

    return hero_cards, board_cards


# ============================================================
# 10. EVALUACIÓN DE MANOS
# ============================================================

def hand_score(
    player_cards,
    board_cards
):
    """
    Evalúa una mano utilizando Treys.
    """

    player_treys = [
        Card.new(card)
        for card in player_cards
    ]

    board_treys = [
        Card.new(card)
        for card in board_cards
    ]

    return EVALUATOR.evaluate(
        board_treys,
        player_treys
    )


# ============================================================
# 11. SIMULACIÓN MONTE CARLO
# ============================================================

def monte_carlo(
    hero_cards,
    board_cards,
    num_players,
    simulations=10000
):
    """
    Completa la mesa, reparte manos rivales
    y calcula victoria, empate y derrota.
    """

    hero_cards, board_cards = validate_inputs(
        hero_cards,
        board_cards,
        num_players
    )

    known_cards = set(
        hero_cards + board_cards
    )

    available_cards = [
        card
        for card in FULL_DECK
        if card not in known_cards
    ]

    wins = 0
    ties = 0
    losses = 0

    missing_board_cards = 5 - len(board_cards)
    number_of_villains = num_players - 1

    cards_needed = (
        missing_board_cards
        + number_of_villains * 2
    )

    for _ in range(simulations):

        simulated_cards = random.sample(
            available_cards,
            cards_needed
        )

        position = 0
        completed_board = board_cards.copy()

        # Completamos las cartas comunitarias pendientes.
        for _ in range(missing_board_cards):

            completed_board.append(
                simulated_cards[position]
            )

            position += 1

        villains = []

        # Repartimos dos cartas a cada rival.
        for _ in range(number_of_villains):

            villain_hand = [
                simulated_cards[position],
                simulated_cards[position + 1]
            ]

            villains.append(villain_hand)

            position += 2

        hero_score = hand_score(
            hero_cards,
            completed_board
        )

        all_scores = [hero_score]

        for villain_hand in villains:

            villain_score = hand_score(
                villain_hand,
                completed_board
            )

            all_scores.append(villain_score)

        best_score = min(all_scores)

        if hero_score != best_score:

            losses += 1

        else:

            number_of_winners = all_scores.count(
                best_score
            )

            if number_of_winners == 1:
                wins += 1

            else:
                ties += 1

    return {
        "victoria": round(
            wins / simulations * 100,
            2
        ),
        "empate": round(
            ties / simulations * 100,
            2
        ),
        "derrota": round(
            losses / simulations * 100,
            2
        ),
        "simulaciones": simulations
    }


# ============================================================
# 12. CABECERA
# ============================================================

st.markdown(
    (
        '<div class="brand-header">'
        '<div class="brand-main">'
        '<span class="brand-symbol">♠</span>'
        '<span>POKER LAB</span>'
        '</div>'
        '<div class="brand-signature">'
        'BY ÁLVARO HDEZ'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True
)


# ============================================================
# 13. PANEL PRINCIPAL
# ============================================================

with st.container(border=True):

    # ========================================================
    # TUS CARTAS
    # ========================================================

    st.markdown(
        (
            '<div class="section-title">'
            'Tus cartas'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    hero_column_1, hero_column_2 = st.columns(2)

    with hero_column_1:

        hero_card_1 = card_picker(
            slot_key="hero_card_1",
            position_label="Carta 1",
            allow_empty=False
        )

    with hero_column_2:

        hero_card_2 = card_picker(
            slot_key="hero_card_2",
            position_label="Carta 2",
            allow_empty=False
        )


    # ========================================================
    # CARTAS COMUNITARIAS
    # ========================================================

    st.markdown(
        (
            '<div class="section-title">'
            'Cartas comunitarias'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    board_columns = st.columns(5)

    board_configuration = [
        ("flop_card_1", "Flop 1"),
        ("flop_card_2", "Flop 2"),
        ("flop_card_3", "Flop 3"),
        ("turn_card", "Turn"),
        ("river_card", "River")
    ]

    for column, configuration in zip(
        board_columns,
        board_configuration
    ):

        slot_key, position_label = configuration

        with column:

            card_picker(
                slot_key=slot_key,
                position_label=position_label,
                allow_empty=True
            )


    # ========================================================
    # JUGADORES Y SIMULACIONES
    # ========================================================

    configuration_column_1, configuration_column_2 = (
        st.columns(2)
    )

    with configuration_column_1:

        active_players = st.number_input(
            label="Jugadores activos, incluyéndote a ti",
            min_value=2,
            max_value=10,
            step=1,
            key="active_players",
            on_change=clear_result
        )

    with configuration_column_2:

        simulations = st.selectbox(
            label="Simulaciones",
            options=[
                10000,
                25000,
                50000,
                100000
            ],
            format_func=lambda value: (
                f"{value:,}".replace(",", ".")
            ),
            key="simulations",
            on_change=clear_result
        )


    # ========================================================
    # BOTONES
    # ========================================================

    calculate_column, reset_column = st.columns(2)

    with calculate_column:

        calculate_button = st.button(
            "Calcular probabilidades",
            type="primary",
            use_container_width=True
        )

    with reset_column:

        st.button(
            "Nueva mano",
            use_container_width=True,
            on_click=reset_hand
        )


# ============================================================
# 14. EJECUTAR EL CÁLCULO
# ============================================================

if calculate_button:

    try:

        hero_cards = [
            st.session_state["hero_card_1"],
            st.session_state["hero_card_2"]
        ]

        board_positions = [
            st.session_state["flop_card_1"],
            st.session_state["flop_card_2"],
            st.session_state["flop_card_3"],
            st.session_state["turn_card"],
            st.session_state["river_card"]
        ]

        # Validamos el orden:
        # flop, turn y river.
        empty_position_found = False

        for card in board_positions:

            if card is None:

                empty_position_found = True

            elif empty_position_found:

                raise ValueError(
                    "Añade las cartas comunitarias en orden: "
                    "primero el flop, después el turn "
                    "y finalmente el river."
                )

        board_cards = [
            card
            for card in board_positions
            if card is not None
        ]

        with st.spinner(
            "Simulando posibles partidas..."
        ):

            result = monte_carlo(
                hero_cards=hero_cards,
                board_cards=board_cards,
                num_players=active_players,
                simulations=simulations
            )

        st.session_state[
            "calculation_result"
        ] = result

        st.session_state[
            "calculation_summary"
        ] = {
            "hero_cards": hero_cards,
            "board_cards": board_cards,
            "active_players": active_players
        }

    except ValueError as error:

        st.error(str(error))

    except Exception as error:

        st.error(
            f"Se ha producido un error inesperado: {error}"
        )


# ============================================================
# 15. MOSTRAR RESULTADOS
# ============================================================

result = st.session_state.get(
    "calculation_result"
)

summary = st.session_state.get(
    "calculation_summary"
)


if result and summary:

    hero_text = " ".join(
        card_visual_name(card)
        for card in summary["hero_cards"]
    )

    if summary["board_cards"]:

        board_text = " ".join(
            card_visual_name(card)
            for card in summary["board_cards"]
        )

    else:

        board_text = "Antes del flop"

    summary_html = (
        '<div class="hand-summary">'

        '<div>'
        '<strong>Tus cartas:</strong> '
        f'{hero_text}'
        '</div>'

        '<div>'
        '<strong>Mesa:</strong> '
        f'{board_text}'
        '</div>'

        '<div>'
        '<strong>Jugadores activos:</strong> '
        f'{summary["active_players"]}'
        '</div>'

        '</div>'
    )

    st.markdown(
        summary_html,
        unsafe_allow_html=True
    )

    st.markdown(
        (
            '<div class="section-title">'
            'Probabilidades'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    # Una única cadena HTML evita que Streamlit
    # muestre el código en pantalla.
    results_html = (
        '<div class="results-grid">'

        '<div class="result-card result-win">'
        '<div class="result-label">'
        'Victoria'
        '</div>'
        '<div class="result-value win-value">'
        f'{result["victoria"]} %'
        '</div>'
        '</div>'

        '<div class="result-card result-tie">'
        '<div class="result-label">'
        'Empate'
        '</div>'
        '<div class="result-value tie-value">'
        f'{result["empate"]} %'
        '</div>'
        '</div>'

        '<div class="result-card result-loss">'
        '<div class="result-label">'
        'Derrota'
        '</div>'
        '<div class="result-value loss-value">'
        f'{result["derrota"]} %'
        '</div>'
        '</div>'

        '</div>'
    )

    st.markdown(
        results_html,
        unsafe_allow_html=True
    )

    simulation_text = (
        f'{result["simulaciones"]:,}'
        .replace(",", ".")
    )

    st.caption(
        f"Resultado basado en "
        f"{simulation_text} simulaciones."
    )


# ============================================================
# 16. PIE DE PÁGINA
# ============================================================

st.divider()

st.caption(
    "Los rivales se simulan con manos aleatorias "
    "entre todas las combinaciones legales disponibles."
)

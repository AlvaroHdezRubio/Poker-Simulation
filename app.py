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
    Convierte joker.png en texto Base64.

    Esto permite utilizar la imagen como elemento decorativo
    dentro del fondo de la aplicación.
    """

    path = Path(image_path)

    # Si la imagen no existe, la aplicación seguirá funcionando.
    if not path.exists():
        return None

    with path.open("rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return encoded_image


# joker.png debe estar en el mismo directorio que app.py.
JOKER_IMAGE = load_image_as_base64("joker.png")


# ============================================================
# 3. ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>

    /* ------------------------------------------------------
       OCULTAR LA CABECERA DE STREAMLIT
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
       FONDO GENERAL TIPO TAPETE
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
        gap: 0.32rem;
    }


    /* ------------------------------------------------------
       CABECERA CORPORATIVA
       ------------------------------------------------------ */

    .brand-header {
        position: relative;
        z-index: 20;

        display: block;

        margin: 0 0 0.70rem 0;
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
       PANEL PRINCIPAL DE LA MESA
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

        margin-top: 0.55rem;
        margin-bottom: 0.28rem;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.82);
    }


    /* ------------------------------------------------------
       NOMBRE DE CADA POSICIÓN
       ------------------------------------------------------ */

    .card-position-label {
        position: relative;
        z-index: 20;

        display: block;

        color: #ffffff !important;

        font-size: 0.72rem;
        font-weight: 750;

        text-align: center;

        margin-top: 0.12rem;
        margin-bottom: 0.30rem;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.90);
    }


    /* ------------------------------------------------------
       CARTA FÍSICA QUE ABRE LA BARAJA
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


    /* Línea interior de la carta */
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


    /* Texto negro de picas y tréboles */
    div[data-testid="stPopover"] > button p {
        position: relative;
        z-index: 2;

        color: #151915 !important;

        font-size: 1.68rem !important;
        font-weight: 850 !important;
        line-height: 1 !important;

        margin: 0 !important;
    }


    /* Texto coloreado de corazones y diamantes */
    div[data-testid="stPopover"] > button span {
        position: relative;
        z-index: 2;

        font-size: 1.68rem !important;
        font-weight: 850 !important;
        line-height: 1 !important;
    }


    div[data-testid="stPopover"] > button:hover {
        transform: translateY(-2px);

        border-color: #e5a923 !important;

        box-shadow:
            0 8px 15px rgba(0, 0, 0, 0.47),
            inset 0 0 10px rgba(0, 0, 0, 0.08) !important;
    }


    /* ------------------------------------------------------
       CONTENIDO DE LA BARAJA DESPLEGADA
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


    /* Botones individuales de la baraja */
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

    div[data-testid="stPopoverBody"] button p {
        color: #121712 !important;

        font-size: 0.88rem !important;
        font-weight: 800 !important;
    }

    div[data-testid="stPopoverBody"] button span {
        font-size: 0.88rem !important;
        font-weight: 800 !important;
    }

    div[data-testid="stPopoverBody"] button:hover {
        background-color: #fff8da !important;
        border-color: #e5a923 !important;
    }


    /* Botones desactivados */
    div[data-testid="stPopoverBody"] button:disabled {
        background-color: #aeb4b0 !important;
        color: #6a6e6b !important;

        opacity: 0.45 !important;
    }


    /* ------------------------------------------------------
       ETIQUETAS DE JUGADORES Y SIMULACIONES
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
       SELECTOR NUMÉRICO DE JUGADORES
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
       TARJETAS DE PROBABILIDADES
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
       TEXTOS INFERIORES
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
       VERSIÓN PARA MÓVIL
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
            gap: 0.22rem;
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
            margin-bottom: 0.18rem;
        }

        .card-position-label {
            color: #ffffff !important;

            font-size: 0.58rem !important;
            font-weight: 750 !important;

            margin-bottom: 0.24rem !important;
        }

        /* Cartas adaptadas a pantalla pequeña */
        div[data-testid="stPopover"] > button {
            min-height: 4.60rem !important;

            padding: 0.10rem !important;

            border-radius: 7px !important;
        }

        div[data-testid="stPopover"] > button p,
        div[data-testid="stPopover"] > button span {
            font-size: 1.08rem !important;
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

# Orden interno utilizado por Treys.
RANKS = "23456789TJQKA"

# Orden de presentación dentro de la baraja visual.
DISPLAY_RANKS = "AKQJT98765432"

# Palos:
# s = picas
# h = corazones
# d = diamantes
# c = tréboles
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
# 6. NOMBRES VISUALES DE LAS CARTAS
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
    Devuelve el texto normal de una carta.

    Se utiliza principalmente en los resúmenes.
    """

    if card is None:
        return "＋"

    rank = RANK_NAMES[card[0]]
    suit = SUIT_SYMBOLS[card[1]]

    return f"{rank} {suit}"


def card_picker_label(card):
    """
    Genera la etiqueta visual de una carta.

    Corazones y diamantes se muestran en rojo.
    Picas y tréboles se muestran en negro.
    """

    if card is None:
        return "＋"

    rank = RANK_NAMES[card[0]]
    suit = SUIT_SYMBOLS[card[1]]

    # Corazones y diamantes.
    if card[1] in ("h", "d"):
        return f":red[{rank} {suit}]"

    # Picas y tréboles.
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


# Inicializamos las variables si todavía no existen.
for state_key, default_value in DEFAULT_STATE.items():

    if state_key not in st.session_state:
        st.session_state[state_key] = default_value


def clear_result():
    """
    Elimina el resultado anterior cuando cambia la situación.
    """

    st.session_state["calculation_result"] = None
    st.session_state["calculation_summary"] = None


def select_card(slot_key, card):
    """
    Guarda una carta en una posición concreta.
    """

    st.session_state[slot_key] = card

    clear_result()


def reset_hand():
    """
    Restaura todos los controles a sus valores iniciales.
    """

    for state_key, default_value in DEFAULT_STATE.items():
        st.session_state[state_key] = default_value


def used_cards_except(current_slot):
    """
    Devuelve las cartas utilizadas en el resto de posiciones.
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
# 8. SELECTOR VISUAL DIRECTO DE CARTAS
# ============================================================

def card_picker(
    slot_key,
    position_label,
    allow_empty=False
):
    """
    Muestra una carta como botón físico.

    Al pulsar la carta se abre la baraja completa,
    organizada por palos.
    """

    selected_card = st.session_state[slot_key]

    # Etiqueta que se mostrará en la carta física.
    trigger_label = card_picker_label(
        selected_card
    )

    # Nombre de la posición:
    # Carta 1, Flop 1, Turn, etc.
    st.markdown(
        (
            '<div class="card-position-label">'
            f'{position_label}'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    # El popover se abre al tocar la carta.
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

        # Las cartas comunitarias pueden vaciarse.
        if allow_empty:

            st.button(
                "＋ Sin carta",
                key=f"clear_{slot_key}",
                use_container_width=True,
                on_click=select_card,
                args=(slot_key, None)
            )

        # Cartas que ya están siendo utilizadas.
        unavailable_cards = used_cards_except(
            slot_key
        )

        # Mostramos los cuatro palos.
        for suit in SUITS:

            st.markdown(
                (
                    '<div class="suit-title">'
                    f'{SUIT_NAMES[suit]}'
                    '</div>'
                ),
                unsafe_allow_html=True
            )

            # Cartas de este palo.
            suit_cards = [
                rank + suit
                for rank in DISPLAY_RANKS
            ]

            # Primera fila: 7 cartas.
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

            # Segunda fila: 6 cartas.
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
# 9. VALIDACIÓN DE LA MANO
# ============================================================

def validate_inputs(
    hero_cards,
    board_cards,
    num_players
):
    """
    Comprueba cartas, mesa y jugadores.
    """

    if len(hero_cards) != 2:
        raise ValueError(
            "Debes seleccionar dos cartas propias."
        )

    if None in hero_cards:
        raise ValueError(
            "Tus dos cartas deben estar seleccionadas."
        )

    # La mesa puede tener:
    # 0 cartas, 3 cartas, 4 cartas o 5 cartas.
    if len(board_cards) not in (0, 3, 4, 5):
        raise ValueError(
            "Debes introducir las tres cartas "
            "del flop juntas."
        )

    if num_players < 2 or num_players > 10:
        raise ValueError(
            "Debe haber entre 2 y 10 jugadores activos."
        )

    all_known_cards = (
        hero_cards + board_cards
    )

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
    Evalúa una mano mediante Treys.

    En Treys, una puntuación menor representa
    una mano mejor.
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
    Completa la mesa y reparte manos aleatorias
    a todos los rivales activos.
    """

    hero_cards, board_cards = validate_inputs(
        hero_cards,
        board_cards,
        num_players
    )

    # Cartas conocidas.
    known_cards = set(
        hero_cards + board_cards
    )

    # Cartas disponibles.
    available_cards = [
        card
        for card in FULL_DECK
        if card not in known_cards
    ]

    wins = 0
    ties = 0
    losses = 0

    # Cartas comunitarias que faltan.
    missing_board_cards = (
        5 - len(board_cards)
    )

    # Número de rivales.
    number_of_villains = (
        num_players - 1
    )

    # Cartas necesarias en cada simulación.
    cards_needed = (
        missing_board_cards
        + number_of_villains * 2
    )

    # Ejecutamos todas las simulaciones.
    for _ in range(simulations):

        # Elegimos todas las cartas necesarias
        # sin repetir.
        simulated_cards = random.sample(
            available_cards,
            cards_needed
        )

        position = 0

        completed_board = (
            board_cards.copy()
        )

        # Completamos la mesa.
        for _ in range(
            missing_board_cards
        ):

            completed_board.append(
                simulated_cards[position]
            )

            position += 1

        # Repartimos cartas a los rivales.
        villains = []

        for _ in range(
            number_of_villains
        ):

            villain_hand = [
                simulated_cards[position],
                simulated_cards[position + 1]
            ]

            villains.append(
                villain_hand
            )

            position += 2

        # Evaluamos nuestra mano.
        hero_score = hand_score(
            hero_cards,
            completed_board
        )

        all_scores = [
            hero_score
        ]

        # Evaluamos las manos rivales.
        for villain_hand in villains:

            villain_score = hand_score(
                villain_hand,
                completed_board
            )

            all_scores.append(
                villain_score
            )

        # La puntuación menor es la mejor.
        best_score = min(
            all_scores
        )

        # Alguien tiene una mano mejor.
        if hero_score != best_score:

            losses += 1

        else:

            # Contamos cuántos jugadores
            # comparten la mejor mano.
            number_of_winners = (
                all_scores.count(
                    best_score
                )
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

# Utilizamos un contenedor nativo de Streamlit.
# Esto permite envolver correctamente todos los controles.
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

    hero_column_1, hero_column_2 = (
        st.columns(2)
    )

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
            label=(
                "Jugadores activos, incluyéndote a ti"
            ),
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

    calculate_column, reset_column = (
        st.columns(2)
    )

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

        # Comprobamos que las cartas se han añadido
        # en el orden correcto.
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

        # Quitamos las posiciones vacías.
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

        # Guardamos el resultado.
        st.session_state[
            "calculation_result"
        ] = result

        # Guardamos la situación analizada.
        st.session_state[
            "calculation_summary"
        ] = {
            "hero_cards": hero_cards,
            "board_cards": board_cards,
            "active_players": active_players
        }

    except ValueError as error:

        st.error(
            str(error)
        )

    except Exception as error:

        st.error(
            f"Se ha producido un error inesperado: {error}"
        )


# ============================================================
# 15. MOSTRAR LOS RESULTADOS
# ============================================================

result = st.session_state.get(
    "calculation_result"
)

summary = st.session_state.get(
    "calculation_summary"
)


if result and summary:

    # Cartas propias en formato visual.
    hero_text = " ".join(
        card_visual_name(card)
        for card in summary["hero_cards"]
    )

    # Mesa en formato visual.
    if summary["board_cards"]:

        board_text = " ".join(
            card_visual_name(card)
            for card in summary["board_cards"]
        )

    else:

        board_text = "Antes del flop"

    # Resumen de la situación.
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

    # Construimos las tarjetas en una única cadena.
    # Esto evita que Streamlit muestre el HTML como texto.
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

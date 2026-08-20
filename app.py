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
# 1. CONFIGURACION GENERAL
# ============================================================

st.set_page_config(
    page_title="Poker Lab by Álvaro Hdez",
    page_icon="♠️",
    layout="centered"
)


# ============================================================
# 2. CARGAR IMAGEN DECORATIVA
# ============================================================

def image_b64(image_path):
    """
    Convierte una imagen local en texto Base64.

    Esto permite utilizar joker.png como fondo decorativo.
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
       FONDO VERDE TIPO TAPETE
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

        padding-top: 0.60rem !important;
        padding-bottom: 1rem !important;
    }


    /* ------------------------------------------------------
       CABECERA DE MARCA
       ------------------------------------------------------ */

    .brand-header {
        p*sition: relative;
        z-index:*20;

        margin: 0 0 0.85rem 0*
        padding: 0;
    }

    .b*and-main {
        display: flex;
*       align-items: center;

     *  gap: 0.42rem;

        color: #f*ffff;

        font-size: 1.75rem;*        font-weight: 850;
        *ine-height: 1.05;

        text-sh*dow:
            0 2px 4px rgba(0,*0, 0, 0.8),
            0 0 14px r*ba(255, 180, 40, 0.28);
    }

   *.brand-symbol {
        color: #e8*d25;
    }

    .brand-signature {*        display: block;

        m*rgin-top: 0.42rem;
        margin-*eft: 2rem;

        color: rgba(25*, 255, 255, 0.88);

        font-s*ze: 0.66rem;
        font-weight: 700;
        line-height: 1.3;
        letter-spacing: 0.13rem;
    }


    /* ------------------------------------------------------
       PANEL PRINCIPAL
       ------------------------------------------------------ */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        ba*kground:
            linear-gradie*t(
                145deg,
       *        rgba(2, 31, 21, 0.86),
   *            rgba(4, 52, 34, 0.72)
*           );

        border:
   *        1px solid rgba(229, 169, 3*, 0.46) !important;

        border-radius: 14px !important;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.28);
    }


    /* ------------------------------------------------------
       TITULOS DE SECCION
       ------------------------------------------------------ */

    .section-title {
      * color: #ffffff !important;

     *  font-size: 0.90rem;
        font*weight: 800;

        letter-spaci*g: 0.05rem;
        text-transform* uppercase;

        margin-top: 0*50rem;
        margin-bottom: 0.30*em;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.85);
    }


    /* ------------------------------------------------------
       ETIQUETAS DE LAS CARTAS
       ------------------------------------------------------ */

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


    /* ------------------------------------------------------
       CARTAS VISUALES
       ------------------------------------------------------ */

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


    /* Contenedor del valor y palo */

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


    /* ------------------------------------------------------
       SELECTOR DE CARTAS
       ------------------------------------------------------ */

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


    /* ------------------------------------------------------
       ETIQUETAS DE CONTROLES
       ------------------------------------------------------ */

    [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;

        font-size: 0.78rem !important;
        font-weight: 700 !important;

        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.70);
    }


    /* ------------------------------------------------------
       JUGADORES ACTIVOS
       ------------------------------------------------------ */

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


    /* ------------------------------------------------------
       SIMULACIONES
       ------------------------------------------------------ */

    div[data-baseweb="select"] > div {
        min-height: 2.40rem;

        background-color: #f7f8f7;

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


    /* ------------------------------------------------------
       RESUMEN DE LA MANO
       ------------------------------------------------------ */

    .hand-summary {
        margin-top: 0.60rem;

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


    /* ------------------------------------------------------
       RESULTADOS
       ------------------------------------------------------ */

    .results-grid {
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 0.35rem;

        margin-top: 0.30rem;
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


    /* ------------------------------------------------------
       PIE DE PAGINA
       ------------------------------------------------------ */

    [data-testid="stCaptionContainer"] p {
        color:
            rgba(255, 255, 255, 0.74) !important;
    }


    hr {
        border-color:
            rgba(255, 255, 255, 0.16);
    }


    /* ------------------------------------------------------
       JOKER LATERAL
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

        opacity: 0.25;
    }


    /* ======================================================
       VERSION MOVIL
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
            margin-bottom: 0.56rem;
        }


        .brand-main {
            font-size: 1.22rem;
        }


        .brand-signature {
            margin-top: 0.32rem;
            margin-left: 1.50rem;

            font-size: 0.46rem;
            line-height: 1.35;
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


        .hand-summary {
            padding: 0.40rem 0.48rem;

            font-size: 0.68rem;
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


        .joker-background {
            width: 130px;
            height: 50vh;

            right: -25px;

            opacity: 0.05;
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
        (
            '<div class="joker-background" '
            'style="background-image:'
            'linear-gradient('
            'to left,'
            'rgba(5,45,31,0.04),'
            'rgba(5,45,31,0.50)'
            '),'
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
    Devuelve una carta en formato visual.
    """

    if card is None:
        return "＋"

    rank = RANK_NAMES[card[0]]
    suit = SUIT_SYMBOLS[card[1]]

    return f"{rank} {suit}"


def card_picker_label(card):
    """
    Genera el texto coloreado de una carta.

    Corazones y diamantes aparecen en rojo.
    Picas y tréboles aparecen en negro.
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
# 6. ESTADO DE LA APLICACION
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
    Borra el cálculo anterior.
    """

    st.session_state["calculation_result"] = None
    st.session_state["calculation_summary"] = None


def select_card(slot_key, card):
    """
    Guarda una carta en la posición seleccionada.
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

    Solo se ejecuta cuando el selector está abierto.
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
    allow_empty=False
):
    """
    Muestra una carta y abre la baraja al pulsarla.
    """

    st.markdown(
        (
            '<div class="card-position-label">'
            f'{position_label}'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    popover = st.popover(
        card_picker_label(
            st.session_state[slot_key]
        ),
        use_container_width=True,
        key=f"picker_{slot_key}",
        on_change="rerun"
    )

    # Las cartas solo se crean cuando abrimos el selector.
    # Esto reduce mucho el tiempo de carga de la página.
    if popover.open:

        with popover:

            st.markdown(
                (
                    '<div class="picker-title">'
                    f'Seleccionar {position_label}'
                    '</div>'
                ),
                unsafe_allow_html=True
            )

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

            render_card_grid(
                slot_key,
                unavailable_cards
            )

            st.caption(
                "Las cartas utilizadas aparecen desactivadas."
            )


# ============================================================
# 8. VALIDACION
# ============================================================

def validate_inputs(
    hero_cards,
    board_cards,
    players
):
    """
    Valida cartas, mesa y jugadores.
    """

    if None in hero_cards:
        raise ValueError(
            "Selecciona tus dos cartas."
        )

    if len(board_cards) not in (
        0,
        3,
        4,
        5
    ):
        raise ValueError(
            "Introduce las tres cartas "
            "del flop juntas."
        )

    if not 2 <= players <= 10:
        raise ValueError(
            "Debe haber entre 2 y 10 jugadores."
        )

    all_cards = (
        hero_cards + board_cards
    )

    if len(all_cards) != len(
        set(all_cards)
    ):
        raise ValueError(
            "Hay cartas repetidas."
        )


# ============================================================
# 9. EVALUACION DE MANOS
# ============================================================

def hand_score(
    player_cards,
    board_cards
):
    """
    Evalúa una mano utilizando Treys.
    """

    player = [
        Card.new(card)
        for card in player_cards
    ]

    board = [
        Card.new(card)
        for card in board_cards
    ]

    return EVALUATOR.evaluate(
        board,
        player
    )


# ============================================================
# 10. SIMULACION MONTE CARLO
# ============================================================

def monte_carlo(
    hero_cards,
    board_cards,
    players,
    simulations
):
    """
    Simula posibles manos y mesas.
    """

    validate_inputs(
        hero_cards,
        board_cards,
        players
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

    missing_board_cards = (
        5 - len(board_cards)
    )

    number_of_villains = (
        players - 1
    )

    cards_needed = (
        missing_board_cards
        + number_of_villains * 2
    )

    for _ in range(simulations):

        sampled_cards = random.sample(
            available_cards,
            cards_needed
        )

        completed_board = (
            board_cards
            + sampled_cards[
                :missing_board_cards
            ]
        )

        position = missing_board_cards

        all_scores = [
            hand_score(
                hero_cards,
                completed_board
            )
        ]

        for _ in range(
            number_of_villains
        ):

            villain_hand = sampled_cards[
                position:position + 2
            ]

            all_scores.append(
                hand_score(
                    villain_hand,
                    completed_board
                )
            )

            position += 2

        best_score = min(
            all_scores
        )

        if all_scores[0] != best_score:

            losses += 1

        elif all_scores.count(
            best_score
        ) == 1:

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
# 11. CABECERA
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
# 12. INTERFAZ PRINCIPAL
# ============================================================

with st.container(border=True):

    # --------------------------------------------------------
    # TUS CARTAS
    # --------------------------------------------------------

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

        card_picker(
            "hero_card_1",
            "Carta 1"
        )

    with hero_column_2:

        card_picker(
            "hero_card_2",
            "Carta 2"
        )


    # --------------------------------------------------------
    # FLOP
    # --------------------------------------------------------

    st.markdown(
        (
            '<div class="section-title">'
            'Cartas comunitarias'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    flop_column_1, flop_column_2, flop_column_3 = (
        st.columns(3)
    )

    with flop_column_1:

        card_picker(
            "flop_card_1",
            "Flop 1",
            True
        )

    with flop_column_2:

        card_picker(
            "flop_card_2",
            "Flop 2",
            True
        )

    with flop_column_3:

        card_picker(
            "flop_card_3",
            "Flop 3",
            True
        )


    # --------------------------------------------------------
    # TURN Y RIVER
    # --------------------------------------------------------

    turn_column, river_column = (
        st.columns(2)
    )

    with turn_column:

        card_picker(
            "turn_card",
            "Turn",
            True
        )

    with river_column:

        card_picker(
            "river_card",
            "River",
            True
        )


    # --------------------------------------------------------
    # CONFIGURACION
    # --------------------------------------------------------

    players_column, simulations_column = (
        st.columns(2)
    )

    with players_column:

        active_players = st.number_input(
            "Jugadores activos",
            min_value=2,
            max_value=10,
            step=1,
            key="active_players",
            on_change=clear_result
        )

    with simulations_column:

        simulations = st.selectbox(
            "Simulaciones",
            [
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


    # --------------------------------------------------------
    # BOTONES
    # --------------------------------------------------------

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
# 13. EJECUTAR EL CALCULO
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

        empty_position_found = False

        for card in board_positions:

            if card is None:

                empty_position_found = True

            elif empty_position_found:

                raise ValueError(
                    "Añade las cartas en orden: "
                    "flop, turn y river."
                )

        board_cards = [
            card
            for card in board_positions
            if card is not None
        ]

        with st.spinner(
            "Simulando partidas..."
        ):

            result = monte_carlo(
                hero_cards,
                board_cards,
                active_players,
                simulations
            )

        st.session_state[
            "calculation_result"
        ] = result

        st.session_state[
            "calculation_summary"
        ] = {
            "hero_cards": hero_cards,
            "board_cards": board_cards,
            "players": active_players
        }

    except ValueError as error:

        st.error(
            str(error)
        )

    except Exception as error:

        st.error(
            f"Error inesperado: {error}"
        )


# ============================================================
# 14. MOSTRAR RESULTADOS
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
        f'{summary["players"]}'
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
# 15. PIE DE PAGINA
# ============================================================

st.divider()

st.caption(
    "Los rivales se simulan con manos aleatorias "
    "entre todas las combinaciones legales disponibles."
)

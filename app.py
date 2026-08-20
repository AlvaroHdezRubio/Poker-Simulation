import base64
import random
from pathlib import Path

import streamlit as st
from treys import Card, Evaluator


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Poker Lab by Álvaro Hdez",
    page_icon="♠️",
    layout="centered"
)


# ============================================================
# CARGAR IMAGEN DEL JOKER
# ============================================================

def image_b64(path):
    image_path = Path(path)

    if not image_path.exists():
        return None

    return base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")


JOKER_IMAGE = image_b64("joker.png")


# ============================================================
# ESTILOS VISUALES
# ============================================================

st.markdown(
    r"""
    <style>

    /* Ocultar cabecera de Streamlit */

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

        color: white;
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

        margin: 0 0 0.80rem 0;
    }

    .brand-main {
        display: flex;
        align-items: center;

        gap: 0.40rem;

        font-size: 1.75rem;
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
    }

    .brand-signature {
        margin:
            0.42rem
            0
            0
            2rem;

        color:
            rgba(255, 255, 255, 0.88);

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
            1px solid
            rgba(229, 169, 35, 0.46) !important;

        border-radius: 14px !important;

        box-shadow:
            0 10px 28px
            rgba(0, 0, 0, 0.28);
    }


    /* Títulos */

    .section-title {
        color: white !important;

        font-size: 0.90rem;
        font-weight: 800;

        letter-spacing: 0.05rem;
        text-transform: uppercase;

        margin:
            0.50rem
            0
            0.30rem;

        text-shadow:
            0 1px 3px
            rgba(0, 0, 0, 0.85);
    }


    /* Etiquetas Carta 1, Flop 1, etc. */

    .card-position-label {
        width: 100%;

        color: white !important;

        font-size: 0.70rem;
        font-weight: 750;
        line-height: 1.15;

        text-align: center;

        margin: 0;
        padding: 0 0 0.28rem;

        text-shadow:
            0 1px 3px #000000;
    }


    /* ======================================================
       NAIPES PRINCIPALES
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
            2px solid
            rgba(255, 255, 255, 0.94) !important;

        border-radius: 9px !important;

        box-shadow:
            0 5px 10px
            rgba(0, 0, 0, 0.40) !important;

        overflow: hidden !important;
    }


    /* Marco interior */

    div[data-testid="stPopover"] > button::after {
        content: "";

        position: absolute;

        inset: 5px;

        border:
            1px solid
            rgba(25, 35, 28, 0.17);

        border-radius: 6px;

        pointer-events: none;
    }


    /* Centrar valor y palo */

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
    }


    /* ======================================================
       SELECTOR DE CARTAS
       ====================================================== */

    .picker-title {
        color: white !important;

        font-size: 0.90rem;
        font-weight: 800;

        margin-bottom: 0.30rem;
    }


    div[data-testid="stPopoverBody"] {
        overflow-x: hidden !important;
    }


    div[data-testid="stPopoverBody"] button {
        width: 100% !important;
        min-width: 0 !important;
        min-height: 2.25rem !important;

        padding: 0.05rem !important;

        background: #ffffff !important;
        background-color: #ffffff !important;

        border:
            1px solid
            rgba(40, 45, 40, 0.25) !important;

        border-radius: 6px !important;

        color: #111111 !important;
    }


    div[data-testid="stPopoverBody"] button p {
        color: #111111 !important;

        font-size: 0.76rem !important;
        font-weight: 800 !important;

        margin: 0 !important;
    }


    div[data-testid="stPopoverBody"] button span {
        font-size: 0.76rem !important;
        font-weight: 800 !important;
    }


    div[data-testid="stPopoverBody"] button:hover {
        background: #fff5c9 !important;
        background-color: #fff5c9 !important;

        border-color: #e5a923 !important;
    }


    div[data-testid="stPopoverBody"] button:disabled {
        background: #b9bfbb !important;
        background-color: #b9bfbb !important;

        opacity: 0.45 !important;
    }


    /* ======================================================
       CONTROLES
       ====================================================== */

    [data-testid="stWidgetLabel"] p {
        color: white !important;

        font-size: 0.78rem !important;
        font-weight: 700 !important;
    }


    [data-testid="stNumberInput"] input {
        min-height: 2.40rem;

        background-color: #ffffff !important;
        color: #17231d !important;

        font-weight: 800;

        text-align: center;
    }


    [data-testid="stNumberInput"] button {
        min-height: 2.40rem;

        color: white !important;
        background-color: #073b29 !important;
    }


    div[data-baseweb="select"] > div {
        min-height: 2.40rem;

        background-color: #ffffff !important;

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

        border:
            1px solid #ffd46d;
    }


    div[data-testid="stButton"] button[kind="secondary"] {
        background-color:
            rgba(3, 42, 27, 0.88);

        color: white;

        border:
            1px solid
            rgba(255, 255, 255, 0.45);
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
        padding:
            0.55rem
            0.15rem;

        background-color:
            rgba(2, 26, 18, 0.92);

        border-radius: 9px;

        text-align: center;
    }


    .result-win {
        border:
            1px solid
            rgba(85, 190, 77, 0.60);
    }


    .result-tie {
        border:
            1px solid
            rgba(229, 169, 35, 0.65);
    }


    .result-loss {
        border:
            1px solid
            rgba(220, 62, 55, 0.65);
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


    .hand-summary {
        margin-top: 0.45rem;
        margin-bottom: 0.15rem;

        padding:
            0.50rem
            0.65rem;

        background-color:
            rgba(2, 28, 19, 0.86);

        border:
            1px solid
            rgba(229, 169, 35, 0.45);

        border-radius: 10px;

        color: white;

        font-size: 0.78rem;
        line-height: 1.50;
    }


    [data-testid="stCaptionContainer"] p {
        color:
            rgba(255, 255, 255, 0.74) !important;
    }


    /* ======================================================
       JOKER
       ====================================================== */

    .joker-background {
        position: fixed;

        z-index: 0;

        pointer-events: none;

        right: -35px;
        bottom: -10px;

        width: 430px;
        height: 96vh;

        background-position: right bottom;
        background-repeat: no-repeat;
        background-size: contain;

        opacity: 0.46;

        mix-blend-mode: multiply;

        -webkit-mask-image:
            linear-gradient(
                to right,
                transparent 0%,
                rgba(0, 0, 0, 0.08) 16%,
                rgba(0, 0, 0, 0.55) 38%,
                black 64%
            );

        mask-image:
            linear-gradient(
                to right,
                transparent 0%,
                rgba(0, 0, 0, 0.08) 16%,
                rgba(0, 0, 0, 0.55) 38%,
                black 64%
            );

        filter:
            saturate(0.82)
            contrast(1.12)
            brightness(0.72);
    }


    /* Mantener los elementos de la interfaz en paralelo */

    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;

        gap: 0.45rem !important;
    }


    /* ======================================================
       VERSIÓN MÓVIL
       ====================================================== */

    @media screen and (max-width: 640px) {

        .block-container {
            width: 100% !important;
            max-width: 100% !important;

            padding:
                0.28rem
                0.32rem
                0.70rem !important;
        }


        .brand-header {
            margin-bottom: 0.56rem;
        }


        .brand-main {
            font-size: 1.22rem;
        }


        .brand-signature {
            margin:
                0.32rem
                0
                0
                1.50rem;

            font-size: 0.46rem;
            line-height: 1.35;
            letter-spacing: 0.085rem;
        }


        .section-title {
            font-size: 0.66rem;

            margin:
                0.32rem
                0
                0.20rem;
        }


        .card-position-label {
            font-size: 0.49rem;

            padding-bottom: 0.16rem;
        }


        /* Mantener cartas blancas */

        div[data-testid="stPopover"] > button {
            min-height: 3.60rem !important;

            background:
                linear-gradient(
                    145deg,
                    #fffef8 0%,
                    #f5f1e5 67%,
                    #ddd6c7 100%
                ) !important;

            color: #111111 !important;

            border-radius: 6px !important;
        }


        div[data-testid="stPopover"] > button
        [data-testid="stMarkdownContainer"] p,
        div[data-testid="stPopover"] > button
        [data-testid="stMarkdownContainer"] span {
            font-size: 0.88rem !important;
        }


        /* Evitar desplazamiento horizontal */

        [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;

            gap: 0.22rem !important;

            max-width: 100% !important;
        }


        div[data-testid="stPopoverBody"] {
            width: 100% !important;
            max-width: 100vw !important;

            overflow-x: hidden !important;
        }


        div[data-testid="stPopoverBody"]
        [data-testid="stHorizontalBlock"] {
            width: 100% !important;
            max-width: 100% !important;

            flex-wrap: wrap !important;

            gap: 0.10rem !important;

            overflow-x: hidden !important;
        }


        /* Tres opciones por fila */

        div[data-testid="stPopoverBody"]
        [data-testid="column"] {
            min-width: 0 !important;
            width: calc(33.333% - 0.10rem) !important;
            flex: 0 0 calc(33.333% - 0.10rem) !important;
        }


        div[data-testid="stPopoverBody"] button {
            width: 100% !important;
            min-width: 0 !important;
            min-height: 2.10rem !important;

            background: #ffffff !important;
            background-color: #ffffff !important;

            color: #111111 !important;
        }


        div[data-testid="stPopoverBody"] button p {
            color: #111111 !important;

            font-size: 0.70rem !important;
        }


        div[data-testid="stPopoverBody"] button span {
            font-size: 0.70rem !important;
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
            padding:
                0.42rem
                0.06rem;
        }


        .result-label {
            font-size: 0.47rem;
        }


        .result-value {
            font-size: 0.90rem;
        }


        .hand-summary {
            padding:
                0.40rem
                0.48rem;

            font-size: 0.68rem;
        }


        .joker-background {
            width: 155px;
            height: 50vh;

            right: -35px;
            bottom: -5px;

            opacity: 0.16;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MOSTRAR JOKER
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
# BARAJA
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
    Convierte una carta en texto visual.
    """

    if card is None:
        return "＋"

    return (
        RANK_NAMES[card[0]]
        + " "
        + SUIT_SYMBOLS[card[1]]
    )


def card_picker_label(card):
    """
    Aplica el color adecuado a cada palo.
    """

    if card is None:
        return (
            ':color[＋]'
            '{foreground="#374151"}'
        )

    text = card_visual_name(card)

    color = (
        "#d62828"
        if card[1] in ("h", "d")
        else "#111111"
    )

    return (
        f':color[{text}]'
        f'{{foreground="{color}"}}'
    )


# ============================================================
# ESTADO
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


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


def clear_result():
    """
    Borra los resultados cuando cambia la situación.
    """

    st.session_state[
        "calculation_result"
    ] = None

    st.session_state[
        "calculation_summary"
    ] = None


def select_card(
    slot_key,
    card
):
    """
    Guarda una carta seleccionada.
    """

    st.session_state[
        slot_key
    ] = card

    clear_result()


def reset_hand():
    """
    Restaura una mano nueva.
    """

    for key, value in DEFAULT_STATE.items():
        st.session_state[key] = value


def used_cards_except(
    current_slot
):
    """
    Devuelve las cartas usadas en otras posiciones.
    """

    return {
        st.session_state[slot]
        for slot in CARD_SLOTS
        if (
            slot != current_slot
            and
            st.session_state[slot]
            is not None
        )
    }


# ============================================================
# SELECTOR DE CARTAS
# ============================================================

def render_card_grid(
    slot_key,
    unavailable_cards
):
    """
    Muestra exactamente tres cartas por fila.

    No se omite ninguna carta y no se genera
    desplazamiento horizontal.
    """

    for start in range(
        0,
        len(FULL_DECK),
        3
    ):

        row_cards = FULL_DECK[
            start:start + 3
        ]

        columns = st.columns(3)

        for column, card in zip(
            columns,
            row_cards
        ):

            with column:

                st.button(
                    card_picker_label(card),

                    key=(
                        f"choose_"
                        f"{slot_key}_"
                        f"{card}"
                    ),

                    disabled=(
                        card
                        in unavailable_cards
                    ),

                    use_container_width=True,

                    on_click=select_card,

                    args=(
                        slot_key,
                        card
                    )
                )


def card_picker(
    slot_key,
    position_label,
    allow_empty=False
):
    """
    Muestra una carta y abre el selector al pulsarla.
    """

    st.markdown(
        (
            '<div '
            'class="card-position-label">'
            f'{position_label}'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    popover = st.popover(
        card_picker_label(
            st.session_state[
                slot_key
            ]
        ),

        use_container_width=True,

        key=(
            f"picker_{slot_key}"
        ),

        on_change="rerun"
    )


    # La baraja solo se genera cuando se abre.
    if popover.open:

        with popover:

            st.markdown(
                (
                    '<div '
                    'class="picker-title">'
                    f'Seleccionar '
                    f'{position_label}'
                    '</div>'
                ),
                unsafe_allow_html=True
            )


            if allow_empty:

                st.button(
                    "＋ Sin carta",

                    key=(
                        f"clear_{slot_key}"
                    ),

                    use_container_width=True,

                    on_click=select_card,

                    args=(
                        slot_key,
                        None
                    )
                )


            unavailable_cards = (
                used_cards_except(
                    slot_key
                )
            )


            render_card_grid(
                slot_key,
                unavailable_cards
            )


            st.caption(
                "Las cartas utilizadas "
                "aparecen desactivadas."
            )


# ============================================================
# VALIDACIÓN
# ============================================================

def validate_inputs(
    hero,
    board,
    players
):
    """
    Valida la situación introducida.
    """

    if None in hero:

        raise ValueError(
            "Selecciona tus dos cartas."
        )


    if len(board) not in (
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
            "Debe haber entre "
            "2 y 10 jugadores."
        )


    all_cards = hero + board


    if len(all_cards) != len(
        set(all_cards)
    ):

        raise ValueError(
            "Hay cartas repetidas."
        )


# ============================================================
# EVALUACIÓN
# ============================================================

def hand_score(
    player_cards,
    board_cards
):
    """
    Evalúa una mano mediante Treys.
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
# MONTE CARLO
# ============================================================

def monte_carlo(
    hero,
    board,
    players,
    simulations
):
    """
    Ejecuta la simulación Monte Carlo.
    """

    validate_inputs(
        hero,
        board,
        players
    )


    known_cards = set(
        hero + board
    )


    available_cards = [
        card
        for card in FULL_DECK
        if card not in known_cards
    ]


    wins = 0
    ties = 0
    losses = 0


    missing_board = (
        5 - len(board)
    )


    villains = (
        players - 1
    )


    cards_needed = (
        missing_board
        + villains * 2
    )


    for _ in range(
        simulations
    ):

        sample = random.sample(
            available_cards,
            cards_needed
        )


        completed_board = (
            board
            + sample[
                :missing_board
            ]
        )


        position = missing_board


        scores = [
            hand_score(
                hero,
                completed_board
            )
        ]


        for _ in range(
            villains
        ):

            villain_hand = sample[
                position:
                position + 2
            ]


            scores.append(
                hand_score(
                    villain_hand,
                    completed_board
                )
            )


            position += 2


        best_score = min(
            scores
        )


        if scores[0] != best_score:

            losses += 1


        elif scores.count(
            best_score
        ) == 1:

            wins += 1


        else:

            ties += 1


    return {
        "victoria": round(
            wins
            / simulations
            * 100,
            2
        ),

        "empate": round(
            ties
            / simulations
            * 100,
            2
        ),

        "derrota": round(
            losses
            / simulations
            * 100,
            2
        ),

        "simulaciones":
            simulations
    }


# ============================================================
# CABECERA
# ============================================================

st.markdown(
    (
        '<div class="brand-header">'

        '<div class="brand-main">'

        '<span class="brand-symbol">'
        '♠'
        '</span>'

        '<span>'
        'POKER LAB'
        '</span>'

        '</div>'

        '<div class="brand-signature">'
        'BY ÁLVARO HDEZ'
        '</div>'

        '</div>'
    ),
    unsafe_allow_html=True
)


# ============================================================
# INTERFAZ
# ============================================================

with st.container(
    border=True
):

    # Tus dos cartas en paralelo

    st.markdown(
        (
            '<div class="section-title">'
            'Tus cartas'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    hero_row = st.container(
        horizontal=True,
        gap="small"
    )


    hero_1 = hero_row.container(
        width="stretch"
    )


    hero_2 = hero_row.container(
        width="stretch"
    )


    with hero_1:

        card_picker(
            "hero_card_1",
            "Carta 1"
        )


    with hero_2:

        card_picker(
            "hero_card_2",
            "Carta 2"
        )


    # Tres cartas del flop en paralelo

    st.markdown(
        (
            '<div class="section-title">'
            'Cartas comunitarias'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    flop_row = st.container(
        horizontal=True,
        gap="small"
    )


    flop_1 = flop_row.container(
        width="stretch"
    )


    flop_2 = flop_row.container(
        width="stretch"
    )


    flop_3 = flop_row.container(
        width="stretch"
    )


    with flop_1:

        card_picker(
            "flop_card_1",
            "Flop 1",
            True
        )


    with flop_2:

        card_picker(
            "flop_card_2",
            "Flop 2",
            True
        )


    with flop_3:

        card_picker(
            "flop_card_3",
            "Flop 3",
            True
        )


    # Turn y river en paralelo

    turn_river_row = st.container(
        horizontal=True,
        gap="small"
    )


    turn_slot = (
        turn_river_row.container(
            width="stretch"
        )
    )


    river_slot = (
        turn_river_row.container(
            width="stretch"
        )
    )


    with turn_slot:

        card_picker(
            "turn_card",
            "Turn",
            True
        )


    with river_slot:

        card_picker(
            "river_card",
            "River",
            True
        )


    # Jugadores y simulaciones

    config_row = st.container(
        horizontal=True,
        gap="small"
    )


    players_slot = (
        config_row.container(
            width="stretch"
        )
    )


    simulations_slot = (
        config_row.container(
            width="stretch"
        )
    )


    with players_slot:

        active_players = (
            st.number_input(
                "Jugadores activos",
                min_value=2,
                max_value=10,
                step=1,
                key="active_players",
                on_change=clear_result
            )
        )


    with simulations_slot:

        simulations = (
            st.selectbox(
                "Simulaciones",
                [
                    10000,
                    25000,
                    50000,
                    100000
                ],

                format_func=lambda value: (
                    f"{value:,}"
                    .replace(",", ".")
                ),

                key="simulations",

                on_change=clear_result
            )
        )


    # Botones

    actions_row = st.container(
        horizontal=True,
        gap="small"
    )


    calculate_slot = (
        actions_row.container(
            width="stretch"
        )
    )


    reset_slot = (
        actions_row.container(
            width="stretch"
        )
    )


    with calculate_slot:

        calculate_button = (
            st.button(
                "Calcular probabilidades",
                type="primary",
                width="stretch"
            )
        )


    with reset_slot:

        st.button(
            "Nueva mano",
            width="stretch",
            on_click=reset_hand
        )


# ============================================================
# CALCULAR
# ============================================================

if calculate_button:

    try:

        hero = [
            st.session_state[
                "hero_card_1"
            ],
            st.session_state[
                "hero_card_2"
            ]
        ]


        positions = [
            st.session_state[
                "flop_card_1"
            ],
            st.session_state[
                "flop_card_2"
            ],
            st.session_state[
                "flop_card_3"
            ],
            st.session_state[
                "turn_card"
            ],
            st.session_state[
                "river_card"
            ]
        ]


        empty_found = False


        for card in positions:

            if card is None:

                empty_found = True


            elif empty_found:

                raise ValueError(
                    "Añade las cartas en orden: "
                    "flop, turn y river."
                )


        board = [
            card
            for card in positions
            if card is not None
        ]


        with st.spinner(
            "Simulando partidas..."
        ):

            result = monte_carlo(
                hero,
                board,
                active_players,
                simulations
            )


        st.session_state[
            "calculation_result"
        ] = result


        st.session_state[
            "calculation_summary"
        ] = {
            "hero": hero,
            "board": board,
            "players":
                active_players
        }


    except ValueError as error:

        st.error(
            str(error)
        )


    except Exception as error:

        st.error(
            f"Error inesperado: "
            f"{error}"
        )


# ============================================================
# RESULTADOS
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
        for card in summary["hero"]
    )


    if summary["board"]:

        board_text = " ".join(
            card_visual_name(card)
            for card in summary["board"]
        )


    else:

        board_text = (
            "Antes del flop"
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

        '<div '
        'class="result-card result-win">'

        '<div class="result-label">'
        'Victoria'
        '</div>'

        '<div class="result-value win-value">'
        f'{result["victoria"]} %'
        '</div>'

        '</div>'


        '<div '
        'class="result-card result-tie">'

        '<div class="result-label">'
        'Empate'
        '</div>'

        '<div class="result-value tie-value">'
        f'{result["empate"]} %'
        '</div>'

        '</div>'


        '<div '
        'class="result-card result-loss">'

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


    simulation_text = (
        f'{result["simulaciones"]:,}'
        .replace(",", ".")
    )


    st.caption(
        f"Resultado basado en "
        f"{simulation_text} simulaciones."
    )


# ============================================================
# PIE
# ============================================================

st.divider()


st.caption(
    "Los rivales se simulan con manos aleatorias "
    "entre todas las combinaciones legales disponibles."
)

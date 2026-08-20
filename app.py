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
    page_title="Poker Lab by Alvaro Hdez",
    page_icon="♠️",
    layout="centered"
)


# ============================================================
# 2. CARGAR LA IMAGEN DEL JOKER
# ============================================================

def load_image_as_base64(image_path):
    """
    Convierte joker.png en texto Base64 para utilizarlo
    como imagen decorativa de fondo.
    """

    path = Path(image_path)

    if not path.exists():
        return None

    with path.open("rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


JOKER_IMAGE = load_image_as_base64("joker.png")


# ============================================================
# 3. ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>

    /* Ocultamos la cabecera de Streamlit */
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

    /* Contenido principal */
    .block-container {
        position: relative;
        z-index: 5;
        max-width: 900px;
        padding-top: 0.75rem !important;
        padding-bottom: 1rem;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.30rem;
    }

    /* Marca */
    .brand-header {
        position: relative;
        z-index: 20;
        margin-bottom: 0.75rem;
    }

    .brand-main {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 850;
        line-height: 1;
        text-shadow:
            0 2px 4px rgba(0, 0, 0, 0.75),
            0 0 14px rgba(255, 180, 40, 0.30);
    }

    .brand-symbol {
        color: #e8ad25;
    }

    .brand-signature {
        margin-top: 0.28rem;
        margin-left: 2.05rem;
        color: rgba(255, 255, 255, 0.82);
        font-size: 0.68rem;
        font-weight: 650;
        letter-spacing: 0.14rem;
    }

    /* Panel principal */
    .poker-panel {
        margin-top: 0.35rem;
        padding: 0.75rem;
        background:
            linear-gradient(
                145deg,
                rgba(3, 31, 22, 0.88),
                rgba(4, 48, 31, 0.78)
            );
        border: 1px solid rgba(225, 169, 35, 0.45);
        border-radius: 14px;
        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.32),
            inset 0 0 25px rgba(255, 255, 255, 0.025);
    }

    /* Títulos de sección */
    .section-title {
        color: #ffffff;
        font-size: 0.86rem;
        font-weight: 750;
        letter-spacing: 0.06rem;
        text-transform: uppercase;
        margin-top: 0.65rem;
        margin-bottom: 0.25rem;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.60);
    }

    /* Nombre de cada posición */
    .card-position-label {
        color: rgba(255, 255, 255, 0.78);
        font-size: 0.70rem;
        font-weight: 650;
        text-align: center;
        margin-bottom: 0.15rem;
    }

    /* Botón que abre la baraja */
    div[data-testid="stPopover"] > button {
        min-height: 5.1rem !important;
        width: 100% !important;
        padding: 0.25rem !important;

        background:
            linear-gradient(
                145deg,
                #fffdf4,
                #e8e3d5
            ) !important;

        color: #121713 !important;

        border:
            2px solid rgba(255, 255, 255, 0.88) !important;

        border-radius: 7px !important;

        font-size: 1.45rem !important;
        font-weight: 850 !important;

        box-shadow:
            0 4px 8px rgba(0, 0, 0, 0.35),
            inset 0 0 8px rgba(0, 0, 0, 0.08);

        transition:
            transform 0.12s ease,
            box-shadow 0.12s ease;
    }

    div[data-testid="stPopover"] > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 7px 13px rgba(0, 0, 0, 0.42);
        border-color: #e5a923 !important;
    }

    /* Reverso para una posición vacía */
    .empty-card-description {
        color: rgba(255, 255, 255, 0.75);
        font-size: 0.78rem;
        text-align: center;
    }

    /* Contenido del selector de cartas */
    .picker-title {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 750;
        margin-bottom: 0.4rem;
    }

    .suit-title {
        margin-top: 0.45rem;
        margin-bottom: 0.15rem;
        color: #ffffff;
        font-size: 0.82rem;
        font-weight: 750;
    }

    /* Botones dentro de la baraja */
    div[data-testid="stPopoverBody"] button {
        min-height: 2.25rem !important;
        padding: 0.15rem !important;
        border-radius: 6px !important;
        font-size: 0.88rem !important;
        font-weight: 750 !important;
    }

    /* Etiquetas de controles */
    [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-size: 0.82rem !important;
        font-weight: 650 !important;
    }

    /* Selector numérico */
    [data-testid="stNumberInput"] input {
        min-height: 2.55rem;
        background-color: #f7f8f7 !important;
        color: #17231d !important;
        font-size: 1rem;
        font-weight: 750;
        text-align: center;
    }

    [data-testid="stNumberInput"] button {
        color: #ffffff !important;
        background-color: #073b29 !important;
        border-color: rgba(255, 255, 255, 0.35) !important;
    }

    /* Desplegable de simulaciones */
    div[data-baseweb="select"] > div {
        min-height: 2.55rem;
        background-color: #f7f8f7;
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 8px;
    }

    div[data-baseweb="select"] span {
        color: #17231d !important;
        font-weight: 600;
    }

    /* Botones generales */
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

    /* Resumen de la mano */
    .hand-summary {
        margin-top: 0.7rem;
        padding: 0.60rem 0.75rem;
        background-color: rgba(2, 28, 19, 0.80);
        border: 1px solid rgba(229, 169, 35, 0.35);
        border-radius: 10px;
        color: #ffffff;
        font-size: 0.84rem;
        line-height: 1.55;
    }

    /* Cuadrícula de resultados */
    .results-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.55rem;
        margin-top: 0.35rem;
    }

    .result-card {
        padding: 0.65rem 0.35rem;
        background-color: rgba(2, 26, 18, 0.88);
        border-radius: 9px;
        text-align: center;
        box-shadow: 0 5px 13px rgba(0, 0, 0, 0.25);
    }

    .result-win {
        border: 1px solid rgba(85, 190, 77, 0.55);
    }

    .result-tie {
        border: 1px solid rgba(229, 169, 35, 0.60);
    }

    .result-loss {
        border: 1px solid rgba(220, 62, 55, 0.60);
    }

    .result-label {
        color: rgba(255, 255, 255, 0.70);
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.04rem;
        text-transform: uppercase;
    }

    .result-value {
        margin-top: 0.18rem;
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

    [data-testid="stCaptionContainer"] p {
        color: rgba(255, 255, 255, 0.75) !important;
    }

    hr {
        border-color: rgba(255, 255, 255, 0.16);
        margin-top: 0.65rem;
        margin-bottom: 0.35rem;
    }

    /* Joker decorativo */
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
        opacity: 0.30;

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

    /* Version para móvil */
    @media screen and (max-width: 640px) {

        .block-container {
            width: 100% !important;
            max-width: 100% !important;
            padding-top: 0.55rem !important;
            padding-left: 0.45rem !important;
            padding-right: 0.45rem !important;
            padding-bottom: 0.8rem !important;
        }

        .brand-header {
            margin-bottom: 0.4rem;
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

        .poker-panel {
            padding: 0.45rem;
            border-radius: 11px;
        }

        .section-title {
            font-size: 0.72rem;
            margin-top: 0.45rem;
            margin-bottom: 0.16rem;
        }

        .card-position-label {
            font-size: 0.56rem;
        }

        /* Cartas adaptadas a la pantalla */
        div[data-testid="stPopover"] > button {
            min-height: 4.3rem !important;
            padding: 0.08rem !important;
            font-size: 1.10rem !important;
            border-radius: 6px !important;
        }

        div[data-testid="stPopoverBody"] button {
            min-height: 2.20rem !important;
            font-size: 0.78rem !important;
        }

        [data-testid="stWidgetLabel"] p {
            font-size: 0.72rem !important;
        }

        [data-testid="stNumberInput"] input,
        div[data-baseweb="select"] > div {
            min-height: 2.40rem;
        }

        div[data-testid="stButton"] button {
            min-height: 2.40rem;
            font-size: 0.82rem;
        }

        .hand-summary {
            padding: 0.45rem 0.55rem;
            font-size: 0.76rem;
        }

        .results-grid {
            gap: 0.30rem;
        }

        .result-card {
            padding: 0.50rem 0.15rem;
        }

        .result-label {
            font-size: 0.57rem;
        }

        .result-value {
            font-size: 1.05rem;
        }

        .joker-background {
            width: 155px;
            height: 55vh;
            right: -28px;
            bottom: 0;
            opacity: 0.08;
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

RANKS = "23456789TJQKA"
DISPLAY_RANKS = "AKQJT98765432"
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
    Convierte Ah en A♥, Ks en K♠, etc.
    """

    if card is None:
        return "＋"

    return (
        RANK_NAMES[card[0]]
        + SUIT_SYMBOLS[card[1]]
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
    Elimina el cálculo anterior cuando cambia alguna carta.
    """

    st.session_state["calculation_result"] = None
    st.session_state["calculation_summary"] = None


def select_card(slot_key, card):
    """
    Guarda la carta seleccionada en la posición indicada.
    """

    st.session_state[slot_key] = card
    clear_result()


def reset_hand():
    """
    Restaura una mano nueva.
    """

    for state_key, default_value in DEFAULT_STATE.items():
        st.session_state[state_key] = default_value


def used_cards_except(current_slot):
    """
    Devuelve las cartas utilizadas en las demás posiciones.
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
# 7. SELECTOR VISUAL DIRECTO DE CARTAS
# ============================================================

def card_picker(
    slot_key,
    position_label,
    allow_empty=False
):
    """
    Muestra una carta como botón.

    Al pulsarla se abre una baraja visual organizada
    por palos. La selección se realiza directamente.
    """

    selected_card = st.session_state[slot_key]
    trigger_label = card_visual_name(selected_card)

    st.markdown(
        f'<div class="card-position-label">'
        f'{position_label}'
        f'</div>',
        unsafe_allow_html=True
    )

    with st.popover(
        trigger_label,
        use_container_width=True,
        key=f"picker_{slot_key}"
    ):

        st.markdown(
            f'<div class="picker-title">'
            f'Seleccionar {position_label}'
            f'</div>',
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

        # Mostramos los cuatro palos.
        for suit in SUITS:

            st.markdown(
                f'<div class="suit-title">'
                f'{SUIT_NAMES[suit]}'
                f'</div>',
                unsafe_allow_html=True
            )

            suit_cards = [
                rank + suit
                for rank in DISPLAY_RANKS
            ]

            # Primera fila: siete cartas.
            first_row = suit_cards[:7]
            first_columns = st.columns(7)

            for column, card in zip(
                first_columns,
                first_row
            ):

                with column:

                    st.button(
                        card_visual_name(card),
                        key=f"choose_{slot_key}_{card}",
                        disabled=(
                            card in unavailable_cards
                        ),
                        use_container_width=True,
                        on_click=select_card,
                        args=(slot_key, card)
                    )

            # Segunda fila: seis cartas.
            second_row = suit_cards[7:]
            second_columns = st.columns(6)

            for column, card in zip(
                second_columns,
                second_row
            ):

                with column:

                    st.button(
                        card_visual_name(card),
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
# 8. VALIDACION
# ============================================================

def validate_inputs(
    hero_cards,
    board_cards,
    num_players
):
    """
    Comprueba que la mano sea válida.
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
            "Debes introducir las tres cartas del flop juntas."
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
# 9. EVALUACION DE MANOS
# ============================================================

def hand_score(
    player_cards,
    board_cards
):
    """
    Evalúa una mano mediante Treys.
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
# 10. SIMULACION MONTE CARLO
# ============================================================

def monte_carlo(
    hero_cards,
    board_cards,
    num_players,
    simulations=10000
):
    """
    Completa las cartas pendientes, reparte manos rivales
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

        for _ in range(missing_board_cards):

            completed_board.append(
                simulated_cards[position]
            )

            position += 1

        villains = []

        for _ in range(number_of_villains):

            villains.append(
                [
                    simulated_cards[position],
                    simulated_cards[position + 1]
                ]
            )

            position += 2

        hero_score = hand_score(
            hero_cards,
            completed_board
        )

        all_scores = [hero_score]

        for villain_hand in villains:

            all_scores.append(
                hand_score(
                    villain_hand,
                    completed_board
                )
            )

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
# 11. CABECERA
# ============================================================

st.markdown(
    '<div class="brand-header">'
    '<div class="brand-main">'
    '<span class="brand-symbol">♠</span>'
    '<span>POKER LAB</span>'
    '</div>'
    '<div class="brand-signature">'
    'BY ALVARO HDEZ'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 12. PANEL DE JUEGO
# ============================================================

st.markdown(
    '<div class="poker-panel">',
    unsafe_allow_html=True
)


# ============================================================
# 13. TUS CARTAS
# ============================================================

st.markdown(
    '<div class="section-title">Tus cartas</div>',
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


# ============================================================
# 14. CARTAS COMUNITARIAS
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Cartas comunitarias'
    '</div>',
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


# ============================================================
# 15. CONFIGURACION
# ============================================================

configuration_column_1, configuration_column_2 = (
    st.columns(2)
)


with configuration_column_1:

    active_players = st.number_input(
        label="Jugadores activos",
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


# ============================================================
# 16. BOTONES
# ============================================================

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


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 17. EJECUTAR EL CALCULO
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
                    "Añade las cartas comunitarias en orden: "
                    "flop, turn y river."
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

        st.session_state["calculation_result"] = result

        st.session_state["calculation_summary"] = {
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
# 18. MOSTRAR RESULTADOS
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

    st.markdown(
        f'<div class="hand-summary">'
        f'<div><strong>Tus cartas:</strong> '
        f'{hero_text}</div>'
        f'<div><strong>Mesa:</strong> '
        f'{board_text}</div>'
        f'<div><strong>Jugadores activos:</strong> '
        f'{summary["active_players"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        'Probabilidades'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="results-grid">

            <div class="result-card result-win">
                <div class="result-label">
                    Victoria
                </div>
                <div class="result-value win-value">
                    {result["victoria"]} %
                </div>
            </div>

            <div class="result-card result-tie">
                <div class="result-label">
                    Empate
                </div>
                <div class="result-value tie-value">
                    {result["empate"]} %
                </div>
            </div>

            <div class="result-card result-loss">
                <div class="result-label">
                    Derrota
                </div>
                <div class="result-value loss-value">
                    {result["derrota"]} %
                </div>
            </div>

        </div>
        """,
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
# 19. PIE DE PAGINA
# ============================================================

st.divider()

st.caption(
    "Los rivales se simulan con manos aleatorias "
    "entre todas las combinaciones legales disponibles."
)

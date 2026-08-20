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
# 2. IMAGEN DECORATIVA
# ============================================================

def load_image_as_base64(image_path):
    """Convierte una imagen local en texto Base64."""

    path = Path(image_path)

    if not path.exists():
        return None

    with path.open("rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


JOKER_IMAGE = load_image_as_base64("joker.png")


# ============================================================
# 3. ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    # Ocultar la cabecera de Streamlit  
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


    # Fondo tipo tapete  
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


    # Contenedor principal  
    .block-container {
        position: relative;
        z-index: 5;

        width: 100%;
        max-width: 920px;

        padding-top: 0.65rem !important;
        padding-bottom: 1rem !important;
    }


    # ------------------------------------------------------
       MARCA
       ------------------------------------------------------  

    .brand-header {
        pos*tion: relative;
        z-index: 2*;

        margin: 0 0 0.85rem 0;
*       padding: 0;
    }

    .bra*d-main {
        display: flex;
  *     align-items: center;

       *gap: 0.42rem;

        color: #fff*ff;

        font-size: 1.8rem;
  *     font-weight: 850;
        lin*-height: 1.05;

        text-shado*:
            0 2px 4px rgba(0, 0,*0, 0.8),
            0 0 14px rgba*255, 180, 40, 0.28);
    }

    .b*and-symbol {
        color: #e8ad2*;
    }

    .brand-signature {
        display: block;

        margin-top: 0.42rem;
        margin-left: 2rem;
        margin-bottom: 0;

        color: rgba(255, 255, 255, 0.87);

        font-size: 0.68rem;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: 0.14rem;
    }


    # ------------------------------------------------------
       PANEL
       ------------------------------------------------------  

    div[data-testid="stVerticalBlockBorderWrapper"] {
        back*round:
            linear-gradient*
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


    # Títulos  
    .section-title {
        color: #ffffff !important;

        font-size: 0.9rem;
        font-weight: 800;

        letter-spacing: 0.05rem;
        text-transform: uppercase;

        margin-top: 0.55rem;
        margin-bottom: 0.35rem;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.85);
    }


    # Etiquetas Carta 1, Flop 1, etc.  
    .card-position-label {
        display: block;

        width: 100%;

        color: #ffffff !important;

        font-size: 0.7rem;
        font-weight: 750;
        line-height: 1.15;

        text-align: center;

        margin: 0;
        padding: 0 0 0.3rem 0;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.95);
    }


    # ------------------------------------------------------
       CARTAS PRINCIPALES
       ------------------------------------------------------  

    div[data-testid="stPopover"] > button {
        position: relative !important;

        width: 100% !important;
        min-height: 5.6rem !important;

        padding: 0.25rem !important;

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
            0 5px 10px rgba(0, 0, 0, 0.4),
            inset 0 0 10px rgba(0, 0, 0, 0.08) !important;

        overflow: hidden !important;
    }


    div[data-testid="stPopover"] > button::after {
        content: "";

        position: absolute;

        inset: 5px;

        border:
            1px solid rgba(25, 35, 28, 0.17);

        border-radius: 6px;

        pointer-events: none;
    }


    # Contenedor del texto del naipe  
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


    # Texto base negro  
    div[data-testid="stPopover"] > button
    [data-testid="stMarkdownContainer"] p {
        color: #111111 !important;

        font-size: 1.55rem !important;
        font-weight: 850 !important;
        line-height: 1 !important;

        margin: 0 !important;
        opacity: 1 !important;
    }


    # Colores personalizados de Streamlit  
    div[data-testid="stPopover"] > button
    [data-testid="stMarkdownContainer"] span {
        font-size: 1.55rem !important;
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


    # ------------------------------------------------------
       POPOVER DE SELECCION
       ------------------------------------------------------  

    .picker-title {
        color: #ffffff !important;

        font-size: 0.95rem;
        font-weight: 800;

        margin-bottom: 0.4rem;
    }


    # Cuadrados del selector  
    div[data-testid="stPopoverBody"] button {
        width: 100% !important;
        min-width: 0 !important;
        min-height: 2.4rem !important;

        padding: 0.1rem !important;

        background-color: #f8f6ee !important;

        border:
            1px solid rgba(40, 45, 40, 0.25) !important;

        border-radius: 6px !important;

        color: #111111 !important;

        font-size: 0.8rem !important;
        font-weight: 800 !important;
    }


    div[data-testid="stPopoverBody"] button
    [data-testid="stMarkdownContainer"] p {
        color: #111111 !important;

        font-size: 0.8rem !important;
        font-weight: 800 !important;

        margin: 0 !important;
    }


    div[data-testid="stPopoverBody"] button
    [data-testid="stMarkdownContainer"] span {
        font-size: 0.8rem !important;
        font-weight: 800 !important;
    }


    div[data-testid="stPopoverBody"] button:hover {
        background-color: #fff5c9 !important;
        border-color: #e5a923 !important;
    }


    div[data-testid="stPopoverBody"] button:disabled {
        background-color: #aeb4b0 !important;

        opacity: 0.4 !important;
    }


    # ------------------------------------------------------
       CONTROLES
       ------------------------------------------------------  

    [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;

        font-size: 0.8rem !important;
        font-weight: 700 !important;

        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.7);
    }


    [data-testid="stNumberInput"] input {
        min-height: 2.5rem;

        background-color: #f7f8f7 !important;
        color: #17231d !important;

        font-size: 1rem;
        font-weight: 800;

        text-align: center;
    }


    [data-testid="stNumberInput"] button {
        min-height: 2.5rem;

        color: #ffffff !important;
        background-color: #073b29 !important;
    }


    div[data-baseweb="select"] > div {
        min-height: 2.5rem;

        background-color: #f7f8f7;

        border-radius: 8px;
    }


    div[data-baseweb="select"] span {
        color: #17231d !important;
        font-weight: 650;
    }


    # Botones  
    div[data-testid="stButton"] button {
        min-height: 2.45rem;

        border-radius: 8px;

        font-weight: 750;
    }


    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #e5a923;

        color: #172016;

        border: 1px solid #ffd46d;
    }


    div[data-testid="stButton"] button[kind="secondary"] {
        background-color:
            rgba(3, 42, 27, 0.88);

        color: #ffffff;

        border:
            1px solid rgba(255, 255, 255, 0.45);
    }


    # ------------------------------------------------------
       RESULTADOS
       ------------------------------------------------------  

    .hand-summary {
        margin-top: 0.65rem;

        padding: 0.55rem 0.7rem;

        background-color:
            rgba(2, 28, 19, 0.86);

        border:
            1px solid rgba(229, 169, 35, 0.45);

        border-radius: 10px;

        color: #ffffff;

        font-size: 0.8rem;
        line-height: 1.5;
    }


    .results-grid {
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 0.4rem;

        margin-top: 0.3rem;
    }


    .result-card {
        padding: 0.6rem 0.2rem;

        background-color:
            rgba(2, 26, 18, 0.92);

        border-radius: 9px;

        text-align: center;
    }


    .result-win {
        border:
            1px solid rgba(85, 190, 77, 0.6);
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

        font-size: 0.62rem;
        font-weight: 750;

        text-transform: uppercase;
    }


    .result-value {
        margin-top: 0.16rem;

        font-size: 1.3rem;
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
        color:
            rgba(255, 255, 255, 0.74) !important;
    }


    hr {
        border-color:
            rgba(255, 255, 255, 0.16);
    }


    # Joker  
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

        opacity: 0.26;
    }


    # ======================================================
       MOVIL
       ======================================================  

    @media screen and (max-width: 640px) {

        .block-container {
            max-width: 100% !important;

            padding-top: 0.3rem !important;
            padding-left: 0.35rem !important;
            padding-right: 0.35rem !important;
            padding-bottom: 0.7rem !important;
        }


        # Marca más compacta y sin solapamiento  
        .brand-header {
            margin-bottom: 0.42rem;
        }

        .brand-main {
            font-size: 1.25rem;
            line-height: 1.05;
        }

        .brand-signature {
            margin-top: 0.3rem;
            margin-left: 1.55rem;

            font-size: 0.48rem;
            line-height: 1.3;
            letter-spacing: 0.09rem;
        }


        .section-title {
            font-size: 0.68rem;

            margin-top: 0.35rem;
            margin-bottom: 0.22rem;
        }


        .card-position-label {
            font-size: 0.5rem;
            line-height: 1.1;

            padding-bottom: 0.18rem;
        }


        # Cartas compactas  
        div[data-testid="stPopover"] > button {
            min-height: 3.8rem !important;

            padding: 0.06rem !important;

            border-radius: 6px !important;
        }


        div[data-testid="stPopover"] > button
        [data-testid="stMarkdownContainer"] p,
        div[data-testid="stPopover"] > button
        [data-testid="stMarkdownContainer"] span {
            font-size: 0.92rem !important;
        }


        # Selector compacto, 6 cartas por fila  
        div[data-testid="stPopoverBody"] button {
            min-height: 2.25rem !important;

            padding: 0.05rem !important;

            font-size: 0.72rem !important;
        }


        div[data-testid="stPopoverBody"] button
        [data-testid="stMarkdownContainer"] p,
        div[data-testid="stPopoverBody"] button
        [data-testid="stMarkdownContainer"] span {
            font-size: 0.72rem !important;
        }


        [data-testid="stWidgetLabel"] p {
            font-size: 0.66rem !important;
        }


        [data-testid="stNumberInput"] input,
        [data-testid="stNumberInput"] button,
        div[data-baseweb="select"] > div {
            min-height: 2.3rem !important;
        }


        div[data-testid="stButton"] button {
            min-height: 2.3rem;

            font-size: 0.76rem;
        }


        .hand-summary {
            padding: 0.42rem 0.5rem;

            font-size: 0.7rem;
        }


        .results-grid {
            gap: 0.22rem;
        }


        .result-card {
            padding: 0.45rem 0.08rem;
        }


        .result-label {
            font-size: 0.49rem;
        }


        .result-value {
            font-size: 0.94rem;
        }


        .joker-background {
            width: 135px;
            height: 52vh;

            right: -25px;

            opacity: 0.06;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. MOSTRAR JOKER
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
# 5. BARAJA
# ============================================================

RANKS = "23456789TJQKA"
DISPLAY_RANKS = "AKQJT98765432"
SUITS = "shdc"

EVALUATOR = Evaluator()


def create_deck():
    """Crea una baraja completa."""

    return [
        rank + suit
        for suit in SUITS
        for rank in DISPLAY_RANKS
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


def card_visual_name(card):
    """Texto utilizado en el resumen."""

    if card is None:
        return "＋"

    return (
        RANK_NAMES[card[0]]
        + " "
        + SUIT_SYMBOLS[card[1]]
    )


def card_picker_label(card):
    """
    Etiqueta visual del naipe.

    Los colores se declaran directamente para impedir
    que el fondo verde los modifique.
    """

    if card is None:
        return ':color[＋]{foreground="#374151"}'

    rank = RANK_NAMES[card[0]]
    suit = SUIT_SYMBOLS[card[1]]

    if card[1] in ("h", "d"):
        return (
            f':color[{rank} {suit}]'
            f'{{foreground="#d62828"}}'
        )

    return (
        f':color[{rank} {suit}]'
        f'{{foreground="#111111"}}'
    )


# ============================================================
# 6. ESTADO
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
    """Borra el cálculo anterior."""

    st.session_state["calculation_result"] = None
    st.session_state["calculation_summary"] = None


def select_card(slot_key, card):
    """Selecciona una carta."""

    st.session_state[slot_key] = card

    clear_result()


def reset_hand():
    """Crea una mano nueva."""

    for key, value in DEFAULT_STATE.items():
        st.session_state[key] = value


def used_cards_except(current_slot):
    """Cartas utilizadas en otras posiciones."""

    return {
        st.session_state[slot]
        for slot in CARD_SLOTS
        if (
            slot != current_slot
            and st.session_state[slot] is not None
        )
    }


# ============================================================
# 7. SELECTOR VISUAL
# ============================================================

def render_button_row(
    cards,
    slot_key,
    unavailable_cards
):
    """
    Crea una fila horizontal de botones cuadrados.

    Se utilizan contenedores horizontales para evitar
    que Streamlit apile cada botón en móvil.
    """

    row = st.container(
        horizontal=True,
        horizontal_alignment="distribute",
        gap="xxsmall"
    )

    for card in cards:

        cell = row.container(
            width="stretch"
        )

        with cell:

            st.button(
                card_picker_label(card),
                key=f"choose_{slot_key}_{card}",
                disabled=(
                    card in unavailable_cards
                ),
                width="stretch",
                on_click=select_card,
                args=(slot_key, card)
            )


def card_picker(
    slot_key,
    position_label,
    allow_empty=False
):
    """
    Muestra un naipe y abre la baraja al pulsarlo.
    """

    selected_card = st.session_state[slot_key]

    st.markdown(
        (
            '<div class="card-position-label">'
            f'{position_label}'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    with st.popover(
        card_picker_label(selected_card),
        width="stretch",
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

        if allow_empty:

            st.button(
                "＋ Sin carta",
                key=f"clear_{slot_key}",
                width="stretch",
                on_click=select_card,
                args=(slot_key, None)
            )

        unavailable_cards = used_cards_except(
            slot_key
        )

        
        #La baraja completa se coloca en filas de seis.
        #Los palos siguen agrupados internamente, pero
        #no se muestran sus nombres.
        

        for start in range(
            0,
            len(FULL_DECK),
            6
        ):

            card_row = FULL_DECK[
                start:start + 6
            ]

            render_button_row(
                cards=card_row,
                slot_key=slot_key,
                unavailable_cards=unavailable_cards
            )

        st.caption(
            "Las cartas utilizadas aparecen desactivadas."
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
    """Valida los datos de la mano."""

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

    if not 2 <= num_players <= 10:
        raise ValueError(
            "Debe haber entre 2 y 10 jugadores."
        )

    all_cards = (
        hero_cards
        + board_cards
    )

    if len(all_cards) != len(
        set(all_cards)
    ):
        raise ValueError(
            "Hay cartas repetidas."
        )

    return hero_cards, board_cards


# ============================================================
# 9. EVALUACION
# ============================================================

def hand_score(
    player_cards,
    board_cards
):
    """Evalúa una mano mediante Treys."""

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
# 10. MONTE CARLO
# ============================================================

def monte_carlo(
    hero_cards,
    board_cards,
    num_players,
    simulations
):
    """Simula posibles partidas."""

    validate_inputs(
        hero_cards,
        board_cards,
        num_players
    )

    known_cards = set(
        hero_cards
        + board_cards
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
        5 - len(board_cards)
    )

    villains_count = (
        num_players - 1
    )

    cards_needed = (
        missing_board
        + villains_count * 2
    )

    for _ in range(simulations):

        sampled_cards = random.sample(
            available_cards,
            cards_needed
        )

        position = 0

        completed_board = (
            board_cards.copy()
        )

        for _ in range(missing_board):

            completed_board.append(
                sampled_cards[position]
            )

            position += 1

        villains = []

        for _ in range(villains_count):

            villains.append(
                [
                    sampled_cards[position],
                    sampled_cards[position + 1]
                ]
            )

            position += 2

        hero_score = hand_score(
            hero_cards,
            completed_board
        )

        all_scores = [
            hero_score
        ]

        for villain in villains:

            all_scores.append(
                hand_score(
                    villain,
                    completed_board
                )
            )

        best_score = min(
            all_scores
        )

        if hero_score != best_score:

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
# 12. INTERFAZ
# ============================================================

with st.container(
    border=True
):

    st.markdown(
        '<div class="section-title">Tus cartas</div>',
        unsafe_allow_html=True
    )


    # Dos cartas propias en una fila.
    hero_row = st.container(
        horizontal=True,
        gap="small"
    )


    hero_slot_1 = hero_row.container(
        width="stretch"
    )

    hero_slot_2 = hero_row.container(
        width="stretch"
    )


    with hero_slot_1:

        card_picker(
            "hero_card_1",
            "Carta 1"
        )


    with hero_slot_2:

        card_picker(
            "hero_card_2",
            "Carta 2"
        )


    st.markdown(
        (
            '<div class="section-title">'
            'Cartas comunitarias'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    # Flop: tres cartas en una fila.
    flop_row = st.container(
        horizontal=True,
        gap="small"
    )


    flop_slots = [
        flop_row.container(
            width="stretch"
        )
        for _ in range(3)
    ]


    flop_config = [
        ("flop_card_1", "Flop 1"),
        ("flop_card_2", "Flop 2"),
        ("flop_card_3", "Flop 3")
    ]


    for slot, config in zip(
        flop_slots,
        flop_config
    ):

        with slot:

            card_picker(
                config[0],
                config[1],
                allow_empty=True
            )


    # Turn y river: dos cartas en una fila.
    turn_river_row = st.container(
        horizontal=True,
        gap="small"
    )


    turn_slot = turn_river_row.container(
        width="stretch"
    )

    river_slot = turn_river_row.container(
        width="stretch"
    )


    with turn_slot:

        card_picker(
            "turn_card",
            "Turn",
            allow_empty=True
        )


    with river_slot:

        card_picker(
            "river_card",
            "River",
            allow_empty=True
        )


    # Configuración.
    config_row = st.container(
        horizontal=True,
        gap="small"
    )


    players_slot = config_row.container(
        width="stretch"
    )

    simulations_slot = config_row.container(
        width="stretch"
    )


    with players_slot:

        active_players = st.number_input(
            "Jugadores activos",
            min_value=2,
            max_value=10,
            step=1,
            key="active_players",
            on_change=clear_result
        )


    with simulations_slot:

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


    # Botones.
    actions_row = st.container(
        horizontal=True,
        gap="small"
    )


    calculate_slot = actions_row.container(
        width="stretch"
    )

    reset_slot = actions_row.container(
        width="stretch"
    )


    with calculate_slot:

        calculate_button = st.button(
            "Calcular probabilidades",
            type="primary",
            width="stretch"
        )


    with reset_slot:

        st.button(
            "Nueva mano",
            width="stretch",
            on_click=reset_hand
        )


# ============================================================
# 13. CALCULAR
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

        empty_found = False

        for card in board_positions:

            if card is None:

                empty_found = True

            elif empty_found:

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
            "active_players": active_players
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
# 14. RESULTADOS
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

    board_text = (
        " ".join(
            card_visual_name(card)
            for card in summary["board_cards"]
        )
        if summary["board_cards"]
        else "Antes del flop"
    )


    summary_html = (
        '<div class="hand-summary">'
        f'<div><strong>Tus cartas:</strong> '
        f'{hero_text}</div>'
        f'<div><strong>Mesa:</strong> '
        f'{board_text}</div>'
        f'<div><strong>Jugadores activos:</strong> '
        f'{summary["active_players"]}</div>'
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
        '<div class="result-label">Victoria</div>'
        f'<div class="result-value win-value">'
        f'{result["victoria"]} %</div>'
        '</div>'

        '<div class="result-card result-tie">'
        '<div class="result-label">Empate</div>'
        f'<div class="result-value tie-value">'
        f'{result["empate"]} %</div>'
        '</div>'

        '<div class="result-card result-loss">'
        '<div class="result-label">Derrota</div>'
        f'<div class="result-value loss-value">'
        f'{result["derrota"]} %</div>'
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
# 15. PIE
# ============================================================

st.divider()

st.caption(
    "Los rivales se simulan con manos aleatorias "
    "entre todas las combinaciones legales disponibles."
)

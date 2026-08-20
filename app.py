# ============================================================
# POKER LAB BY RAZA CHOPE
# Calculadora de probabilidades de Texas Hold'em
# ============================================================

import base64
import random
from pathlib import Path

import streamlit as st
from treys import Card, Evaluator


# ============================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Poker Lab by Raza Chope",
    page_icon="♠️",
    layout="centered"
)


# ============================================================
# 2. CARGAR LA IMAGEN DEL JOKER
# ============================================================

def load_image_as_base64(image_path):
    """
    Convierte joker.png en texto Base64 para utilizarlo
    como imagen de fondo dentro del CSS.
    """

    path = Path(image_path)

    # Si joker.png no existe, la aplicación seguirá funcionando.
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
       OCULTAR LA CABECERA SUPERIOR DE STREAMLIT
       ------------------------------------------------------ */

    [data-testid="stHeader"] {
        display: none !important;
    }

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
        z-index: 2;

        max-width: 850px;

        padding-top: 0.8rem !important;
        padding-bottom: 1rem;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.32rem;
    }


    /* ------------------------------------------------------
       CABECERA DE MARCA
       ------------------------------------------------------ */

    .brand-header {
        display: block !important;
        position: relative;
        z-index: 100;

        margin: 0 0 0.8rem 0;
        padding: 0;

        color: #ffffff;
    }

    .brand-main {
        display: flex;
        align-items: center;
        gap: 0.45rem;

        color: #ffffff;

        font-size: 1.75rem;
        font-weight: 850;
        line-height: 1;
        letter-spacing: -0.02rem;

        text-shadow:
            0 2px 4px rgba(0, 0, 0, 0.75),
            0 0 14px rgba(255, 180, 40, 0.30);
    }

    .brand-symbol {
        color: #e8ad25;
    }

    .brand-signature {
        margin-top: 0.3rem;
        margin-left: 2.05rem;

        color: rgba(255, 255, 255, 0.82);

        font-size: 0.70rem;
        font-weight: 650;
        letter-spacing: 0.14rem;
    }


    /* ------------------------------------------------------
       TÍTULOS DE LAS SECCIONES
       ------------------------------------------------------ */

    .section-title {
        display: block !important;
        position: relative;
        z-index: 10;

        color: #ffffff !important;

        font-size: 1.18rem;
        font-weight: 750;
        line-height: 1.2;

        margin-top: 0.65rem;
        margin-bottom: 0.20rem;

        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.60);
    }


    /* ------------------------------------------------------
       ETIQUETAS DE LOS CONTROLES
       ------------------------------------------------------ */

    [data-testid="stWidgetLabel"] {
        color: #ffffff !important;
    }

    [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;

        font-size: 0.86rem !important;
        font-weight: 650 !important;

        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.55);
    }

    [data-testid="stSelectbox"] label,
    [data-testid="stNumberInput"] label {
        color: #ffffff !important;
    }

    [data-testid="stSelectbox"] label p,
    [data-testid="stNumberInput"] label p {
        color: #ffffff !important;
    }


    /* ------------------------------------------------------
       DESPLEGABLES
       ------------------------------------------------------ */

    div[data-baseweb="select"] > div {
        min-height: 2.55rem;

        background-color:
            rgba(247, 249, 248, 0.97);

        border:
            1px solid rgba(255, 255, 255, 0.40);

        border-radius: 9px;
    }

    div[data-baseweb="select"] span {
        color: #17231d !important;
        font-weight: 550;
    }

    div[data-testid="stSelectbox"] {
        margin-bottom: 0;
    }


    /* ------------------------------------------------------
       SELECTOR NUMÉRICO DE JUGADORES
       ------------------------------------------------------ */

    [data-testid="stNumberInput"] input {
        min-height: 2.55rem;

        background-color:
            rgba(247, 249, 248, 0.97) !important;

        color: #17231d !important;

        font-size: 1rem;
        font-weight: 750;

        text-align: center;
    }

    [data-testid="stNumberInput"] button {
        color: #ffffff !important;

        background-color:
            rgba(3, 55, 35, 0.95) !important;

        border-color:
            rgba(255, 255, 255, 0.38) !important;
    }

    [data-testid="stNumberInput"] button:hover {
        background-color:
            rgba(10, 95, 59, 1) !important;
    }


    /* ------------------------------------------------------
       BOTONES
       ------------------------------------------------------ */

    div[data-testid="stButton"] button {
        min-height: 2.55rem;
        border-radius: 9px;
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
        border-color: #ffe69b;
    }

    div[data-testid="stButton"] button[kind="secondary"] {
        background-color:
            rgba(3, 42, 27, 0.84);

        color: #ffffff;

        border:
            1px solid rgba(255, 255, 255, 0.48);
    }

    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background-color:
            rgba(8, 76, 49, 0.96);

        color: #ffffff;
    }


    /* ------------------------------------------------------
       RESUMEN DE LA MANO
       ------------------------------------------------------ */

    .hand-summary {
        margin-top: 0.65rem;
        margin-bottom: 0.35rem;

        padding: 0.60rem 0.75rem;

        background-color:
            rgba(3, 40, 26, 0.72);

        border:
            1px solid rgba(255, 255, 255, 0.20);

        border-radius: 10px;

        color: #ffffff;

        font-size: 0.88rem;
        line-height: 1.55;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.18);
    }

    .hand-summary strong {
        color: #ffffff;
    }


    /* ------------------------------------------------------
       TARJETAS DE PROBABILIDAD
       ------------------------------------------------------ */

    div[data-testid="stMetric"] {
        min-height: auto;

        padding: 0.45rem 0.55rem;

        background-color:
            rgba(3, 40, 26, 0.80);

        border:
            1px solid rgba(255, 255, 255, 0.23);

        border-radius: 10px;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.18);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color:
            rgba(255, 255, 255, 0.84) !important;

        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
    }


    /* ------------------------------------------------------
       TEXTOS Y PIE DE PÁGINA
       ------------------------------------------------------ */

    .stMarkdown p {
        color: #ffffff;
    }

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color:
            rgba(255, 255, 255, 0.80) !important;
    }

    hr {
        border-color:
            rgba(255, 255, 255, 0.20);

        margin-top: 0.75rem;
        margin-bottom: 0.4rem;
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

        width: 430px;
        height: 100vh;

        background-position: right center;
        background-repeat: no-repeat;
        background-size: cover;

        opacity: 0.40;

        -webkit-mask-image:
            linear-gradient(
                to right,
                transparent 0%,
                rgba(0, 0, 0, 0.20) 18%,
                black 52%
            );

        mask-image:
            linear-gradient(
                to right,
                transparent 0%,
                rgba(0, 0, 0, 0.20) 18%,
                black 52%
            );
    }


    /* ------------------------------------------------------
       VERSIÓN PARA MÓVIL
       ------------------------------------------------------ */

    @media (max-width: 640px) {

        .block-container {
            padding-top: 0.55rem !important;
            padding-left: 0.55rem;
            padding-right: 0.55rem;
            padding-bottom: 0.75rem;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.20rem;
        }

        .brand-header {
            margin-bottom: 0.45rem;
        }

        .brand-main {
            font-size: 1.42rem;
        }

        .brand-signature {
            margin-top: 0.20rem;
            margin-left: 1.80rem;

            font-size: 0.58rem;
            letter-spacing: 0.11rem;
        }

        .section-title {
            font-size: 1.02rem;

            margin-top: 0.48rem;
            margin-bottom: 0.12rem;
        }

        [data-testid="stWidgetLabel"] p {
            color: #ffffff !important;
            font-size: 0.76rem !important;
        }

        div[data-baseweb="select"] > div {
            min-height: 2.35rem;
            border-radius: 8px;
        }

        [data-testid="stNumberInput"] input {
            min-height: 2.35rem;
            font-size: 1rem;
        }

        [data-testid="stNumberInput"] button {
            min-height: 2.35rem;
            min-width: 2.7rem;
        }

        div[data-testid="stButton"] button {
            min-height: 2.40rem;
            font-size: 0.82rem;
        }

        .hand-summary {
            font-size: 0.78rem;
            padding: 0.45rem 0.55rem;
            line-height: 1.45;
        }

        div[data-testid="stMetric"] {
            padding: 0.35rem 0.40rem;
        }

        [data-testid="stMetricLabel"] p {
            font-size: 0.70rem !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.20rem !important;
        }

        .joker-background {
            width: 190px;
            height: 65vh;

            right: -25px;
            bottom: 0;

            background-position: 69% center;
            background-size: cover;

            opacity: 0.14;

            -webkit-mask-image:
                linear-gradient(
                    to right,
                    transparent 0%,
                    rgba(0, 0, 0, 0.15) 25%,
                    black 65%
                );

            mask-image:
                linear-gradient(
                    to right,
                    transparent 0%,
                    rgba(0, 0, 0, 0.15) 25%,
                    black 65%
                );
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. MOSTRAR EL JOKER LATERAL
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
                        rgba(5, 45, 31, 0.03),
                        rgba(5, 45, 31, 0.52)
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


def card_visual_name(card):
    """
    Convierte Ah en A♥, Ks en K♠, etc.
    """

    if card is None:
        return "Sin carta"

    rank = card[0]
    suit = card[1]

    return RANK_NAMES[rank] + SUIT_SYMBOLS[suit]


# ============================================================
# 7. VALIDACIÓN DE DATOS
# ============================================================

def validate_inputs(
    hero_cards,
    board_cards,
    num_players
):
    """
    Valida cartas, mesa y jugadores.
    """

    if len(hero_cards) != 2:
        raise ValueError(
            "Debes seleccionar exactamente dos cartas."
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

    if len(all_known_cards) != len(set(all_known_cards)):
        raise ValueError(
            "Hay cartas repetidas. "
            "Una carta no puede aparecer dos veces."
        )

    for card in all_known_cards:

        if card not in FULL_DECK:
            raise ValueError(
                f"La carta {card} no es válida."
            )

    return hero_cards, board_cards


# ============================================================
# 8. EVALUAR UNA MANO
# ============================================================

def hand_score(
    player_cards,
    board_cards
):
    """
    Evalúa una mano utilizando Treys.

    Una puntuación menor representa una mano mejor.
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
# 9. SIMULACIÓN MONTE CARLO
# ============================================================

def monte_carlo(
    hero_cards,
    board_cards,
    num_players,
    simulations=10000
):
    """
    Completa la mesa, reparte cartas aleatorias a los rivales
    y calcula victorias, empates y derrotas.
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

        # Completamos las cartas comunitarias restantes.
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
        "simulaciones": simulations,
        "jugadores": num_players,
        "rivales": number_of_villains
    }


# ============================================================
# 10. REINICIAR LA MANO
# ============================================================

def reset_hand():
    """
    Limpia la mesa y restaura los valores iniciales.
    """

    st.session_state["hero_card_1"] = "Kh"
    st.session_state["hero_card_2"] = "Ks"

    st.session_state["flop_card_1"] = None
    st.session_state["flop_card_2"] = None
    st.session_state["flop_card_3"] = None
    st.session_state["turn_card"] = None
    st.session_state["river_card"] = None

    st.session_state["active_players"] = 6
    st.session_state["simulations"] = 25000


# ============================================================
# 11. TÍTULO CORPORATIVO
# ============================================================

# Las cadenas contiguas se unen automáticamente.
# Esta forma evita errores con comillas multilínea.
st.markdown(
    '<div class="brand-header">'
    '<div class="brand-main">'
    '<span class="brand-symbol">♠</span>'
    '<span>POKER LAB</span>'
    '</div>'
    '<div class="brand-signature">BY RAZA CHOPE</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 12. TUS CARTAS
# ============================================================

st.markdown(
    '<div class="section-title">Tus cartas</div>',
    unsafe_allow_html=True
)


hero_column_1, hero_column_2 = st.columns(2)


with hero_column_1:

    hero_card_1 = st.selectbox(
        label="Carta 1",
        options=FULL_DECK,
        index=FULL_DECK.index("Kh"),
        format_func=card_visual_name,
        key="hero_card_1"
    )


with hero_column_2:

    hero_card_2 = st.selectbox(
        label="Carta 2",
        options=FULL_DECK,
        index=FULL_DECK.index("Ks"),
        format_func=card_visual_name,
        key="hero_card_2"
    )


# ============================================================
# 13. CARTAS COMUNITARIAS
# ============================================================

st.markdown(
    '<div class="section-title">Cartas comunitarias</div>',
    unsafe_allow_html=True
)


BOARD_OPTIONS = [None] + FULL_DECK


flop_column_1, flop_column_2, flop_column_3 = st.columns(3)


with flop_column_1:

    flop_card_1 = st.selectbox(
        label="Flop 1",
        options=BOARD_OPTIONS,
        format_func=card_visual_name,
        key="flop_card_1"
    )


with flop_column_2:

    flop_card_2 = st.selectbox(
        label="Flop 2",
        options=BOARD_OPTIONS,
        format_func=card_visual_name,
        key="flop_card_2"
    )


with flop_column_3:

    flop_card_3 = st.selectbox(
        label="Flop 3",
        options=BOARD_OPTIONS,
        format_func=card_visual_name,
        key="flop_card_3"
    )


turn_column, river_column = st.columns(2)


with turn_column:

    turn_card = st.selectbox(
        label="Turn",
        options=BOARD_OPTIONS,
        format_func=card_visual_name,
        key="turn_card"
    )


with river_column:

    river_card = st.selectbox(
        label="River",
        options=BOARD_OPTIONS,
        format_func=card_visual_name,
        key="river_card"
    )


# ============================================================
# 14. JUGADORES ACTIVOS Y SIMULACIONES
# ============================================================

active_players = st.number_input(
    label="Jugadores activos, incluyéndote a ti",
    min_value=2,
    max_value=10,
    value=6,
    step=1,
    key="active_players"
)


simulations = st.selectbox(
    label="Simulaciones",
    options=[
        10000,
        25000,
        50000,
        100000
    ],
    index=1,
    format_func=lambda value: (
        f"{value:,}".replace(",", ".")
    ),
    key="simulations"
)


# ============================================================
# 15. BOTONES
# ============================================================

calculate_column, reset_column = st.columns(2)


with calculate_column:

    calculate_button = st.button(
        "Calcular",
        type="primary",
        use_container_width=True
    )


with reset_column:

    st.button(
        "Nueva mano",
        on_click=reset_hand,
        use_container_width=True
    )


# ============================================================
# 16. CALCULAR Y MOSTRAR RESULTADOS
# ============================================================

if calculate_button:

    try:

        hero_cards = [
            hero_card_1,
            hero_card_2
        ]

        board_positions = [
            flop_card_1,
            flop_card_2,
            flop_card_3,
            turn_card,
            river_card
        ]

        # Validamos que no haya una carta
        # después de una posición vacía.
        empty_position_found = False

        for card in board_positions:

            if card is None:
                empty_position_found = True

            elif empty_position_found:
                raise ValueError(
                    "Añade las cartas comunitarias en orden: "
                    "primero las tres cartas del flop, "
                    "después el turn y finalmente el river."
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
                hero_cards=hero_cards,
                board_cards=board_cards,
                num_players=active_players,
                simulations=simulations
            )

        hero_text = " ".join(
            card_visual_name(card)
            for card in hero_cards
        )

        if board_cards:

            board_text = " ".join(
                card_visual_name(card)
                for card in board_cards
            )

        else:

            board_text = "Antes del flop"

        # Resumen compacto de la situación.
        st.markdown(
            f'<div class="hand-summary">'
            f'<div><strong>Tus cartas:</strong> {hero_text}</div>'
            f'<div><strong>Mesa:</strong> {board_text}</div>'
            f'<div><strong>Jugadores activos:</strong> '
            f'{active_players}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">Probabilidades</div>',
            unsafe_allow_html=True
        )

        win_column, tie_column, loss_column = st.columns(3)


        with win_column:

            st.metric(
                label="Victoria",
                value=f"{result['victoria']} %"
            )


        with tie_column:

            st.metric(
                label="Empate",
                value=f"{result['empate']} %"
            )


        with loss_column:

            st.metric(
                label="Derrota",
                value=f"{result['derrota']} %"
            )


        simulation_text = (
            f"{result['simulaciones']:,}"
            .replace(",", ".")
        )

        st.caption(
            f"Resultado basado en "
            f"{simulation_text} simulaciones."
        )


    except ValueError as error:

        st.error(str(error))


    except Exception as error:

        st.error(
            f"Se ha producido un error inesperado: {error}"
        )


# ============================================================
# 17. INFORMACIÓN FINAL
# ============================================================

st.divider()

st.caption(
    "Los rivales se simulan con manos aleatorias "
    "entre todas las combinaciones legales disponibles."
)

# ============================================================
# RAZA CHOPE POKAH
# Calculadora de probabilidades para Texas Hold'em
# ============================================================

import base64
import random

from pathlib import Path

import streamlit as st

from treys import Card, Evaluator


# ============================================================
# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA
# ============================================================

# Configuramos el nombre de la pestaña, el icono
# y la anchura general de la aplicación.
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
    Convierte la imagen joker.png en texto Base64.

    Esto nos permite utilizar la imagen como fondo lateral
    mediante HTML y CSS.
    """

    path = Path(image_path)

    # Si la imagen no existe, devolvemos None.
    # La calculadora seguirá funcionando sin la imagen.
    if not path.exists():
        return None

    # Abrimos la imagen en modo binario.
    with path.open("rb") as image_file:

        # Convertimos la imagen en texto Base64.
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return encoded_image


# Buscamos joker.png en la misma ubicación que app.py.
JOKER_IMAGE = load_image_as_base64("joker.png")


# ============================================================
# 3. ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       FONDO GENERAL TIPO TAPETE
       ====================================================== */

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


    /* ======================================================
       CONTENEDOR PRINCIPAL
       ====================================================== */

    .block-container {
        position: relative;
        z-index: 2;

        max-width: 850px;

        padding-top: 0.65rem;
        padding-bottom: 1rem;
    }


    /* Reducimos los espacios verticales entre elementos */
    div[data-testid="stVerticalBlock"] {
        gap: 0.34rem;
    }


    /* ======================================================
       TÍTULO PRINCIPAL
       ====================================================== */

st.markdown(
    """
    <div
        style="
            display: block;
            position: relative;
            z-index: 100;
            margin: 0 0 0.7rem 0;
            padding: 0;
            color: #ffffff;
            line-height: 1;
            text-shadow:
                0 2px 4px rgba(0, 0, 0, 0.75),
                0 0 14px rgba(255, 180, 40, 0.30);
        "
    >
        <div
            style="
                display: flex;
                align-items: center;
                gap: 0.45rem;
                font-size: 1.75rem;
                font-weight: 850;
                letter-spacing: -0.02rem;
            "
        >
            <span style="color: #e8ad25;">♠</span>
            <span>POKER LAB</span>
        </div>

        <div
            style="
                margin-top: 0.3rem;
                margin-left: 2.05rem;
                color: rgba(255, 255, 255, 0.78);
                font-size: 0.7rem;
                font-weight: 650;
                letter-spacing: 0.14rem;
            "
        >
            BY RAZA CHOPE
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
   


    /* ======================================================
       TÍTULOS DE LAS SECCIONES
       ====================================================== */

    .section-title {
        display: block !important;
        position: relative;
        z-index: 10;

        color: #ffffff !important;

        font-size: 1.18rem;
        font-weight: 750;
        line-height: 1.2;

        margin-top: 0.7rem;
        margin-bottom: 0.22rem;

        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.60);
    }


    /* ======================================================
       ETIQUETAS DE LOS CONTROLES
       Carta 1, Carta 2, Flop, Turn, etc.
       ====================================================== */

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


    /* Etiquetas de los desplegables */
    [data-testid="stSelectbox"] label {
        color: #ffffff !important;
    }

    [data-testid="stSelectbox"] label p {
        color: #ffffff !important;
    }


    /* Etiquetas del selector de jugadores */
    [data-testid="stNumberInput"] label {
        color: #ffffff !important;
    }

    [data-testid="stNumberInput"] label p {
        color: #ffffff !important;
    }


    /* ======================================================
       DESPLEGABLES DE CARTAS Y SIMULACIONES
       ====================================================== */

    div[data-baseweb="select"] > div {
        min-height: 2.55rem;

        background-color:
            rgba(247, 249, 248, 0.97);

        border:
            1px solid rgba(255, 255, 255, 0.40);

        border-radius: 9px;
    }


    /* Texto seleccionado dentro del desplegable */
    div[data-baseweb="select"] span {
        color: #17231d !important;
        font-weight: 550;
    }


    /* Reducimos el margen inferior */
    div[data-testid="stSelectbox"] {
        margin-bottom: 0;
    }


    /* ======================================================
       SELECTOR NUMÉRICO DE JUGADORES
       ====================================================== */

    [data-testid="stNumberInput"] input {
        min-height: 2.55rem;

        background-color:
            rgba(247, 249, 248, 0.97) !important;

        color: #17231d !important;

        font-size: 1rem;
        font-weight: 750;

        text-align: center;
    }


    /* Botones para aumentar o reducir jugadores */
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


    /* ======================================================
       BOTONES PRINCIPALES
       ====================================================== */

    div[data-testid="stButton"] button {
        min-height: 2.55rem;

        border-radius: 9px;

        font-weight: 750;
    }


    /* Botón Calcular */
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


    /* Botón Nueva mano */
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


    /* ======================================================
       RESUMEN DE LA MANO ANALIZADA
       ====================================================== */

    .hand-summary {
        margin-top: 0.65rem;
        margin-bottom: 0.35rem;

        padding: 0.6rem 0.75rem;

        background-color:
            rgba(3, 40, 26, 0.70);

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


    /* ======================================================
       TARJETAS DE RESULTADOS
       ====================================================== */

    div[data-testid="stMetric"] {
        min-height: auto;

        padding: 0.45rem 0.55rem;

        background-color:
            rgba(3, 40, 26, 0.78);

        border:
            1px solid rgba(255, 255, 255, 0.23);

        border-radius: 10px;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.18);
    }


    /* Títulos Victoria, Empate y Derrota */
    [data-testid="stMetricLabel"] {
        color:
            rgba(255, 255, 255, 0.84) !important;
    }


    [data-testid="stMetricLabel"] p {
        color:
            rgba(255, 255, 255, 0.84) !important;

        font-weight: 650 !important;
    }


    /* Porcentajes */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }


    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
    }


    /* ======================================================
       TEXTOS Y AVISOS
       ====================================================== */

    .stMarkdown p {
        color: #ffffff;
    }


    [data-testid="stCaptionContainer"] {
        color:
            rgba(255, 255, 255, 0.80) !important;
    }


    [data-testid="stCaptionContainer"] p {
        color:
            rgba(255, 255, 255, 0.80) !important;
    }


    /* Línea divisoria */
    hr {
        border-color:
            rgba(255, 255, 255, 0.20);

        margin-top: 0.75rem;
        margin-bottom: 0.4rem;
    }


    /* ======================================================
       IMAGEN LATERAL DEL JOKER
       ====================================================== */

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

        /*
        La máscara integra el lateral izquierdo de la imagen
        con el tapete verde.
        */
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


    /* ======================================================
       AJUSTES PARA PANTALLAS DE MÓVIL
       ====================================================== */

    @media (max-width: 640px) {

        /* Reducimos los márgenes generales */
        .block-container {
            padding-top: 0.30rem;
            padding-left: 0.55rem;
            padding-right: 0.55rem;
            padding-bottom: 0.75rem;
        }


        div[data-testid="stVerticalBlock"] {
            gap: 0.20rem;
        }


        /* Título más pequeño */
        .app-title {
            display: block !important;

            font-size: 1.45rem;

            margin-top: 0;
            margin-bottom: 0.32rem;
        }


        /* Títulos de sección más pequeños */
        .section-title {
            font-size: 1.02rem;

            margin-top: 0.48rem;
            margin-bottom: 0.12rem;
        }


        /* Mini títulos de los controles */
        [data-testid="stWidgetLabel"] p {
            color: #ffffff !important;

            font-size: 0.76rem !important;
        }


        /* Desplegables un poco más compactos */
        div[data-baseweb="select"] > div {
            min-height: 2.35rem;

            border-radius: 8px;
        }


        /* Selector numérico */
        [data-testid="stNumberInput"] input {
            min-height: 2.35rem;

            font-size: 1rem;
        }


        /* Botones de aumento y reducción */
        [data-testid="stNumberInput"] button {
            min-height: 2.35rem;
            min-width: 2.7rem;
        }


        /* Botones principales */
        div[data-testid="stButton"] button {
            min-height: 2.4rem;

            font-size: 0.82rem;
        }


        /* Resumen de la mano */
        .hand-summary {
            font-size: 0.78rem;

            padding: 0.45rem 0.55rem;

            line-height: 1.45;
        }


        /* Tarjetas de resultados */
        div[data-testid="stMetric"] {
            padding: 0.35rem 0.4rem;
        }


        [data-testid="stMetricLabel"] p {
            font-size: 0.70rem !important;
        }


        [data-testid="stMetricValue"] {
            font-size: 1.20rem !important;
        }


        /* Joker menos intenso para no molestar */
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
# 4. MOSTRAR EL JOKER COMO FONDO LATERAL
# ============================================================

# Solo añadimos la imagen si joker.png existe.
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

# Valores de las cartas.
#
# T representa el 10.
# J representa la jota.
# Q representa la reina.
# K representa el rey.
# A representa el as.
RANKS = "23456789TJQKA"


# Palos:
#
# s = picas
# h = corazones
# d = diamantes
# c = tréboles
SUITS = "shdc"


# Creamos el evaluador de Treys.
EVALUATOR = Evaluator()


def create_deck():
    """
    Crea y devuelve una baraja completa de 52 cartas.
    """

    return [
        rank + suit
        for rank in RANKS
        for suit in SUITS
    ]


# Creamos la baraja una sola vez.
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
    Convierte el formato interno al formato visual.

    Ejemplos:
        Ah se convierte en A♥
        Ks se convierte en K♠
        Td se convierte en 10♦
    """

    if card is None:
        return "Sin carta"

    rank = card[0]
    suit = card[1]

    return (
        RANK_NAMES[rank]
        + SUIT_SYMBOLS[suit]
    )


# ============================================================
# 7. VALIDACIÓN DE DATOS
# ============================================================

def validate_inputs(
    hero_cards,
    board_cards,
    num_players
):
    """
    Comprueba que las cartas y jugadores sean válidos.
    """

    # Debemos tener exactamente dos cartas.
    if len(hero_cards) != 2:
        raise ValueError(
            "Debes seleccionar exactamente dos cartas."
        )

    # Estados válidos de la mesa:
    #
    # 0 = antes del flop.
    # 3 = flop.
    # 4 = turn.
    # 5 = river.
    if len(board_cards) not in (0, 3, 4, 5):
        raise ValueError(
            "Debes introducir las tres cartas "
            "del flop juntas."
        )

    # Número válido de jugadores.
    if num_players < 2 or num_players > 10:
        raise ValueError(
            "Debe haber entre 2 y 10 "
            "jugadores activos."
        )

    # Unimos todas las cartas conocidas.
    all_known_cards = (
        hero_cards
        + board_cards
    )

    # Comprobamos si hay cartas repetidas.
    if len(all_known_cards) != len(
        set(all_known_cards)
    ):
        raise ValueError(
            "Hay cartas repetidas. "
            "Una carta no puede aparecer dos veces."
        )

    # Comprobamos que todas las cartas existan.
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

    En Treys, una puntuación más pequeña
    representa una mano mejor.
    """

    # Convertimos las cartas del jugador.
    player_treys = [
        Card.new(card)
        for card in player_cards
    ]

    # Convertimos las cartas comunitarias.
    board_treys = [
        Card.new(card)
        for card in board_cards
    ]

    # Calculamos y devolvemos la puntuación.
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
    Simula posibles partidas de Texas Hold'em.

    Completa la mesa, reparte cartas a los rivales
    y cuenta victorias, empates y derrotas.
    """

    # Validamos los datos.
    hero_cards, board_cards = validate_inputs(
        hero_cards,
        board_cards,
        num_players
    )

    # Cartas conocidas que no pueden volver a salir.
    known_cards = set(
        hero_cards + board_cards
    )

    # Baraja sin las cartas conocidas.
    available_cards = [
        card
        for card in FULL_DECK
        if card not in known_cards
    ]

    # Contadores.
    wins = 0
    ties = 0
    losses = 0

    # Cartas comunitarias que faltan.
    missing_board_cards = (
        5 - len(board_cards)
    )

    # Número de rivales activos.
    number_of_villains = (
        num_players - 1
    )

    # Cartas necesarias en cada simulación.
    cards_needed = (
        missing_board_cards
        + number_of_villains * 2
    )

    # Repetimos el proceso miles de veces.
    for _ in range(simulations):

        # Elegimos todas las cartas necesarias
        # sin repetir ninguna.
        simulated_cards = random.sample(
            available_cards,
            cards_needed
        )

        # Posición dentro de las cartas simuladas.
        position = 0

        # Copiamos la mesa actual.
        completed_board = (
            board_cards.copy()
        )

        # Completamos turn y river.
        for _ in range(
            missing_board_cards
        ):

            completed_board.append(
                simulated_cards[position]
            )

            position += 1

        # Guardamos las manos rivales.
        villains = []

        # Repartimos dos cartas a cada rival.
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

        # Empezamos la lista de puntuaciones
        # con nuestra propia puntuación.
        all_scores = [
            hero_score
        ]

        # Evaluamos cada mano rival.
        for villain_hand in villains:

            villain_score = hand_score(
                villain_hand,
                completed_board
            )

            all_scores.append(
                villain_score
            )

        # En Treys, la puntuación menor es mejor.
        best_score = min(
            all_scores
        )

        # Si no tenemos la mejor puntuación,
        # perdemos esta simulación.
        if hero_score != best_score:

            losses += 1

        else:

            # Contamos cuántos jugadores
            # tienen la mejor puntuación.
            number_of_winners = (
                all_scores.count(
                    best_score
                )
            )

            # Si solo hay un ganador,
            # hemos ganado.
            if number_of_winners == 1:

                wins += 1

            # Si hay varios ganadores,
            # hemos empatado.
            else:

                ties += 1

    # Convertimos los contadores en porcentajes.
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
    Restaura los controles a sus valores iniciales.
    """

    # Cartas propias iniciales.
    st.session_state["hero_card_1"] = "Kh"
    st.session_state["hero_card_2"] = "Ks"

    # Dejamos la mesa vacía.
    st.session_state["flop_card_1"] = None
    st.session_state["flop_card_2"] = None
    st.session_state["flop_card_3"] = None
    st.session_state["turn_card"] = None
    st.session_state["river_card"] = None

    # Restauramos jugadores y simulaciones.
    st.session_state["active_players"] = 6
    st.session_state["simulations"] = 25000


# ============================================================
# 11. TÍTULO PRINCIPAL
# ============================================================

st.markdown(
    """
    <div class="app-title">
        🃏 Raza Chope Pokah
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 12. SELECTORES DE NUESTRAS CARTAS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Tus cartas
    </div>
    """,
    unsafe_allow_html=True
)


# Creamos dos columnas.
hero_column_1, hero_column_2 = (
    st.columns(2)
)


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
    """
    <div class="section-title">
        Cartas comunitarias
    </div>
    """,
    unsafe_allow_html=True
)


# None representa una posición sin carta.
BOARD_OPTIONS = [
    None
] + FULL_DECK


# Las tres cartas del flop aparecen juntas.
flop_column_1, flop_column_2, flop_column_3 = (
    st.columns(3)
)


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


# Turn y river aparecen juntos.
turn_column, river_column = (
    st.columns(2)
)


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

# Campo numérico con controles para aumentar
# o reducir el número de jugadores.
active_players = st.number_input(
    label=(
        "Jugadores activos, "
        "incluyéndote a ti"
    ),
    min_value=2,
    max_value=10,
    value=6,
    step=1,
    key="active_players"
)


# Selector del número de simulaciones.
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

calculate_column, reset_column = (
    st.columns(2)
)


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
# 16. CALCULAR Y MOSTRAR LAS PROBABILIDADES
# ============================================================

if calculate_button:

    try:

        # Recogemos nuestras dos cartas.
        hero_cards = [
            hero_card_1,
            hero_card_2
        ]

        # Recogemos las posiciones de la mesa.
        board_positions = [
            flop_card_1,
            flop_card_2,
            flop_card_3,
            turn_card,
            river_card
        ]

        # Comprobamos que las cartas se hayan
        # introducido en el orden correcto.
        empty_position_found = False

        for card in board_positions:

            if card is None:

                empty_position_found = True

            elif empty_position_found:

                raise ValueError(
                    "Añade las cartas comunitarias "
                    "en orden: primero las tres "
                    "cartas del flop, después el "
                    "turn y finalmente el river."
                )

        # Eliminamos las posiciones sin carta.
        board_cards = [
            card
            for card in board_positions
            if card is not None
        ]

        # Ejecutamos la simulación.
        with st.spinner(
            "Simulando partidas..."
        ):

            result = monte_carlo(
                hero_cards=hero_cards,
                board_cards=board_cards,
                num_players=active_players,
                simulations=simulations
            )

        # Convertimos nuestras cartas
        # al formato visual.
        hero_text = " ".join(
            card_visual_name(card)
            for card in hero_cards
        )

        # Convertimos las cartas comunitarias.
        if board_cards:

            board_text = " ".join(
                card_visual_name(card)
                for card in board_cards
            )

        else:

            board_text = "Antes del flop"

        # Mostramos un resumen compacto de la mano.
        st.markdown(
            f"""
            <div class="hand-summary">
                <div>
                    <strong>Tus cartas:</strong>
                    {hero_text}
                </div>

                <div>
                    <strong>Mesa:</strong>
                    {board_text}
                </div>

                <div>
                    <strong>Jugadores activos:</strong>
                    {active_players}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Título de resultados.
        st.markdown(
            """
            <div class="section-title">
                Probabilidades
            </div>
            """,
            unsafe_allow_html=True
        )

        # Creamos tres columnas para los resultados.
        win_column, tie_column, loss_column = (
            st.columns(3)
        )


        with win_column:

            st.metric(
                label="Victoria",
                value=(
                    f"{result['victoria']} %"
                )
            )


        with tie_column:

            st.metric(
                label="Empate",
                value=(
                    f"{result['empate']} %"
                )
            )


        with loss_column:

            st.metric(
                label="Derrota",
                value=(
                    f"{result['derrota']} %"
                )
            )


        # Formateamos el número de simulaciones.
        simulation_text = (
            f"{result['simulaciones']:,}"
            .replace(",", ".")
        )


        # Mostramos la cantidad de simulaciones utilizadas.
        st.caption(
            f"Resultado basado en "
            f"{simulation_text} simulaciones."
        )


    # Errores previsibles de los datos introducidos.
    except ValueError as error:

        st.error(
            str(error)
        )


    # Cualquier otro problema inesperado.
    except Exception as error:

        st.error(
            f"Se ha producido un error "
            f"inesperado: {error}"
        )


# ============================================================
# 17. INFORMACIÓN FINAL
# ============================================================

st.divider()


st.caption(
    "Los rivales se simulan con manos aleatorias "
    "entre todas las combinaciones legales disponibles."
)

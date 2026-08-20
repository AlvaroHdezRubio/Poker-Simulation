# ============================================================
# RAZA CHOPE POKAH
# Calculadora de probabilidades de Texas Hold'em
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
    page_title="Raza Chope Pokah",
    page_icon="🃏",
    layout="centered"
)


# ============================================================
# 2. CARGAR LA IMAGEN LATERAL
# ============================================================

def load_image_as_base64(image_path):
    """
    Convierte una imagen del repositorio en un texto Base64.

    Esto permite utilizar joker.png como imagen de fondo
    dentro de los estilos de la aplicación.
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


# Buscamos joker.png en el mismo lugar que app.py.
JOKER_IMAGE = load_image_as_base64("joker.png")


# ============================================================
# 3. ESTILOS VISUALES
# ============================================================

st.markdown(
    """
    <style>

    /* Fondo general verde tipo tapete */
    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #176b45 0%,
                #0d5638 35%,
                #073b29 75%,
                #052d20 100%
            );
        color: #f5f7f5;
    }

    /*
    Colocamos el contenido delante de la imagen lateral.
    */
    .block-container {
        position: relative;
        z-index: 2;
        max-width: 850px;
        padding-top: 0.7rem;
        padding-bottom: 1.2rem;
    }

    /* Título principal compacto */
    .app-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 850;
        line-height: 1.1;
        margin: 0 0 0.7rem 0;
        text-shadow:
            0 2px 3px rgba(0, 0, 0, 0.65),
            0 0 14px rgba(255, 183, 55, 0.22);
    }

    /* Títulos de sección compactos */
    .section-title {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 750;
        line-height: 1.2;
        margin-top: 0.75rem;
        margin-bottom: 0.25rem;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.55);
    }

    /* Reducimos espacios verticales */
    div[data-testid="stVerticalBlock"] {
        gap: 0.38rem;
    }

    /* Etiquetas de los controles */
    div[data-testid="stWidgetLabel"] p {
        color: #f4f8f5;
        font-size: 0.86rem;
        font-weight: 650;
    }

    /* Contenedor de los desplegables */
    div[data-baseweb="select"] > div {
        min-height: 2.55rem;
        background-color: rgba(247, 249, 248, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 9px;
    }

    /* Texto de los desplegables */
    div[data-baseweb="select"] span {
        color: #17231d;
    }

    /* Reducimos márgenes de los desplegables */
    div[data-testid="stSelectbox"] {
        margin-bottom: 0;
    }

    /* Deslizador */
    div[data-testid="stSlider"] p {
        color: #ffffff;
    }

    /* Botones */
    div[data-testid="stButton"] button {
        min-height: 2.55rem;
        border-radius: 9px;
        font-weight: 750;
    }

    /* Botón principal */
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
        background-color: rgba(3, 42, 27, 0.82);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.48);
    }

    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background-color: rgba(8, 76, 49, 0.95);
        color: #ffffff;
    }

    /* Tarjetas de probabilidades */
    div[data-testid="stMetric"] {
        background-color: rgba(3, 40, 26, 0.76);
        border: 1px solid rgba(255, 255, 255, 0.20);
        border-radius: 10px;
        padding: 0.55rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.20);
    }

    div[data-testid="stMetricLabel"] {
        color: #dceae1;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }

    /* Textos normales */
    .stMarkdown,
    [data-testid="stCaptionContainer"] {
        color: #edf5f0;
    }

    /* Línea divisoria */
    hr {
        border-color: rgba(255, 255, 255, 0.20);
        margin-top: 0.8rem;
        margin-bottom: 0.5rem;
    }

    /* Imagen fija que sale desde el lateral derecho */
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

        opacity: 0.42;

        /*
        La máscara elimina progresivamente la parte izquierda,
        integrando la imagen con el fondo verde.
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

    /* Ajustes específicos para móvil */
    @media (max-width: 640px) {

        .block-container {
            padding-top: 0.35rem;
            padding-left: 0.60rem;
            padding-right: 0.60rem;
            padding-bottom: 0.8rem;
        }

        .app-title {
            font-size: 1.5rem;
            margin-bottom: 0.35rem;
        }

        .section-title {
            font-size: 1.02rem;
            margin-top: 0.5rem;
            margin-bottom: 0.15rem;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.22rem;
        }

        div[data-testid="stWidgetLabel"] p {
            font-size: 0.75rem;
        }

        div[data-baseweb="select"] > div {
            min-height: 2.35rem;
            border-radius: 8px;
        }

        div[data-testid="stSlider"] {
            margin-top: -0.15rem;
            margin-bottom: -0.15rem;
        }

        div[data-testid="stButton"] button {
            min-height: 2.4rem;
            font-size: 0.82rem;
        }

        /*
        En teléfono mostramos una parte más pequeña del Joker
        y bajamos mucho su intensidad para que no moleste.
        */
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

        /*
        Las métricas ocupan menos espacio en móvil.
        */
        div[data-testid="stMetric"] {
            padding: 0.4rem;
        }

        div[data-testid="stMetricLabel"] p {
            font-size: 0.72rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.15rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Añadimos la imagen solamente si joker.png existe.
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
# 4. BARAJA Y EVALUADOR
# ============================================================

RANKS = "23456789TJQKA"
SUITS = "shdc"

EVALUATOR = Evaluator()


def create_deck():
    """
    Crea las 52 cartas de la baraja.
    """

    return [
        rank + suit
        for rank in RANKS
        for suit in SUITS
    ]


FULL_DECK = create_deck()


# ============================================================
# 5. NOMBRES VISUALES
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
# 6. VALIDAR LOS DATOS
# ============================================================

def validate_inputs(hero_cards, board_cards, num_players):
    """
    Comprueba cartas repetidas, mesa y jugadores.
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
# 7. EVALUAR UNA MANO
# ============================================================

def hand_score(player_cards, board_cards):
    """
    Evalúa una mano mediante Treys.

    En Treys, una puntuación menor representa una mano mejor.
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
# 8. SIMULACIÓN MONTE CARLO
# ============================================================

def monte_carlo(
    hero_cards,
    board_cards,
    num_players,
    simulations=10000
):
    """
    Simula partidas completando la mesa y repartiendo
    manos aleatorias a todos los rivales activos.
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

        # Elegimos todas las cartas necesarias sin repetir.
        simulated_cards = random.sample(
            available_cards,
            cards_needed
        )

        position = 0
        completed_board = board_cards.copy()

        # Completamos turn y river si todavía no han salido.
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
# 9. REINICIAR LA MANO
# ============================================================

def reset_hand():
    """
    Vuelve a una mano vacía.
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
# 10. TÍTULO
# ============================================================

st.markdown(
    '<div class="app-title">🃏 Raza Chope Pokah</div>',
    unsafe_allow_html=True
)


# ============================================================
# 11. TUS CARTAS
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
# 12. CARTAS COMUNITARIAS
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
# 13. JUGADORES Y SIMULACIONES
# ============================================================

active_players = st.slider(
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
# 14. BOTONES
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
# 15. CALCULAR PROBABILIDADES
# ================================
# ============================================================
# 15. CALCULAR PROBABILIDADES
# ============================================================

# Este bloque solamente se ejecuta cuando pulsamos
# el botón "Calcular".
if calculate_button:

    try:

        # Guardamos nuestras dos cartas en una lista.
        hero_cards = [
            hero_card_1,
            hero_card_2
        ]

        # Guardamos todas las posiciones posibles de la mesa.
        #
        # Algunas posiciones pueden contener None,
        # que significa "Sin carta".
        board_positions = [
            flop_card_1,
            flop_card_2,
            flop_card_3,
            turn_card,
            river_card
        ]

        # ----------------------------------------------------
        # COMPROBAR EL ORDEN DE LAS CARTAS COMUNITARIAS
        # ----------------------------------------------------

        # Utilizamos esta variable para recordar si hemos
        # encontrado una posición vacía.
        empty_position_found = False

        # Recorremos las cinco posiciones en orden:
        # flop 1, flop 2, flop 3, turn y river.
        for card in board_positions:

            # Si la posición está vacía, guardamos esa información.
            if card is None:

                empty_position_found = True

            # Si encontramos una carta después de una posición
            # vacía, las cartas no se han añadido en orden.
            elif empty_position_found:

                raise ValueError(
                    "Añade las cartas comunitarias en orden: "
                    "primero las tres cartas del flop, "
                    "después el turn y finalmente el river."
                )

        # Eliminamos las posiciones que contienen None.
        #
        # El resultado será:
        #
        # [] antes del flop.
        # [carta, carta, carta] en el flop.
        # [carta, carta, carta, carta] en el turn.
        # [carta, carta, carta, carta, carta] en el river.
        board_cards = [
            card
            for card in board_positions
            if card is not None
        ]

        # ----------------------------------------------------
        # EJECUTAR LA SIMULACIÓN
        # ----------------------------------------------------

        # Mientras se realizan los cálculos, Streamlit
        # mostrará un indicador visual.
        with st.spinner(
            "Simulando partidas..."
        ):

            result = monte_carlo(
                hero_cards=hero_cards,
                board_cards=board_cards,
                num_players=active_players,
                simulations=simulations
            )

        # ----------------------------------------------------
        # PREPARAR LOS TEXTOS VISUALES
        # ----------------------------------------------------

        # Convertimos nuestras cartas a formato visual.
        #
        # Por ejemplo:
        # ["Kh", "Ks"] se convierte en "K♥ K♠".
        hero_text = " ".join(
            card_visual_name(card)
            for card in hero_cards
        )

        # Si ya hay cartas comunitarias, las convertimos
        # también a su formato visual.
        if board_cards:

            board_text = " ".join(
                card_visual_name(card)
                for card in board_cards
            )

        # Si todavía no hay cartas comunitarias,
        # indicamos que estamos antes del flop.
        else:

            board_text = "Antes del flop"

        # ----------------------------------------------------
        # MOSTRAR LA SITUACIÓN ANALIZADA
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="hand-summary">
                <div>
                    <strong>Tus cartas:</strong> {hero_text}
                </div>
                <div>
                    <strong>Mesa:</strong> {board_text}
                </div>
                <div>
                    <strong>Jugadores activos:</strong>
                    {active_players}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Título compacto de probabilidades.
        st.markdown(
            '<div class="section-title">Probabilidades</div>',
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # MOSTRAR LOS TRES PORCENTAJES
        # ----------------------------------------------------

        # Creamos tres columnas:
        # victoria, empate y derrota.
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

        # ----------------------------------------------------
        # MOSTRAR BARRAS DE PROGRESO
        # ----------------------------------------------------

        st.markdown(
            '<div class="probability-label">Victoria</div>',
            unsafe_allow_html=True
        )

        # st.progress necesita un valor entre 0 y 1.
        # Por eso dividimos el porcentaje entre 100.
        st.progress(
            result["victoria"] / 100
        )

        st.markdown(
            '<div class="probability-label">Empate</div>',
            unsafe_allow_html=True
        )

        st.progress(
            result["empate"] / 100
        )

        st.markdown(
            '<div class="probability-label">Derrota</div>',
            unsafe_allow_html=True
        )

        st.progress(
            result["derrota"] / 100
        )

        # Formateamos el número de simulaciones.
        #
        # Por ejemplo:
        # 25000 se mostrará como 25.000.
        simulation_text = (
            f"{result['simulaciones']:,}"
            .replace(",", ".")
        )

        st.caption(
            f"Resultado basado en "
            f"{simulation_text} simulaciones."
        )

    # --------------------------------------------------------
    # ERRORES DE LOS DATOS INTRODUCIDOS
    # --------------------------------------------------------

    except ValueError as error:

        # Aquí aparecerán errores como:
        #
        # Carta repetida.
        # Flop incompleto.
        # Turn introducido antes del flop.
        st.error(
            str(error)
        )

    # --------------------------------------------------------
    # ERRORES INESPERADOS
    # --------------------------------------------------------

    except Exception as error:

        st.error(
            f"Se ha producido un error inesperado: {error}"
        )


# ============================================================
# 16. INFORMACIÓN FINAL
# ============================================================

st.divider()

st.caption(
    "Los rivales se simulan con manos aleatorias "
    "entre todas las combinaciones legales disponibles."
)

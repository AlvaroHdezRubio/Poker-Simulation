# ============================================================
# CALCULADORA DE PROBABILIDADES DE PÓKER
# Aplicación creada con Streamlit
# ============================================================

# random se utiliza para mezclar las cartas.
import random

# Streamlit crea la interfaz visual.
import streamlit as st

# Treys evalúa las manos de Texas Hold'em.
from treys import Card, Evaluator


# ============================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ============================================================

# Esta instrucción configura la pestaña del navegador.
# Debe aparecer antes de cualquier otro elemento de Streamlit.
st.set_page_config(
    page_title="Calculadora de póker",
    page_icon="♠️",
    layout="centered"
)


# ============================================================
# 2. VALORES Y PALOS DE LA BARAJA
# ============================================================

# Valores admitidos por Treys.
#
# T representa el 10.
# J representa la jota.
# Q representa la reina.
# K representa el rey.
# A representa el as.
RANKS = "23456789TJQKA"


# Palos admitidos por Treys.
#
# s = picas
# h = corazones
# d = diamantes
# c = tréboles
SUITS = "shdc"


# Creamos el evaluador de manos una única vez.
EVALUATOR = Evaluator()


# ============================================================
# 3. CREAR LA BARAJA
# ============================================================

def create_deck():
    """
    Crea una baraja completa de 52 cartas.

    Ejemplos:
        Ah = as de corazones
        Ks = rey de picas
        Td = diez de diamantes
        7c = siete de tréboles
    """

    deck = []

    # Recorremos todos los valores.
    for rank in RANKS:

        # Recorremos los cuatro palos.
        for suit in SUITS:

            # Unimos valor y palo.
            deck.append(rank + suit)

    return deck


# Creamos la baraja completa.
FULL_DECK = create_deck()


# ============================================================
# 4. NOMBRES VISUALES DE LAS CARTAS
# ============================================================

# Traducción de los palos internos a símbolos.
SUIT_SYMBOLS = {
    "s": "♠",
    "h": "♥",
    "d": "♦",
    "c": "♣"
}


# Traducción especial del 10.
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


def card_visual_name(card):
    """
    Convierte el formato interno en un formato visual.

    Ejemplos:
        Ah se muestra como A♥
        Ks se muestra como K♠
        Td se muestra como 10♦
    """

    # None representa una posición sin carta.
    if card is None:
        return "Sin carta"

    rank = card[0]
    suit = card[1]

    return R[1ANK_NAMESank] + SUIT_SYMBOLS[suit]


# ============================================================
# 5. VALIDAR LOS DATOS
# ============================================================

def validate_inputs(hero_cards, board_cards, num_players):
    """
    Comprueba que las cartas y los jugadores sean válidos.
    """

    # Debemos tener exactamente dos cartas propias.
    if len(hero_cards) != 2:
        raise ValueError(
            "Debes seleccionar exactamente dos cartas propias."
        )

    # La mesa solamente puede tener:
    #
    # 0 cartas antes del flop.
    # 3 cartas en el flop.
    # 4 cartas después del turn.
    # 5 cartas después del river.
    if len(board_cards) not in (0, 3, 4, 5):
        raise ValueError(
            "Debes introducir las tres cartas del flop juntas."
        )

    # Comprobamos el número de jugadores activos.
    if num_players < 2 or num_players > 10:
        raise ValueError(
            "Debe haber entre 2 y 10 jugadores activos."
        )

    # Juntamos todas las cartas conocidas.
    all_known_cards = hero_cards + board_cards

    # Comprobamos que ninguna carta esté repetida.
    if len(all_known_cards) != len(set(all_known_cards)):
        raise ValueError(
            "Hay cartas repetidas. "
            "Una misma carta no puede aparecer dos veces."
        )

    # Comprobamos que todas las cartas pertenezcan a la baraja.
    for card in all_known_cards:

        if card not in FULL_DECK:
            raise ValueError(
                f"La carta {card} no es válida."
            )

    return hero_cards, board_cards


# ============================================================
# 6. EVALUAR UNA MANO
# ============================================================

def hand_score(player_cards, board_cards):
    """
    Calcula la puntuación de una mano con Treys.

    En Treys:
        una puntuación más baja representa una mano mejor.
    """

    # Convertimos las cartas del jugador al formato Treys.
    player_treys = [
        Card.new(card)
        for card in player_cards
    ]

    # Convertimos las cartas de la mesa.
    board_treys = [
        Card.new(card)
        for card in board_cards
    ]

    # Evaluamos las siete cartas disponibles:
    # dos del jugador y cinco de la mesa.
    return EVALUATOR.evaluate(
        board_treys,
        player_treys
    )


# ============================================================
# 7. SIMULACIÓN MONTE CARLO
# ============================================================

def monte_carlo(
    hero_cards,
    board_cards,
    num_players,
    simulations=10000
):
    """
    Simula miles de partidas posibles.

    En cada simulación:

        1. Elimina las cartas conocidas.
        2. Completa las cartas que faltan en la mesa.
        3. Reparte dos cartas a cada rival.
        4. Evalúa todas las manos.
        5. Cuenta victoria, empate o derrota.
    """

    # Validamos los datos antes de comenzar.
    hero_cards, board_cards = validate_inputs(
        hero_cards,
        board_cards,
        num_players
    )

    # Cartas conocidas que no pueden volver a repartirse.
    known_cards = set(hero_cards + board_cards)

    # Creamos una baraja base sin las cartas conocidas.
    available_cards = [
        card
        for card in FULL_DECK
        if card not in known_cards
    ]

    # Contadores de resultados.
    wins = 0
    ties = 0
    losses = 0

    # Calculamos cuántas cartas faltan en la mesa.
    missing_board_cards = 5 - len(board_cards)

    # Calculamos el número de rivales.
    number_of_villains = num_players - 1

    # Calculamos cuántas cartas necesitamos en cada simulación.
    cards_needed = (
        missing_board_cards
        + number_of_villains * 2
    )

    # Repetimos la simulación el número de veces indicado.
    for _ in range(simulations):

        # Elegimos cartas aleatorias sin repetir.
        simulated_cards = random.sample(
            available_cards,
            cards_needed
        )

        # Posición actual dentro de las cartas simuladas.
        position = 0

        # Copiamos la mesa visible.
        completed_board = board_cards.copy()

        # Añadimos las cartas comunitarias que faltan.
        for _ in range(missing_board_cards):

            completed_board.append(
                simulated_cards[position]
            )

            position += 1

        # Guardamos las manos de los rivales.
        villains = []

        # Repartimos dos cartas a cada rival.
        for _ in range(number_of_villains):

            villain_hand = [
                simulated_cards[position],
                simulated_cards[position + 1]
            ]

            villains.append(villain_hand)

            position += 2

        # Evaluamos nuestra mano.
        hero_score = hand_score(
            hero_cards,
            completed_board
        )

        # Lista que contendrá todas las puntuaciones.
        all_scores = [hero_score]

        # Evaluamos a cada rival.
        for villain_hand in villains:

            villain_score = hand_score(
                villain_hand,
                completed_board
            )

            all_scores.append(villain_score)

        # La puntuación más baja es la mejor.
        best_score = min(all_scores)

        # Si nuestra puntuación no es la mejor, perdemos.
        if hero_score != best_score:

            losses += 1

        else:

            # Contamos cuántos jugadores tienen la mejor mano.
            number_of_winners = all_scores.count(best_score)

            # Si solo somos nosotros, ganamos.
            if number_of_winners == 1:

                wins += 1

            # Si hay más jugadores con la misma mano, empatamos.
            else:

                ties += 1

    # Convertimos los contadores en porcentajes.
    win_percentage = wins / simulations * 100
    tie_percentage = ties / simulations * 100
    loss_percentage = losses / simulations * 100

    return {
        "victoria": round(win_percentage, 2),
        "empate": round(tie_percentage, 2),
        "derrota": round(loss_percentage, 2),
        "simulaciones": simulations,
        "jugadores": num_players,
        "rivales": number_of_villains
    }


# ============================================================
# 8. FUNCIÓN PARA REINICIAR LA MANO
# ============================================================

def reset_hand():
    """
    Restaura las cartas y los jugadores a sus valores iniciales.
    """

    # Restauramos nuestras cartas.
    st.session_state["hero_card_1"] = "Kh"
    st.session_state["hero_card_2"] = "Ks"

    # Vaciamos las cartas comunitarias.
    st.session_state["flop_card_1"] = None
    st.session_state["flop_card_2"] = None
    st.session_state["flop_card_3"] = None
    st.session_state["turn_card"] = None
    st.session_state["river_card"] = None

    # Restauramos el número de jugadores.
    st.session_state["active_players"] = 6

    # Restauramos las simulaciones.
    st.session_state["simulations"] = 25000


# ============================================================
# 9. TÍTULO DE LA APLICACIÓN
# ============================================================

st.title("♠️ Calculadora de póker")

st.caption(
    "Texas Hold'em · Simulación Monte Carlo"
)

st.write(
    "Selecciona tus cartas, añade las cartas comunitarias "
    "que hayan salido y especifica cuántos jugadores "
    "continúan activos."
)


# ============================================================
# 10. SELECTORES DE NUESTRAS CARTAS
# ============================================================

st.subheader("Tus cartas")

# Creamos dos columnas para mostrar las cartas juntas.
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
# 11. SELECTORES DE LAS CARTAS COMUNITARIAS
# ============================================================

st.subheader("Cartas comunitarias")

# Añadimos None para permitir posiciones sin carta.
BOARD_OPTIONS = [None] + FULL_DECK


# Las tres cartas del flop aparecen en tres columnas.
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


# Turn y river aparecen juntos.
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
# 12. CONFIGURACIÓN DE LA SIMULACIÓN
# ============================================================

st.subheader("Configuración")

active_players = st.slider(
    label="Jugadores activos, incluyéndote a ti",
    min_value=2,
    max_value=10,
    value=6,
    step=1,
    key="active_players"
)


simulations = st.selectbox(
    label="Número de simulaciones",
    options=[
        10000,
        25000,
        50000,
        100000
    ],
    index=1,
    format_func=lambda value: f"{value:,}".replace(",", "."),
    key="simulations"
)


# ============================================================
# 13. BOTONES
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
        on_click=reset_hand,
        use_container_width=True
    )


# ============================================================
# 14. EJECUTAR EL CÁLCULO
# ============================================================

if calculate_button:

    try:

        # Recogemos nuestras cartas.
        hero_cards = [
            hero_card_1,
            hero_card_2
        ]

        # Recogemos las cinco posiciones de la mesa.
        board_positions = [
            flop_card_1,
            flop_card_2,
            flop_card_3,
            turn_card,
            river_card
        ]

        # Comprobamos que no haya cartas después
        # de una posición vacía.
        empty_position_found = False

        for card in board_positions:

            if card is None:
                empty_position_found = True

            elif empty_position_found:
                raise ValueError(
                    "Las cartas comunitarias deben añadirse "
                    "en orden: flop, turn y river."
                )

        # Eliminamos las posiciones sin carta.
        board_cards = [
            card
            for card in board_positions
            if card is not None
        ]

        # Mostramos un indicador mientras se calcula.
        with st.spinner(
            "Simulando posibles partidas..."
        ):

            result = monte_carlo(
                hero_cards=hero_cards,
                board_cards=board_cards,
                num_players=active_players,
                simulations=simulations
            )

        # Mostramos un mensaje de finalización.
        st.success(
            "Simulación completada correctamente."
        )

        # Mostramos la situación analizada.
        st.subheader("Situación analizada")

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

        st.write("**Tus cartas:**", hero_text)
        st.write("**Mesa:**", board_text)
        st.write("**Jugadores activos:**", active_players)
        st.write("**Rivales activos:**", active_players - 1)

        # Mostramos los resultados en tres columnas.
        st.subheader("Probabilidades")

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

        # Añadimos barras visuales.
        st.write("**Victoria**")
        st.progress(
            result["victoria"] / 100
        )

        st.write("**Empate**")
        st.progress(
            result["empate"] / 100
        )

        st.write("**Derrota**")
        st.progress(
            result["derrota"] / 100
        )

        # Información de la simulación.
        st.caption(
            f"Resultado basado en "
            f"{result['simulaciones']:,} simulaciones."
            .replace(",", ".")
        )

    except ValueError as error:

        # Mostramos errores de cartas repetidas,
        # flop incompleto u orden incorrecto.
        st.error(str(error))

    except Exception as error:

        # Mostramos otros errores inesperados.
        st.error(
            f"Se ha producido un error inesperado: {error}"
        )


# ============================================================
# 15. INFORMACIÓN FINAL
# ============================================================

st.divider()

st.caption(
    "Los rivales se simulan con manos aleatorias entre "
    "todas las combinaciones legales disponibles."
)

import base64
import random
from pathlib import Path

import streamlit as st
from treys import Card, Evaluator

st.set_page_config(page_title="Poker Lab by Álvaro Hdez", page_icon="♠️", layout="centered")


def image_b64(path):
    p = Path(path)
    return base64.b64encode(p.read_bytes()).decode("utf-8") if p.exists() else None


JOKER_IMAGE = image_b64("joker.png")

st.markdown(r"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"] {display:none!important}
header[data-testid="stHeader"] {height:0!important;min-height:0!important}
.stAppViewContainer {padding-top:0!important}
.stApp {background:radial-gradient(circle at top left,#176b45 0%,#0d5638 35%,#073b29 75%,#052d20 100%);color:white}
.block-container {position:relative;z-index:5;max-width:920px;padding-top:.6rem!important;padding-bottom:1rem!important}
.brand-header {margin:0 0 .8rem 0;position:relative;z-index:20}
.brand-main {display:flex;align-items:center;gap:.4rem;font-size:1.75rem;font-weight:900;line-height:1.05;background:linear-gradient(180deg,#fff2a8 0%,#f2c24f 42%,#d99a16 100%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 2px 4px rgba(0,0,0,.72),0 0 16px rgba(242,194,79,.22)}
.brand-symbol {color:#f2c24f;-webkit-text-fill-color:#f2c24f}.brand-signature {margin:.42rem 0 0 2rem;color:rgba(255,255,255,.88);font-size:.66rem;font-weight:700;line-height:1.3;letter-spacing:.13rem}
div[data-testid="stVerticalBlockBorderWrapper"] {background:linear-gradient(145deg,rgba(2,31,21,.86),rgba(4,52,34,.72));border:1px solid rgba(229,169,35,.46)!important;border-radius:14px!important;box-shadow:0 10px 28px rgba(0,0,0,.28)}
.section-title {color:white!important;font-size:.9rem;font-weight:800;letter-spacing:.05rem;text-transform:uppercase;margin:.5rem 0 .3rem;text-shadow:0 1px 3px rgba(0,0,0,.85)}
.card-position-label {color:white!important;font-size:.7rem;font-weight:750;line-height:1.15;text-align:center;margin:0;padding:0 0 .28rem;text-shadow:0 1px 3px #000}
/* Naipe principal */
div[data-testid="stPopover"]>button {position:relative!important;width:100%!important;min-height:5.4rem!important;padding:.2rem!important;background:linear-gradient(145deg,#fffef8,#f5f1e5 67%,#ddd6c7)!important;border:2px solid rgba(255,255,255,.94)!important;border-radius:9px!important;box-shadow:0 5px 10px rgba(0,0,0,.4)!important;overflow:hidden!important}
div[data-testid="stPopover"]>button:after {content:"";position:absolute;inset:5px;border:1px solid rgba(25,35,28,.17);border-radius:6px;pointer-events:none}
div[data-testid="stPopover"]>button [data-testid="stMarkdownContainer"] {position:relative!important;z-index:5!important;display:flex!important;align-items:center!important;justify-content:center!important;width:100%!important;height:100%!important}
div[data-testid="stPopover"]>button [data-testid="stMarkdownContainer"] p {font-size:1.5rem!important;font-weight:850!important;line-height:1!important;margin:0!important}
/* Selector: botones compactos */
div[data-testid="stPopoverBody"] button {min-height:2.25rem!important;padding:.05rem!important;background:#f8f6ee!important;border:1px solid rgba(40,45,40,.25)!important;border-radius:6px!important;color:#111!important}
div[data-testid="stPopoverBody"] button p {color:#111!important;font-size:.76rem!important;font-weight:800!important;margin:0!important}
div[data-testid="stPopoverBody"] button:disabled {background:#aeb4b0!important;opacity:.4!important}
.picker-title {color:white!important;font-size:.9rem;font-weight:800;margin-bottom:.3rem}
[data-testid="stWidgetLabel"] p {color:white!important;font-size:.78rem!important;font-weight:700!important}
[data-testid="stNumberInput"] input {min-height:2.4rem;background:#f7f8f7!important;color:#17231d!important;font-weight:800;text-align:center}
[data-testid="stNumberInput"] button {min-height:2.4rem;color:white!important;background:#073b29!important}
div[data-baseweb="select"]>div {min-height:2.4rem;background:#f7f8f7;border-radius:8px} div[data-baseweb="select"] span {color:#17231d!important;font-weight:650}
div[data-testid="stButton"] button {min-height:2.4rem;border-radius:8px;font-weight:750}
div[data-testid="stButton"] button[kind="primary"] {background:#e5a923;color:#172016;border:1px solid #ffd46d}
.hand-summary {margin-top:.6rem;padding:.5rem .65rem;background:rgba(2,28,19,.86);border:1px solid rgba(229,169,35,.45);border-radius:10px;color:white;font-size:.78rem;line-height:1.5}
.results-grid {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.35rem;margin-top:.3rem}.result-card {padding:.55rem .15rem;background:rgba(2,26,18,.92);border-radius:9px;text-align:center}.result-win{border:1px solid rgba(85,190,77,.6)}.result-tie{border:1px solid rgba(229,169,35,.65)}.result-loss{border:1px solid rgba(220,62,55,.65)}.result-label{color:rgba(255,255,255,.72);font-size:.58rem;font-weight:750;text-transform:uppercase}.result-value{margin-top:.14rem;font-size:1.15rem;font-weight:850}.win-value{color:#61c854}.tie-value{color:#e5a923}.loss-value{color:#ed514a}
[data-testid="stCaptionContainer"] p {color:rgba(255,255,255,.74)!important}.joker-background {position:fixed;z-index:0;pointer-events:none;right:-35px;bottom:-10px;width:430px;height:96vh;background-position:right bottom;background-repeat:no-repeat;background-size:contain;opacity:.46;mix-blend-mode:multiply;-webkit-mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,.08) 16%,rgba(0,0,0,.55) 38%,black 64%),linear-gradient(to top,transparent 0%,black 10%);-webkit-mask-composite:source-in;mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,.08) 16%,rgba(0,0,0,.55) 38%,black 64%),linear-gradient(to top,transparent 0%,black 10%);mask-composite:intersect;filter:saturate(.82) contrast(1.12) brightness(.72)}
@media(max-width:640px){
.block-container{max-width:100%!important;padding:.28rem .32rem .7rem!important}.brand-header{margin-bottom:.56rem}.brand-main{font-size:1.22rem}.brand-signature{margin:.32rem 0 0 1.5rem;font-size:.46rem;line-height:1.35;letter-spacing:.085rem}.section-title{font-size:.66rem;margin:.32rem 0 .2rem}.card-position-label{font-size:.49rem;padding-bottom:.16rem}
div[data-testid="stPopover"]>button{min-height:3.6rem!important;border-radius:6px!important}div[data-testid="stPopover"]>button [data-testid="stMarkdownContainer"] p{font-size:.88rem!important}
div[data-testid="stPopoverBody"] button{min-height:2.1rem!important}div[data-testid="stPopoverBody"] button p{font-size:.68rem!important}
[data-testid="stWidgetLabel"] p{font-size:.64rem!important}[data-testid="stNumberInput"] input,[data-testid="stNumberInput"] button,div[data-baseweb="select"]>div{min-height:2.25rem!important}div[data-testid="stButton"] button{min-height:2.25rem;font-size:.74rem}.hand-summary{padding:.4rem .48rem;font-size:.68rem}.results-grid{gap:.2rem}.result-card{padding:.42rem .06rem}.result-label{font-size:.47rem}.result-value{font-size:.9rem}.joker-background{width:155px;height:50vh;right:-35px;bottom:-5px;opacity:.16;mix-blend-mode:multiply;-webkit-mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,.12) 30%,black 72%),linear-gradient(to top,transparent 0%,black 14%);-webkit-mask-composite:source-in;mask-image:linear-gradient(to right,transparent 0%,rgba(0,0,0,.12) 30%,black 72%),linear-gradient(to top,transparent 0%,black 14%);mask-composite:intersect;filter:saturate(.75) contrast(1.1) brightness(.72)}
}

/* Mantener filas compactas en móvil */
[data-testid="stHorizontalBlock"] {flex-wrap:nowrap!important;gap:.45rem!important}
@media(max-width:640px){
[data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;gap:.22rem!important}

/* Las cartas principales siempre conservan fondo blanco en móvil */
div[data-testid="stPopover"] > button {
    background: linear-gradient(145deg,#fffef8 0%,#f5f1e5 67%,#ddd6c7 100%) !important;
    color:#111111 !important;
}

/* Las opciones del selector son blancas y no se desplazan horizontalmente */
div[data-testid="stPopoverBody"] [data-testid="stHorizontalBlock"]{
    flex-wrap:wrap!important;
    gap:.10rem!important;
    overflow-x:hidden!important;
}

div[data-testid="stPopoverBody"] button{
    background:#ffffff!important;
    color:#111111!important;
    min-width:0!important;
    width:100%!important;
}

div[data-testid="stPopoverBody"] button p{
    color:#111111!important;
}
}


/* CORRECCION DEFINITIVA MOVIL */
@media screen and (max-width: 640px) {
  /* Disparadores de Carta 1, Carta 2, flop, turn y river */
  [class*="st-key-picker_"] > div > button,
  [class*="st-key-picker_"] button[aria-haspopup="dialog"],
  div[data-testid="stPopover"] > button {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #d6d6d6 !important;
    opacity: 1 !important;
  }
  [class*="st-key-picker_"] button[aria-haspopup="dialog"] p,
  [class*="st-key-picker_"] button[aria-haspopup="dialog"] span,
  div[data-testid="stPopover"] > button p,
  div[data-testid="stPopover"] > button span {
    opacity: 1 !important;
  }

  /* El popover nunca debe tener desplazamiento horizontal */
  div[data-testid="stPopoverBody"],
  div[data-testid="stPopoverBody"] > div {
    width: min(92vw, 420px) !important;
    max-width: min(92vw, 420px) !important;
    overflow-x: hidden !important;
    box-sizing: border-box !important;
  }

  /* Cada fila mantiene exactamente tres columnas */
  div[data-testid="stPopoverBody"] div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    width: 100% !important;
    max-width: 100% !important;
    gap: 0.35rem !important;
    overflow: hidden !important;
  }

  div[data-testid="stPopoverBody"] div[data-testid="stColumn"] {
    display: block !important;
    flex: 1 1 0 !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: none !important;
  }

  div[data-testid="stPopoverBody"] div[data-testid="stColumn"] button {
    display: flex !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    min-height: 2.15rem !important;
    padding: 0.10rem 0.05rem !important;
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #d5d5d5 !important;
    border-radius: 6px !important;
    box-sizing: border-box !important;
  }

  div[data-testid="stPopoverBody"] div[data-testid="stColumn"] button p,
  div[data-testid="stPopoverBody"] div[data-testid="stColumn"] button span {
    font-size: 0.72rem !important;
    line-height: 1 !important;
    white-space: nowrap !important;
  }
}


/* ==========================================================
   AJUSTE FINAL PARA POPOVERS EN MOVIL
   ========================================================== */
@media screen and (max-width: 640px) {

    /* Pop-up de ayuda: ancho contenido y texto siempre dentro */
    div[data-testid="stPopoverBody"]:has(h3) {
        width: calc(100vw - 34px) !important;
        max-width: 330px !important;
        min-width: 0 !important;
        padding: 0.85rem !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stPopoverBody"]:has(h3) * {
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stPopoverBody"]:has(h3) p,
    div[data-testid="stPopoverBody"]:has(h3) li,
    div[data-testid="stPopoverBody"]:has(h3) div {
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    div[data-testid="stPopoverBody"]:has(h3) h3 {
        font-size: 1.15rem !important;
        line-height: 1.25 !important;
        margin-bottom: 0.65rem !important;
    }

    div[data-testid="stPopoverBody"]:has(h3) p,
    div[data-testid="stPopoverBody"]:has(h3) li {
        font-size: 0.78rem !important;
        line-height: 1.4 !important;
    }

    div[data-testid="stPopoverBody"]:has(h3) ol,
    div[data-testid="stPopoverBody"]:has(h3) ul {
        padding-left: 1.15rem !important;
        margin-right: 0 !important;
    }

    /* Selector de cartas: algo mas estrecho que la pantalla */
    div[data-testid="stPopoverBody"]:has(.picker-title) {
        width: calc(100vw - 38px) !important;
        max-width: 338px !important;
        min-width: 0 !important;
        padding: 0.70rem !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stPopoverBody"]:has(.picker-title) > div,
    div[data-testid="stPopoverBody"]:has(.picker-title) [data-testid="stVerticalBlock"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }

    /* Exactamente tres cartas por fila, sin scroll lateral */
    div[data-testid="stPopoverBody"]:has(.picker-title)
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        gap: 0.28rem !important;
        overflow: hidden !important;
    }

    div[data-testid="stPopoverBody"]:has(.picker-title)
    div[data-testid="stColumn"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        flex: none !important;
        padding: 0 !important;
    }

    div[data-testid="stPopoverBody"]:has(.picker-title)
    div[data-testid="stColumn"] button {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        min-height: 2.05rem !important;
        padding: 0.08rem 0.02rem !important;
        background: #ffffff !important;
        background-color: #ffffff !important;
        color: #111111 !important;
        border: 1px solid #d7d7d7 !important;
        border-radius: 6px !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stPopoverBody"]:has(.picker-title)
    div[data-testid="stColumn"] button p,
    div[data-testid="stPopoverBody"]:has(.picker-title)
    div[data-testid="stColumn"] button span {
        font-size: 0.68rem !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        margin: 0 !important;
    }

    /* Sin carta ocupa el ancho disponible, sin salirse */
    div[data-testid="stPopoverBody"]:has(.picker-title)
    .st-key-clear_flop_card_1 button,
    div[data-testid="stPopoverBody"]:has(.picker-title)
    .st-key-clear_flop_card_2 button,
    div[data-testid="stPopoverBody"]:has(.picker-title)
    .st-key-clear_flop_card_3 button,
    div[data-testid="stPopoverBody"]:has(.picker-title)
    .st-key-clear_turn_card button,
    div[data-testid="stPopoverBody"]:has(.picker-title)
    .st-key-clear_river_card button {
        width: 100% !important;
        max-width: 100% !important;
    }
}

</style>
""", unsafe_allow_html=True)

# Estilo exclusivo del botón de ayuda.
# Está separado del CSS de las cartas para no modificar sus anchos.
st.markdown(
    r"""
    <style>
    .st-key-help_popover {
        position: relative !important;
        z-index: 40 !important;
        display: block !important;
        width: fit-content !important;
        margin: 0 0 0.50rem 0 !important;
    }

    .st-key-help_popover button[aria-haspopup="dialog"] {
        display: inline-flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        width: auto !important;
        min-width: 0 !important;
        min-height: 2rem !important;
        padding: 0.22rem 0.65rem !important;
        background: rgba(3, 42, 27, 0.94) !important;
        color: #ffffff !important;
        border: 1px solid rgba(242, 194, 79, 0.78) !important;
        border-radius: 999px !important;
        box-shadow: none !important;
    }

    .st-key-help_popover button[aria-haspopup="dialog"] p,
    .st-key-help_popover button[aria-haspopup="dialog"] span {
        color: #ffffff !important;
        font-size: 0.75rem !important;
        font-weight: 750 !important;
        line-height: 1 !important;
        margin: 0 !important;
    }

    @media screen and (max-width: 640px) {
        .st-key-help_popover {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            margin-bottom: 0.45rem !important;
        }

        .st-key-help_popover button[aria-haspopup="dialog"] {
            display: inline-flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            min-height: 1.85rem !important;
            padding: 0.18rem 0.55rem !important;
        }

        .st-key-help_popover button[aria-haspopup="dialog"] p,
        .st-key-help_popover button[aria-haspopup="dialog"] span {
            font-size: 0.66rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

if JOKER_IMAGE:
    st.markdown(f'<div class="joker-background" style="background-image:url(data:image/png;base64,{JOKER_IMAGE})"></div>', unsafe_allow_html=True)

RANKS = "23456789TJQKA"
DISPLAY_RANKS = "AKQJT98765432"
SUITS = "shdc"
EVALUATOR = Evaluator()
FULL_DECK = [rank + suit for suit in SUITS for rank in DISPLAY_RANKS]
RANK_NAMES = {**{str(i): str(i) for i in range(2, 10)}, "T":"10", "J":"J", "Q":"Q", "K":"K", "A":"A"}
SUIT_SYMBOLS = {"s":"♠", "h":"♥", "d":"♦", "c":"♣"}


def card_visual_name(card):
    return "＋" if card is None else f"{RANK_NAMES[card[0]]} {SUIT_SYMBOLS[card[1]]}"


def card_picker_label(card):
    if card is None:
        return ':color[＋]{foreground="#374151"}'
    text = card_visual_name(card)
    color = "#d62828" if card[1] in ("h", "d") else "#111111"
    return f':color[{text}]{{foreground="{color}"}}'


CARD_SLOTS = ["hero_card_1","hero_card_2","flop_card_1","flop_card_2","flop_card_3","turn_card","river_card"]
DEFAULT_STATE = {"hero_card_1":None,"hero_card_2":None,"flop_card_1":None,"flop_card_2":None,"flop_card_3":None,"turn_card":None,"river_card":None,"active_players":3,"simulations":25000,"calculation_result":None,"calculation_summary":None}
for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


def clear_result():
    st.session_state.calculation_result = None
    st.session_state.calculation_summary = None


def select_card(slot_key, card):
    st.session_state[slot_key] = card
    clear_result()


def reset_hand():
    for key, value in DEFAULT_STATE.items():
        st.session_state[key] = value


def used_cards_except(current_slot):
    return {st.session_state[s] for s in CARD_SLOTS if s != current_slot and st.session_state[s] is not None}


def render_card_grid(slot_key, unavailable):
    """Renderiza 52 cartas en filas de 6, solo cuando el popover está abierto."""
    for start in range(0, len(FULL_DECK), 3):
        row_cards = FULL_DECK[start:start + 3]
        columns = st.columns(3)
        for column, card in zip(columns, row_cards):
            with column:
                st.button(
                    card_picker_label(card),
                    key=f"choose_{slot_key}_{card}",
                    disabled=card in unavailable,
                    use_container_width=True,
                    on_click=select_card,
                    args=(slot_key, card),
                )


def card_picker(slot_key, position_label, allow_empty=False):
    st.markdown(f'<div class="card-position-label">{position_label}</div>', unsafe_allow_html=True)
    pop = st.popover(
        card_picker_label(st.session_state[slot_key]),
        use_container_width=True,
        key=f"picker_{slot_key}",
        on_change="rerun",
    )
    # Clave de rendimiento: no crear los 52 botones si el selector está cerrado.
    if pop.open:
        with pop:
            st.markdown(f'<div class="picker-title">Seleccionar {position_label}</div>', unsafe_allow_html=True)
            if allow_empty:
                st.button("＋ Sin carta", key=f"clear_{slot_key}", use_container_width=True, on_click=select_card, args=(slot_key, None))
            render_card_grid(slot_key, used_cards_except(slot_key))
            st.caption("Las cartas utilizadas aparecen desactivadas.")


def validate_inputs(hero, board, players):
    if None in hero:
        raise ValueError("Selecciona tus dos cartas.")
    if len(board) not in (0, 3, 4, 5):
        raise ValueError("Introduce las tres cartas del flop juntas.")
    if not 2 <= players <= 10:
        raise ValueError("Debe haber entre 2 y 10 jugadores.")
    if len(hero + board) != len(set(hero + board)):
        raise ValueError("Hay cartas repetidas.")


def hand_score(player_cards, board_cards):
    return EVALUATOR.evaluate([Card.new(c) for c in board_cards], [Card.new(c) for c in player_cards])


def monte_carlo(hero, board, players, simulations):
    validate_inputs(hero, board, players)
    available = [c for c in FULL_DECK if c not in set(hero + board)]
    wins = ties = losses = 0
    missing = 5 - len(board)
    villains = players - 1
    needed = missing + villains * 2
    for _ in range(simulations):
        sample = random.sample(available, needed)
        completed = board + sample[:missing]
        pos = missing
        scores = [hand_score(hero, completed)]
        for _ in range(villains):
            scores.append(hand_score(sample[pos:pos + 2], completed))
            pos += 2
        best = min(scores)
        if scores[0] != best:
            losses += 1
        elif scores.count(best) == 1:
            wins += 1
        else:
            ties += 1
    return {"victoria":round(wins/simulations*100,2),"empate":round(ties/simulations*100,2),"derrota":round(losses/simulations*100,2),"simulaciones":simulations}



# ============================================================
# INTERPRETACIÓN AUTOMÁTICA DEL RESULTADO
# ============================================================

def interpret_result(result, board_cards, active_players):
    """
    Genera una lectura estadística neutral del resultado.

    No recomienda apostar, igualar o retirarse porque esas
    decisiones también requieren información sobre el bote,
    el coste de continuar, la posición y los rangos rivales.
    """

    win_probability = result["victoria"]
    tie_probability = result["empate"]
    loss_probability = result["derrota"]
    advantage = win_probability - loss_probability
    board_size = len(board_cards)

    if board_size == 0:
        phase_name = "preflop"
        uncertainty_text = (
            "La incertidumbre todavía es elevada porque no se ha "
            "mostrado ninguna carta comunitaria."
        )
    elif board_size == 3:
        phase_name = "flop"
        uncertainty_text = (
            "La estimación todavía puede cambiar considerablemente "
            "con el turn y el river."
        )
    elif board_size == 4:
        phase_name = "turn"
        uncertainty_text = (
            "Solo queda una carta por aparecer, por lo que la "
            "estimación es más estable que en el flop."
        )
    else:
        phase_name = "river"
        uncertainty_text = (
            "La mesa está completa. La variación restante procede "
            "de las posibles manos rivales."
        )

    if win_probability >= 75:
        strength_text = "Tu mano presenta una ventaja estadística muy alta"
    elif win_probability >= 60:
        strength_text = "Tu mano presenta una ventaja estadística alta"
    elif win_probability >= 50:
        strength_text = "Tu mano presenta una ventaja estadística moderada"
    elif win_probability >= 35:
        strength_text = (
            "El resultado está relativamente equilibrado, aunque "
            "tu mano no parte con ventaja"
        )
    elif win_probability >= 20:
        strength_text = "Tu mano presenta una probabilidad de victoria baja"
    else:
        strength_text = (
            "Tu mano presenta una probabilidad de victoria muy reducida"
        )

    absolute_advantage = abs(advantage)

    if absolute_advantage < 5:
        comparison_text = (
            "Victoria y derrota muestran valores muy próximos, por lo "
            "que el escenario está estadísticamente equilibrado."
        )
    elif advantage >= 20:
        comparison_text = (
            "La probabilidad de victoria supera claramente a la "
            "probabilidad de derrota."
        )
    elif advantage > 0:
        comparison_text = (
            "La probabilidad de victoria supera ligeramente a la "
            "probabilidad de derrota."
        )
    elif advantage <= -20:
        comparison_text = (
            "La probabilidad de derrota supera claramente a la "
            "probabilidad de victoria."
        )
    else:
        comparison_text = (
            "La probabilidad de derrota supera ligeramente a la "
            "probabilidad de victoria."
        )

    if active_players >= 7:
        players_text = (
            f"El análisis incluye {active_players} jugadores activos. "
            "Al competir contra muchos rivales, existen más "
            "combinaciones capaces de superar tu mano."
        )
    elif active_players >= 4:
        players_text = (
            f"El análisis incluye {active_players} jugadores activos, "
            "por lo que la mano se compara con varios rivales "
            "simultáneamente."
        )
    else:
        players_text = (
            f"El análisis incluye {active_players} jugadores activos, "
            "un escenario con pocos rivales."
        )

    if tie_probability >= 10:
        tie_text = (
            "La probabilidad de empate es relevante y puede estar "
            "relacionada con combinaciones compartidas mediante las "
            "cartas comunitarias."
        )
    elif tie_probability >= 3:
        tie_text = (
            "Existe una probabilidad apreciable de compartir la mejor "
            "mano con uno o más rivales."
        )
    else:
        tie_text = "Los empates tienen poca influencia en el resultado."

    frequency = round(win_probability)

    return {
        "main": (
            f"{strength_text}: gana aproximadamente {frequency} de cada "
            f"100 escenarios simulados en la fase de {phase_name}."
        ),
        "comparison": comparison_text,
        "uncertainty": uncertainty_text,
        "players": players_text,
        "tie": tie_text,
    }


# Estilo aislado para la interpretación.
# No modifica los anchos de los selectores ni de los pop-ups.
st.markdown(
    r"""
    <style>
    .interpretation-card {
        margin-top: 0.45rem;
        margin-bottom: 0.20rem;
        padding: 0.70rem 0.80rem;
        background: linear-gradient(
            145deg,
            rgba(4, 42, 33, 0.94),
            rgba(5, 58, 43, 0.88)
        );
        border: 1px solid rgba(99, 179, 255, 0.48);
        border-radius: 10px;
        color: #ffffff;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.22);
    }

    .interpretation-title {
        margin-bottom: 0.38rem;
        color: #8bc7ff;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.04rem;
        text-transform: uppercase;
    }

    .interpretation-main {
        margin-bottom: 0.42rem;
        color: #ffffff;
        font-size: 0.84rem;
        font-weight: 700;
        line-height: 1.48;
    }

    .interpretation-detail {
        margin-top: 0.25rem;
        color: rgba(255, 255, 255, 0.80);
        font-size: 0.75rem;
        line-height: 1.45;
    }

    .interpretation-note {
        margin-top: 0.55rem;
        padding-top: 0.45rem;
        border-top: 1px solid rgba(255, 255, 255, 0.14);
        color: rgba(255, 255, 255, 0.62);
        font-size: 0.66rem;
        line-height: 1.40;
    }

    @media screen and (max-width: 640px) {
        .interpretation-card {
            margin-top: 0.35rem;
            padding: 0.55rem 0.60rem;
        }

        .interpretation-title {
            margin-bottom: 0.30rem;
            font-size: 0.62rem;
        }

        .interpretation-main {
            margin-bottom: 0.32rem;
            font-size: 0.72rem;
            line-height: 1.42;
        }

        .interpretation-detail {
            margin-top: 0.20rem;
            font-size: 0.66rem;
            line-height: 1.40;
        }

        .interpretation-note {
            margin-top: 0.40rem;
            padding-top: 0.35rem;
            font-size: 0.58rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="brand-header"><div class="brand-main"><span class="brand-symbol">♠</span><span>POKER LAB</span></div><div class="brand-signature">BY ÁLVARO HDEZ</div></div>', unsafe_allow_html=True)

# ============================================================
# AYUDA: CÓMO FUNCIONA
# ============================================================

with st.popover(
    "ℹ️ Cómo funciona",
    key="help_popover",
    use_container_width=False,
    on_change="ignore"
):
    st.markdown(
        """
        ### Cómo utilizar Poker Lab

        1. **Selecciona tus dos cartas** pulsando sobre cada naipe.
        2. Añade las tres cartas del **flop** cuando aparezcan.
        3. Incorpora después el **turn** y el **river**.
        4. Indica los **jugadores activos**, incluyéndote.
        5. Elige el número de **simulaciones**.
        6. Pulsa **Calcular probabilidades**.

        Poker Lab simula miles de posibles repartos y estima:

        - 🟢 **Victoria**
        - 🟡 **Empate**
        - 🔴 **Derrota**
        """
    )

    st.info(
        "Cuantas más simulaciones selecciones, más estable será "
        "la estimación, aunque el cálculo puede tardar algo más."
    )

    st.caption(
        "Los resultados son estimaciones estadísticas y pueden "
        "variar ligeramente entre cálculos."
    )


with st.container(border=True):
    st.markdown('<div class="section-title">Tus cartas</div>', unsafe_allow_html=True)

    hero_row = st.container(horizontal=True, gap="small")
    hero_1 = hero_row.container(width="stretch")
    hero_2 = hero_row.container(width="stretch")
    with hero_1:
        card_picker("hero_card_1", "Carta 1")
    with hero_2:
        card_picker("hero_card_2", "Carta 2")

    st.markdown('<div class="section-title">Cartas comunitarias</div>', unsafe_allow_html=True)

    flop_row = st.container(horizontal=True, gap="small")
    flop_1 = flop_row.container(width="stretch")
    flop_2 = flop_row.container(width="stretch")
    flop_3 = flop_row.container(width="stretch")
    with flop_1:
        card_picker("flop_card_1", "Flop 1", True)
    with flop_2:
        card_picker("flop_card_2", "Flop 2", True)
    with flop_3:
        card_picker("flop_card_3", "Flop 3", True)

    turn_river_row = st.container(horizontal=True, gap="small")
    turn_slot = turn_river_row.container(width="stretch")
    river_slot = turn_river_row.container(width="stretch")
    with turn_slot:
        card_picker("turn_card", "Turn", True)
    with river_slot:
        card_picker("river_card", "River", True)

    config_row = st.container(horizontal=True, gap="small")
    players_slot = config_row.container(width="stretch")
    simulations_slot = config_row.container(width="stretch")
    with players_slot:
        active_players = st.number_input(
            "Jugadores activos", 2, 10, step=1,
            key="active_players", on_change=clear_result
        )
    with simulations_slot:
        simulations = st.selectbox(
            "Simulaciones", [10000, 25000, 50000, 100000],
            format_func=lambda value: f"{value:,}".replace(",", "."),
            key="simulations", on_change=clear_result
        )

    actions_row = st.container(horizontal=True, gap="small")
    calculate_slot = actions_row.container(width="stretch")
    reset_slot = actions_row.container(width="stretch")
    with calculate_slot:
        calculate_button = st.button(
            "Calcular probabilidades", type="primary", width="stretch"
        )
    with reset_slot:
        st.button("Nueva mano", width="stretch", on_click=reset_hand)

if calculate_button:
    try:
        hero = [st.session_state.hero_card_1, st.session_state.hero_card_2]
        positions = [st.session_state.flop_card_1,st.session_state.flop_card_2,st.session_state.flop_card_3,st.session_state.turn_card,st.session_state.river_card]
        empty = False
        for card in positions:
            if card is None: empty = True
            elif empty: raise ValueError("Añade las cartas en orden: flop, turn y river.")
        board = [c for c in positions if c is not None]
        with st.spinner("Simulando partidas..."):
            result = monte_carlo(hero, board, active_players, simulations)
        st.session_state.calculation_result = result
        st.session_state.calculation_summary = {"hero":hero,"board":board,"players":active_players}
    except Exception as error:
        st.error(str(error))

result = st.session_state.calculation_result
summary = st.session_state.calculation_summary

if result and summary:
    hero_text = " ".join(card_visual_name(c) for c in summary["hero"])
    board_text = " ".join(card_visual_name(c) for c in summary["board"]) if summary["board"] else "Antes del flop"

    st.markdown('<div class="section-title">Probabilidades</div>', unsafe_allow_html=True)

    results_html = (
        '<div class="results-grid">'
        f'<div class="result-card result-win"><div class="result-label">Victoria</div><div class="result-value win-value">{result["victoria"]} %</div></div>'
        f'<div class="result-card result-tie"><div class="result-label">Empate</div><div class="result-value tie-value">{result["empate"]} %</div></div>'
        f'<div class="result-card result-loss"><div class="result-label">Derrota</div><div class="result-value loss-value">{result["derrota"]} %</div></div>'
        '</div>'
    )
    st.markdown(results_html, unsafe_allow_html=True)

    interpretation = interpret_result(
        result=result,
        board_cards=summary["board"],
        active_players=summary["players"],
    )

    interpretation_html = (
        '<div class="interpretation-card">'
        '<div class="interpretation-title">Lectura del resultado</div>'
        f'<div class="interpretation-main">{interpretation["main"]}</div>'
        f'<div class="interpretation-detail">{interpretation["comparison"]}</div>'
        f'<div class="interpretation-detail">{interpretation["uncertainty"]}</div>'
        f'<div class="interpretation-detail">{interpretation["players"]}</div>'
        f'<div class="interpretation-detail">{interpretation["tie"]}</div>'
        '<div class="interpretation-note">'
        'Esta lectura describe únicamente los resultados estadísticos '
        'de la simulación. No constituye una recomendación de apuesta.'
        '</div>'
        '</div>'
    )

    st.markdown(interpretation_html, unsafe_allow_html=True)

    summary_html = (
        '<div class="hand-summary">'
        f'<div><strong>Tus cartas:</strong> {hero_text}</div>'
        f'<div><strong>Mesa:</strong> {board_text}</div>'
        f'<div><strong>Jugadores activos:</strong> {summary["players"]}</div>'
        '</div>'
    )
    st.markdown(summary_html, unsafe_allow_html=True)

    st.caption(
        f'Resultado basado en {result["simulaciones"]:,} simulaciones.'.replace(",", ".")
    )

st.divider()
st.caption("Los rivales se simulan con manos aleatorias entre todas las combinaciones legales disponibles.")

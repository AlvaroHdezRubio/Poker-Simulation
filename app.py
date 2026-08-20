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
</style>
""", unsafe_allow_html=True)

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
DEFAULT_STATE = {"hero_card_1":"Kh","hero_card_2":"Ks","flop_card_1":None,"flop_card_2":None,"flop_card_3":None,"turn_card":None,"river_card":None,"active_players":6,"simulations":25000,"calculation_result":None,"calculation_summary":None}
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
    for start in range(0, len(FULL_DECK), 6):
        row_cards = FULL_DECK[start:start + 6]
        columns = st.columns(6)
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


st.markdown('<div class="brand-header"><div class="brand-main"><span class="brand-symbol">♠</span><span>POKER LAB</span></div><div class="brand-signature">BY ÁLVARO HDEZ</div></div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div class="section-title">Tus cartas</div>', unsafe_allow_html=True)
    h1, h2 = st.columns(2)
    with h1: card_picker("hero_card_1", "Carta 1")
    with h2: card_picker("hero_card_2", "Carta 2")

    st.markdown('<div class="section-title">Cartas comunitarias</div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1: card_picker("flop_card_1", "Flop 1", True)
    with f2: card_picker("flop_card_2", "Flop 2", True)
    with f3: card_picker("flop_card_3", "Flop 3", True)
    t, r = st.columns(2)
    with t: card_picker("turn_card", "Turn", True)
    with r: card_picker("river_card", "River", True)

    c1, c2 = st.columns(2)
    with c1:
        active_players = st.number_input("Jugadores activos", 2, 10, step=1, key="active_players", on_change=clear_result)
    with c2:
        simulations = st.selectbox("Simulaciones", [10000,25000,50000,100000], format_func=lambda v:f"{v:,}".replace(",","."), key="simulations", on_change=clear_result)

    b1, b2 = st.columns(2)
    with b1: calculate_button = st.button("Calcular probabilidades", type="primary", use_container_width=True)
    with b2: st.button("Nueva mano", use_container_width=True, on_click=reset_hand)

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

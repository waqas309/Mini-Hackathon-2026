"""
Leukopenia / CBC Blood Analyzer  -  front end (Marvi)
Run locally:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="CBC Analyzer · Leukopenia Screen",
    page_icon="🩸",
    layout="wide",
)

# ------------------------------------------------------------------
# 1. CONFIG - the only block you edit if Waqas renames a column
#    "key" MUST match the column name in cleaned_cbc.csv exactly.
# ------------------------------------------------------------------
FEATURES = [
    dict(key="WBC",  label="White cells (WBC)", unit="×10³/µL", lo=4.0,  hi=11.0,  min=0.1,  max=60.0,   step=0.1),
    dict(key="RBC",  label="Red cells (RBC)",   unit="×10⁶/µL", lo=4.2,  hi=5.9,   min=0.5,  max=9.0,    step=0.01),
    dict(key="HGB",  label="Hemoglobin (HGB)",  unit="g/dL",    lo=12.0, hi=17.5,  min=3.0,  max=22.0,   step=0.1),
    dict(key="PCV",  label="Hematocrit (PCV)",  unit="%",       lo=36.0, hi=52.0,  min=10.0, max=65.0,   step=0.1),
    dict(key="PLT",  label="Platelets (PLT)",   unit="×10³/µL", lo=150.0, hi=450.0, min=5.0, max=1000.0, step=1.0),
    dict(key="MCV",  label="MCV",               unit="fL",      lo=80.0, hi=100.0, min=50.0, max=130.0,  step=0.1),
    dict(key="MCH",  label="MCH",               unit="pg",      lo=27.0, hi=33.0,  min=15.0, max=45.0,   step=0.1),
    dict(key="MCHC", label="MCHC",              unit="g/dL",    lo=32.0, hi=36.0,  min=25.0, max=40.0,   step=0.1),
    dict(key="RDW",  label="Red cell width (RDW)", unit="%",    lo=11.5, hi=14.5,  min=5.0,  max=40.0,   step=0.1),
]
GENDER_MAP = {"Male": 1, "Female": 0}   # CONFIRM which of 0/1 is Male in cleaned_cbc.csv

NORMAL = dict(WBC=6.8, RBC=4.9, HGB=14.2, PCV=42.0, PLT=260.0, MCV=89.0, MCH=29.5, MCHC=33.5, RDW=13.0, Age=34, Gender="Male")
LEUKO  = dict(WBC=2.4, RBC=4.3, HGB=11.8, PCV=36.0, PLT=145.0, MCV=86.0, MCH=28.0, MCHC=32.5, RDW=14.0, Age=47, Gender="Female")


def out_of_range(values):
    """Used only by the stand-in predictor below."""
    flags = []
    for f in FEATURES:
        v = values[f["key"]]
        if v < f["lo"]:
            flags.append(f'{f["key"]} low ({v:g} < {f["lo"]:g})')
        elif v > f["hi"]:
            flags.append(f'{f["key"]} high ({v:g} > {f["hi"]:g})')
    return flags


# ------------------------------------------------------------------
# 2. Backend hookup (Farman's src/predictor.py)
#    Until his file exists, a stand-in keeps the UI testable.
# ------------------------------------------------------------------
try:
    from src.predictor import predict_leukopenia
    DEMO_MODE = False
except ImportError:
    DEMO_MODE = True

    def predict_leukopenia(values):
        risk = values["WBC"] < 4.0
        return {
            "prediction": int(risk),
            "probability": 0.93 if risk else 0.06,
            "flagged_metrics": out_of_range(values),
        }


# ------------------------------------------------------------------
# 3. Look & feel: "lab report slip on paper" theme
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500&display=swap');

:root{--paper:#F7F1E6;--card:#FFFDF8;--ink:#2A211C;--muted:#7A6B5D;--line:#D9CDB8;
      --red:#8E1B2E;--red-tint:#F4DEDD;--sage:#3F6B5A;--sage-tint:#DDE9E1;}

#MainMenu, footer, header[data-testid="stHeader"]{visibility:hidden;height:0;}
.stApp{background:var(--paper);border-top:6px solid var(--red);}
.block-container{padding-top:2rem;max-width:1150px;}
html, body, .stApp{font-family:'IBM Plex Sans',sans-serif;color:var(--ink);}

.tag{display:inline-block;font:500 .7rem 'IBM Plex Mono',monospace;letter-spacing:.14em;
     color:var(--red);border:1px solid var(--red);padding:.2rem .6rem;margin-bottom:.8rem;}
.title{font:700 2.5rem/1.1 'Fraunces',serif;margin:0 0 .4rem 0;}
.title em{color:var(--red);font-style:italic;}
.sub{color:var(--muted);max-width:640px;margin-bottom:1.6rem;}
.sec{font:500 .75rem 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;
     color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:.4rem;margin:1rem 0 .8rem;}

[data-testid="stWidgetLabel"] p{font:500 .7rem 'IBM Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}
div[data-baseweb="input"], div[data-baseweb="select"] > div{background:var(--card)!important;border:1px solid var(--line)!important;border-radius:2px!important;}
input{font-family:'IBM Plex Mono',monospace!important;color:var(--ink)!important;}

.stButton > button{border-radius:2px;font:500 .85rem 'IBM Plex Sans',sans-serif;border:1px solid var(--ink);
     background:transparent;color:var(--ink);width:100%;}
.stButton > button:hover{background:var(--ink);color:var(--paper);border-color:var(--ink);}
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"]{
     background:var(--red);border-color:var(--red);color:#fff;letter-spacing:.04em;padding:.6rem 0;}
.stButton > button[kind="primary"]:hover, .stButton > button[data-testid="stBaseButton-primary"]:hover{background:#6F1424;border-color:#6F1424;}

.verdict{border:1.5px solid;padding:1.1rem 1.3rem;margin-bottom:1rem;background:var(--card);}
.verdict.risk{border-color:var(--red);box-shadow:6px 6px 0 var(--red-tint);}
.verdict.ok{border-color:var(--sage);box-shadow:6px 6px 0 var(--sage-tint);}
.verdict .k{font:500 .7rem 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);}
.verdict .h{font:700 1.6rem 'Fraunces',serif;margin:.2rem 0 .5rem;}
.verdict.risk .h{color:var(--red);} .verdict.ok .h{color:var(--sage);}
.verdict .p{font:500 2rem 'IBM Plex Mono',monospace;}
.verdict .p small{font:400 .8rem 'IBM Plex Sans',sans-serif;color:var(--muted);margin-left:.4rem;}
.chip{display:inline-block;font:400 .78rem 'IBM Plex Mono',monospace;background:var(--red-tint);
      color:var(--red);padding:.15rem .5rem;margin:.5rem .35rem 0 0;}

.strip{position:relative;height:16px;background:#E9DFCC;margin:1.8rem 0 0;}
.band{position:absolute;top:0;bottom:0;background:var(--sage-tint);border-left:2px solid var(--sage);border-right:2px solid var(--sage);}
.pin{position:absolute;top:-8px;width:3px;height:32px;background:var(--red);}
.pin span{position:absolute;top:-22px;left:50%;transform:translateX(-50%);font:500 .8rem 'IBM Plex Mono',monospace;color:var(--red);white-space:nowrap;}
.ticks{position:relative;height:22px;font:400 .7rem 'IBM Plex Mono',monospace;color:var(--muted);margin-top:.35rem;}
.ticks span{position:absolute;transform:translateX(-50%);}
.cap{font-size:.8rem;color:var(--muted);margin-top:.2rem;}

.slip{background:var(--card);border:1px solid var(--line);font-family:'IBM Plex Mono',monospace;font-size:.82rem;}
.slip .row, .slip-h{display:grid;grid-template-columns:2.2fr 1.6fr 1.2fr .4fr;padding:.45rem .9rem;border-bottom:1px dashed var(--line);}
.slip-h{color:var(--muted);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;}
.slip .v small{color:var(--muted);font-size:.68rem;}
.slip .r{color:var(--muted);}
.f.flag{color:var(--red);font-weight:500;} .f.ok{color:var(--line);}
.slip .row:has(.flag){background:var(--red-tint);}

.note{font-size:.78rem;color:var(--muted);border-top:1px solid var(--line);margin-top:2rem;padding-top:.8rem;}
.demo{font:500 .7rem 'IBM Plex Mono',monospace;color:#7A5200;background:#FBEBC8;padding:.2rem .5rem;margin-left:.6rem;}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------
# 4. Small helpers that build the HTML pieces
# ------------------------------------------------------------------
def wbc_strip(v, lo=4.0, hi=11.0):
    top = max(15.0, v * 1.15)
    pct = lambda x: min(max(x / top * 100, 0), 100)
    return (
        f'<div class="strip"><div class="band" style="left:{pct(lo)}%;width:{pct(hi)-pct(lo)}%"></div>'
        f'<div class="pin" style="left:{pct(v)}%"><span>{v:g}</span></div></div>'
        f'<div class="ticks"><span style="left:0%">0</span><span style="left:{pct(lo)}%">{lo:g}</span>'
        f'<span style="left:{pct(hi)}%">{hi:g}</span><span style="left:100%">{top:.0f}</span></div>'
        f'<div class="cap">Patient WBC against the normal 4.0 – 11.0 ×10³/µL band</div>'
    )


def slip_html(values):
    rows = ""
    for f in FEATURES:
        v = values[f["key"]]
        flag = "L" if v < f["lo"] else "H" if v > f["hi"] else ""
        rows += (
            f'<div class="row"><span>{f["label"]}</span>'
            f'<span class="v">{v:g} <small>{f["unit"]}</small></span>'
            f'<span class="r">{f["lo"]:g} – {f["hi"]:g}</span>'
            f'<span class="f {"flag" if flag else "ok"}">{flag or "·"}</span></div>'
        )
    return ('<div class="slip"><div class="slip-h"><span>Test</span><span>Result</span>'
            f'<span>Reference</span><span></span></div>{rows}</div>')


def load_sample(sample):
    """Button callback: fills every input box and clears the old result."""
    for k, v in sample.items():
        st.session_state[f"in_{k}"] = v
    st.session_state.pop("result", None)


if "in_WBC" not in st.session_state:
    load_sample(NORMAL)


# ------------------------------------------------------------------
# 5. Page
# ------------------------------------------------------------------
badge = '<span class="demo">STAND-IN MODEL</span>' if DEMO_MODE else ""
st.markdown(
    f'<div class="tag">EDUCATIONAL SCREENING TOOL{badge}</div>'
    '<div class="title">Leukopenia <em>/</em> CBC Blood Analyzer</div>'
    '<div class="sub">Enter a Complete Blood Count and the model estimates the risk of '
    'leukopenia, a low white-cell count, and shows which values fall outside the normal range.</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1.05, 1.2], gap="large")

with left:
    st.markdown('<div class="sec">01 · Patient values</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    b1.button("Load normal sample", on_click=load_sample, args=(NORMAL,))
    b2.button("Load leukopenia sample", on_click=load_sample, args=(LEUKO,))

    grid = st.columns(2)
    for i, f in enumerate(FEATURES):
        grid[i % 2].number_input(
            f'{f["label"]} · {f["unit"]}',
            min_value=f["min"], max_value=f["max"], step=f["step"], key=f'in_{f["key"]}',
        )
    grid[0].number_input("Age · years", min_value=1, max_value=110, step=1, key="in_Age")
    grid[1].selectbox("Gender", list(GENDER_MAP), key="in_Gender")

    if st.button("Analyze blood report", type="primary"):
        values = {f["key"]: st.session_state[f'in_{f["key"]}'] for f in FEATURES}
        values["Age"] = st.session_state["in_Age"]
        values["Gender"] = GENDER_MAP[st.session_state["in_Gender"]]
        try:
            st.session_state["result"] = {"inputs": values, "out": predict_leukopenia(values)}
        except Exception as e:
            st.session_state.pop("result", None)
            st.error(f"The prediction backend failed: {e}")

with right:
    st.markdown('<div class="sec">02 · Result</div>', unsafe_allow_html=True)
    res = st.session_state.get("result")
    if not res:
        st.markdown('<div class="cap">Fill in the values (or load a sample) and press '
                    '<b>Analyze blood report</b>.</div>', unsafe_allow_html=True)
    else:
        out, vals = res["out"], res["inputs"]
        risk = out["prediction"] == 1
        chips = "".join(f'<span class="chip">{m}</span>' for m in out["flagged_metrics"]) \
                or '<span class="cap">No parameter outside its reference range.</span>'
        st.markdown(
            f'<div class="verdict {"risk" if risk else "ok"}">'
            f'<div class="k">Screening outcome</div>'
            f'<div class="h">{"Leukopenia risk flagged" if risk else "No leukopenia signal"}</div>'
            f'<div class="p">{out["probability"] * 100:.1f}%<small>model probability of leukopenia</small></div>'
            f'{chips}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="sec">03 · WBC against normal range</div>', unsafe_allow_html=True)
        st.markdown(wbc_strip(vals["WBC"]), unsafe_allow_html=True)
        st.markdown('<div class="sec">Lab slip</div>', unsafe_allow_html=True)
        st.markdown(slip_html(vals), unsafe_allow_html=True)

st.markdown(
    '<div class="note">Educational project built for the Machine Learning course, Sukkur IBA University. '
    'Not a medical device and not a substitute for a clinician.</div>',
    unsafe_allow_html=True,
)

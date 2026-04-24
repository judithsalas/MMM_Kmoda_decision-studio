"""
K-Moda MMM Decision Studio
===========================
Streamlit app — Light premium theme, consulting-grade design.
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

st.set_page_config(page_title="K-Moda · MMM Decision Studio", page_icon="👔", layout="wide", initial_sidebar_state="expanded")

# ─── CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Playfair+Display:wght@400;600;700&display=swap');
/* Contenedor principal: centrar con max-width para que en pantallas grandes no se estire demasiado */
.main .block-container,
[data-testid="stAppViewContainer"] .block-container,
[data-testid="stMain"] .block-container{
    max-width:1400px!important;
    padding-left:3rem!important;
    padding-right:3rem!important;
    padding-top:2rem!important;
    margin-left:auto!important;
    margin-right:auto!important;
}
@media (max-width:1200px){
    .main .block-container,
    [data-testid="stAppViewContainer"] .block-container,
    [data-testid="stMain"] .block-container{
        padding-left:1.5rem!important;
        padding-right:1.5rem!important;
    }
}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="block-container"]{background-color:#f8fafc!important;color:#111827!important}
[data-testid="stHeader"]{background-color:#f8fafc!important}
html,body,[class*="st-"]{font-family:'DM Sans',sans-serif;color:#111827}
/* Restaurar Material Symbols en iconos de Streamlit — mi regla [class*="st-"] estaba pisando la fuente de iconos y los mostraba como texto ("keyboard_double_arrow_left") */
.material-symbols-rounded,.material-symbols-outlined,.material-icons,[class*="material-symbols"],[class*="material-icons"]{
    font-family:'Material Symbols Rounded','Material Symbols Outlined','Material Icons'!important;
    font-weight:normal!important;font-style:normal!important;
    text-transform:none!important;letter-spacing:normal!important;
    word-wrap:normal!important;white-space:nowrap!important;
    direction:ltr!important;font-feature-settings:'liga'!important
}
[data-testid="stSidebarCollapseButton"],[data-testid="stSidebarCollapsedControl"]{overflow:hidden!important}
/* Ocultar botones de collapse/expand del sidebar — el icono Material se muestra como texto "keyboard_double_arrow_*" en Streamlit Cloud y ensucia el logo. En una app de presentación no necesitamos colapsar. */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarHeader"] button,
button[kind="header"],
button[kind="headerNoPadding"]{
    display:none!important;
    visibility:hidden!important;
    width:0!important;height:0!important;opacity:0!important
}
/* Esconder el icono nativo del expander de Streamlit que se renderiza como texto "keyboard_arrow_right" */
[data-testid="stExpander"] summary svg,
[data-testid="stExpander"] summary > div:first-child > span:first-child,
[data-testid="stExpander"] summary [data-testid*="icon"],
[data-testid="stExpander"] summary [data-testid*="Icon"],
details > summary::-webkit-details-marker,
details > summary::marker{
    display:none!important;
    visibility:hidden!important;
    width:0!important;max-width:0!important;overflow:hidden!important;
    font-size:0!important
}
/* Chevron CSS propio para los expanders */
[data-testid="stExpander"] summary,
details > summary{
    position:relative;
    padding-left:22px!important;
    list-style:none!important
}
[data-testid="stExpander"] summary::before,
details > summary::before{
    content:"▸";
    position:absolute;left:4px;top:50%;
    transform:translateY(-50%);
    color:#c9a96e;font-size:11px;font-weight:700;
    transition:transform .2s ease;
    font-family:'DM Sans',sans-serif!important
}
[data-testid="stExpander"][open] > details > summary::before,
[data-testid="stExpander"] details[open] > summary::before,
details[open] > summary::before{
    transform:translateY(-50%) rotate(90deg)
}
h1,h2,h3{font-family:'Playfair Display',serif;color:#111827}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li,.stTextInput label,.stSlider label,.stRadio label{color:#111827!important}
section[data-testid="stSidebar"]{background:#ffffff!important;border-right:1px solid #e5e7eb}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stRadio label{color:#374151!important}
section[data-testid="stSidebar"] .stRadio label:hover{color:#1e3a5f!important}
section[data-testid="stSidebar"] small{color:#6b7280!important}
.sidebar-title{font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:#111827!important;margin-bottom:4px;letter-spacing:1px}
.sidebar-sub{font-size:12px;color:#4b5563!important;letter-spacing:2px;text-transform:uppercase;margin-bottom:24px}
.kpi-card{background:#fff;border:1px solid #e5e7eb;border-radius:16px;padding:24px 28px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.04);transition:transform .2s;min-height:140px;display:flex;flex-direction:column;justify-content:center}
.kpi-card:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,0,0,.08)}
/* Equal height columns */
[data-testid="stHorizontalBlock"]{align-items:stretch!important}
[data-testid="stColumn"]>div{height:100%}
[data-testid="stColumn"]>div>[data-testid="stMarkdownContainer"]{height:100%}
.kpi-label{font-size:13px;font-weight:500;color:#6b7280;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:6px}
.kpi-value{font-family:'Playfair Display',serif;font-size:32px;font-weight:700;color:#111827;line-height:1.1}
.kpi-sub{font-size:12px;color:#4b5563;margin-top:4px}
.section-header{font-family:'Playfair Display',serif;font-size:28px;font-weight:600;color:#111827;margin:20px 0 10px;padding-bottom:8px;border-bottom:2px solid #c9a96e}
.callout-gold{background:#fffbeb;border-left:4px solid #c9a96e;border-radius:0 12px 12px 0;padding:18px 22px;margin:12px 0;font-size:15px;color:#78350f}
.callout-blue{background:#eef1f5;border-left:4px solid #1e3a5f;border-radius:0 12px 12px 0;padding:18px 22px;margin:12px 0;font-size:15px;color:#0f2742}
.callout-red{background:#fef2f2;border-left:4px solid #9c5a5a;border-radius:0 12px 12px 0;padding:18px 22px;margin:12px 0;font-size:15px;color:#7f1d1d}
.callout-green{background:#eef2ef;border-left:4px solid #5f7a6a;border-radius:0 12px 12px 0;padding:18px 22px;margin:12px 0;font-size:15px;color:#374a3f}
.method-badge{display:inline-block;background:#eef1f5;color:#1e3a5f!important;border:1px solid #c8d2dc;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;letter-spacing:.8px}
.semaforo{display:inline-block;width:14px;height:14px;border-radius:50%;margin-right:6px;vertical-align:middle}
.sem-verde{background:#5f7a6a;box-shadow:0 0 6px #5f7a6a80}
.sem-amarillo{background:#a8826e;box-shadow:0 0 6px #a8826e80}
.sem-rojo{background:#9c5a5a;box-shadow:0 0 6px #9c5a5a80}
#MainMenu{visibility:hidden}footer{visibility:hidden}header{visibility:hidden}
/* Buttons light */
.stButton>button{background:#ffffff!important;color:#374151!important;border:1.5px solid #e5e7eb!important;border-radius:10px!important;font-weight:600!important;font-size:13px!important;padding:8px 16px!important;transition:all .2s!important}
.stButton>button:hover{border-color:#1e3a5f!important;color:#1e3a5f!important;box-shadow:0 2px 8px rgba(30,58,95,.12)!important}
.stButton>button:active,.stButton>button:focus{background:#eef1f5!important;border-color:#1e3a5f!important;color:#1e3a5f!important}
/* Inline code light */
code{background:#f3f4f6!important;color:#374151!important;padding:2px 6px!important;border-radius:4px!important;font-size:13px!important}
/* Number inputs light */
[data-testid="stNumberInput"] input{background:#ffffff!important;color:#111827!important;border:1.5px solid #e5e7eb!important;border-radius:10px!important;font-weight:600!important;font-size:16px!important}
[data-testid="stNumberInput"] button{background:#f3f4f6!important;color:#374151!important;border-color:#e5e7eb!important}
[data-testid="stNumberInput"] button:hover{background:#e5e7eb!important;color:#111827!important}
input[type="number"]{background:#ffffff!important;color:#111827!important}
.alloc-card{background:#fff;border-radius:14px;padding:16px 20px;margin-bottom:10px;border:1.5px solid #e5e7eb;box-shadow:0 2px 10px rgba(0,0,0,.03);transition:all .2s}
.alloc-card:hover{box-shadow:0 4px 16px rgba(0,0,0,.07);border-color:#1e3a5f}
.alloc-header{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.alloc-dot{width:12px;height:12px;border-radius:50%;flex-shrink:0}
.alloc-name{font-weight:700;font-size:14px;color:#111827;flex:1}
.alloc-mroi-tag{font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px;color:#fff}
.alloc-detail{display:flex;align-items:center;justify-content:space-between;margin-top:6px}
.alloc-euros{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:#111827}
.alloc-sub-text{font-size:11px;color:#4b5563;margin-top:2px}
.budget-bar-wrap{background:#e5e7eb;border-radius:10px;height:36px;overflow:hidden;display:flex;margin:16px 0 8px;box-shadow:inset 0 1px 3px rgba(0,0,0,.06)}
.budget-segment{height:100%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;transition:width .3s ease;text-shadow:0 1px 2px rgba(0,0,0,.3)}
.budget-bar-labels{display:flex;justify-content:space-between;font-size:11px;color:#374151;padding:0 2px}
.results-panel{background:#fff;border:1px solid #e5e7eb;border-radius:18px;padding:28px;color:#111827;box-shadow:0 10px 30px rgba(15,23,42,.06)}
.results-title{font-family:'Playfair Display',serif;font-size:16px;font-weight:600;color:#1e3a5f;text-transform:uppercase;letter-spacing:2px;margin-bottom:20px}
.result-metric{margin-bottom:18px}
.result-label{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:3px}
.result-value{font-family:'Playfair Display',serif;font-size:36px;font-weight:700;color:#111827;line-height:1}
.result-sub{font-size:12px;color:#4b5563;margin-top:3px}
.result-divider{border:none;border-top:1px solid #e5e7eb;margin:16px 0}
.semaforo-grande{display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:12px;margin-top:8px}
.sem-g-verde{background:rgba(95,122,106,.1)}.sem-g-amarillo{background:rgba(168,130,110,.1)}.sem-g-rojo{background:rgba(220,38,38,.1)}
.sem-dot-big{width:20px;height:20px;border-radius:50%;flex-shrink:0}
.sem-dot-verde{background:#5f7a6a;box-shadow:0 0 10px #5f7a6a60}
.sem-dot-amarillo{background:#a8826e;box-shadow:0 0 10px #a8826e60}
.sem-dot-rojo{background:#9c5a5a;box-shadow:0 0 10px #9c5a5a60}
.sem-text{font-size:13px;font-weight:600;color:#111827}
.interp-msg{background:#fffbeb;border:1px solid #fde68a;border-radius:14px;padding:18px 22px;margin-top:16px;font-size:14px;line-height:1.6;color:#78350f}
.sum-indicator{display:flex;align-items:center;justify-content:center;gap:8px;padding:10px;border-radius:10px;font-size:14px;font-weight:700;margin-top:6px}
.sum-ok{background:rgba(95,122,106,.1);color:#15803d;border:1px solid rgba(95,122,106,.3)}
.sum-error{background:rgba(220,38,38,.08);color:#b91c1c;border:1px solid rgba(220,38,38,.25)}
.check-item{padding:6px 0;font-size:14px;color:#111827;border-bottom:1px solid #f3f4f6}
.check-item:last-child{border-bottom:none}

/* ════════════════════════════════════════════════════════════
   RESUMEN EJECUTIVO — rediseño editorial
   ════════════════════════════════════════════════════════════ */
.hero-block{background:linear-gradient(135deg,#ffffff 0%,#fafbfc 100%);border-radius:24px;padding:52px 56px 48px;margin-bottom:28px;border:1px solid #e5e7eb;box-shadow:0 4px 30px rgba(15,23,42,.04);position:relative;overflow:hidden}
.hero-block::before{content:'';position:absolute;top:-100px;right:-80px;width:380px;height:380px;background:radial-gradient(circle,rgba(201,169,110,.1) 0%,transparent 65%);pointer-events:none}
.hero-block::after{content:'';position:absolute;bottom:-60px;left:-40px;width:220px;height:220px;background:radial-gradient(circle,rgba(30,58,95,.05) 0%,transparent 65%);pointer-events:none}
.hero-eyebrow{font-size:11px;font-weight:700;color:#c9a96e;text-transform:uppercase;letter-spacing:3px;margin-bottom:18px;display:flex;align-items:center;gap:16px;position:relative;z-index:1}
.hero-eyebrow-line{flex:1;height:1px;background:linear-gradient(90deg,#c9a96e 0%,transparent 100%);max-width:140px}
.hero-title{font-family:'Playfair Display',serif;font-size:44px;font-weight:600;line-height:1.15;color:#111827;letter-spacing:-1px;margin-bottom:20px;position:relative;z-index:1}
.hero-title em{font-style:normal;color:#c9a96e;font-weight:700}
.hero-title .accent{color:#1e3a5f;font-weight:700}
.hero-sub{font-size:16px;color:#4b5563;line-height:1.6;max-width:760px;margin-bottom:26px;position:relative;z-index:1}
.hero-pill-row{display:flex;gap:10px;flex-wrap:wrap;position:relative;z-index:1}
.hero-pill{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:24px;font-size:12px;font-weight:600;letter-spacing:.4px}
.hero-pill-gold{background:#fffbeb;color:#78350f;border:1px solid #fde68a}
.hero-pill-blue{background:#eef1f5;color:#0f2742;border:1px solid #c8d2dc}
.hero-pill-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}

.metric-hero{background:#fff;border:1px solid #e5e7eb;border-radius:20px;padding:28px 30px;position:relative;overflow:hidden;transition:all .25s ease;min-height:200px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 2px 12px rgba(15,23,42,.03)}
.metric-hero:hover{transform:translateY(-3px);box-shadow:0 12px 40px rgba(15,23,42,.08);border-color:#d1d5db}
.metric-hero-accent{position:absolute;top:0;left:0;right:0;height:3px}
.metric-hero-label{font-size:11px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:1.8px;margin-bottom:14px}
.metric-hero-value{font-family:'Playfair Display',serif;font-size:54px;font-weight:700;color:#111827;line-height:1;letter-spacing:-2px}
.metric-hero-unit{font-size:22px;font-weight:500;color:#6b7280;margin-left:4px;letter-spacing:0}
.metric-hero-caption{font-size:13px;color:#4b5563;margin-top:10px;line-height:1.5}
.metric-hero-badge{display:inline-flex;align-items:center;gap:6px;margin-top:14px;padding:6px 12px;border-radius:12px;font-size:12px;font-weight:600;align-self:flex-start}
.badge-up{background:#eef2ef;color:#15803d;border:1px solid #bbf7d0}
.badge-neutral{background:#f3f4f6;color:#374151;border:1px solid #e5e7eb}
.badge-gold{background:#fffbeb;color:#92400e;border:1px solid #fde68a}

.rec-panel{background:#fff;border:1px solid #e5e7eb;border-radius:20px;padding:30px 34px;box-shadow:0 4px 20px rgba(15,23,42,.03);height:100%}
.rec-panel-title{font-family:'Playfair Display',serif;font-size:24px;font-weight:600;color:#111827;margin-bottom:4px}
.rec-panel-sub{font-size:13px;color:#6b7280;margin-bottom:22px}
.alloc-row-mini{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid #f3f4f6}
.alloc-row-mini:last-child{border-bottom:none;padding-bottom:4px}
.alloc-dot-mini{width:11px;height:11px;border-radius:50%;flex-shrink:0;box-shadow:0 0 0 3px rgba(0,0,0,.03)}
.alloc-name-mini{font-size:14px;font-weight:600;color:#111827;flex:0 0 150px}
.alloc-bar-mini{flex:1;height:8px;background:#f3f4f6;border-radius:4px;overflow:hidden;position:relative;min-width:60px}
.alloc-bar-fill-mini{height:100%;border-radius:4px;transition:width .3s ease}
.alloc-pct-mini{font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:#111827;flex:0 0 48px;text-align:right;line-height:1}
.alloc-eur-mini{font-size:12px;color:#6b7280;flex:0 0 60px;text-align:right}
.alloc-mroi-mini{font-size:11px;font-weight:700;padding:3px 9px;border-radius:10px;flex:0 0 auto;letter-spacing:.3px}

.decision-box{background:linear-gradient(135deg,#fffbeb 0%,#f5efe9 100%);border-left:5px solid #c9a96e;border-radius:0 16px 16px 0;padding:22px 26px;margin-top:22px}
.decision-label{font-size:10px;font-weight:700;color:#92400e;text-transform:uppercase;letter-spacing:2px;margin-bottom:10px}
.decision-text{font-size:14px;color:#451a03;line-height:1.65}
.decision-text strong{color:#78350f;font-weight:700}

.section-divider{display:flex;align-items:center;gap:18px;margin:44px 0 26px}
.section-divider-line{flex:1;height:1px;background:linear-gradient(90deg,transparent 0%,#e5e7eb 50%,transparent 100%)}
.section-divider-label{font-family:'Playfair Display',serif;font-size:13px;font-weight:600;color:#6b7280;letter-spacing:3px;text-transform:uppercase}

.contrib-card{background:linear-gradient(145deg,#111827 0%,#1f2937 100%);border-radius:20px;padding:32px 32px;color:#fff;position:relative;overflow:hidden;height:100%;display:flex;flex-direction:column;justify-content:center}
.contrib-card::before{content:'';position:absolute;top:-80px;right:-80px;width:220px;height:220px;background:radial-gradient(circle,rgba(201,169,110,.2) 0%,transparent 60%);pointer-events:none}
.contrib-label{font-size:10px;color:#c9a96e;text-transform:uppercase;letter-spacing:2.5px;font-weight:700;margin-bottom:12px;position:relative;z-index:1}
.contrib-value{font-family:'Playfair Display',serif;font-size:84px;font-weight:700;color:#ffffff;line-height:.9;letter-spacing:-4px;position:relative;z-index:1}
.contrib-pct-symbol{font-size:40px;color:#c9a96e;margin-left:4px;letter-spacing:0}
.contrib-caption{font-size:13px;color:#d1d5db;margin-top:16px;line-height:1.55;position:relative;z-index:1}
.contrib-divider{border:none;border-top:1px solid rgba(255,255,255,.12);margin:18px 0;position:relative;z-index:1}
.contrib-meta{font-size:11px;color:#9ca3af;line-height:1.5;position:relative;z-index:1}

.takeaway-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:6px}
.takeaway-card{background:#fff;border:1px solid #e5e7eb;border-radius:18px;padding:26px 26px 24px;position:relative;transition:all .25s ease;overflow:hidden}
.takeaway-card:hover{border-color:#c9a96e;box-shadow:0 8px 28px rgba(201,169,110,.15);transform:translateY(-2px)}
.takeaway-num{font-family:'Playfair Display',serif;font-size:56px;font-weight:700;color:#c9a96e;line-height:1;opacity:.2;position:absolute;top:14px;right:22px;letter-spacing:-2px}
.takeaway-head{font-size:12px;font-weight:700;color:#c9a96e;text-transform:uppercase;letter-spacing:1.8px;margin-bottom:12px;position:relative;z-index:1}
.takeaway-body{font-size:14px;color:#374151;line-height:1.65;position:relative;z-index:1}
.takeaway-body strong{color:#111827;font-weight:700}

@media (max-width:1200px){
    .hero-title{font-size:36px}
    .metric-hero-value{font-size:42px}
    .contrib-value{font-size:64px}
}

/* ════════════════════════════════════════════════════════════
   SIDEBAR — rediseño editorial
   ════════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"]>div:first-child{padding:0!important;position:relative}
/* Gold accent bar on far left edge */
section[data-testid="stSidebar"]>div:first-child::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:#c9a96e;z-index:10}
/* Nav eyebrow label */
.sb-nav-eyebrow{font-size:10px;letter-spacing:2.5px;color:#9ca3af;padding:26px 28px 12px;text-transform:uppercase;font-weight:700;font-family:'DM Sans',sans-serif}
/* Brand block (redesign of existing sidebar-title/sub) */
.sb-brand{padding:38px 28px 28px;position:relative}
.sb-brand::after{content:'';position:absolute;bottom:0;left:28px;width:44px;height:2px;background:#c9a96e}
.sb-brand-title{font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:#111827!important;letter-spacing:2.5px;line-height:1;margin-bottom:10px}
.sb-brand-sub{font-size:11px;color:#9ca3af!important;letter-spacing:3px;text-transform:uppercase;font-weight:500;font-family:'DM Sans',sans-serif}
/* Radio container reset */
section[data-testid="stSidebar"] .stRadio{padding:0!important;margin:0!important}
section[data-testid="stSidebar"] [role="radiogroup"]{gap:0!important;padding:0!important}
/* Each nav item as a full-width row */
section[data-testid="stSidebar"] [role="radiogroup"]>label{padding:12px 28px!important;margin:0!important;border-left:3px solid transparent!important;transition:all .2s ease!important;cursor:pointer!important;border-radius:0!important;background:transparent!important;align-items:center!important}
/* Hide the default radio circle */
section[data-testid="stSidebar"] [role="radiogroup"]>label>div:first-child{display:none!important}
/* Typography inside nav item */
section[data-testid="stSidebar"] [role="radiogroup"]>label p{font-size:14px!important;font-weight:500!important;color:#4b5563!important;margin:0!important;letter-spacing:.3px!important;transition:color .2s ease,font-weight .2s ease!important;font-family:'DM Sans',sans-serif!important}
/* Hover state */
section[data-testid="stSidebar"] [role="radiogroup"]>label:hover{background:#f9fafb!important;border-left-color:#e5e7eb!important}
section[data-testid="stSidebar"] [role="radiogroup"]>label:hover p{color:#111827!important}
/* Selected state (gold accent + warm cream wash) */
section[data-testid="stSidebar"] [role="radiogroup"]>label:has(input:checked){background:linear-gradient(90deg,#fffbeb 0%,#fffbeb 70%,transparent 100%)!important;border-left-color:#c9a96e!important}
section[data-testid="stSidebar"] [role="radiogroup"]>label:has(input:checked) p{color:#111827!important;font-weight:600!important}
/* Override legacy hover rule */
section[data-testid="stSidebar"] .stRadio label:hover{color:inherit!important}
/* Footer brand mark */
.sb-footer{padding:24px 28px;margin-top:24px;border-top:1px solid #f3f4f6}
.sb-footer-line{font-size:10px;letter-spacing:2px;color:#c9a96e;font-weight:700;margin-bottom:4px;font-family:'DM Sans',sans-serif}
.sb-footer-sub{font-size:10px;color:#9ca3af;font-style:italic;font-family:'DM Sans',sans-serif}
</style>
""", unsafe_allow_html=True)

# ─── DATA: outputs del pipeline de modeling ───
# Los resultados del modelo (métricas, mROIs calibrados, escenarios, adstock params)
# se cargan desde el archivo JSON generado por los notebooks de las fases 1-7.
# Ver 04b_coherencia_trazabilidad.ipynb para la trazabilidad entre el β crudo del
# Elastic Net y los mROIs publicados tras calibración ejecutiva.
import json
from pathlib import Path

_MODEL_RESULTS_PATH = Path(__file__).parent / "data" / "model_results.json"
with open(_MODEL_RESULTS_PATH, "r", encoding="utf-8") as _f:
    _MR = json.load(_f)

# Constantes derivadas del output del modelo
BUDGET          = _MR["budget_annual_eur"]
SUPUESTOS       = _MR["mroi_groups"]
SQ_PCT          = _MR["status_quo_mix_historico"]
ADSTOCK_PARAMS  = _MR["adstock_params"]

# Eliminar keys auxiliares (metadatos) que empiezan por "_"
SUPUESTOS       = {k: v for k, v in SUPUESTOS.items() if not k.startswith("_")}
SQ_PCT          = {k: v for k, v in SQ_PCT.items() if not k.startswith("_")}
ADSTOCK_PARAMS  = {k: v for k, v in ADSTOCK_PARAMS.items() if not k.startswith("_")}

# ─── PALETA EDITORIAL · sobreescribe cualquier color que pueda venir del JSON ───
# Esto garantiza que la app SIEMPRE use los colores correctos aunque el JSON
# del repo esté desactualizado por cache de Streamlit Cloud.
_PALETA_GRUPOS = {
    'perf':    '#1e3a5f',  # navy profundo
    'crm':     '#7b3f4d',  # borgoña apagado
    'brand':   '#a8826e',  # terracota empolvado
    'offline': '#4a4e5a',  # carbón cálido
}
for _g, _hex in _PALETA_GRUPOS.items():
    if _g in SUPUESTOS:
        SUPUESTOS[_g]['color'] = _hex

# Escenarios: inyectar SQ_PCT como el mix del S0
_ESC_RAW = {k: v for k, v in _MR["scenarios"].items() if not k.startswith("_")}
ESCENARIOS = {name: {**data, "pesos": SQ_PCT if name.startswith("S0") else data["pesos"]}
              for name, data in _ESC_RAW.items()}

REC = "S3 — Recomendado prudente"

HOLDOUT_WINDOWS = [{'s': '4w', 'r2': .9856, 'm': 6.92}, {'s': '8w', 'r2': .9852, 'm': 4.18}, {'s': '13w', 'r2': .9836, 'm': 3.11}, {'s': '20w', 'r2': .9821, 'm': 2.39}, {'s': '26w', 'r2': .9808, 'm': 2.04}, {'s': '39w', 'r2': .9652, 'm': 2.11}]
INV_HIST = {'Performance Digital': 23.9, 'Brand Digital': 13.9, 'Offline Tradicional': 19.3, 'CRM / Email': 2.9}

# ─── HELPERS ───
def simular(pesos, nivel='base'):
    t = 0; d = {}
    for g, p in pesos.items():
        inv = BUDGET * p
        if nivel == 'base': mr = SUPUESTOS[g]['mroi_base']
        elif nivel == 'pesimista': mr = SUPUESTOS[g]['mroi_pess']
        else: mr = SUPUESTOS[g]['mroi_opt']
        v = inv * mr; d[g] = {'inv': inv, 'mroi': mr, 'ventas': v, 'pct': p}; t += v
    return t, d

def kpi_card(label, value, sub=""):
    return f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'

def sem_html(roi):
    if roi >= 6: return '<span class="semaforo sem-verde"></span> Prudente'
    elif roi >= 3: return '<span class="semaforo sem-amarillo"></span> Moderado'
    return '<span class="semaforo sem-rojo"></span> Agresivo'

def sem_big(roi):
    if roi >= 6: c, d, t = 'sem-g-verde', 'sem-dot-verde', 'Asignación prudente — eficiencia esperada alta'
    elif roi >= 3: c, d, t = 'sem-g-amarillo', 'sem-dot-amarillo', 'Asignación moderada — diversificación equilibrada'
    else: c, d, t = 'sem-g-rojo', 'sem-dot-rojo', 'Asignación agresiva — revisar distribución'
    return f'<div class="semaforo-grande {c}"><div class="sem-dot-big {d}"></div><div class="sem-text">{t}</div></div>'

PL = dict(
    font=dict(family="DM Sans, sans-serif", size=13, color="#374151"),
    paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
    margin=dict(l=55, r=35, t=65, b=55),
)
PL_NO_MARGIN = {k: v for k, v in PL.items() if k != 'margin'}

def style_axes(fig):
    fig.update_xaxes(tickfont=dict(color="#374151", size=12), title_font=dict(color="#374151", size=13), gridcolor="rgba(107,114,128,0.22)", zerolinecolor="rgba(107,114,128,0.35)")
    fig.update_yaxes(tickfont=dict(color="#374151", size=12), title_font=dict(color="#374151", size=13), gridcolor="rgba(107,114,128,0.22)", zerolinecolor="rgba(107,114,128,0.35)")
    fig.update_layout(title_font=dict(size=17, color="#111827"), legend_font=dict(color="#374151", size=12))
    return fig

GC = {'perf': '#1e3a5f', 'crm': '#7b3f4d', 'brand': '#a8826e', 'offline': '#4a4e5a'}
GN = {'perf': 'Performance', 'crm': 'CRM / Loyalty', 'brand': 'Brand Digital', 'offline': 'Offline'}

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-title">K·MODA</div>
        <div class="sb-brand-sub">MMM Decision Studio</div>
    </div>
    <div class="sb-nav-eyebrow">Navegación</div>
    """, unsafe_allow_html=True)
    page = st.radio("Nav", [
        "Resumen Ejecutivo",
        "Simulador",
        "Comparador",
        "Modelo y Confianza",
        "Grupos y Cobertura",
        "Sensibilidad"
    ], label_visibility="collapsed")
    st.markdown("""
    <div class="sb-footer">
        <div class="sb-footer-line">ANÁLISIS EJECUTIVO</div>
        <div class="sb-footer-sub">Presupuesto 2026 · Comité de Dirección</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE 1 — RESUMEN EJECUTIVO (rediseñado: editorial / consulting)
# ═══════════════════════════════════════════════════════════════
if page == "Resumen Ejecutivo":
    # Cálculos base
    rp = ESCENARIOS[REC]['pesos']
    vb, db = simular(rp, 'base')
    vp, _ = simular(rp, 'pesimista')
    vo, _ = simular(rp, 'optimista')
    vsq, _ = simular(SQ_PCT, 'base')
    delta = vb - vsq
    roi = vb / BUDGET

    # ── HERO BLOCK ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-block">
        <div class="hero-eyebrow">
            <span>K-MODA · PRESUPUESTO 2026 · COMITÉ DE DIRECCIÓN</span>
            <div class="hero-eyebrow-line"></div>
        </div>
        <div class="hero-title">
            Reasignar los 12M€ hacia <em>Performance</em> y <em>CRM</em><br>
            estima <span class="accent">+{delta/1e6:.1f} M€</span> de ventas incrementales
        </div>
        <div class="hero-sub">
            El escenario recomendado (S3 — Prudente) concentra la inversión en los canales con mayor
            retorno marginal estimado, manteniendo cobertura estratégica de marca frente a la presión
            competitiva. Las cifras son estimaciones direccionales sobre los 12M€ analizados.
        </div>
        <div class="hero-pill-row">
            <span class="hero-pill hero-pill-gold">
                <span class="hero-pill-dot" style="background:#c9a96e;"></span>
                S3 · Prudente · 50 / 30 / 15 / 5
            </span>
            <span class="hero-pill hero-pill-blue">
                <span class="hero-pill-dot" style="background:#1e3a5f;"></span>
                Confianza metodológica · Media-Alta
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3 METRIC HEROES ─────────────────────────────────────────
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(f"""
        <div class="metric-hero">
            <div class="metric-hero-accent" style="background:linear-gradient(90deg,#1e3a5f,#4a6b8c);"></div>
            <div>
                <div class="metric-hero-label">Ventas incrementales</div>
                <div class="metric-hero-value">{vb/1e6:.1f}<span class="metric-hero-unit"> M€</span></div>
                <div class="metric-hero-caption">Rango pesimista–optimista<br><strong style="color:#111827;">{vp/1e6:.0f} – {vo/1e6:.0f} M€</strong></div>
            </div>
            <div class="metric-hero-badge badge-neutral">Bajo supuestos base del modelo MMM</div>
        </div>
        """, unsafe_allow_html=True)
    with mc2:
        st.markdown(f"""
        <div class="metric-hero">
            <div class="metric-hero-accent" style="background:linear-gradient(90deg,#c9a96e,#e0bf7a);"></div>
            <div>
                <div class="metric-hero-label">ROI atribuido esperado</div>
                <div class="metric-hero-value">{roi:.1f}<span class="metric-hero-unit">x</span></div>
                <div class="metric-hero-caption">Retorno estimado sobre los<br><strong style="color:#111827;">12M€ de presupuesto anual</strong></div>
            </div>
            <div class="metric-hero-badge badge-gold">Incluye ajustes por efectos de largo plazo</div>
        </div>
        """, unsafe_allow_html=True)
    with mc3:
        mejora_pct = (delta/vsq*100) if vsq > 0 else 0
        st.markdown(f"""
        <div class="metric-hero">
            <div class="metric-hero-accent" style="background:linear-gradient(90deg,#5f7a6a,#85a194);"></div>
            <div>
                <div class="metric-hero-label">Mejora vs Status Quo</div>
                <div class="metric-hero-value">+{delta/1e6:.1f}<span class="metric-hero-unit"> M€</span></div>
                <div class="metric-hero-caption">Oportunidad estimada frente a la<br><strong style="color:#111827;">distribución histórica</strong></div>
            </div>
            <div class="metric-hero-badge badge-up">▲ {mejora_pct:.0f}% sobre el baseline histórico</div>
        </div>
        """, unsafe_allow_html=True)

    # ── SECCIÓN: LA RECOMENDACIÓN ───────────────────────────────
    st.markdown('<div class="section-divider"><div class="section-divider-line"></div><div class="section-divider-label">LA RECOMENDACIÓN</div><div class="section-divider-line"></div></div>', unsafe_allow_html=True)

    rc1, rc2 = st.columns([5, 6])
    with rc1:
        fig_donut = go.Figure(go.Pie(
            labels=[GN[k] for k in rp],
            values=[rp[k]*100 for k in rp],
            hole=.64,
            marker=dict(colors=[GC[k] for k in rp], line=dict(color='white', width=3)),
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='horizontal',
            textfont=dict(size=13, color='#ffffff', family='DM Sans'),
            hovertemplate='<b>%{label}</b><br>%{value:.0f}% · €%{customdata:,.0f}<extra></extra>',
            customdata=[BUDGET*rp[k] for k in rp],
            sort=False,
            rotation=90,
        ))
        fig_donut.update_layout(
            showlegend=False,
            height=460,
            margin=dict(l=20, r=20, t=10, b=10),
            **PL_NO_MARGIN,
        )
        fig_donut.add_annotation(
            text="<span style='font-family:Playfair Display;font-size:38px;font-weight:700;color:#111827;'>12M€</span>",
            x=.5, y=.56, showarrow=False,
        )
        fig_donut.add_annotation(
            text="<span style='font-family:DM Sans;font-size:11px;color:#6b7280;letter-spacing:2px;'>PRESUPUESTO ANUAL</span>",
            x=.5, y=.44, showarrow=False,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with rc2:
        mix_html = '<div class="rec-panel"><div class="rec-panel-title">El Mix Propuesto</div><div class="rec-panel-sub">Asignación por grupo de canal · 12M€ total</div>'
        conf_col_map = {'ALTA': '#5f7a6a', 'MEDIA': '#a8826e', 'BAJA': '#9ca3af'}
        for g in ['perf', 'crm', 'brand', 'offline']:
            s = SUPUESTOS[g]
            pct = rp[g] * 100
            eur = rp[g] * BUDGET / 1e6
            mroi_col = conf_col_map[s['confianza']]
            bar_w = min(pct * 2, 100)  # width: 50%→100, 30%→60, 15%→30, 5%→10
            mix_html += (
                f'<div class="alloc-row-mini">'
                f'<div class="alloc-dot-mini" style="background:{s["color"]};"></div>'
                f'<div class="alloc-name-mini">{s["nombre"]}</div>'
                f'<div class="alloc-bar-mini"><div class="alloc-bar-fill-mini" style="width:{bar_w}%;background:linear-gradient(90deg,{s["color"]} 0%,{s["color"]}cc 100%);"></div></div>'
                f'<div class="alloc-pct-mini">{pct:.0f}%</div>'
                f'<div class="alloc-eur-mini">{eur:.1f} M€</div>'
                f'<div class="alloc-mroi-mini" style="background:{mroi_col}15;color:{mroi_col};border:1px solid {mroi_col}30;">{s["mroi_base"]}x</div>'
                f'</div>'
            )
        mix_html += (
            '<div class="decision-box">'
            '<div class="decision-label">Lógica de la recomendación</div>'
            '<div class="decision-text">'
            'Mover peso desde <strong>Offline</strong> (sobreasignado históricamente con 32%) hacia '
            '<strong>CRM</strong> (la palanca más infrautilizada, solo 5% histórico) y '
            '<strong>Performance Digital</strong> (mayor señal del modelo). Se mantiene '
            '<strong>Brand Digital</strong> al 15% como cobertura frente a la presión competitiva del '
            'Ultra-Fast Fashion.'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(mix_html, unsafe_allow_html=True)

    # ── SECCIÓN: CONTEXTO DE IMPACTO ────────────────────────────
    st.markdown('<div class="section-divider"><div class="section-divider-line"></div><div class="section-divider-label">CONTEXTO DE IMPACTO</div><div class="section-divider-line"></div></div>', unsafe_allow_html=True)

    TOTAL_VENTAS = _MR["dataset"]["ventas_totales_estimadas_anuales_meur"]
    mkt_pct = vb / (TOTAL_VENTAS * 1e6) * 100
    base_pct = 100 - mkt_pct
    base_m = TOTAL_VENTAS - vb/1e6

    cx1, cx2 = st.columns([6, 4])
    with cx1:
        fig_dec = go.Figure()
        fig_dec.add_trace(go.Bar(
            name='Línea base', x=[base_pct], y=[''], orientation='h',
            marker=dict(color='#e5e7eb', line=dict(width=0)),
            text=[f'<b>Línea base orgánica</b>    {base_m:.0f} M€ · {base_pct:.0f}%'],
            textposition='inside',
            textfont=dict(size=13, color='#374151', family='DM Sans'),
            hovertemplate='Línea base: %{x:.0f}%<extra></extra>',
            insidetextanchor='middle',
        ))
        fig_dec.add_trace(go.Bar(
            name='Marketing', x=[mkt_pct], y=[''], orientation='h',
            marker=dict(color='#c9a96e', line=dict(width=0)),
            text=[f'<b>Marketing</b>  {vb/1e6:.0f} M€ · {mkt_pct:.0f}%'],
            textposition='inside',
            textfont=dict(size=13, color='#ffffff', family='DM Sans'),
            hovertemplate='Marketing: %{x:.0f}%<extra></extra>',
            insidetextanchor='middle',
        ))
        fig_dec.update_layout(
            barmode='stack', height=110, showlegend=False,
            yaxis=dict(visible=False, fixedrange=True),
            xaxis=dict(visible=False, range=[0, 100], fixedrange=True),
            margin=dict(l=0, r=0, t=20, b=10),
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font=dict(family="DM Sans, sans-serif"),
        )
        st.plotly_chart(fig_dec, use_container_width=True)

        st.markdown(f"""
        <div style='font-size:15px;color:#374151;line-height:1.7;margin-top:6px;padding:0 4px;'>
            De las <strong style='color:#111827;'>~{TOTAL_VENTAS} M€</strong> de ventas anuales estimadas, el escenario recomendado
            proyecta que <strong style='color:#c9a96e;'>~{mkt_pct:.0f}%</strong> se vincularía a la inversión en medios bajo el mix propuesto —
            vs. <strong style='color:#6b7280;'>~{(vsq/1e6)/TOTAL_VENTAS*100:.0f}%</strong> bajo el Status Quo histórico.
            El resto corresponde a la <strong style='color:#374151;'>línea base orgánica</strong>:
            ventas explicadas por estacionalidad, tendencia, marca acumulada y factores no pagados.
        </div>
        <div style='font-size:13px;color:#6b7280;line-height:1.5;margin-top:12px;padding:10px 14px;background:#f9fafb;border-radius:10px;border-left:3px solid #e5e7eb;'>
            <strong>Nota:</strong> La diferencia entre ambos escenarios (~{(mkt_pct - (vsq/1e6)/TOTAL_VENTAS*100):.0f} pp) refleja el valor teórico de la reasignación hacia canales de mayor retorno marginal. Es una proyección del simulador, no una garantía — se validará con tests geo durante Q1–Q2 2026.
        </div>
        """, unsafe_allow_html=True)

    with cx2:
        st.markdown(f"""
        <div class="contrib-card">
            <div class="contrib-label">CONTRIBUCIÓN DEL MARKETING</div>
            <div class="contrib-value">
                {mkt_pct:.0f}<span class="contrib-pct-symbol">%</span>
            </div>
            <div class="contrib-caption">
                de las ventas totales estimadas de K-Moda provienen de la inversión en medios bajo el escenario recomendado.
            </div>
            <hr class="contrib-divider">
            <div class="contrib-meta">
                Estimación basada en modelo MMM · Elastic Net<br>
                MAPE = 12,47% en holdout · R² = 0,847
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── SECCIÓN: VISIÓN COMPARADA ───────────────────────────────
    st.markdown('<div class="section-divider"><div class="section-divider-line"></div><div class="section-divider-label">VISIÓN COMPARADA</div><div class="section-divider-line"></div></div>', unsafe_allow_html=True)

    en = list(ESCENARIOS.keys())
    short_labels = {'S0 — Status Quo': 'Status Quo', 'S1 — Perf + CRM': 'Crec. digital', 'S2 — Eficiencia máxima': 'Eficiencia máx.', 'S3 — Recomendado prudente': 'Recomendado ★'}
    sl = [short_labels.get(e, e) for e in en]
    vbs = [simular(ESCENARIOS[e]['pesos'], 'base')[0]/1e6 for e in en]
    vps = [simular(ESCENARIOS[e]['pesos'], 'pesimista')[0]/1e6 for e in en]
    vos = [simular(ESCENARIOS[e]['pesos'], 'optimista')[0]/1e6 for e in en]
    bar_colors = ['#9ca3af', '#1e3a5f', '#7b3f4d', '#c9a96e']

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name='Ventas incrementales (base)', x=sl, y=vbs, marker_color=bar_colors,
        text=[f'<b>{v:.0f}</b>' for v in vbs], textposition='outside',
        textfont=dict(size=18, family='Playfair Display', color='#111827'),
        width=0.58,
        hovertemplate='<b>%{x}</b><br>Base: %{y:.1f} M€<extra></extra>',
    ))
    fig2.add_trace(go.Scatter(
        name='Rango', x=sl, y=vbs,
        error_y=dict(type='data', symmetric=False,
                     array=[o-b for o, b in zip(vos, vbs)],
                     arrayminus=[b-p for b, p in zip(vbs, vps)],
                     color='#374151', thickness=2.5, width=14),
        mode='markers', marker=dict(size=.1, color='rgba(0,0,0,0)'),
        showlegend=False,
        hoverinfo='skip',
    ))
    # Anotación apuntando al recomendado
    rec_idx = en.index(REC)
    fig2.add_annotation(
        x=sl[rec_idx], y=vos[rec_idx] + 4,
        text="<b>★ Recomendación ejecutiva</b>",
        showarrow=True, arrowhead=0, arrowcolor='#c9a96e', arrowwidth=2,
        ax=0, ay=-38,
        font=dict(size=12, color='#78350f', family='DM Sans'),
        bgcolor='#fffbeb', bordercolor='#c9a96e', borderwidth=1.5,
        borderpad=7, opacity=1,
    )
    fig2.update_layout(
        title=dict(text="Ventas incrementales estimadas por escenario · M€",
                   font=dict(size=16, color="#111827", family='Playfair Display')),
        yaxis_title="M€",
        yaxis=dict(gridcolor="rgba(107,114,128,0.15)", zeroline=True, zerolinecolor="#d1d5db",
                   range=[0, max(vos) * 1.22]),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        height=440,
        showlegend=False,
        bargap=0.45,
        **PL_NO_MARGIN,
        margin=dict(l=55, r=35, t=80, b=55),
    )
    style_axes(fig2)
    st.plotly_chart(fig2, use_container_width=True)

    # Leyenda del rango
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;justify-content:center;margin-top:-18px;font-size:12px;color:#6b7280;'>
        <div style='width:2px;height:14px;background:#374151;'></div>
        <span>Líneas verticales: rango pesimista–optimista según supuestos de mROI</span>
    </div>
    """, unsafe_allow_html=True)

    # ── SECCIÓN: PARA EL COMITÉ ─────────────────────────────────
    st.markdown('<div class="section-divider"><div class="section-divider-line"></div><div class="section-divider-label">PARA EL COMITÉ</div><div class="section-divider-line"></div></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="takeaway-grid">
        <div class="takeaway-card">
            <div class="takeaway-num">01</div>
            <div class="takeaway-head">Decisión propuesta</div>
            <div class="takeaway-body">
                Adoptar el escenario <strong>S3 — Prudente</strong> (50/30/15/5) como asignación ejecutiva
                para el ciclo 2026, manteniendo los <strong>12M€</strong> de presupuesto total sin recortes.
            </div>
        </div>
        <div class="takeaway-card">
            <div class="takeaway-num">02</div>
            <div class="takeaway-head">Evidencia metodológica</div>
            <div class="takeaway-body">
                Modelo MMM con Adstock calibrado y regularización <strong>Elastic Net</strong>.
                <strong>MAPE = 12,47%</strong> en holdout — señal direccional robusta, con ajustes documentados por efectos de largo plazo.
            </div>
        </div>
        <div class="takeaway-card">
            <div class="takeaway-num">03</div>
            <div class="takeaway-head">Siguientes pasos</div>
            <div class="takeaway-body">
                Validar la reasignación mediante <strong>seguimiento mensual</strong> y tests controlados
                (geo-experiments o holdouts) durante <strong>Q1–Q2 2026</strong> antes de consolidar la política.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer disclaimer
    st.markdown("""
    <div style='margin-top:36px;padding:18px 24px;background:#f9fafb;border:1px dashed #e5e7eb;border-radius:12px;font-size:12px;color:#6b7280;line-height:1.6;'>
        <strong style='color:#374151;'>Alcance de las estimaciones.</strong>
        Todas las cifras presentadas son estimaciones direccionales diseñadas para apoyar la decisión presupuestaria,
        no proyecciones financieras garantizadas. Los mROIs combinan la señal del modelo con ajustes por efectos de
        largo plazo no capturados en la ventana temporal de análisis. La recomendación debe validarse con seguimiento
        operativo y tests controlados antes de su consolidación definitiva.
    </div>
    """, unsafe_allow_html=True)


# ═══ PAGE 2: SIMULADOR ═══
elif page == "Simulador":
    st.markdown('<div class="section-header">Construye tu escenario</div>', unsafe_allow_html=True)
    st.markdown("¿Qué pasa si cambias el mix? Ajusta los porcentajes y observa el impacto estimado sobre los **12M€**.")
    if 'sp' not in st.session_state: st.session_state.sp = {'perf': 50, 'crm': 30, 'brand': 15, 'offline': 5}
    presets = {'Status Quo': {'perf':40,'crm':5,'brand':23,'offline':32}, 'Crecimiento digital': {'perf':45,'crm':30,'brand':20,'offline':5}, 'Eficiencia máx.': {'perf':55,'crm':35,'brand':10,'offline':0}, 'Recomendado ★': {'perf':50,'crm':30,'brand':15,'offline':5}, 'Balanced': {'perf':35,'crm':25,'brand':25,'offline':15}}
    pc = st.columns(len(presets))
    for i, (pn, pw) in enumerate(presets.items()):
        with pc[i]:
            if st.button(pn, use_container_width=True, key=f"p_{i}"):
                st.session_state.sp = dict(pw); st.rerun()
    st.markdown("")
    cl, _, cr = st.columns([4.5, .2, 6.3])
    go_ = ['perf', 'crm', 'brand', 'offline']
    cc_ = {'ALTA': '#5f7a6a', 'MEDIA': '#a8826e', 'BAJA': '#9ca3af'}
    with cl:
        np_ = {}
        for g in go_:
            s = SUPUESTOS[g]; ci, cn = st.columns([1, 3])
            with ci: v = st.number_input(s['nombre'], 0, 100, st.session_state.sp[g], 5, key=f"n_{g}", label_visibility="collapsed"); np_[g] = v
            with cn:
                eu = BUDGET*v/100; cc = cc_.get(s['confianza'], '#6b7280')
                st.markdown(f'<div class="alloc-card"><div class="alloc-header"><div class="alloc-dot" style="background:{s["color"]};"></div><div class="alloc-name">{s["nombre"]}</div><div class="alloc-mroi-tag" style="background:{cc};">{s["mroi_base"]}x mROI</div></div><div class="alloc-detail"><div><div class="alloc-euros">{eu/1e6:.2f} M€</div><div class="alloc-sub-text">{v}% del presupuesto</div></div><div style="text-align:right;"><div style="font-size:11px;color:#6b7280;">Confianza</div><div style="font-weight:700;color:{cc};font-size:13px;">{s["confianza"]}</div></div></div></div>', unsafe_allow_html=True)
        tp = sum(np_.values())
        seg = "".join(f'<div class="budget-segment" style="width:{np_[g]}%;background:{SUPUESTOS[g]["color"]};">{np_[g]}%</div>' for g in go_ if np_[g] > 0)
        st.markdown(f'<div style="margin-top:12px;"><div style="font-size:12px;font-weight:600;color:#4b5563;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Distribución visual</div><div class="budget-bar-wrap">{seg}</div><div class="budget-bar-labels"><span>0 €</span><span>6 M€</span><span>12 M€</span></div></div>', unsafe_allow_html=True)
        if tp == 100:
            st.markdown(f'<div class="sum-indicator sum-ok">✓ Presupuesto asignado correctamente</div>', unsafe_allow_html=True); ok = True
        else:
            d = 100 - tp
            st.markdown(f'<div class="sum-indicator sum-error">Total: {tp}% — {"Faltan" if d>0 else "Sobran"} {abs(d)} pp para completar el 100%</div>', unsafe_allow_html=True); ok = False
    with cr:
        if ok:
            ps = {g: np_[g]/100 for g in go_}
            vb, db = simular(ps, 'base'); vp, _ = simular(ps, 'pesimista'); vo, _ = simular(ps, 'optimista')
            rb = vb/BUDGET; vsq, _ = simular(SQ_PCT, 'base'); dl = vb - vsq
            sn = "+" if dl >= 0 else ""; dc = "#5f7a6a" if dl >= 0 else "#9c5a5a"
            st.markdown(f'<div class="results-panel"><div class="results-title">Resultados estimados</div><div style="display:flex;gap:24px;"><div style="flex:1;"><div class="result-metric"><div class="result-label">Ventas Incrementales</div><div class="result-value">{vb/1e6:.1f}<span style="font-size:18px;color:#111827;"> M€</span></div><div class="result-sub">Rango {vp/1e6:.1f} – {vo/1e6:.1f} M€</div></div></div><div style="flex:1;"><div class="result-metric"><div class="result-label">ROI Esperado</div><div class="result-value">{rb:.1f}<span style="font-size:18px;color:#111827;">x</span></div><div class="result-sub">Sobre 12M€</div></div></div><div style="flex:1;"><div class="result-metric"><div class="result-label">vs Status Quo</div><div class="result-value" style="color:{dc};">{sn}{dl/1e6:.1f}<span style="font-size:18px;"> M€</span></div><div class="result-sub">Diferencia estimada</div></div></div></div><hr class="result-divider">{sem_big(rb)}</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

            # Waterfall only
            vg = [db[g]['ventas']/1e6 for g in go_]
            fig = go.Figure(go.Waterfall(name="Contribución", orientation="v", measure=["relative"]*4+["total"], x=[GN[g] for g in go_]+["TOTAL"], y=vg+[0], text=[f"{x:.1f}M" for x in vg]+[f"{vb/1e6:.1f}M"], textposition="outside", connector=dict(line=dict(color="#d1d5db", width=1, dash="dot")), increasing=dict(marker=dict(color="#1e3a5f")), decreasing=dict(marker=dict(color="#9c5a5a")), totals=dict(marker=dict(color="#c9a96e"))))
            fig.update_layout(title="Contribución por Grupo a Ventas Incrementales", yaxis_title="M€", showlegend=False, height=380, **PL)
            st.plotly_chart(style_axes(fig), use_container_width=True)

            # Interpretive text
            bg = max(ps, key=lambda k: db[k]['ventas'])
            vd = f"genera <strong>{sn}{dl/1e6:.0f} M€ más</strong> que el Status Quo" if dl > 0 else (f"genera <strong>{abs(dl)/1e6:.0f} M€ menos</strong> que el Status Quo" if dl < 0 else "iguala al Status Quo")
            st.markdown(f'<div class="interp-msg">Tu asignación {vd}. El grupo con mayor contribución es <strong>{GN[bg]}</strong> ({ps[bg]*100:.0f}% → {db[bg]["ventas"]/1e6:.1f}M€). El rango de incertidumbre oscila entre <strong>{vp/1e6:.1f}</strong> y <strong>{vo/1e6:.1f} M€</strong>.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="results-panel" style="text-align:center;padding:60px 28px;"><div class="results-title">Ajusta la asignación</div><div style="font-size:48px;margin:20px 0;">⚖️</div><div style="color:#6b7280;font-size:15px;">Los porcentajes deben sumar exactamente 100%<br>para calcular los resultados.</div></div>', unsafe_allow_html=True)


# ═══ PAGE 3: COMPARADOR ═══
elif page == "Comparador":
    st.markdown('<div class="section-header">Comparador de Escenarios</div>', unsafe_allow_html=True)

    # ── Comparison cards ──
    vsq_base, _ = simular(SQ_PCT, 'base')
    esc_data = {}
    for en, es in ESCENARIOS.items():
        vb, db = simular(es['pesos'], 'base')
        vp, _ = simular(es['pesos'], 'pesimista')
        vo, _ = simular(es['pesos'], 'optimista')
        esc_data[en] = {'vb': vb, 'vp': vp, 'vo': vo, 'roi': vb/BUDGET, 'delta': vb - vsq_base, 'det': db, 'pesos': es['pesos']}

    colors_esc = {'S0 — Status Quo': '#6b7280', 'S1 — Perf + CRM': '#1e3a5f', 'S2 — Eficiencia máxima': '#7b3f4d', 'S3 — Recomendado prudente': '#c9a96e'}

    cols = st.columns(4)
    for i, (en, ed) in enumerate(esc_data.items()):
        col_c = colors_esc.get(en, '#6b7280')
        delta_s = f"+{ed['delta']/1e6:.1f}" if ed['delta'] >= 0 else f"{ed['delta']/1e6:.1f}"
        delta_c = "#5f7a6a" if ed['delta'] >= 0 else "#9c5a5a"
        star = " ★" if "Recomendado" in en else ""
        with cols[i]:
            st.markdown(f"""<div style="background:#fff;border:2px solid {col_c};border-radius:16px;padding:20px;text-align:center;min-height:260px;">
                <div style="font-size:11px;font-weight:700;color:{col_c};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">{en.split(' — ')[1]}{star}</div>
                <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:#111827;">{ed['vb']/1e6:.1f} M€</div>
                <div style="font-size:12px;color:#6b7280;margin-top:2px;">Ventas incrementales</div>
                <div style="margin:12px 0;border-top:1px solid #e5e7eb;"></div>
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="font-size:12px;color:#6b7280;">ROI</span>
                    <span style="font-size:14px;font-weight:700;color:#111827;">{ed['roi']:.1f}x</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="font-size:12px;color:#6b7280;">vs Status Quo</span>
                    <span style="font-size:14px;font-weight:700;color:{delta_c};">{delta_s} M€</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="font-size:12px;color:#6b7280;">Rango</span>
                    <span style="font-size:12px;color:#374151;">{ed['vp']/1e6:.0f} – {ed['vo']/1e6:.0f} M€</span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts: bars + mix ──
    el = list(ESCENARIOS.keys())
    short = {'S0 — Status Quo': 'Status Quo', 'S1 — Perf + CRM': 'Crec. digital', 'S2 — Eficiencia máxima': 'Eficiencia máx.', 'S3 — Recomendado prudente': 'Recomendado ★'}
    sl = [short.get(e, e) for e in el]
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Ventas Incrementales (M€)", "Composición del Mix"], column_widths=[.55, .45])
    vbs = [esc_data[e]['vb']/1e6 for e in el]; vps = [esc_data[e]['vp']/1e6 for e in el]; vos = [esc_data[e]['vo']/1e6 for e in el]
    fig.add_trace(go.Bar(name='Base', x=sl, y=vbs, marker_color=[colors_esc[e] for e in el], text=[f'{v:.0f}M' for v in vbs], textposition='outside'), row=1, col=1)
    fig.add_trace(go.Scatter(name='Rango', x=sl, y=vbs, error_y=dict(type='data', symmetric=False, array=[o-b for o,b in zip(vos,vbs)], arrayminus=[b-p for b,p in zip(vbs,vps)], color='#374151', thickness=2, width=6), mode='markers', marker=dict(size=.1, color='rgba(0,0,0,0)')), row=1, col=1)
    for g in ['perf','crm','brand','offline']:
        fig.add_trace(go.Bar(name=GN[g], x=sl, y=[ESCENARIOS[e]['pesos'][g]*100 for e in el], marker_color=GC[g], showlegend=True), row=1, col=2)
    fig.update_layout(barmode='stack', height=420, legend=dict(orientation='h', y=-.2), **PL)
    fig.update_yaxes(title_text="M€", row=1, col=1); fig.update_yaxes(title_text="%", row=1, col=2)
    style_axes(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── BCG Matrix: mROI vs Inversión por Grupo ──
    st.markdown("### Matriz BCG — Grupos de Canales")
    st.markdown("Posición de cada grupo según su **eficiencia estimada** (mROI) y su **peso en el presupuesto recomendado** (S3).")

    rec_p = ESCENARIOS[REC]['pesos']
    # Data: [perf, crm, brand, offline] — mROIs vienen de SUPUESTOS (dinámico, no hardcoded)
    bcg = [
        {'g': 'perf',    'x': rec_p['perf']*100,    'y': SUPUESTOS['perf']['mroi_base'],    'sz': 38, 'label_pos': 'bottom center'},
        {'g': 'crm',     'x': rec_p['crm']*100,     'y': SUPUESTOS['crm']['mroi_base'],     'sz': 30, 'label_pos': 'top center'},
        {'g': 'brand',   'x': rec_p['brand']*100,   'y': SUPUESTOS['brand']['mroi_base'],   'sz': 22, 'label_pos': 'top center'},
        {'g': 'offline', 'x': rec_p['offline']*100, 'y': SUPUESTOS['offline']['mroi_base'], 'sz': 16, 'label_pos': 'top center'},
    ]

    fig_bcg = go.Figure()

    # Quadrant shading
    fig_bcg.add_shape(type="rect", x0=0, x1=35, y0=3, y1=13, fillcolor="rgba(95,122,106,0.04)", line=dict(width=0))
    fig_bcg.add_shape(type="rect", x0=35, x1=65, y0=3, y1=13, fillcolor="rgba(30,58,95,0.04)", line=dict(width=0))
    fig_bcg.add_shape(type="rect", x0=0, x1=35, y0=-0.5, y1=3, fillcolor="rgba(156,163,175,0.04)", line=dict(width=0))
    fig_bcg.add_shape(type="rect", x0=35, x1=65, y0=-0.5, y1=3, fillcolor="rgba(220,38,38,0.04)", line=dict(width=0))

    # Bubbles
    for b in bcg:
        inv_m = rec_p[b['g']] * BUDGET / 1e6
        fig_bcg.add_trace(go.Scatter(
            x=[b['x']], y=[b['y']], mode='markers',
            marker=dict(size=b['sz'], color=GC[b['g']], opacity=0.75, line=dict(width=2, color='#ffffff')),
            name=f"{GN[b['g']]} ({inv_m:.1f}M€)",
            hovertemplate=f"<b>{GN[b['g']]}</b><br>{b['x']:.0f}% del presupuesto<br>mROI: {b['y']}x<br>Inversión: {inv_m:.1f}M€<extra></extra>",
            showlegend=True,
        ))

    # Labels as annotations (no overlap) — posiciones dinámicas desde SUPUESTOS
    fig_bcg.add_annotation(x=50, y=SUPUESTOS['perf']['mroi_base'],    text=f"<b>Performance</b><br>{rec_p['perf']*BUDGET/1e6:.1f}M€ · {rec_p['perf']*100:.0f}%",    font=dict(size=12, color="#1e3a5f"), showarrow=True, arrowhead=0, arrowcolor="#1e3a5f", arrowwidth=1, ax=55, ay=-40)
    fig_bcg.add_annotation(x=30, y=SUPUESTOS['crm']['mroi_base'],     text=f"<b>CRM / Loyalty</b><br>{rec_p['crm']*BUDGET/1e6:.1f}M€ · {rec_p['crm']*100:.0f}%",     font=dict(size=12, color="#7b3f4d"), showarrow=True, arrowhead=0, arrowcolor="#7b3f4d", arrowwidth=1, ax=-70, ay=-35)
    fig_bcg.add_annotation(x=15, y=SUPUESTOS['brand']['mroi_base'],   text=f"<b>Brand Digital</b><br>{rec_p['brand']*BUDGET/1e6:.1f}M€ · {rec_p['brand']*100:.0f}%",   font=dict(size=12, color="#a8826e"), showarrow=True, arrowhead=0, arrowcolor="#a8826e", arrowwidth=1, ax=60, ay=-30)
    fig_bcg.add_annotation(x=5,  y=SUPUESTOS['offline']['mroi_base'], text=f"<b>Offline</b><br>{rec_p['offline']*BUDGET/1e6:.1f}M€ · {rec_p['offline']*100:.0f}%", font=dict(size=12, color="#6b7280"), showarrow=True, arrowhead=0, arrowcolor="#6b7280", arrowwidth=1, ax=55, ay=25)

    # Quadrant lines
    fig_bcg.add_hline(y=3.0, line_dash="dot", line_color="#d1d5db", line_width=1)
    fig_bcg.add_vline(x=35, line_dash="dot", line_color="#d1d5db", line_width=1)

    # Quadrant labels in corners
    fig_bcg.add_annotation(x=1, y=12.5, text="<b>OPORTUNIDAD</b>", font=dict(size=10, color="#5f7a6a"), showarrow=False, xanchor='left')
    fig_bcg.add_annotation(x=64, y=12.5, text="<b>ALTA PRIORIDAD</b>", font=dict(size=10, color="#1e3a5f"), showarrow=False, xanchor='right')
    fig_bcg.add_annotation(x=1, y=-0.2, text="<b>REVISAR</b>", font=dict(size=10, color="#9ca3af"), showarrow=False, xanchor='left')
    fig_bcg.add_annotation(x=64, y=-0.2, text="<b>RIESGO</b>", font=dict(size=10, color="#9c5a5a"), showarrow=False, xanchor='right')

    fig_bcg.update_layout(
        title="Posición estratégica por grupo de canal",
        xaxis_title="% del presupuesto (S3 Recomendado)",
        yaxis_title="mROI estimado",
        height=500,
        showlegend=True,
        legend=dict(orientation='h', y=-.12, font=dict(size=11)),
        xaxis=dict(range=[-2, 67], dtick=10),
        yaxis=dict(range=[-1, 13.5], dtick=2),
        **PL,
    )
    style_axes(fig_bcg)
    st.plotly_chart(fig_bcg, use_container_width=True)

    st.markdown("""<div class="callout-gold">
        <strong>Lectura de la matriz:</strong> Performance Digital ocupa la posición de <strong>Alta Prioridad</strong> (alta inversión + alto retorno esperado).
        CRM/Loyalty es la gran <strong>Oportunidad</strong> — alto mROI pero históricamente infrautilizado.
        Brand Digital tiene retorno moderado pero cumple función de protección de marca.
        Offline se mantiene como cobertura institucional mínima.
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Scenario detail expanders ──
    for en, es in ESCENARIOS.items():
        with st.expander(f"{en}  ·  {es['desc']}"):
            st.write(f"**Lógica:** {es['logica']}"); _, dt = simular(es['pesos'], 'base')
            for g in ['perf','crm','brand','offline']: st.write(f"- **{GN[g]}**: {es['pesos'][g]*100:.0f}% → {dt[g]['inv']/1e6:.1f}M€ → {dt[g]['ventas']/1e6:.1f}M€ ventas inc. (mROI {dt[g]['mroi']}x)")


# ═══ PAGE 4: MODELO Y CONFIANZA ═══
elif page == "Modelo y Confianza":
    st.markdown('<div class="section-header">Modelo y Confianza</div>', unsafe_allow_html=True)

    # ── Ecuación maestra del MMM (especificada en el PDF del caso) ──
    st.markdown("""
    <div style="background:#f9fafb;border:1px solid #e5e7eb;border-left:4px solid #c9a96e;border-radius:0 14px 14px 0;padding:22px 28px;margin:8px 0 24px;">
        <div style="font-size:11px;color:#c9a96e;letter-spacing:2.5px;font-weight:700;margin-bottom:14px;">ECUACIÓN MAESTRA · MARKETING MIX MODEL</div>
        <div style="font-family:'Playfair Display',serif;font-size:28px;color:#111827;text-align:center;margin:8px 0 18px;font-style:italic;line-height:1.2;">
            Ŷ<sub style="font-size:15px;color:#6b7280;">t</sub>
            <span style="color:#c9a96e;font-style:normal;font-weight:400;">  =  </span>
            <strong>β<sub style="font-size:15px;color:#6b7280;font-weight:400;">0</sub></strong>
            <span style="color:#c9a96e;font-style:normal;font-weight:400;">  +  </span>
            Σ β<sub style="font-size:15px;color:#6b7280;">m</sub>
            <span style="color:#374151;"> · </span>
            A<sub style="font-size:15px;color:#6b7280;">t,m</sub>
            <span style="color:#c9a96e;font-style:normal;font-weight:400;">  +  </span>
            Σ δ<sub style="font-size:15px;color:#6b7280;">j</sub>
            <span style="color:#374151;"> · </span>
            C<sub style="font-size:15px;color:#6b7280;">t,j</sub>
            <span style="color:#c9a96e;font-style:normal;font-weight:400;">  +  </span>
            <strong>ε<sub style="font-size:15px;color:#6b7280;font-weight:400;">t</sub></strong>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px 32px;font-size:13px;color:#374151;line-height:1.6;margin-top:14px;border-top:1px solid #e5e7eb;padding-top:16px;">
            <div><strong style="color:#111827;">β<sub>0</sub> · constante</strong> — línea base orgánica de ventas (lo que ocurriría sin marketing).</div>
            <div><strong style="color:#111827;">Σ β<sub>m</sub> · A<sub>t,m</sub> · medios</strong> — peso de cada canal sobre su inversión con adstock aplicado.</div>
            <div><strong style="color:#111827;">Σ δ<sub>j</sub> · C<sub>t,j</sub> · controles exógenos</strong> — variables que K-Moda no controla (calendario, clima, festivos, COVID).</div>
            <div><strong style="color:#111827;">ε<sub>t</sub> · ruido</strong> — error residual asumido como gaussiano N(0, σ).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── A. How the model works (visual) ──
    st.markdown("### Cómo funciona el modelo")
    a1, a2 = st.columns([3, 2])
    with a1:
        st.markdown("""<div class="callout-blue">
            <strong>Pipeline en 3 pasos:</strong><br><br>
            <strong>1.</strong> Se construye una línea base de ventas a partir de estacionalidad, calendario y clima (explica el 80,2% de la varianza).<br>
            <strong>2.</strong> Sobre los residuales, se mide la señal marginal de la inversión en medios (4,5% adicional).<br>
            <strong>3.</strong> Los mROIs se estiman combinando señal del modelo con ajustes por efectos no capturados en la ventana temporal, y se usan para simular la reasignación de los 12M€.
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:16px 20px;margin-top:12px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-size:13px;font-weight:600;color:#6b7280;">MAPE (error medio)</span>
                <span style="font-family:'Playfair Display',serif;font-size:24px;font-weight:700;color:#111827;">12,47%</span>
            </div>
            <div style="font-size:12px;color:#4b5563;">Error medio de predicción en holdout — aceptable para datos agregados semanales. En línea con el objetivo de error asumido para el caso.</div>
        </div>""", unsafe_allow_html=True)
    with a2:
        # Variance decomposition donut
        fig_v = go.Figure(go.Pie(
            labels=['Baseline<br>(estacionalidad)', 'Señal de<br>medios', 'Residual<br>(ruido)'],
            values=[80.2, 4.5, 15.3],
            hole=.55,
            marker=dict(colors=['#1e3a5f', '#c9a96e', '#e5e7eb'], line=dict(color='#ffffff', width=2)),
            textinfo='label+percent', textfont=dict(size=11, color='#374151'),
            hovertemplate='%{label}: %{value}%<extra></extra>',
            sort=False,
        ))
        fig_v.update_layout(title="Descomposición de la varianza", showlegend=False, height=340, **PL)
        fig_v.add_annotation(text="<b>R² = 0,847</b>", x=.5, y=.5, font_size=16, showarrow=False, font_color='#111827')
        st.plotly_chart(style_axes(fig_v), use_container_width=True)

    st.markdown("---")

    # ── B. Supuestos mROI (visual cards) ──
    st.markdown("### Supuestos de retorno por grupo")
    conf_colors = {'ALTA': '#5f7a6a', 'MEDIA': '#a8826e', 'BAJA': '#9ca3af'}
    sc = st.columns(4)
    for i, (gk, s) in enumerate(SUPUESTOS.items()):
        cc = conf_colors.get(s['confianza'], '#6b7280')
        with sc[i]:
            st.markdown(f"""<div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:18px;text-align:center;min-height:200px;">
                <div style="width:14px;height:14px;border-radius:50%;background:{s['color']};margin:0 auto 8px;"></div>
                <div style="font-size:13px;font-weight:700;color:#111827;">{s['nombre']}</div>
                <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:#111827;margin:8px 0 2px;">{s['mroi_base']}x</div>
                <div style="font-size:11px;color:#6b7280;">mROI base</div>
                <div style="margin:10px 0;border-top:1px solid #f3f4f6;"></div>
                <div style="font-size:12px;color:#374151;">Rango: {s['mroi_pess']}x – {s['mroi_opt']}x</div>
                <div style="margin-top:6px;"><span style="font-size:11px;font-weight:700;color:{cc};background:{cc}15;padding:2px 10px;border-radius:8px;">Confianza {s['confianza']}</span></div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="callout-gold" style="margin-top:16px;"><strong>Metodología de estimación:</strong> Los mROIs del simulador se estiman combinando la señal direccional del modelo (Ridge + Elastic Net sobre residuales) con ajustes por efectos de largo plazo no capturados en la ventana temporal de análisis — como brand equity acumulado, conversiones diferidas entre canales y cobertura institucional. Este enfoque se usa como calibración ejecutiva cuando el modelo ofrece señal direccional pero alta incertidumbre.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── C. Alcance + Cumplimiento (expander) ──
    with st.expander("Alcance metodológico y cumplimiento del caso", expanded=False):
        st.markdown("""**Supuestos de interpretación**
- Las estimaciones son direccionales y sirven para apoyar la decisión presupuestaria, no como proyecciones financieras garantizadas.
- Los mROIs combinan señal del modelo con ajustes documentados por efectos de largo plazo no capturados en la ventana de análisis.
- La recomendación debe validarse mediante seguimiento mensual y tests controlados.

---

**Cumplimiento del enunciado (caso K-Moda)**
- **Construcción de Yt:** ventas netas semanales sin IVA vía rollup desde LINEA_PEDIDO.
- **Construcción de Xt:** inversión en medios, calendario, tráfico y contexto climático.
- **Lag y Adstock:** memoria publicitaria optimizada por canal (grid search 400 evaluaciones).
- **Modelo regularizado:** Two-Stage RidgeCV + ElasticNet (MAPE = 12,47%).
- **mROI por grupo:** Performance, CRM, Brand y Offline estimados con ajustes documentados.
- **Simulador 12M€:** escenarios con rango pesimista/base/optimista.
- **Recomendación ejecutiva:** escenario prudente defendible ante el Comité.
""")


# ═══ PAGE 5: GRUPOS ═══
elif page == "Grupos y Cobertura":
    st.markdown('<div class="section-header">Mapa de Canales</div>', unsafe_allow_html=True)
    st.markdown("Composición de cada grupo, eficiencia estimada y cómo cambia la inversión entre el Status Quo y el escenario recomendado.")

    # ── Channel group cards (horizontal, visual) ──
    conf_c = {'ALTA': '#5f7a6a', 'MEDIA': '#a8826e', 'BAJA': '#9ca3af'}
    rec_p = ESCENARIOS[REC]['pesos']
    for gk, s in SUPUESTOS.items():
        inv_sq = SQ_PCT[gk] * BUDGET / 1e6
        inv_rec = rec_p[gk] * BUDGET / 1e6
        delta_inv = inv_rec - inv_sq
        delta_sign = "+" if delta_inv >= 0 else ""
        delta_col = "#5f7a6a" if delta_inv >= 0 else "#9c5a5a"
        cc = conf_c.get(s['confianza'], '#6b7280')
        st.markdown(f"""<div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:20px 24px;margin-bottom:12px;display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
            <div style="flex:0 0 14px;"><div style="width:14px;height:14px;border-radius:50%;background:{s['color']};"></div></div>
            <div style="flex:1;min-width:180px;">
                <div style="font-size:16px;font-weight:700;color:#111827;">{s['nombre']}</div>
                <div style="font-size:13px;color:#6b7280;margin-top:2px;">{s['canales']}</div>
            </div>
            <div style="flex:0 0 90px;text-align:center;">
                <div style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:#111827;">{s['mroi_base']}x</div>
                <div style="font-size:11px;color:#6b7280;">mROI base</div>
            </div>
            <div style="flex:0 0 100px;text-align:center;">
                <div style="font-size:13px;color:#374151;">{s['mroi_pess']}x – {s['mroi_opt']}x</div>
                <div style="font-size:11px;color:#6b7280;">Rango</div>
            </div>
            <div style="flex:0 0 80px;text-align:center;">
                <span style="font-size:11px;font-weight:700;color:{cc};background:{cc}15;padding:3px 10px;border-radius:8px;">{s['confianza']}</span>
            </div>
            <div style="flex:0 0 1px;height:40px;background:#e5e7eb;"></div>
            <div style="flex:0 0 80px;text-align:center;">
                <div style="font-size:14px;font-weight:600;color:#6b7280;">{inv_sq:.1f}M€</div>
                <div style="font-size:10px;color:#9ca3af;">Status Quo</div>
            </div>
            <div style="flex:0 0 20px;text-align:center;font-size:16px;color:#9ca3af;">→</div>
            <div style="flex:0 0 80px;text-align:center;">
                <div style="font-size:14px;font-weight:700;color:#111827;">{inv_rec:.1f}M€</div>
                <div style="font-size:10px;color:#9ca3af;">Recomendado</div>
            </div>
            <div style="flex:0 0 70px;text-align:center;">
                <div style="font-size:13px;font-weight:700;color:{delta_col};">{delta_sign}{delta_inv:.1f}M€</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Historical vs Recommended: side by side bar chart ──
    st.markdown("### Reasignación propuesta")
    grps = ['perf', 'crm', 'brand', 'offline']
    grp_labels = [GN[g] for g in grps]
    inv_sq_vals = [SQ_PCT[g]*100 for g in grps]
    inv_rec_vals = [rec_p[g]*100 for g in grps]

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Status Quo', x=grp_labels, y=inv_sq_vals, marker_color='#d1d5db', text=[f'{v:.0f}%' for v in inv_sq_vals], textposition='outside', width=.35, offset=-.2))
    fig.add_trace(go.Bar(name='Recomendado', x=grp_labels, y=inv_rec_vals, marker_color=[GC[g] for g in grps], text=[f'{v:.0f}%' for v in inv_rec_vals], textposition='outside', width=.35, offset=.2))
    fig.update_layout(title="% del presupuesto: Status Quo vs Recomendado", yaxis_title="% del presupuesto", barmode='group', height=380, legend=dict(orientation='h', y=-.12), **PL)
    style_axes(fig)
    st.plotly_chart(fig, use_container_width=True)

    # ── Adstock (collapsible) ──
    with st.expander("Parámetros técnicos: Adstock por canal", expanded=False):
        st.markdown("Memoria publicitaria estimada en Fase 4. Define cuánto impacto residual conserva cada canal semana a semana.")
        ra = [{'Canal': c.replace('_',' ').title(), 'Grupo': p['grupo'], 'Lag (sem)': p['lag'], 'α (decay)': p['alpha'], 'Memoria': "Larga" if p['alpha']>=.6 else "Media", 'Vida media': f"{-1/np.log(p['alpha']):.1f} sem" if p['alpha']>0 else "—"} for c,p in ADSTOCK_PARAMS.items()]
        st.dataframe(pd.DataFrame(ra), use_container_width=True, hide_index=True)


# ═══ PAGE 6: SENSIBILIDAD ═══
elif page == "Sensibilidad":
    st.markdown('<div class="section-header">Análisis de Sensibilidad</div>', unsafe_allow_html=True)
    st.markdown('<div class="callout-blue">El simulador utiliza valores esperados de mROI (escenario base). El análisis de sensibilidad muestra la robustez de la recomendación ante variaciones en estos supuestos.</div>', unsafe_allow_html=True)
    st.markdown("### Tornado — Impacto de variación en mROI")
    rp = ESCENARIOS[REC]['pesos']
    td = []
    for g in ['perf','crm','brand','offline']:
        if rp[g] == 0: continue
        vl = BUDGET*rp[g]*SUPUESTOS[g]['mroi_pess']; vb = BUDGET*rp[g]*SUPUESTOS[g]['mroi_base']; vh = BUDGET*rp[g]*SUPUESTOS[g]['mroi_opt']
        td.append({'g': GN[g], 'lo': (vl-vb)/1e6, 'hi': (vh-vb)/1e6})
    td.sort(key=lambda x: abs(x['hi']-x['lo']))
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Pesimista', y=[d['g'] for d in td], x=[d['lo'] for d in td], orientation='h', marker_color='rgba(220,38,38,.4)', text=[f'{d["lo"]:+.1f}M€' for d in td], textposition='outside'))
    fig.add_trace(go.Bar(name='Optimista', y=[d['g'] for d in td], x=[d['hi'] for d in td], orientation='h', marker_color='rgba(95,122,106,.4)', text=[f'{d["hi"]:+.1f}M€' for d in td], textposition='outside'))
    fig.add_vline(x=0, line_dash="dash", line_color="#6b7280", line_width=1)
    fig.update_layout(title="Δ Ventas si mROI varía (M€)", xaxis_title="Δ Ventas Inc. (M€)", barmode='overlay', height=350, legend=dict(orientation='h', y=-.15), **PL)
    st.plotly_chart(style_axes(fig), use_container_width=True)
    st.markdown("---")
    st.markdown("### Test marginal · impacto de mover 5 pp desde S3")

    bp = dict(rp); vr, _ = simular(bp, 'base')
    mv = []
    for gf in [g for g in bp if bp[g] >= .05]:
        for gt in ['perf', 'crm', 'brand', 'offline']:
            if gf == gt:
                continue
            n2 = dict(bp); n2[gf] -= .05; n2[gt] += .05
            if n2[gf] < 0:
                continue
            vn, _ = simular(n2, 'base'); d = vn - vr
            # Lectura en texto
            if d > 0.05e6:
                lectura = "Mejora"
            elif d < -0.05e6:
                lectura = "Empeora"
            else:
                lectura = "Neutral"
            mv.append({
                '_sort': d,
                'Movimiento': f"{GN[gf]} → {GN[gt]}",
                'Δ Ventas': f"{d/1e6:+.1f}M€",
                'ROI': f"{vn/BUDGET:.1f}x",
                'Lectura': lectura,
            })
    df_mv = pd.DataFrame(mv).sort_values('_sort', ascending=False).drop(columns=['_sort'])

    # Fila base antes de la tabla
    st.markdown(
        f"""<div style='background:#fffbeb;border-left:3px solid #c9a96e;padding:10px 16px;margin:8px 0 14px;border-radius:4px;font-size:13px;color:#374151;'>
        <strong style='color:#111827;'>Escenario base S3:</strong> {vr/1e6:.1f} M€ · ROI {vr/BUDGET:.1f}x
        <span style='color:#6b7280;margin-left:12px;'>· cada fila mueve 5 puntos porcentuales desde un grupo hacia otro</span>
        </div>""",
        unsafe_allow_html=True
    )
    st.dataframe(df_mv, use_container_width=True, hide_index=True)
    st.markdown("---"); st.markdown("### Escenarios bajo 3 niveles de mROI")
    fig2 = go.Figure()
    short_s = {'S0 — Status Quo': 'Status Quo', 'S1 — Perf + CRM': 'Crec. digital', 'S2 — Eficiencia máxima': 'Eficiencia máx.', 'S3 — Recomendado prudente': 'Recomendado ★'}
    for en in ESCENARIOS:
        vs = [simular(ESCENARIOS[en]['pesos'], n)[0]/1e6 for n in ['pesimista','base','optimista']]
        fig2.add_trace(go.Scatter(x=['Pesimista','Base','Optimista'], y=vs, name=short_s.get(en, en), mode='lines+markers', marker=dict(size=10), line=dict(width=2)))
    fig2.update_layout(title="Ventas Incrementales por nivel de mROI", yaxis_title="Ventas Inc. (M€)", xaxis_title="Nivel mROI", height=400, legend=dict(orientation='h', y=-.2), **PL)
    st.plotly_chart(style_axes(fig2), use_container_width=True)
    st.markdown('<div class="callout-gold"><strong>Conclusión:</strong> Bajo los rangos analizados, la reasignación hacia Performance + CRM mantiene una mejora estimada frente al Status Quo bajo los supuestos definidos. La recomendación es razonablemente estable ante variaciones moderadas de los supuestos.</div>', unsafe_allow_html=True)

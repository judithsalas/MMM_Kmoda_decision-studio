# K-Moda · MMM Decision Studio

> **Marketing Mix Modeling end-to-end para defender un presupuesto de marketing de 12 M€ ante un comité de dirección.**
> Caso académico desarrollado bajo metodología econométrica rigurosa, con simulador interactivo y entregables ejecutivos.

🔗 **App en vivo:** [mmmkmodadecision-studio.streamlit.app](https://mmmkmodadecision-studiogit-fnqfswx8b57gd7hdz6ssgf.streamlit.app/)

---

## Contexto

K-Moda es una marca ficticia de moda premium española. En el caso, Elena Torres (CMO) debe defender ante Ricardo Sanz (CFO) un presupuesto anual de marketing de **12 millones de euros** en un entorno post-cookie donde el modelo tradicional de atribución por clic ha colapsado tras GDPR, iOS 14+ y la presión competitiva del *ultra-fast fashion* asiático.

El reto: construir una **Single Source of Truth** independiente de los walled gardens, que justifique cada euro invertido y proponga una reasignación óptima del mix.

## Solución propuesta

Un sistema MMM completo construido en Python que cubre desde la auditoría de integridad referencial del dataset hasta el simulador ejecutivo de escenarios, pasando por la calibración de Adstock por canal y la regresión penalizada Elastic Net.

### Resultados clave

| KPI | Valor |
|---|---|
| Presupuesto defendido | **12 M€** |
| Ventas incrementales proyectadas | **78,1 M€** |
| ROI atribuido | **6,5x** |
| Delta vs. Status Quo | **+26,7 M€** |
| Reasignación propuesta | **35 puntos porcentuales** (Offline + Brand → Performance + CRM) |
| MAPE holdout | **12,47%** |
| R² holdout | **0,847** |

---

## Metodología

El modelo implementa la ecuación maestra clásica del MMM:

```
Ŷₜ = β₀ + Σ βₘ · Aₜ,ₘ + Σ δⱼ · Cₜ,ⱼ + εₜ
```

donde:
- **β₀** — intercepto / línea base orgánica (53,2 M€)
- **βₘ · Aₜ,ₘ** — coeficientes de medios sobre inversión con adstock geométrico aplicado
- **δⱼ · Cₜ,ⱼ** — controles exógenos (calendario, clima, festivos, COVID)
- **εₜ ~ N(0, 0,053)** — residual gaussiano

### Pipeline en 7 fases

1. **EDA y validación** — Integridad referencial entre 8 tablas, validación con DuckDB sobre el esquema `CASOMAT_MMM` (2020–2024 · 10 ciudades · 8 canales)
2. **Variable dependiente Yₜ** — Rollup semanal nacional de ventas netas vía LEFT JOIN desde calendar spine
3. **Matriz Xₜ** — Construcción de 22 features (inversión, tráfico, clima, calendario), VIF y feature importance con Random Forest + Gradient Boosting
4. **Optimización Adstock + Lag** — Grid search 400 combinaciones (5 lags × ~8 alphas por canal) con criterio Pearson sobre Yₜ residualizado
5. **Modelado Elastic Net two-stage** — RidgeCV para baseline + ElasticNetCV regularizado sobre residuales con `TimeSeriesSplit(7)`, α=1e⁻⁴, l1_ratio=0,10
6. **Coherencia y calibración** — Reconciliación analítica vs. leave-one-out, documentación de desviaciones D1–D5
7. **Modelo robusto ejecutivo** — Bootstrap, intervalos de confianza, mROI por grupo estratégico

### Decisiones técnicas justificadas

- **Granularidad nacional semanal** — Suficiente señal con 260 puntos sin sobreajustar; el panel-data por ciudad introducía colinealidad excesiva
- **Log-linear specification** — Captura saturación implícita y elasticidades interpretables
- **Two-stage approach** — Separa varianza explicada por estacionalidad (~80%) de la señal incremental de medios (~5%) evitando contaminación
- **Adstock geométrico (no Weibull)** — Especificación del PDF del caso, más interpretable para comité
- **Hill saturation sólo como cap** — Aplicada únicamente fuera del rango histórico observado para no degradar el simulador

---

## El entregable: app Streamlit

La aplicación es una **decision tool** completa con 6 secciones:

| Sección | Función |
|---|---|
| **Resumen Ejecutivo** | KPIs principales · donut del mix · contexto de impacto |
| **Simulador** | Sliders interactivos por grupo · waterfall de impacto · proyección dinámica |
| **Comparador** | 4 escenarios (Status Quo, Crecimiento digital, Eficiencia máxima, Recomendado) con matriz BCG dinámica |
| **Modelo y Confianza** | Ecuación maestra · parámetros calibrados · descomposición de varianza |
| **Grupos y Cobertura** | Visualización de la reasignación SQ → S3 por grupo |
| **Sensibilidad** | Tornado chart · tabla marginal ±5pp · 3 niveles de mROI |

### Arquitectura

```
mmm_kmoda_decision-studio/
├── app.py                      # Streamlit app (78 KB, ~1100 líneas)
├── requirements.txt
└── data/
    └── model_results.json      # Outputs del pipeline serializados
```

La app **no contiene los datos ni el modelo**: consume los outputs del pipeline (notebooks Python con pandas/sklearn/statsmodels) a través de un JSON canónico. Esto permite:
- Reproducibilidad: cualquier cambio en el modelo se refleja en la app sin tocar código UI
- Trazabilidad: cada cifra mostrada apunta a un campo específico del JSON
- Despliegue ligero: ~85 KB total sin dependencias pesadas

---

## Stack técnico

**Modelado:**
- Python 3.12
- pandas, numpy
- scikit-learn (`ElasticNetCV`, `RidgeCV`, `TimeSeriesSplit`)
- statsmodels (Durbin-Watson, Ljung-Box, Breusch-Pagan, Shapiro-Wilk)
- DuckDB (validación de integridad)

**Visualización y producto:**
- Streamlit (app interactiva)
- Plotly (gráficos dinámicos con paleta editorial custom)
- pptxgenjs (generación programática del deck ejecutivo)

**Diseño:**
- Paleta editorial sobria (navy, borgoña, terracota, carbón + dorado institucional)
- Tipografía Playfair Display (serif) + DM Sans (sans-serif)
- CSS custom con max-width 1400px y dark sidebar tipo consulting

---

## Entregables del proyecto

1. **App Streamlit en producción** — desplegada en Streamlit Cloud
2. **Deck ejecutivo** — 6 slides PowerPoint con narrativa estructurada (Diagnóstico → Rigor metodológico → Asignación → Posición estratégica BCG → Proyección)
3. **Documento Q&A defensivo** — 15 preguntas anticipadas con respuestas preparadas para comité
4. **Notebooks de las 7 fases** — pipeline reproducible end-to-end

---

## Aprendizajes clave

Este proyecto integra competencias de:

- **Econometría aplicada** — Series temporales, regularización, diagnóstico residual
- **Ingeniería de datos** — Schema relacional, integridad referencial, agregación multidimensional
- **Marketing analytics** — Adstock, atribución multi-touch, mROI marginal
- **Diseño de producto** — UX de dashboards ejecutivos, jerarquía visual, storytelling con datos
- **Comunicación a C-level** — Defensa de inversión, frameworks estratégicos (BCG), gestión de incertidumbre

---

## Autora

**Judith Velareb**
Proyecto académico desarrollado en el grado de Ingeniería Matemátics (UAX) bajo el caso *El Dilema de los 12 Millones y la Ciencia del Retorno*.

---

## Notas

- Los datos del dataset son sintéticos, generados para el caso de estudio académico
- Las cifras de mROI publicadas son resultado del modelo Elastic Net calibrado con ajustes ejecutivos documentados para conversiones diferidas y efectos de largo plazo
- El proyecto está pensado como demostración de capacidad analítica y de producto, no como recomendación financiera real

# FraudShield

Aplicación web para la detección y prevención de fraudes digitales
mediante análisis automatizado e inteligencia artificial (TFG).

## Instalación

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```
cd backend
python app.py
```

Después, abre http://127.0.0.1:5000 en el navegador.

## Datos

El modelo de correos usa el dataset SpaPhish (Mendeley Data,
DOI 10.17632/hz2d6gz7pc). No se incluye en este repositorio:
descárgalo y guárdalo como `backend/datos/spaphish.csv`.

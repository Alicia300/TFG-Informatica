# FraudShield

Aplicación web para la detección y prevención de fraudes digitales mediante análisis automatizado e inteligencia artificial (TFG).

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
Después, se abre http://127.0.0.1:5000 en el navegador.

## Datos

El modelo de correos usa el dataset SpaPhish (Mendeley Data, DOI 10.17632/hz2d6gz7pc). No se incluye en este repositorio:está guardado como `backend/datos/spaphish.csv`.

## Reentrenar los modelos

Los modelos entrenados están en `backend/modelos/`. Para reentrenarlos, desde la carpeta `backend`:
```
python entrenar.py
```
Resultados de la validación cruzada (5 folds):

| Modelo | Datos | Exactitud | Recall |
|---|---|---|---|
| SMS | 144 mensajes propios | 88,9 % | 92,0 % |
| Correo | 1.395 correos (SpaPhish) | 94,3 % | 91,4 % |

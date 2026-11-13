from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
    cross_val_predict
)
from sklearn.metrics import confusion_matrix
from datasetPublico import crear_modelo
from datosEntrenamiento import mensajes
from entrenar import CONFIGURACION


# Separar los textos y sus etiquetas.
textos = [texto for texto, etiqueta in mensajes]
etiquetas = [etiqueta for texto, etiqueta in mensajes]


# Mismo modelo que se usa en la aplicación para los SMS.
modelo = crear_modelo(**CONFIGURACION["sms"])


# 5 bloques (folds), manteniendo la proporción de cada clase en todos.
validacion = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

metricas = {
    "accuracy": "Exactitud (accuracy)",
    "precision": "Precisión (precision)",
    "recall": "Sensibilidad (recall)",
    "f1": "F1"
}

resultados = cross_validate(
    modelo,
    textos,
    etiquetas,
    cv=validacion,
    scoring=list(metricas.keys())
)

print("VALIDACIÓN CRUZADA (5 folds)")
print(f"Mensajes totales: {len(textos)}")
print("-" * 60)

for clave, nombre in metricas.items():
    valores = resultados[f"test_{clave}"]
    por_fold = " ".join(f"{v:.2f}" for v in valores)
    print(f"{nombre:<24} {valores.mean():.2%} (± {valores.std():.2%})")
    print(f"   por fold: {por_fold}")


# Matriz de confusión con las predicciones de todos los folds.
predicciones = cross_val_predict(modelo, textos, etiquetas, cv=validacion)
matriz = confusion_matrix(etiquetas, predicciones, labels=[0, 1])

print("\nMATRIZ DE CONFUSIÓN (acumulada de los 5 folds)")
print("                     Pred. legítimo   Pred. sospechoso")
print(f"Real legítimo        {matriz[0][0]:>10}   {matriz[0][1]:>14}")
print(f"Real sospechoso      {matriz[1][0]:>10}   {matriz[1][1]:>14}")

print(
    "\nFalsos negativos (fraude no detectado): "
    f"{matriz[1][0]}"
)
print(
    "Falsos positivos (mensaje legítimo marcado como sospechoso): "
    f"{matriz[0][1]}"
)


# Listado de errores para el análisis.
print("\nMENSAJES MAL CLASIFICADOS")
print("-" * 60)

hay_errores = False

for texto, real, predicho in zip(textos, etiquetas, predicciones):
    if real != predicho:
        hay_errores = True
        nombre_real = "Sospechoso" if real == 1 else "Legítimo"
        nombre_predicho = "Sospechoso" if predicho == 1 else "Legítimo"
        print(f"\n{texto}")
        print(f"   Real: {nombre_real} | IA: {nombre_predicho}")

if not hay_errores:
    print("No hay errores.")
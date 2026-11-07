
import unittest
from analizador import analizar_contenido


class TestAnalizador(unittest.TestCase):

    def test_mensaje_sin_indicios(self):
        resultado = analizar_contenido(
            "Hola, ¿cómo estás?",
            "sms"
        )

        self.assertEqual(resultado["nivel_riesgo"], "bajo")
        self.assertEqual(resultado["puntuacion"], 0)

    def test_mensaje_con_urgencia(self):
        resultado = analizar_contenido(
            "URGENTE: revisa este aviso",
            "sms"
        )

        self.assertEqual(resultado["nivel_riesgo"], "medio")
        self.assertEqual(resultado["puntuacion"], 1)

    def test_solicitud_de_contrasena(self):
        resultado = analizar_contenido(
            "Confirma tu contraseña",
            "email"
        )

        self.assertEqual(resultado["nivel_riesgo"], "alto")
        self.assertEqual(resultado["puntuacion"], 2)

    def test_url_http(self):
        resultado = analizar_contenido(
            "http://example.com",
            "url"
        )

        self.assertEqual(resultado["nivel_riesgo"], "medio")
        self.assertEqual(resultado["puntuacion"], 1)

    def test_url_con_ip(self):
        resultado = analizar_contenido(
            "http://192.0.2.1/login",
            "url"
        )

        self.assertEqual(resultado["nivel_riesgo"], "alto")
        self.assertEqual(resultado["puntuacion"], 3)

    def test_mensaje_con_varios_indicios(self):
        resultado = analizar_contenido(
            "URGENTE: confirma tu contraseña",
            "sms"
        )

        self.assertEqual(resultado["nivel_riesgo"], "alto")
        self.assertEqual(resultado["puntuacion"], 3)
        self.assertEqual(resultado["numero_indicios"], 2)

    def test_resultado_incluye_todos_los_campos(self):
        resultado = analizar_contenido(
            "Hola",
            "sms"
        )

        self.assertIn("nivel_riesgo", resultado)
        self.assertIn("puntuacion", resultado)
        self.assertIn("indicios", resultado)
        self.assertIn("numero_indicios", resultado)


if __name__ == "__main__":
    unittest.main()
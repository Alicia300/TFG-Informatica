# Conjunto de mensajes etiquetados para entrenar la IA.
# 0 = legítimo, 1 = sospechoso.

mensajes = [
    # Mensajes legítimos: conversaciones cotidianas
    ("Hola, ¿quedamos mañana para tomar un café?", 0),
    ("Gracias por tu ayuda, hablamos esta tarde.", 0),
    ("Mañana te envío los apuntes de clase.", 0),
    ("La reunión empieza a las diez en el despacho.", 0),
    ("Te adjunto el documento que me pediste.", 0),
    ("Recuerda que hoy tenemos clase a las nueve.", 0),
    ("¿Puedes llamarme cuando tengas un momento?", 0),
    ("Feliz cumpleaños, espero que pases un buen día.", 0),
    ("Nos vemos el sábado en el restaurante de siempre.", 0),
    ("He terminado el trabajo y te lo envío esta tarde.", 0),

    # Mensajes legítimos: pedidos, citas y servicios
    ("Tu pedido ha sido enviado y llegará mañana.", 0),
    ("El paquete está listo para recoger en la tienda.", 0),
    ("La cita está confirmada para el próximo lunes.", 0),
    ("Hemos recibido correctamente tu solicitud.", 0),
    ("La reserva se ha confirmado correctamente.", 0),
    ("Tu factura está disponible en el área de cliente.", 0),
    ("El pago se ha realizado correctamente.", 0),
    ("Tu suscripción se renovará el próximo mes.", 0),
    ("Puedes consultar el horario actualizado en nuestra página web.", 0),
    ("Te recordamos que mañana tienes una cita a las once.", 0),

    # Mensajes legítimos con términos potencialmente ambiguos
    ("Puedes acceder a tu cuenta desde la aplicación oficial.", 0),
    ("Consulta el enlace que te envié para ver las fotografías.", 0),
    ("Tu cuenta de usuario se ha creado correctamente.", 0),
    ("Hemos actualizado el horario de atención al cliente.", 0),
    ("El banco ha publicado el extracto mensual en su aplicación.", 0),
    ("Verifica que los datos del formulario sean correctos antes de enviarlo.", 0),
    ("Puedes recuperar tu contraseña desde la página oficial.", 0),
    ("El departamento de informática actualizará el sistema esta noche.", 0),
    ("La tienda ofrece descuentos en productos seleccionados.", 0),
    ("El profesor ha publicado las notas en el campus virtual.", 0),

    # Mensajes legítimos adicionales para ampliar la variedad
    ("Feliz cumpleaños, espero que pases un buen día.", 0),
    ("¿Puedes llamarme cuando tengas un momento?", 0),
    ("Tu pedido ha sido enviado y llegará mañana.", 0),
    ("Puedes acceder a tu cuenta desde la aplicación oficial.", 0),
    ("Nos vemos mañana para estudiar juntos.", 0),
    ("Gracias por avisarme, te llamo luego.", 0),
    ("He recibido tu mensaje, muchas gracias.", 0),
    ("La entrega de tu paquete está prevista para mañana.", 0),
    ("Puedes consultar tu factura desde la aplicación oficial.", 0),
    ("Tu cuenta está activa y funciona correctamente.", 0),
    ("La reunión se ha cambiado al jueves por la mañana.", 0),
    ("Te envío el enlace a las fotografías del viaje.", 0),

    # Mensajes sospechosos: urgencia y amenazas
    ("URGENTE: confirma tu contraseña inmediatamente.", 1),
    ("Tu cuenta será suspendida si no actúas inmediatamente.", 1),
    ("Último aviso: verifica tu cuenta en las próximas 24 horas.", 1),
    ("Actúa ahora o perderás el acceso a tu cuenta.", 1),
    ("Tu cuenta ha sido bloqueada, confirma tus datos urgentemente.", 1),
    ("Evita el cierre de tu cuenta introduciendo tus datos ahora.", 1),
    ("Responde inmediatamente para evitar una sanción.", 1),
    ("Aviso urgente: tu acceso será eliminado si no confirmas tu identidad.", 1),

    # Mensajes sospechosos: contraseñas y datos personales
    ("Introduce tus datos bancarios para recibir el reembolso.", 1),
    ("Confirma tu contraseña para desbloquear el acceso.", 1),
    ("Facilita tus datos personales para recibir el premio.", 1),
    ("Tu banco necesita que confirmes tus datos bancarios.", 1),
    ("Para evitar el bloqueo, envía tu contraseña por este mensaje.", 1),
    ("Introduce el número de tu tarjeta y el código de seguridad.", 1),
    ("Confirma tu identidad enviando una copia de tu documento.", 1),
    ("Necesitamos tu clave bancaria para validar la transferencia.", 1),
    ("Proporciona tus credenciales para recuperar el acceso.", 1),
    ("Envía el código de verificación que acabas de recibir.", 1),

    # Mensajes sospechosos: premios y ofertas engañosas
    ("Has ganado un premio gratis, reclámalo ahora.", 1),
    ("Has sido seleccionado para recibir un regalo exclusivo.", 1),
    ("Reclama tu premio gratis antes de que expire.", 1),
    ("Enhorabuena, has ganado un móvil. Paga los gastos para recibirlo.", 1),
    ("Tu premio está reservado, introduce tus datos para reclamarlo.", 1),
    ("Has ganado un sorteo en el que no participaste.", 1),
    ("Oferta exclusiva: recibe dinero gratis si confirmas tus datos.", 1),
    ("Reclama tu recompensa ahora o la perderás para siempre.", 1),

    # Mensajes sospechosos adicionales: códigos, pagos y tarjetas
    ("Comparte el código de seguridad recibido por SMS para validar tu cuenta.", 1),
    ("Introduce el código de verificación para evitar el bloqueo de tu cuenta.", 1),
    ("Envía el código que acabas de recibir para completar la operación.", 1),
    ("Tu paquete está retenido, paga ahora para recibir la entrega.", 1),
    ("Paga una tasa de aduanas mediante este enlace para liberar tu paquete.", 1),
    ("Para recibir tu pedido, introduce los datos de tu tarjeta bancaria.", 1),
    ("Confirma el número de tu tarjeta y su código de seguridad.", 1),
    ("Facilita tus datos bancarios para desbloquear el reembolso pendiente.", 1),
    ("Tu envío no puede continuar hasta que realices el pago indicado.", 1),
    
    # Mensajes sospechosos: bancos, entregas y enlaces
    ("Detectamos un problema con tu cuenta bancaria, verifica tus datos.", 1),
    ("Tu paquete está retenido, paga una tasa desde este enlace.", 1),
    ("No se pudo entregar tu pedido, introduce los datos de tu tarjeta.", 1),
    ("Tu cuenta bancaria será bloqueada, accede al enlace para evitarlo.", 1),
    ("Confirma el pago pendiente para liberar tu envío.", 1),
    ("Hemos detectado movimientos sospechosos, envía tus credenciales.", 1),
    ("Actualiza tus datos de pago para evitar la cancelación del servicio.", 1),
    ("Accede y verifica tu cuenta inmediatamente.", 1),
    ("Para recibir la devolución, confirma tu identidad y tus datos bancarios.", 1),
    ("Tu suscripción será cancelada, introduce tu contraseña para renovarla.", 1),

    # Legítimos: entregas y pedidos
    ("Tu pedido está en reparto y llegará hoy entre las 14:00 y las 18:00.", 0),
    ("Hemos entregado tu paquete en el punto de recogida. Recuerda llevar tu DNI.", 0),
    ("Tu envío ha salido del centro logístico y llegará en 24 horas.", 0),
    ("El repartidor ha dejado tu paquete con el portero del edificio.", 0),
    ("Tu pedido número 48213 ha sido enviado. Puedes seguirlo desde tu cuenta en la web oficial.", 0),
    ("Hemos recibido tu devolución y el reembolso se realizará en 3 a 5 días laborables.", 0),
    ("Gracias por tu compra. Tu pedido llegará en 3 días laborables y recibirás un aviso cuando salga del almacén.", 0),

    # Legítimos: bancos, pagos y códigos
    ("Compra de 25,40 euros en el supermercado con tu tarjeta terminada en 1234.", 0),
    ("Has recibido un Bizum de 10 euros de Ana.", 0),
    ("Tu código de acceso es 482913. Caduca en 5 minutos. No lo compartas con nadie.", 0),
    ("Tu transferencia de 300 euros se ha realizado correctamente.", 0),
    ("El cargo mensual de tu suscripción se ha procesado correctamente.", 0),
    ("Por tu seguridad, nunca compartas tus claves con nadie. Tu banco no te las pedirá por SMS.", 0),
    ("Tu contraseña se ha cambiado correctamente.", 0),
    ("Si no has solicitado este cambio de contraseña, ignora este mensaje.", 0),
    ("Hemos actualizado nuestros términos de servicio. Puedes leerlos en nuestra web.", 0),

    # Legítimos: citas y gestiones
    ("Tu cita en el centro de salud es el martes a las 9:30. Si no puedes acudir, cancélala con antelación.", 0),
    ("Tu reserva para dos personas el sábado a las 21:00 está confirmada.", 0),
    ("Le confirmamos que su solicitud de matrícula ha sido registrada. Recibirá novedades por correo en los próximos días.", 0),

    # Legítimos: conversaciones cotidianas
    ("Mamá, llego tarde a cenar, empezad sin mí.", 0),
    ("¿Has visto el partido de anoche? Qué locura.", 0),
    ("Te mando la ubicación del restaurante por aquí.", 0),
    ("Mañana no hay clase porque el profesor está enfermo.", 0),
    ("Compra pan y leche cuando vuelvas, por favor.", 0),
    ("Ya he llegado a casa, gracias por acompañarme.", 0),
    ("Recuerda que el viernes tenemos la entrega del trabajo de grupo.", 0),
    ("¿Me puedes pasar el número del fontanero que nos recomendaste?", 0),

    # Legítimos: correos
    ("Estimado cliente, le adjuntamos la factura correspondiente al mes de octubre. Puede consultarla en su área privada.", 0),
    ("Buenos días, te adjunto el informe de la reunión de ayer. Cualquier duda me dices. Un saludo.", 0),
    ("Hola equipo, os recuerdo que la reunión semanal es mañana a las 10:00 en la sala 2.", 0),
    ("El lunes empezamos con el nuevo proyecto, te paso la agenda por correo.", 0),

    # Sospechosos: falsos avisos de paquetes
    ("Correos: tu paquete no ha podido entregarse. Reprograma la entrega y paga 1,99 euros de gastos en este enlace.", 1),
    ("SEUR: dirección incorrecta, actualiza tus datos para recibir tu paquete hoy.", 1),
    ("Su paquete está en el almacén. Abone la tasa de 2,50 euros para programar la entrega.", 1),
    ("Tu envío ha sido devuelto por falta de datos. Completa tu dirección y tu tarjeta en este enlace.", 1),
    ("Último intento de entrega. Confirma tu dirección y paga los gastos de envío o se devolverá.", 1),
    ("Tienes un paquete pendiente de aduana. Regulariza el pago ahora para evitar su destrucción.", 1),

    # Sospechosos: banca
    ("BBVA: hemos bloqueado tu tarjeta por seguridad. Accede aquí para desbloquearla.", 1),
    ("CaixaBank: acceso no autorizado a tu cuenta. Verifica tu identidad en el siguiente enlace.", 1),
    ("Santander: tu cuenta quedará limitada. Actualiza tus datos de acceso hoy.", 1),
    ("Se ha intentado un cargo de 899 euros en tu tarjeta. Si no has sido tú, pulsa el enlace para anularlo.", 1),
    ("Tu clave de firma ha caducado. Renuévala introduciendo tu DNI y tu PIN en este enlace.", 1),
    ("Se ha detectado un inicio de sesión sospechoso en tu cuenta. Confirma que eres tú con tu contraseña.", 1),

    # Sospechosos: organismos públicos
    ("DGT: tienes una multa pendiente con descuento. Págala hoy en este enlace para evitar recargos.", 1),
    ("Agencia Tributaria: tienes una devolución pendiente. Facilita tu IBAN para recibirla.", 1),
    ("Seguridad Social: tu pensión está bloqueada. Confirma tus datos para reactivarla.", 1),

    # Sospechosos: suplantación de familiares y jefes
    ("Hola mamá, he cambiado de número. Guárdalo y escríbeme por WhatsApp, necesito un favor urgente.", 1),
    ("Papá, se me ha roto el móvil y uso uno prestado. ¿Me haces un Bizum de 300 euros?", 1),
    ("Hola, soy tu jefe. Necesito que compres tarjetas regalo ahora y me envíes los códigos. Es urgente y confidencial.", 1),

    # Sospechosos: servicios online
    ("Netflix: tu pago ha sido rechazado. Actualiza tu método de pago para no perder tu cuenta.", 1),
    ("Tu cuenta de Amazon ha sido suspendida. Verifica tu información de pago aquí.", 1),
    ("Aviso final: su cuenta de PayPal ha sido limitada. Confirme su información para restablecerla.", 1),
    ("Tu factura de la luz está vencida. Paga hoy con tu tarjeta en este enlace o se cortará el suministro.", 1),
    ("Soporte técnico: tu ordenador está infectado. Llama ahora y facilítanos acceso remoto.", 1),

    # Sospechosos: estafas económicas
    ("Gana 300 euros al día trabajando desde casa. Escríbenos y paga solo la cuota de inscripción.", 1),
    ("Invierte 250 euros hoy y recibe 1.500 en una semana con criptomonedas. Plazas limitadas.", 1),
    ("Préstamo aprobado sin papeles ni comprobaciones. Envía tu DNI y tu cuenta bancaria.", 1),
    ("Felicidades, tu número ha sido premiado con 1.000 euros. Responde con tus datos para cobrarlo.", 1),

    # Sospechosos: correos
    ("Estimado cliente: hemos detectado actividad inusual en su cuenta. Para evitar el bloqueo, haga clic en el enlace y verifique su identidad en las próximas 24 horas.", 1),
    ("Su buzón de correo está lleno. Haga clic aquí e introduzca su contraseña para ampliar el espacio o perderá sus mensajes.", 1),
    ("Adjuntamos la factura pendiente. Abra el archivo adjunto y habilite las macros para verla.", 1),
]


# Eliminar mensajes repetidos para evitar fugas de datos en la evaluación.
mensajes = list(dict.fromkeys(mensajes))


if __name__ == "__main__":
    total = len(mensajes)
    legitimos = sum(1 for _, etiqueta in mensajes if etiqueta == 0)
    sospechosos = sum(1 for _, etiqueta in mensajes if etiqueta == 1)

    print("Conjunto de entrenamiento")
    print(f"Total de mensajes: {total}")
    print(f"Legítimos: {legitimos}")
    print(f"Sospechosos: {sospechosos}")
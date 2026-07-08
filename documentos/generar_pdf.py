"""
Genera el documento PDF de políticas financieras de NexoFin.
El agente RAG usará este documento como fuente de conocimiento.
"""

from fpdf import FPDF


class NexoFinPDF(FPDF):
    """PDF personalizado con header y footer para NexoFin."""

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "NexoFin - Banco Digital", align="L")
        self.cell(0, 8, "Documento Interno - Confidencial", align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, title: str):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def chapter_subtitle(self, subtitle: str):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 76, 153)
        self.cell(0, 8, subtitle, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def chapter_body(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def bullet_point(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(6, 5.5, "- ")
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")

    def section_break(self):
        self.ln(4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)


def build_pdf() -> NexoFinPDF:
    pdf = NexoFinPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ────────────────────────────────────────────────────────────────
    # PORTADA
    # ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, "NexoFin", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(0, 76, 153)
    pdf.cell(0, 12, "Banco Digital", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Manual de Politicas y Procedimientos", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Documento Interno - Version 1.0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, "Elaborado por el Departamento de Cumplimiento Normativo", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Julio 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    # ────────────────────────────────────────────────────────────────
    # 1. POLÍTICA DE PRIVACIDAD Y PROTECCIÓN DE DATOS
    # ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("1. Politica de Privacidad y Proteccion de Datos")

    pdf.chapter_subtitle("1.1 Introduccion")
    pdf.chapter_body(
        "En NexoFin, la privacidad y seguridad de los datos de nuestros clientes es una prioridad "
        "fundamental. Esta politica describe como recopilamos, utilizamos, almacenamos y protegemos "
        "la informacion personal de nuestros usuarios, en cumplimiento con la Ley de Proteccion de "
        "Datos Personales y el Reglamento General de Proteccion de Datos (RGPD)."
    )

    pdf.chapter_subtitle("1.2 Datos que Recopilamos")
    pdf.chapter_body(
        "Para brindar nuestros servicios financieros, recopilamos los siguientes tipos de datos:"
    )
    pdf.bullet_point("Datos de identificacion: nombre completo, numero de documento, fecha de nacimiento, nacionalidad.")
    pdf.bullet_point("Datos de contacto: direccion de correo electronico, numero de telefono, direccion postal.")
    pdf.bullet_point("Datos financieros: historial de transacciones, saldos de cuentas, ingresos declarados.")
    pdf.bullet_point("Datos de dispositivo: direccion IP, tipo de navegador, sistema operativo, identificadores unicos del dispositivo.")
    pdf.bullet_point("Datos biométricos: huella digital y reconocimiento facial, solo con consentimiento explicito del usuario.")

    pdf.chapter_subtitle("1.3 Finalidad del Tratamiento")
    pdf.chapter_body(
        "Los datos recopilados se utilizan exclusivamente para:"
    )
    pdf.bullet_point("Gestion de cuentas bancarias y procesamiento de transacciones.")
    pdf.bullet_point("Verificacion de identidad y prevencion de fraudes.")
    pdf.bullet_point("Cumplimiento de obligaciones legales y regulatorias (KYC, AML).")
    pdf.bullet_point("Mejora continua de nuestros servicios y atencion al cliente.")
    pdf.bullet_point("Envio de comunicaciones relevantes sobre el estado de la cuenta, solo si el usuario lo autoriza.")

    pdf.chapter_subtitle("1.4 Derechos del Usuario")
    pdf.chapter_body(
        "Los titulares de los datos tienen los siguientes derechos en cualquier momento:"
    )
    pdf.bullet_point("Derecho de acceso: solicitar una copia de los datos personales que tenemos sobre usted.")
    pdf.bullet_point("Derecho de rectificacion: corregir datos inexactos o incompletos.")
    pdf.bullet_point("Derecho de supresion ('derecho al olvido'): solicitar la eliminacion de sus datos.")
    pdf.bullet_point("Derecho de portabilidad: recibir sus datos en un formato estructurado y de uso comun.")
    pdf.bullet_point("Derecho de oposicion: oponerse al tratamiento de sus datos para fines de marketing.")

    pdf.chapter_subtitle("1.5 Seguridad de los Datos")
    pdf.chapter_body(
        "Implementamos las siguientes medidas de seguridad para proteger los datos de nuestros clientes: "
        "cifrado AES-256 en reposo y TLS 1.3 en transmision, autenticacion multifactor (MFA), "
        "monitoreo continuo de accesos no autorizados, y auditorias de seguridad trimestrales "
        "realizadas por empresas externas certificadas."
    )

    pdf.chapter_subtitle("1.6 Retencion de Datos")
    pdf.chapter_body(
        "Conservamos los datos personales durante el tiempo necesario para cumplir con las finalidades "
        "descritas en esta politica, o hasta que el usuario solicite su eliminacion. Por cumplimiento "
        "normativo, los registros financieros se conservan por un periodo minimo de 5 anos despues "
        "del cierre de la cuenta, segun lo establecido por la legislacion aplicable."
    )

    pdf.chapter_subtitle("1.7 Contacto del DPO")
    pdf.chapter_body(
        "Para cualquier consulta relacionada con la proteccion de datos, los usuarios pueden contactar "
        "a nuestro Delegado de Proteccion de Datos (DPO) a traves del correo electronico "
        "dpo@nexofin.com o mediante nuestra linea de atencion al cliente: +54 11 5555-0200."
    )

    # ────────────────────────────────────────────────────────────────
    # 2. TÉRMINOS Y CONDICIONES DE USO
    # ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("2. Terminos y Condiciones de Uso")

    pdf.chapter_subtitle("2.1 Aceptacion de los Terminos")
    pdf.chapter_body(
        "Al crear una cuenta en NexoFin y utilizar nuestros servicios, el usuario acepta los terminos "
        "y condiciones descritos en este documento. Si no esta de acuerdo con alguno de estos terminos, "
        "debera abstenerse de utilizar la plataforma."
    )

    pdf.chapter_subtitle("2.2 Requisitos de Uso")
    pdf.chapter_body(
        "Para utilizar los servicios de NexoFin, el usuario debe:"
    )
    pdf.bullet_point("Ser mayor de 18 anos y tener capacidad legal para contratar.")
    pdf.bullet_point("Proporcionar informacion veraz, completa y actualizada durante el proceso de registro.")
    pdf.bullet_point("No estar inhabilitado para operar sistemas financieros por ninguna autoridad regulatoria.")
    pdf.bullet_point("Mantener la confidencialidad de sus credenciales de acceso.")

    pdf.chapter_subtitle("2.3 Responsabilidades del Usuario")
    pdf.chapter_body(
        "El usuario es el unico responsable de:"
    )
    pdf.bullet_point("Mantener la confidencialidad de su usuario, contrasena y codigos de verificacion.")
    pdf.bullet_point("Todas las operaciones realizadas desde su cuenta, incluso aquellas realizadas sin su conocimiento.")
    pdf.bullet_point("Notificar inmediatamente a NexoFin sobre cualquier uso no autorizado de su cuenta.")
    pdf.bullet_point("No utilizar la plataforma para actividades ilegales o fraudulentas.")

    pdf.chapter_subtitle("2.4 Limitacion de Responsabilidad")
    pdf.chapter_body(
        "NexoFin no sera responsable por danos directos, indirectos, incidentales o consecuentes "
        "derivados del uso o la imposibilidad de usar la plataforma, incluyendo pero no limitado a: "
        "perdida de datos, interrupcion del servicio, o transacciones no autorizadas que no sean "
        "resultado directo de una negligencia comprobada de NexoFin."
    )

    pdf.chapter_subtitle("2.5 Modificaciones")
    pdf.chapter_body(
        "NexoFin se reserva el derecho de modificar estos terminos en cualquier momento. "
        "Los cambios significativos seran notificados a los usuarios con al menos 30 dias de "
        "anticipacion a traves del correo electronico registrado y mediante notificacion en "
        "la aplicacion. El uso continuado de la plataforma despues de la entrada en vigor de "
        "las modificaciones constituye la aceptacion de los nuevos terminos."
    )

    pdf.chapter_subtitle("2.6 Resolucion de Conflictos")
    pdf.chapter_body(
        "Cualquier controversia derivada de estos terminos se resolvera mediante arbitraje "
        "de conformidad con las reglas del Centro de Arbitraje Comercial. El arbitraje se "
        "llevara a cabo en la Ciudad de Buenos Aires, Argentina, y el idioma del procedimiento "
        "sera el espanol."
    )

    # ────────────────────────────────────────────────────────────────
    # 3. PREGUNTAS FRECUENTES SOBRE TRANSACCIONES Y LÍMITES
    # ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("3. Preguntas Frecuentes sobre Transacciones y Limites")

    pdf.chapter_subtitle("3.1 Transferencias")
    pdf.chapter_body("A continuacion se responden las preguntas mas comunes sobre transacciones.")

    pdf.chapter_subtitle("?Cual es el limite diario para transferencias?")
    pdf.chapter_body(
        "El limite diario para transferencias a cuentas de terceros es de $500,000 ARS (pesos argentinos) "
        "para cuentas personales verificadas. Para cuentas empresariales, el limite es de $2,000,000 ARS. "
        "Estos limites pueden ajustarse temporalmente a solicitud del cliente a traves de atencion al cliente."
    )

    pdf.chapter_subtitle("?Cuanto tiempo tarda una transferencia en acreditarse?")
    pdf.chapter_body(
        "Las transferencias entre cuentas NexoFin se acreditan de forma inmediata (menos de 30 segundos) "
        "las 24 horas del dia, los 7 dias de la semana. Las transferencias a otros bancos nacionales se "
        "acreditan en un plazo de 1 a 24 horas habiles. Las transferencias internacionales pueden demorar "
        "entre 2 y 5 dias habiles, dependiendo del pais de destino y las entidades intermediarias."
    )

    pdf.chapter_subtitle("?Existe un limite minimo para transferencias?")
    pdf.chapter_body(
        "No existe un limite minimo para transferencias entre cuentas NexoFin. Para transferencias a "
        "terceros en otros bancos, el monto minimo es de $100 ARS. Las transferencias internacionales "
        "tienen un monto minimo de $50 USD o su equivalente en otras monedas."
    )

    pdf.chapter_subtitle("?Que tipos de transacciones estan disponibles?")
    pdf.chapter_body(
        "NexoFin ofrece los siguientes tipos de transacciones: transferencias entre cuentas NexoFin, "
        "transferencias a otros bancos nacionales e internacionales, pago de facturas y servicios, "
        "recarga de telefonos, compra y venta de divisas, y retiros en efectivo en cajeros asociados. "
        "Todas las transacciones estan sujetas a los limites diarios y mensuales segun el tipo de cuenta."
    )

    pdf.chapter_subtitle("?Las transferencias tienen algun costo adicional?")
    pdf.chapter_body(
        "Las transferencias entre cuentas NexoFin son completamente gratuitas e ilimitadas. "
        "Las transferencias a otros bancos nacionales tienen un costo de $150 ARS por transaccion. "
        "Las transferencias internacionales tienen un costo del 0.5% del monto transferido, con un "
        "minimo de $5 USD y un maximo de $50 USD. Estos costos no incluyen las comisiones que puedan "
        "aplicar los bancos intermediarios o receptores."
    )

    pdf.chapter_subtitle("?Puedo programar transferencias recurrentes?")
    pdf.chapter_body(
        "Si, NexoFin permite programar transferencias recurrentes con frecuencia diaria, semanal, "
        "quincenal o mensual. Puede configurar hasta 10 transferencias recurrentes activas simultaneamente. "
        "Las transferencias programadas se ejecutan automaticamente siempre que la cuenta tenga saldo "
        "suficiente en la fecha programada."
    )

    pdf.chapter_subtitle("3.2 Limites de la Cuenta")
    pdf.chapter_body(
        "Los limites de cuenta varian segun el nivel de verificacion del usuario: "
        "Cuenta Basica (verificacion minima): saldo maximo de $100,000 ARS, depositos mensuales "
        "de hasta $50,000 ARS. Cuenta Estandar (verificacion completa): saldo maximo de $2,000,000 ARS, "
        "depositos mensuales de hasta $500,000 ARS. Cuenta Premium (verificacion plus): sin limite de "
        "saldo, depositos mensuales de hasta $5,000,000 ARS. Para aumentar el nivel de verificacion, "
        "el usuario debe completar el proceso KYC correspondiente."
    )

    # ────────────────────────────────────────────────────────────────
    # 4. POLÍTICA DE SEGURIDAD Y PREVENCIÓN DE FRAUDES
    # ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("4. Politica de Seguridad y Prevencion de Fraudes")

    pdf.chapter_subtitle("4.1 Autenticacion y Acceso")
    pdf.chapter_body(
        "NexoFin implementa un sistema de autenticacion multifactor (MFA) obligatorio para todos "
        "los accesos a la plataforma. Los factores de autenticacion incluyen: contrasena segura "
        "(minimo 12 caracteres, con mayusculas, minusculas, numeros y simbolos), codigo de verificacion "
        "enviado via SMS o correo electronico, y verificacion biometrica (huella digital o reconocimiento "
        "facial) disponible en la aplicacion movil."
    )

    pdf.chapter_subtitle("4.2 Deteccion de Fraudes")
    pdf.chapter_body(
        "Nuestro sistema de deteccion de fraudes utiliza inteligencia artificial y machine learning "
        "para analizar patrones de transacciones en tiempo real. El sistema evalua los siguientes "
        "factores de riesgo: ubicacion geografica inusual, monto elevado fuera del patron habitual, "
        "multiples intentos de inicio de sesion fallidos, acceso desde dispositivos no registrados, "
        "y transacciones en horarios no habituales para el usuario."
    )

    pdf.chapter_subtitle("4.3 Bloqueo de Seguridad")
    pdf.chapter_body(
        "La cuenta se bloqueara automaticamente en los siguientes casos: "
        "despues de 5 intentos fallidos de inicio de sesion (bloqueo temporal de 30 minutos), "
        "deteccion de acceso desde una ubicacion no habitual sin verificacion adicional, "
        "3 intentos fallidos de confirmacion de transaccion en un periodo de 1 hora, "
        "o notificacion de robo o extravio del dispositivo movil registrado. "
        "Para desbloquear la cuenta, el usuario debe contactar a atencion al cliente y "
        "completar el proceso de verificacion de identidad."
    )

    pdf.chapter_subtitle("4.4 Notificaciones de Seguridad")
    pdf.chapter_body(
        "NexoFin notifica al usuario inmediatamente sobre: inicio de sesion desde un nuevo dispositivo "
        "o ubicacion, transacciones superiores a $10,000 ARS, cambios en la configuracion de seguridad, "
        "e intentos de recuperacion de contrasena. Las notificaciones se envian via correo electronico "
        "y notificaciones push en la aplicacion movil. Si el usuario recibe una notificacion de una "
        "accion que no reconocio, debe reportarla inmediatamente."
    )

    pdf.chapter_subtitle("4.5 Recomendaciones de Seguridad para el Usuario")
    pdf.chapter_body("Recomendamos a nuestros usuarios seguir estas buenas practicas de seguridad:")
    pdf.bullet_point("No compartir jamas la contrasena, codigos de verificacion o datos biometricos con terceros.")
    pdf.bullet_point("Activar la verificacion biometrica en la aplicacion movil.")
    pdf.bullet_point("Mantener la aplicacion y el sistema operativo del dispositivo actualizados.")
    pdf.bullet_point("No utilizar redes WiFi publicas no seguras para realizar transacciones.")
    pdf.bullet_point("Revisar periodicamente el historial de transacciones y notificar cualquier irregularidad.")
    pdf.bullet_point("Configurar alertas de transacciones para montos superiores a $5,000 ARS.")

    pdf.chapter_subtitle("4.6 Procedimiento ante Fraudes")
    pdf.chapter_body(
        "En caso de detectar una transaccion no autorizada, el usuario debe: "
        "1) Contactar inmediatamente a NexoFin a traves de la linea de emergencia (+54 11 5555-0299) "
        "disponible 24/7. 2) Bloquear temporalmente la cuenta desde la aplicacion movil. "
        "3) Presentar un reclamo formal dentro de las 48 horas siguientes a traves del centro de ayuda. "
        "4) Proporcionar toda la documentacion solicitada por el equipo de investigacion. "
        "NexoFin investigara el caso en un plazo maximo de 10 dias habiles y, de comprobarse el fraude, "
        "realizara el reembolso total de los fondos en un plazo de 48 horas adicionales."
    )

    # ────────────────────────────────────────────────────────────────
    # 5. TARIFAS Y COMISIONES DEL SERVICIO
    # ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("5. Tarifas y Comisiones del Servicio")

    pdf.chapter_subtitle("5.1 Cuentas")
    pdf.chapter_body(
        "NexoFin ofrece los siguientes tipos de cuentas con sus respectivas tarifas: "
        "Cuenta Basica: sin costo de apertura ni mantenimiento. Incluye 10 transferencias gratis por mes. "
        "Cuenta Estandar: sin costo de apertura, mantenimiento mensual de $200 ARS. "
        "Incluye 30 transferencias gratis por mes y acceso a soporte prioritario. "
        "Cuenta Premium: sin costo de apertura, mantenimiento mensual de $500 ARS. "
        "Incluye transferencias ilimitadas gratis, soporte dedicado 24/7 y acceso a salas VIP "
        "en aeropuertos asociados."
    )

    pdf.chapter_subtitle("5.2 Transferencias")
    pdf.chapter_body("Las tarifas por transferencias se detallan a continuacion:")
    pdf.bullet_point("Transferencias entre cuentas NexoFin: GRATIS (sin limite de cantidad).")
    pdf.bullet_point("Transferencias a otros bancos nacionales: $150 ARS por transaccion.")
    pdf.bullet_point("Transferencias internacionales (SWIFT): 0.5% del monto (min. $5 USD, max. $50 USD).")
    pdf.bullet_point("Transferencias programadas recurrentes: GRATIS (aplica la tarifa del tipo de transferencia).")

    pdf.chapter_subtitle("5.3 Retiros")
    pdf.chapter_body("Las tarifas por retiros de efectivo son las siguientes:")
    pdf.bullet_point("Retiros en cajeros automaticos de la red NexoFin: GRATIS (hasta 5 retiros por mes).")
    pdf.bullet_point("Retiros en cajeros de otras redes: $100 ARS por transaccion.")
    pdf.bullet_point("Retiros en ventanilla (sucursales asociadas): $300 ARS por transaccion.")
    pdf.bullet_point("Retiros internacionales en cajeros: 3% del monto retirado.")

    pdf.chapter_subtitle("5.4 Depositos")
    pdf.chapter_body("Los depositos en cuentas NexoFin no tienen ningun costo:")
    pdf.bullet_point("Depositos por transferencia bancaria: GRATIS.")
    pdf.bullet_point("Depositos en efectivo en sucursales asociadas: GRATIS (hasta $50,000 ARS por mes).")
    pdf.bullet_point("Depositos internacionales entrantes: GRATIS.")

    pdf.chapter_subtitle("5.5 Servicios Adicionales")
    pdf.chapter_body("Tarifas de otros servicios ofrecidos por NexoFin:")
    pdf.bullet_point("Emision de tarjeta de debito fisica: $500 ARS (unico pago).")
    pdf.bullet_point("Tarjeta de debito virtual: GRATIS.")
    pdf.bullet_point("Reposicion de tarjeta por extravio o dano: $800 ARS.")
    pdf.bullet_point("Cambio de divisas (compra/venta): spread del 1% sobre el tipo de cambio de referencia.")
    pdf.bullet_point("Pago de facturas y servicios: GRATIS.")
    pdf.bullet_point("Estado de cuenta mensual impreso: $100 ARS (digital es GRATIS).")

    pdf.chapter_subtitle("5.6 Exenciones y Promociones")
    pdf.chapter_body(
        "NexoFin ofrece las siguientes exenciones de tarifas: "
        "Los estudiantes universitarios que acrediten condicion regular obtienen la Cuenta Estandar "
        "sin costo de mantenimiento por 12 meses. Los nuevos usuarios obtienen 3 meses de Cuenta Premium "
        "gratis al abrir su primera cuenta. Los jubilados y pensionados tienen descuento del 50% en "
        "todas las tarifas de mantenimiento. Promociones adicionales pueden estar disponibles segun "
        "campanas vigentes publicadas en la aplicacion."
    )

    pdf.chapter_subtitle("5.7 Actualizacion de Tarifas")
    pdf.chapter_body(
        "NexoFin se reserva el derecho de modificar sus tarifas y comisiones. Cualquier cambio "
        "sera notificado a los usuarios con al menos 30 dias de anticipacion a traves del correo "
        "electronico registrado y mediante notificacion en la aplicacion. Si el usuario no esta "
        "de acuerdo con los nuevos valores, puede solicitar el cierre de su cuenta sin penalizacion "
        "dentro del periodo de preaviso."
    )

    # ────────────────────────────────────────────────────────────────
    # NOTA FINAL
    # ────────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.chapter_title("Nota Final")
    pdf.chapter_body(
        "Este documento contiene las politicas oficiales de NexoFin Banco Digital y esta sujeto a "
        "actualizaciones periodicas. Para consultar la version mas reciente, los usuarios pueden "
        "acceder a la seccion 'Documentacion Legal' dentro de la aplicacion o visitar el sitio web "
        "oficial: www.nexofin.com/documentacion."
    )
    pdf.chapter_body(
        "Para cualquier consulta adicional, nuestro equipo de atencion al cliente esta disponible "
        "de lunes a viernes de 8:00 a 20:00 horas y sabados de 9:00 a 14:00 horas (huso horario "
        "de Argentina, UTC-3). Puede contactarnos a traves del correo ayuda@nexofin.com, "
        "por telefono al +54 11 5555-0200 o mediante el chat en vivo disponible en nuestra "
        "aplicacion y sitio web."
    )
    pdf.chapter_body(
        "NexoFin Banco Digital - Comprometidos con tu futuro financiero."
    )

    return pdf


if __name__ == "__main__":
    pdf = build_pdf()
    pdf.output("documentos/politica_fintech.pdf")
    print("PDF generado exitosamente: documentos/politica_fintech.pdf")

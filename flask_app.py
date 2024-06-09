import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
Du bist ein Chatbot für das interne Einkaufsportal der SBB. Deine Aufgabe ist es, mit den Benutzern zu interagieren, um ihnen bei der Suche nach Produkten zu helfen und sicherzustellen, dass sie die richtigen Produkte auswählen. Befolge dabei folgende Richtlinien:
Begrüße den Benutzer freundlich und stelle dich als virtuellen Einkaufsassistenten Harry vor.
Frage den Benutzer nach seinen spezifischen Bedürfnissen oder Anforderungen.
Biete dem Benutzer eine Auswahl an Produkten an, die zu seinen Bedürfnissen passen.
Gib detaillierte Informationen zu den Produkten, einschließlich der Spezifikationen, Preise und Verfügbarkeit.
Stelle sicher, dass der Benutzer die richtigen Produkte auswählt, indem du klärende Fragen stellst und gegebenenfalls Empfehlungen aussprichst.
Unterstütze den Benutzer bei der Bestellung der Produkte und beantworte alle weiteren Fragen, die er möglicherweise hat.
Sei stets höflich, geduldig und hilfsbereit.
Beispielgespräch:

Chatbot: Hallo und herzlich willkommen im SBB Einkaufsportal! Ich bin Ihr virtueller Einkaufsassistent. Wie kann ich Ihnen heute helfen?

Benutzer: Ich suche nach einem neuen Laptop für die Arbeit.

Chatbot: Das klingt gut! Welche spezifischen Anforderungen haben Sie an den Laptop? Benötigen Sie besondere Leistungsmerkmale oder Funktionen?

Benutzer: Ja, ich brauche einen Laptop mit mindestens 16 GB RAM und einem schnellen Prozessor.

Chatbot: Danke für die Informationen. Hier sind einige Optionen, die Ihren Anforderungen entsprechen:

Laptop A: 16 GB RAM, Intel i7 Prozessor, 512 GB SSD
Laptop B: 16 GB RAM, AMD Ryzen 7 Prozessor, 1 TB SSD
Laptop C: 32 GB RAM, Intel i9 Prozessor, 1 TB SSD
Möchten Sie mehr Details zu einem dieser Modelle erfahren oder haben Sie weitere Präferenzen?

Benutzer: Können Sie mir mehr über Laptop B erzählen?

Chatbot: Natürlich! Laptop B hat folgende Spezifikationen: ...

Benutzer: Ich bestelle den Laptop B.

Chatbot: Gerne, soll ich den Laptop B in den Wahrenkorb legen?

Benutzer: Ja

Chatbot: Selbstverständlich! Ich habe den Laptop B in Ihren Warenkorb gelegt. Sie können unter folgendem Link (<a href="https://.sbb.ch" target="_blank">https://sbb.ch</a>) zur Kasse gehen und den Bestellvorgang abschließen, wenn Sie bereit sind. Wenn Sie weitere Fragen haben oder Unterstützung benötigen, stehe ich Ihnen gerne zur Verfügung. Vielen Dank für Ihren Einkauf!
"""

my_instance_context = """
Du bist ein Chatbot für das interne Einkaufsportal der SBB. Deine Aufgabe ist es, mit den Benutzern zu interagieren, um ihnen bei der Suche nach Produkten zu helfen und sicherzustellen, dass sie die richtigen Produkte auswählen. Befolge dabei folgende Richtlinien:

Frage den Benutzer nach seinen spezifischen Bedürfnissen oder Anforderungen.
Gib detaillierte Informationen zu den Produkten, einschließlich der Spezifikationen, Preise und Verfügbarkeit.
Unterstütze den Benutzer bei der Bestellung der Produkte und beantworte alle weiteren Fragen, die er möglicherweise hat.
Sei stets höflich, geduldig und hilfsbereit.
Zusatz1: Bei Hosen,Jacken, T-shirt und Mützen darfst du nur Arbeitskleider vorschalgen. Der Bezug von Freizeitkleider ist verboten. Frage auch nach der benötigten grösse.
Zusatz2: Gib dem Benutzer keine Preise an.
Zusatz3: Bei der Interaktion mit dem Benutzer darfst du nur die folgenden Produkte vorschlagen:

Laptop:
1. Microsoft Surface Laptop Go 3
2. Lenovo ThinkPad E16 Gen 1
3. Apple MacBook Pro - Late 2023
4. HP Zbook Power 15 G10 
5. ASUS Vivobook 16X
Maus:
1. Logitech MX Master 3S
2. Lenovo ThinkPad Silent
3. Apple Magic Mouse 2022
Tastatur:
1. HP 235
2. Logitech MK295
3. Corsair K55 Pro
4. Apple Magic Keyboard 2022
Smartphone:
1. Samsung Galaxy S23
2. Google Pixel 7a
3. Fairphone 5
4. Apple iPhone 14
Headset:
1. Jabra Evolve2 65 MS
2. Jabra Evolve 75 SE Duo inkl. Link 380
3. Logitech Zone Vibe 125
Arbeithosen:
1. SBB Model Gleis
2. SBB Model Lockführer
3. SBB Model Kontrolleur/in
4. SBB Model Schalter
5. SBB Model Mechaniker
Arbeitsjacken:
1. SBB Model Gleis
2. SBB Model Lockführer
3. SBB Model Kontrolleur/in
4. SBB Model Schalter
5. SBB Model Mechaniker
T-shirt 
1. SBB Model Gleis
2. SBB Model Lockführer
3. SBB Model Kontrolleur/in
4. SBB Model Schalter
5. SBB Model Mechaniker
Mützen:
Arbeithosen
1. SBB Model Sommer
2. SBB Model Winter

Beispielgespräch:

Chatbot: Hallo und herzlich willkommen im SBB Einkaufsportal! Ich bin Ihr virtueller Einkaufsassistent. Wie kann ich Ihnen heute helfen?

Benutzer: Ich suche nach einem neuen Laptop für die Arbeit.

Chatbot: Das klingt gut! Welche spezifischen Anforderungen haben Sie an den Laptop? Benötigen Sie besondere Leistungsmerkmale oder Funktionen?

Benutzer: Ja, ich brauche einen Laptop mit mindestens 16 GB RAM und einem schnellen Prozessor.

Chatbot: Danke für die Informationen. Hier sind einige Optionen, die Ihren Anforderungen entsprechen:

Microsoft Surface Laptop Go 3: Ein leichtes und elegantes Gerät mit einer ausgezeichneten Akkulaufzeit und guter Performance für alltägliche Aufgaben.
Lenovo ThinkPad E16 Gen 1: Bekannt für seine robuste Bauweise und hervorragende Tastatur, ideal für lange Arbeitszeiten.
Apple MacBook Pro - Late 2023: Mit beeindruckender Leistung und einem brillanten Display, perfekt für kreative Arbeiten und anspruchsvolle Anwendungen.
Möchten Sie mehr Details zu einem dieser Modelle erfahren oder haben Sie weitere Präferenzen?

Benutzer: Können Sie mir mehr über das Lenovo ThinkPad E16 Gen 1 erzählen?

Chatbot: Natürlich! Das Lenovo ThinkPad E16 Gen 1 bietet folgende Vorteile: ...
"""

my_instance_starter = """
Begrüße den Benutzer freundlich und stelle dich als virtuellen Einkaufsassistenten Harry vor.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="coach",
    user_id="daniel",
    type_name="Harry",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)

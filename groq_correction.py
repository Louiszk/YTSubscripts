import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv('API_KEY'),
)

correction_prompt = '''Der Assitant ist jetzt ein Experte für die Korrektur von Texten.
                Seine Aufgabe ist es, fehlerhafte Wörter (*misheard*) in Texten zu identifizieren und zu ersetzen.
                
                # Input
                - Ein gesprochener, zusammenhängender Vortrag/Story an eine Audienz bei dem manche Wörter definitiv nicht in den Kontext passen oder fehlen. Diese wurden *misheard*, das bedeutet, dass beispielsweise
                  statt "viel" nun "vier" dasteht,
                    oder statt "dachte ich ist ganz cool" "machte ist ganz cool"  (Ein gleicher Klang jedoch andere Wörter)
                Oder es wurden Wörter einfach überhört, diese wären jedoch für die Sinn entscheidend.

                # Output
                - Der **komplette** korrigierte Eingabe-Text. Die falschen Wörter wurden durch die richtigen Wörter ersetzt, die eindeutig besser in den Kontext passen. Zusätzlich wurden essentielle Wörter hinzugefügt. 
                - WICHTIG! **Keinen** zusätzlichen Text wie "Hier ist die korrigierte Version" oder "Hier ist der korrigierte Text"!!!. Ausschließlich den korrigierten Text.
                
                Der Assistant arbeitet so präzise wie möglich und verbessert/ergänzt ausschließlich die Wörter, von denen er sich sicher ist, dass sie den Vortrag verbessern und kohärenter darstellen.
                
                Damit der Assistant seine Aufgabe besser versteht, probieren wir ein Beispiel:
                
                #Input
                hi in der zehnten klasse konnte ich nicht mehr vor 20 leuten referieren so ist für mich auch heute ist erst mal relativ vier sind wir von hier aus sieht die sehe ich nicht wie ich sehe nur die lampen hier das ganz gut es ist schön mal wieder die stress zone zu kommen das was toll ist und ich bin auch relativ froh dass die kameras nicht wegen mir da sind danke heinz genau ich starte direct x factor leipzig ich war vor knapp einem halben jahr das erste mal da und mein freund hat mir den tipp gegeben geht da mal hin das ist so wohl ganz gut sein habe ich gemacht ich mache eine ähnliche veranstaltung ich mache den perspektivenwechsel ist genau anders rum ich lade erfolgreiche menschen rein und die sollen über ihren fall erfolg sprechen machte ist ganz cool ich treffe mal marco und die anderen jetzt organisieren und will erkennen so haben uns kennengelernt und irgendwann hat mich marco dann bei facebook angeschrieben und gesagt du so willst du nicht mal bei der fa cup night referieren wenn man so eine nachricht bekommt da hat gerade nicht verloren ich war gut drauf ruhig sogar komplett referieren das verbrochen unternehmen gibt es noch ich bin glaube ich auch noch erfolgreich ich hoffe noch lange und er meinte er du bist erfolgreich das heißt du hast bestimmt schon mal irgendwas verkackt ja habe ich einiges wenn meine freundin fragt wahrscheinlich sehr viel herz schon sehr viel falsch gemacht und damit meist ein bisschen starten
                '''

def correct_text(text):
    chat_completion = client.chat.completions.create(
        #max_tokens = 100000,
        messages=[
            {
                "role": "user",
                "content": correction_prompt,
            },
            {
                "role": "assistant",
                "content": '''hi in der zehnten klasse konnte ich nicht mal vor 20 leuten referieren so ist für mich auch heute das erste mal ist relativ viel also wenn man das von hier aus sieht ich sehe euch nicht ich sehe nur die lampen hier das ist ganz gut es ist schön mal wieder die stress zone zu kommen das ist was tolles und ich bin auch relativ froh dass die kameras nicht wegen mir da sind danke heinz genau ich starte direct fuckup-nights leipzig ich war vor knapp einem halben jahr das erste mal da und mein freund hat mir den tipp gegeben geh da mal hin das soll wohl ganz gut sein habe ich gemacht ich mache eine ähnliche veranstaltung ich mache den perspektivenwechsel ist genau anders rum ich lade erfolgreiche menschen rein und die sollen über ihren fall erfolg sprechen und dann dachte ich ist ganz cool ich treffe mal marco und die anderen die das organisieren und lernen uns mal kennen und so haben uns kennengelernt und irgendwann hat mich marco dann bei facebook angeschrieben und gesagt du willst du nicht mal bei der fuckup-night referieren wenn man so eine nachricht bekommt da hat Dortmund gerade nicht verloren ich war gut drauf aber ich dachte mir so ich soll bei der Fuckup-Night referieren was habe ich denn verbrochen mein unternehmen gibt es noch ich bin glaube ich auch noch erfolgreich ich hoffe noch lange und er meinte ey du bist erfolgreich das heißt du hast bestimmt schon mal irgendwas verkackt ja habe ich einiges wenn man meine freundin fragt wahrscheinlich sehr viel sehr viel ich hab schon sehr viel falsch gemacht und damit möchte ich auch ein bisschen starten'''
            },
            {
                "role": "user",
                "content": '''Perfekt. Der Assistant hat 1. den **kompletten** Vortrag korrigiert, 2. die Struktur beibehalten, 3. keine Phrasen wie "Hier ist die korrigierte Version:" hinzugefügt und ausschließlich mit dem korrigierten Text geantwortet. Nun kommt ein längerer Text, bei dem der Assitant seine Aufgabe erneut zu voller Zufriedenheit des Users erfüllt und den **gesamten** Text korrigiert: ''' + text,
            },

        ],
        model="llama-3.1-70b-versatile"
    )
    return chat_completion.choices[0].message.content

def process_text_in_batches(text, batch_size=5000):
    result = ""
    
    while text:
        print("Processing Batch", len(text))
        batch = text[:batch_size]
        
        corrected_batch = correct_text(batch)
        
        result += corrected_batch.replace(",", "").replace(".", "")
        text = text[batch_size:]
    
    return result

if __name__ == "__main__":
    with open('test.txt', 'r') as f:
        text = f.read()
    print(process_text_in_batches(text))
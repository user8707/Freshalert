Wo geschieht Foodwaste?
Die Gastronomie und die Haushalte verursachen zusammen 35% der Lebensmittelabfälle.
In den Haushalten entsteht Food Waste zum Beispiel, weil
- wir mehr kaufen, als wir benötigen.
- wir grössere Verpackungen kaufen, als wir brauchen.
- wir Lebensmittel im Kühlschrank vergessen.
- wir Lebensmittel nicht korrekt lagern und sich so die Haltbarkeit verringert.
- wir das Mindesthaltbarkeitsdatum falsch interpretieren und Produkte nicht mit unseren Sinnen beurteilen.
- wir mehr kochen, als wir brauchen und Resten nicht verwerten.

INFOGRAFIK 2a
https://foodwaste.ch/was-ist-food-waste/

INFOGRAFIK 2

5 Einfache Tipps
1. Clever Einkaufen - nur so viel wie man braucht
Plane deinen Wochenbedarf und erstelle eine Einkaufsliste. Bevor du einkaufen gehst, wirf einen Blick in den Kühlschrank um zu sehen, was noch da ist.
Kaufe nur was du brauchst. Gib kleinen oder unverpackten Portionen den Vorzug und sei vorsichtig mit Aktionen – nur kaufen, wenn du sie auch wirklich konsumieren wirst.
Kaufe wenn immer möglich lokal und saisonal.
Iss etwas Kleines vor dem Einkauf – ein knurrender Magen wird dich dazu verleiten, mehr zu kaufen als du brauchst!   

2. Optimal Lagern - verlängere die Haltbarkeit deiner Lebensmittel
„Zu verbrauchen bis“, „Zu verkaufen bis“ und „Mindestens haltbar bis“ haben unterschiedliche Bedeutungen! Wenn das Datum „zu verbrauchen bis“ überschritten wurde, solltest du die Lebensmittel nicht mehr konsumieren. Ansonsten gilt: Orientiere dich nicht nur an den Daten, sondern vertraue auf deine Sinne – sehen, riechen, schmecken – um herauszufinden, ob die Lebensmittel noch geniessbar sind.
Stelle die Temperatur deines Kühlschranks auf 5ºC ein – bei wärmeren Temperaturen wird das Wachstum schädlicher Bakterien begünstigt.
Bewahre Essensreste in durchsichtigen Behältern auf. Platziere sie so, dass du sie nicht vergisst und konsumiere sie innerhalb von 1 bis 3 Tagen.
Hast du zu viel eingekauft und kannst nicht alles davon essen? Die meisten Lebensmittel können eingefroren werden! Brot bis zu drei Monaten, gewisse tierische Produkte bis zu einem Jahr! Achte bei tierischen Produkten darauf, dass die Kühlkette nicht unterbrochen wird.
Organisiere dich gut – verwende das first-in-first-out-Prinzip für verderbliche Lebensmittel wie Früchte und Gemüse: Ältere Produkte kommen nach vorne, was neu in den Kühlschrank kommt, geht nach hinten.

3. Richtig Portionieren - kleinere Mengen kochen und Servieren
Hier eine Kartoffel zu viel, dort ein kleiner Rest Pasta im Topf – häufig sind es kleine Portionen, die übrig bleiben und dann entsorgt werden. Der beste Trick, dies zu umgehen: Schon vor dem Kochen richtig portionieren!
Serviere kleinere Portionen und schöpfe nach, falls du noch immer hungrig bist.
Wenn dennoch etwas übrig bleibt: Richtig lagern, dann kannst du es zu einem späteren Zeitpunkt geniessen oder daraus ein neues Menü zaubern. Oder nimm die Reste deines Abendessens am nächsten Tag mit zur Arbeit.

4. Spass am Kochen - mit einfachen und kreativen Ideen
Weisst du nicht, was du kochen sollst? Viele Rezeptideen findest du online. Fehlt dir für dein Rezept eine Zutat? Bestimmt lässt es sich umwandeln – lass deiner Kreativität freien Lauf!
Widme einen Tag pro Woche der Resteverwertung, z.B. den Montag, wenn du Reste hast vom Wochenende und keine Lust, lange in der Küche zu stehen.
Keine lust, nochmals die gleichen Reste zu Essen? Verwandle die Reste in ein neues Menü – hast du zum Beispiel schon einmal daran gedacht, aus Kräuterresten ein leckeres Pesto zu zaubern?

5. Gemeinsam geniessen - weil du dein Essen liebst
Teile deine Liebe zum Essen mit Freunden und Familie, damit die Reduktion von Food Waste auch in deinem Umfeld zur Ehrensache wird.
Zu viel Essen im Haus? Verschenke es an Freunde oder Nachbarn oder bringe die noch verpackten Lebensmittel zu einem öffentlichen Kühlschrank.
Kenne deine Lebensmittel – und wie du sie am besten lagerst, portionierst und zubereitest. Nützliche Tipps findest du unter foodwaste.ch.

import streamlit as st

def main():
    st.title("Tipps zur Reduzierung von Food Waste")
    
    image = Image.open("foodwaste2")
        resized_image = image.resize((300, 300))
    st.image(resized_image, caption='Wo geschieht Foodwaste')
    
    st.header("Wo geschieht Foodwaste?")
    st.write("Die Gastronomie und die Haushalte verursachen zusammen 35% der Lebensmittelabfälle.")
    st.write("In den Haushalten entsteht Food Waste zum Beispiel, weil:")
    st.write("- wir mehr kaufen, als wir benötigen.")
    st.write("- wir größere Verpackungen kaufen, als wir brauchen.")
    st.write("- wir Lebensmittel im Kühlschrank vergessen.")
    st.write("- wir Lebensmittel nicht korrekt lagern und sich so die Haltbarkeit verringert.")
    st.write("- wir das Mindesthaltbarkeitsdatum falsch interpretieren und Produkte nicht mit unseren Sinnen beurteilen.")
    st.write("- wir mehr kochen, als wir brauchen und Reste nicht verwerten.")

    image = Image.open("foodwaste3")
        resized_image = image.resize((300, 300))
    st.image(resized_image, caption='Wodurch wird Foodwaste veruracht?')
    
    st.title("5 Einfache Tipps")
    st.subheader("**1. Clever Einkaufen - nur so viel wie man braucht**")
    st.write("Plane deinen Wochenbedarf und erstelle eine Einkaufsliste. Bevor du einkaufen gehst, wirf einen Blick in den Kühlschrank, um zu sehen, was noch da ist.")
    st.write("Kaufe nur, was du brauchst. Gib kleinen oder unverpackten Portionen den Vorzug und sei vorsichtig mit Aktionen – nur kaufen, wenn du sie auch wirklich konsumieren wirst.")
    st.write("Kaufe, wenn immer möglich, lokal und saisonal.")
    st.write("Iss etwas Kleines vor dem Einkauf – ein knurrender Magen wird dich dazu verleiten, mehr zu kaufen, als du brauchst!")
    
    st.subheader("**2. Optimal Lagern - verlängere die Haltbarkeit deiner Lebensmittel**")
    st.write("„Zu verbrauchen bis“, „Zu verkaufen bis“ und „Mindestens haltbar bis“ haben unterschiedliche Bedeutungen! Wenn das Datum „zu verbrauchen bis“ überschritten wurde, solltest du die Lebensmittel nicht mehr konsumieren. Ansonsten gilt: Orientiere dich nicht nur an den Daten, sondern vertraue auf deine Sinne – sehen, riechen, schmecken – um herauszufinden, ob die Lebensmittel noch genießbar sind.")
    st.write("Stelle die Temperatur deines Kühlschranks auf 5ºC ein – bei wärmeren Temperaturen wird das Wachstum schädlicher Bakterien begünstigt.")
    st.write("Bewahre Essensreste in durchsichtigen Behältern auf. Platziere sie so, dass du sie nicht vergisst, und konsumiere sie innerhalb von 1 bis 3 Tagen.")
    st.write("Hast du zu viel eingekauft und kannst nicht alles davon essen? Die meisten Lebensmittel können eingefroren werden! Brot bis zu drei Monaten, gewisse tierische Produkte bis zu einem Jahr! Achte bei tierischen Produkten darauf, dass die Kühlkette nicht unterbrochen wird.")
    st.write("Organisiere dich gut – verwende das first-in-first-out-Prinzip für verderbliche Lebensmittel wie Früchte und Gemüse: Ältere Produkte kommen nach vorne, was neu in den Kühlschrank kommt, geht nach hinten.")

    st.subheader("**3. Richtig Portionieren - kleinere Mengen kochen und servieren**")
    st.write("Hier eine Kartoffel zu viel, dort ein kleiner Rest Pasta im Topf – häufig sind es kleine Portionen, die übrig bleiben und dann entsorgt werden. Der beste Trick, dies zu umgehen: Schon vor dem Kochen richtig portionieren!")
    st.write("Serviere kleinere Portionen und schöpfe nach, falls du noch immer hungrig bist.")
    st.write("Wenn dennoch etwas übrig bleibt: Richtig lagern, dann kannst du es zu einem späteren Zeitpunkt genießen oder daraus ein neues Menü zaubern. Oder nimm die Reste deines Abendessens am nächsten Tag mit zur Arbeit.")

    st.subheader("**4. Spaß am Kochen - mit einfachen und kreativen Ideen**")
    st.write("Weißt du nicht, was du kochen sollst? Viele Rezeptideen findest du online. Fehlt dir für dein Rezept eine Zutat? Bestimmt lässt es sich umwandeln – lass deiner Kreativität freien Lauf!")
    st.write("Widme einen Tag pro Woche der Resteverwertung, z.B. den Montag, wenn du Reste hast vom Wochenende und keine Lust, lange in der Küche zu stehen.")
    st.write("Keine Lust, nochmals die gleichen Reste zu essen? Verwandle die Reste in ein neues Menü – hast du zum Beispiel schon einmal daran gedacht, aus Kräuterresten ein leckeres Pesto zu zaubern?")

    st.subheader("**5. Gemeinsam genießen - weil du dein Essen liebst**")
    st.write("Teile deine Liebe zum Essen mit Freunden und Familie, damit die Reduktion von Food Waste auch in deinem Umfeld zur Ehrensache wird.")
    st.write("Zu viel Essen im Haus? Verschenke es an Freunde oder Nachbarn oder bringe die noch verpackten Lebensmittel zu einem öffentlichen Kühlschrank.")
    st.write("Kenne deine Lebensmittel – und wie du sie am besten lagerst, portionierst und zubereitest. Nützliche Tipps findest du unter foodwaste.ch.")

st.title("Quellen")
st.write("https://foodwaste.ch/was-ist-food-waste/")
st.write("https://foodwaste.ch/was-ist-food-waste/5-schritte/")

if __name__ == "__main__":
    main()


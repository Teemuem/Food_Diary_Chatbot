# Food Diary Chatbot

![](https://gitlab.dclabra.fi/wiki/uploads/c0da1a5a-a7ea-46f8-8537-039ba588ec89.png)

*Localhostissa pyörivä sivu.*

## TL;DR:
Tekoälypohjainen ruokapäiväkirja joka helpottaa syömisten kirjaamista luonnollisella kielellä. Ollama LLM ja LangChain jäsentävät tiedot, jotka tallennetaan MySQL-tietokantaan ja näytetään visuaalisesti Streamlit-käyttöliittymässä.


## Projektin Loppuraportti: Tekoälypohjainen Ruokapäiväkirjan Täydennys 

✅ **Reasoning: Miten tämä idea syntyi?**

Tämä projekti sai alkunsa tarpeesta helpottaa ruokapäiväkirjan täyttämistä ja automasoida prosessia. Perinteisen ruokapäiväkirjan pitäminen voi olla aikaa vievää ja vaatii tarkkuuttaa ruokien syöttämisessä. Tavoitteena oli luoda järjestelmä, jossa käyttäjät voivat syöttää tietoja lunnollisella kielellä ja tekoäly analysoi syötteet, tallentaa ne tietokantaan ja tarjoaa käyttäjälle tietoa ravitsemuksesta. Tämä parantaa käyttäjäkokemusta ja luo pohjan laajemmille tekoälypohjaiseille toiminoille, kuten ruokavaliosuositukselle ja ravitsemusanalyysille. 

![](https://gitlab.dclabra.fi/wiki/uploads/1929b8f4-84ec-4d44-af3f-8b150695de39.png)
*Luotu tekoälyllä.*

---

✅ **Scope: Mitä vaatimuksia otettiin mukaan ja mitä jätettiin pois?**

***Sisätyvät vaatimukset:***

-    Käyttäjän syöttämä luonnollinen teksti ruokapäiväkirjan täyttämiseksi.
-    Kuvien liittäminen.
-    Tekoälyn käyttö syötteen analysointiin ja jäsentämiseen (ruoka-aineet, ajankohtam määrät) ja näiden tallenminen tietokantaan.
-    Käyttäjän päivittäinen yhteenveto ravinteista ja aterioiden koostimuksista.
-    Käyttöliittymän kehittäminen Streamlitillä.
-    Docker-ympäristön käyttö palveluiden hallintaan ja käyttöönottoon.

***Poissuljetut vaatimukset:***

-    Laajat graafiset analyysityökalut ja suositukset ruokavalion paramiseksi (näitä voidaan lisätä myöhemmin).
-    Yksityiskohtaiset henkilökohtaiset suositukset, jotka vaativat lisää AI-pohjaista analyysiä ja käyttäjätietojen käsittelyä. 

---

✅ **Tech Stack: Teknologia, jota käytettiin**

-    ***Backend:***
        -    **MySQL**: Tietokannan hallinta ja ruokapäiväkirjan tietojen tallentaminen.
        - **Ollama LLM**: Luonnollisen kielen käsittely ja tekstin analyösointi. Tämä mahdollistaa ruokapäiväkirjan täyttämisen luonnollisella kielellä, mikä on käyttäjäystävällinen lähestymistapa.
            - Projektissa käytetty llama3.2 , 3b mallia: https://ollama.com/library/llama3.2
        - **LangChain**: Kehys tekstin jäsentämiseen ja syötteiden käsittelyyn, sekä yhdistämään datan MySQL-tietokantaan tehokkaasti.
        - **Nutrition API** - Calories Ninja: Ravintotietojen hakeminen syödyn ruoan perusteella. Tämä API auttaa varmistamaan, että tiedot ovat tarkkoja ja ajantasaisia. https://calorieninjas.com/

        Ohjevideoita joista saatu ideoita projektissa Ollaman ja LangChain käyttöön: 
        
        -   https://www.youtube.com/watch?v=UtSSMs6ObqY&ab_channel=TechWithTim
        -   https://www.youtube.com/watch?v=6ExFTPcJJFs&ab_channel=CodeWithAarohi
        -   https://www.youtube.com/watch?v=dcHSxUqZ7No&ab_channel=GreyMatterz

-    ***Frontend:***
        -  **Streamlit**: käyttöliittymän luominen, jossa käyttäjä voi syöttää tietoja ja tarkastella ravintotietoja. Streamlitin yksinkertainen ja visuaalinen rakenne mahdollistaa nopeat päivitykset ja interaktiivisuuden.

**Docker**: Dockerin avulla voidaan helposti hallita eri palveluja ja varmistaa, että sovellus toimii eri ympäristöissä ilman asennusongelmia. Tämä mahdollistaa myös sovelluksen skaalautuvuuden ja eristämisen.

 <img src="https://gitlab.dclabra.fi/wiki/uploads/afbf8469-beb9-4ad7-a0f7-62388b26b3db.svg" width="200" style="display:inline-block; margin-right:10px;">
<img src="https://gitlab.dclabra.fi/wiki/uploads/26f835e5-ad0a-4c6f-8407-b8c5617eba3b.png" width="200" style="display:inline-block; margin-right:10px;">
<img src="https://gitlab.dclabra.fi/wiki/uploads/0d88d216-1fcd-45ed-bf8e-d45c0260fc1e.svg" width="200" style="display:inline-block;">

---


✅ **Arkkitehtuuri ja Toimintatapa**

![](https://gitlab.dclabra.fi/wiki/uploads/ad5315ef-e8c0-42df-b1a4-2894b9972b64.jpg)
*Arkkitehtuurikuva*.

Arkkitehtuurikuvassa esitetään selkeästi sovelluksen eri osien integraatio. Tekoälyprosessin avulla käyttäjän syöttämä luonnollinen teksti ja kuvat käsitellään ja jäsennetään.

-    **Käyttäjän syöte:** Käyttäjä voi syöttää ruokapäiväkirjan tietoja luonnollisella kielellä, kuten "for breakfast i had toast with egg and tomatoes with a cup of coffee ")
![](https://gitlab.dclabra.fi/wiki/uploads/fc8b728b-1f9e-4932-a46c-59b50dca0257.png)

-    **Ollama LLM:**  Prosessoi luonnollisen kielen syötteen. LLM käyttää luotua prompt-templatea, joka määrittelee, miten ruokalistapäiväkirjan syötteet (esim. käyttäjän kuvaukset aterioista) tulee käsitellä ja muuntaa rakenteiseksi tiedoksi. Tiedosto sisältää ohjeet ja esimerkit siitä, miten ruokailutapahtumat jäsennetään ja palautetaan JSON-muodossa.

        -    Aterian jäsentäminen: Kun käyttäjä antaa kuvauksen ateriastaan (esim. "toast with tomatoes and cheese"), malli pilkkoo sen osiin ja määrittää:

                -    Säännöt ja esimerkit:

                      - Kirjoitusvirheiden käsittely: Jos käyttäjä kirjoittaa ruoan nimen väärin (esim. "cheece" → "cheese"), malli tunnistaa virheen ja korjaa sen.

                       - Yhdistettyjen ruokanimien erottaminen: Jos ruokalaji on yhdistelmä (esim. "chickenburger"), malli erottaa sen kahdeksi eri tuotteeksi ("chicken" ja "burger").

                      -  Yleisten ruokaparien tunnistus: Tunnistaa tavalliset ruokaparit (esim. "beefstew" → "beef" ja "stew").

                       - Oletuskäyttäytyminen: Jos ruokaa ei voida jakaa (esim. "spaghetti"), se käsitellään yhtenä kokonaisuutena.

*template.txt:*
```
You are an AI that helps to log food diary entries. The user will provide a description of their meal, 
and you will break it down into structured data that includes food items, their quantities, meal time, category, and nutrient values (calories, protein, carbohydrates, fats, fiber, sugars). Here's an examples:

Additional Rules:
Handle Typos: Recognize and correct misspelled food names.
Split Compound Food Names: If a food name consists of multiple components (e.g., "chickenburger"), separate them into distinct items.
Recognize Common Pairings: Identify well-known food combinations (e.g., "beefstew" → "beef" and "stew").
Default Behavior: If a food cannot be split (e.g., "spaghetti"), treat it as a single item.

Input: "I had oatmeal and a banana for breakfast."
Output: {{"food_items": [{{"food_name": "oatmeal", "quantity": "1 bowl", "category": "carb"}}, {{"food_name": "banana", "quantity": "1 banana", "category": "fruit"}}], "meal_time": "breakfast"}}

Input: "I had spaghetti for dinner and a glass of milk."
Output: {{"food_items": [{{"food_name": "spaghetti", "quantity": "some", "category": "carb"}}, {{"food_name": "milk", "quantity": "1 glass", "category": "dairy"}}], "meal_time": "dinner"}}

Input: "I had a sandwich with turkey and cheese for lunch."
Output: {{"food_items": [{{"food_name": "sandwich", "quantity": "1 serving", "category": "carb"}}, {{"food_name": "turkey", "quantity": "some", "category": "protein"}}, {{"food_name": "cheese", "quantity": "some", "category": "dairy"}}], "meal_time": "lunch"}}

Input: "For breakfast, I had pancakes with syrup and a glass of orange juice."
Output: {{"food_items": [{{"food_name": "pancakes", "quantity": "some", "category": "carb"}}, {{"food_name": "syrup", "quantity": "some", "category": "sweet"}}, {{"food_name": "orange juice", "quantity": "1 glass", "category": "drink"}}], "meal_time": "breakfast"}}

Input: "I had a bowl of salad with chicken and dressing for dinner."
Output: {{"food_items": [{{"food_name": "salad", "quantity": "1 bowl", "category": "vegetable"}}, {{"food_name": "chicken", "quantity": "some", "category": "protein"}}, {{"food_name": "dressing", "quantity": "some", "category": "sauce"}}], "meal_time": "dinner"}}
.
.
.
Your task is to correctly interpret and output a JSON object, even when typos occur in the input, such as misspellings of common words (e.g., "cheese" as "cheece" or "strawberry" as "strabery").

Make sure to strictly follow the JSON format and avoid any additional text.

Only give Raw Ai Response as {{"food_items": [{{"food_name": "xx", "quantity": "xx", "category": "xx"}}, {{"food_name": "xx", "quantity": "xx", "category": "xx"}}, {{"food_name": "xx", "quantity": "xx", "category": "xx"}}], "meal_time": "xx"}}, as given examples. 

User Input: {meal_description}

Structured Output:
```


![](https://gitlab.dclabra.fi/wiki/uploads/fce972ad-cf1f-473c-97ac-2a9ad22bc2db.png)

**TESTI:** Templatea myös testattu, että pienenetty templaten sisäistä ohjeistusta kielimallille. Ohjeena annettu vain yksi esimerkki:
```
Input: " I had toast with tomatoes and cheese, with a cup of coffee for lunch"
Output: {{"food_items": [{{"food_name": "toast", "quantity": "1 slice", "category": "carb"}}, {{"food_name": "tomatoes", "quantity": "some", "category": "vegetable"}}, {{"food_name": "cheese", "quantity": "1 serving", "category": "dairy"}}, {{"food_name": "coffee", "quantity": "1 cup", "category": "drink"}}], "meal_time": "lunch"}}
```
Syötetty esimerkki lause: "For dinner i had pizza: with toppings kebab, red onion, jalapenos, feta cheese. for drink i had 0,5 l pepsi."

Eri templatejen käytössä ei huomattu huomattavaa eroa, siirretty käyttämään templatea, jossa on vain yksi esimerkki. Tämä on toiminut hyvin. Tähän lisätty vielä yksi esimerkki eli viimeisin versio käytössä on template, jossa kaksi esimerkkiä. 

![](https://gitlab.dclabra.fi/wiki/uploads/9f3767b4-8d10-4dbc-9a12-9456df3c09af.png)
![](https://gitlab.dclabra.fi/wiki/uploads/98d27166-cf21-44a1-a82e-b06a98ddbf7e.png)



-    **LangChain:** Tekstin jäsentäminen ja tiedon tallentaminen MySQL-tietokantaan. Tämä vaihe takaa, että tiedot ovat oikeassa muodossa ja helpottavat myöhempää analysointia.

![](https://gitlab.dclabra.fi/wiki/uploads/d35aa67d-7403-42d2-813a-10c66d78974d.png)

Tietokannassa:
![](https://gitlab.dclabra.fi/wiki/uploads/0e53dc11-741a-4f2b-aa90-b828d2eec306.png)


-    **Calories Ninja API:** hakee ravitsemustiedot ja lisää ne ruokapäiväkirjan tietokantaan.
        - Käyttäjä voi halutessaan muokata taulun tietoja suoraan. Käyttäjä voi muokata  nimiä ja määriä. Tiedot päivittyvät MySQL-tietokannassa. 
        - Käyttäjä voi poistaa ruokalajeja valitsemalla "Delete"-valintaruutuja.

![](https://gitlab.dclabra.fi/wiki/uploads/de7c3ca3-03f4-46ea-8d79-468954b39b75.png)


- **Streamlit:** Käyttöliittymä, jossa käyttäjä voi tarkastella päivittäistä ravitsemusyhteenvetoa ja saada tietoa aterioiden koostumuksesta.
    - Sovellus laskee ja näyttää päivän kokonaissummat kaloreista, proteiineista, hiilihydraateista.
    - Jos ruokalajille on lisätty kuva, se näytetään ruokailu ajan yhteydessä.
    

![](https://gitlab.dclabra.fi/wiki/uploads/98e7efcc-7d6f-4535-9975-51a6535d58a9.png)

![](https://gitlab.dclabra.fi/wiki/uploads/e64cfab9-c881-4676-aa4d-32387e8b2369.png)


- **Docker:** Varmistaa, että sovelluksen eri osat toimivat yhdessä ja ovat helposti otettavissa käyttöön.    





---

✅ **Yhteenveto ja Tulevaisuuden Suunnitelmat**

Projektissa saavutettiin sen päätavoitteet: käyttäjät voivat syöttää ruokapäiväkirjan tiedot helposti luonnollisella kiellä, yksittäisinä lauseina ja tekoäly prosessoi nämä tiedot automaattisesti. Tämä parantaa ruokapäiväkirjan käyttäjäkokemusta ja tekee ruokapäiväkirjan pitämisestä helpompaa ja nopeampaa. Teknologiavalinnoissa yhdistettiin tekoälyä, tietokantoja ja käyttöliittymä.  

***Tulevaisuudessa:***
-    Ruokavaliosusitukset: AI-pohjaiset suositukset voivat auttaa käyttäjiä parantamaan ruokavaliota.
-    Ravitsemusanalyysi: Voidaan lisätä syvällisempää analyysiä ruokavalion koostumuksesta ja sen vaikutuksista terveyteen.
-    Voisi olla pohjna sovellukselle, joka auttaa käyttäjiä seuraamaan FODMAP-ruokavaliota ja tunnistamaan ruoka-aineet, jotka voivat aiheuttaa oireita. 
-    Skaalautuvuus: Järjestelmää voidaan laajentaa muihin kieliin ja kulttuureihin, jolloin se on käyttökelpoionen globaalisti.
-    Kuvasta ruoan tunnistus tekoälyllä



Projektin avulla luodaan vahva pohja tekoälypohjaiselle ruokavalion hallinnalle ja tarjoaa monia mahdollisuuksia jatkokehitykselle. 

## Ohjeet 

Käyttöön tarvitaan luodan .env -tiedosto jonne syöttää
```
OLLAMA_SERVER_URL=http://host.docker.internal:11434
X_API_KEY= *****-*****     #luo API avain https://calorieninjas.com/ 
MYSQL_HOST=mysql_db        #tai luo oma nimi
MYSQL_USER=root            #tai luo oma nimi
MYSQL_PASSWORD= ***        #lisää oma salasana
MYSQL_DATABASE=food_db     #tai luo oma nimi
```

Kun .env -tiedosto luotu. 

Aja terminaalissa 
```docker-compose up -d --build```

Ollama mallin lataus docker konttiin, aja manuaalisesti: 

```docker exec -it ollama bash```
root@35cdce3268c7:/# ollama list  

Aja komento ``` ollama run llama3.2```

Mikäli ladataan eri malli kuin llama3.2 muuta lataamasi malli kohtaan **model=""** tiedostossa: 

ai_utils.py:
```
def initialize_llm():
    load_dotenv(override=True)
    OLLAMA_SERVER_URL = os.environ["OLLAMA_SERVER_URL"]
    llm = OllamaLLM(model="llama3.2", base_url=OLLAMA_SERVER_URL)
    return llm
```
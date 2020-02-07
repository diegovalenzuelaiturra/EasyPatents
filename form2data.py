import json
import urllib.request


def main():

    # Insrtar Keys cuenta Typeform ( www.typeform.com )
    usr = ""
    key = ""

    url = "https://api.typeform.com/v1/form/" + usr + "?" + "key=" + key
    url_specs = "&" + "completed=true" + "&" + "order_by[]=date_submit,desc"  # + "&" + "limit=10"

    url = url + url_specs

    page = urllib.request.urlopen(url)

    content_bytes = page.read()
    content = content_bytes.decode('utf8')

    obj = json.loads(content)

    ##print(json.dumps(obj, indent=4)) ### NO BORRAR

    completed = obj['stats']['responses'][
        'completed']  # total de respuestas completadas
    showing = obj['stats']['responses'][
        'showing']  # total de respuestas que son mostradas

    #print(completed)
    #print(showing)

    for i in range(showing):

        respuesta = obj['responses'][i]['answers']['textarea_52850750']
        email = obj['responses'][i]['answers']['email_52850524']
        nombre = obj['responses'][i]['answers']['textfield_52850379']

        print('\n')
        print(nombre)
        print(email)
        print(respuesta)


if __name__ == "__main__":
    main()

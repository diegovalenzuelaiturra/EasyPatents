from EPmail import EPmail

def initMG(apiurl = 'https://api.mailgun.net/v3/mail.easypatents.cl/messages',
        apikey = 'key-a4953915dffa936b1e83070c0de3c3ef'):
    return EPmail(apiurl, apikey)

#
#
#
# mtext = 'Hola! soy Ro, y te adjunto mi auxiliar 12'
# msubject = 'Auxiliar 12'
# mfrom = 'ribanez@easypatents.cl'
# mto = '@gmail.com'
#
# #archivos adjuntos
# fname = '/home/ribanez/Descargas/Auxiliar12.pdf'
# fformat = 'Auxiliar12.pdf'
# epm = EPmail(apiurl, apikey)
# aux = epm.send_simple_message(mto, mfrom, msubject, mtext)
# aux = epm.send_complex_message(mto,mfrom,msubject,mtext,fformat,fname)
# print(aux)
import xmlrpc.client
#import datetime
class AllowNoneTransport(xmlrpc.client.Transport):
    def __init__(self, use_datetime=False, allow_none=True):
        super().__init__(use_datetime)
        self.allow_none = allow_none
        
    def get_encoder(self, *args, **kwargs):
        encoder = super().get_encoder(*args, **kwargs)
        encoder.allow_none = self.allow_none
        return encoder 


def mailsend(card, loc, tt, vehicle_id,vehicle, plaque,person):
    server_url = 'http://localhost:8081'
    db = 'analytic_odoo'
    username = 'admin'
    password = 'p@5dM_'

    common = xmlrpc.client.ServerProxy(server_url+'/xmlrpc/2/common')

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy(server_url + '/xmlrpc/2/object', transport=AllowNoneTransport())



    body_html = """
    <p>Bonjour,</p>
    <p>Bienvennue dans l'enceinte viseo Andraharo</p>
    <p>Vous êtes passé à {} le {} portant l'identifiant : {} , avec le vehicule {} portant l'immatriculation {} .</p>
    <p>Cordialement</p>
    """

    message = {
        'subject':'RFID',
        'body_html':body_html.format(loc, tt, card, vehicle, plaque),
        'email_to':'alt.dev@viseo.mg',
        'email_from':'odoo@viseo.mg',
    }
    
    records = {
        'id_vehicle':vehicle_id,
        'date_check': tt,
        
        'rfid_tag': card,
        'location':loc,
        'vehicle':vehicle+' / '+plaque,
    }




    message_create_id = models.execute_kw(db, uid,password, 'mail.mail', 'create', [message])
    record_id = models.execute_kw(db, uid,password, 'fleet.viseo.vehicule.logs', 'create', [records])

    mail_id = message_create_id
    
    if record_id:
        print("Record create successfully")
    else:
        print("Error creating record")

    if message_create_id:
        try:
            result = models.execute_kw(db, uid, password, 'mail.mail', 'send',[mail_id])
            print("Mail send successfully!!")
        except xmlrpc.client.Fault as e :
            print("Error!! mais pas de souci, le mail est belle et bien envoyé")
    else:
        print('Erreur!!')



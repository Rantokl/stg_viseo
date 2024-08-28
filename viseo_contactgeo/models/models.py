

from odoo import models, fields, api

class ContactGeo(models.Model):
    _inherit = "res.partner"

    commune= fields.Char(string='Commune')
    district= fields.Char(string= 'District')
    region= fields.Selection([
        ('Analamanga', 'Analamanga'),('Bongolava', 'Bongolava'),('Itasy', 'Itasy'),('Vakinankaratra', 'Vakinankaratra'), ('Diana', 'Diana'),
        ('Sava', 'Sava'), ('Amoron\'i Mania', 'Amoron\'i Mania'), ('Atsimo-Atsinanana', 'Atsimo-Atsinanana'), ('Fitovinany', 'Fitovinany'), ('Haute Matsiatra', 'Haute Matsiatra'),
        ('Ihorombe', 'Ihorombe'), ('Vatovavy', 'vatovavy'), ('Betsiboka', 'Betsiboka'), ('Boeny', 'Boeny'), ('Melaky', 'Melaky'), ('Sofia', 'Sofia'), ('Alaotra-Mangoro', 'Alaotra-Mangoro'),
        ('Ambatosoa', 'Ambatosoa'), ('Analanjirofo', 'Analanjirofo'), ('Atsinanana', 'Atsinanana'), ('Androy', 'Androy'), ('Anosy', 'Anosy'), ('Atsimo-Andrefana', 'Atsimo-Andrefana'), ('Menabe', 'Menabe')
    ], string= 'Région')
    province= fields.Selection([
        ('Antananarivo', 'Antananarivo'), ('Antsiranana', 'Antsiranana'), ('Fianarantsoa', 'Fianarantsoa'),
        ('Mahajanga', 'Mahajanga'), ('Toamasina', 'Toamasina'), ('Toliara', 'Toliara')
    ], string= 'Province')



from odoo import models, fields, api,SUPERUSER_ID
from odoo.exceptions import UserError

from dateutil.relativedelta import relativedelta

class TypeServicetools(models.Model):
    _name = 'type.services.tools.contract'

    name = fields.Char('Type de service')

class ProductContracts(models.Model):
    _name = 'product.for.tools.contracts'


    type_svc_id = fields.Many2one('type.services.tools.contract', string="Type entretien")
    company_id = fields.Many2one('res.company', string='Société')
    product_id = fields.Many2one('product.product', string="Article") #, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    qty = fields.Float(string="Qté")
    price_unit = fields.Float(string="Prix unitaire")
    price_subtotal = fields.Float(string="Prix total")

    @api.onchange('price_unit')
    def _onchange_price_subtotal(self):
        self.price_subtotal = self.price_unit * self.qty


    def _create_stock_moves_transfer(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            template = {
                'name': line.product_id.name or '',
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.qty,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'picking_id': picking.id,
                'state': 'draft',
                'company_id': line.company_id.id,
                'picking_type_id': picking.picking_type_id.id,
                'warehouse_id': picking.picking_type_id.warehouse_id.id,
            }

            done += moves.create(template)
        return done


class TypeWorkServiceToolsContracts(models.Model):
    _name = 'type.services.equipment.contract'

    contract_id = fields.Many2one('equipment.log.contract', string='Contrat')
    model_type_work_id = fields.Many2one('type.services.contract', string='Type ')
    servicing_id = fields.Many2one('fleet.service.work', string="Type entretien", required=True)
    order_servicing = fields.Integer("Nom", related='servicing_id.level')
    model_vehicle_id = fields.Many2one('fleet.vehicle.model', string="Modèle vehicule")
    product_ids = fields.One2many('product.for.tools.contracts', 'type_svc_id', string="Articles")
    company_id = fields.Many2one('res.company', string='société')
    amount_total = fields.Float("Montant total")
    is_reserved = fields.Boolean("Est reservé")
    is_done = fields.Boolean("Est déjà utilisé")

    @api.onchange('model_type_work_id')
    def get_domain_type_work(self):
        domain = []
        type_work_ids = self.model_vehicle_id.type_work_ids.ids
        if len(type_work_ids) > 0:
            domain += [('id', 'in', type_work_ids)]
        else:
            domain += [('id', 'in', False)]
        return {'domain': {'model_type_work_id': domain}}

class EquipementCost(models.Model):
    _name = 'equipment.cost'
    _description = 'Cost related to a equipment'
    _order = 'date desc, vehicle_id asc'

    name = fields.Char(related='equipment_id.name', string='Name', store=True, readonly=False)
    equipment_id = fields.Many2one('equipement.bike.tools', 'Vehicle', required=True, help='Vehicle concerned by this log')
    cost_subtype_id = fields.Many2one('fleet.service.type', 'Type', help='Cost type purchased with this cost')
    amount = fields.Float('Total Price')
    cost_type = fields.Selection([
        ('contract', 'Contract'),
        ('services', 'Services'),
        ('fuel', 'Fuel'),
        ('other', 'Other')
        ], 'Category of the cost', default="other", help='For internal purpose only', required=True)
    parent_id = fields.Many2one('fleet.vehicle.cost', 'Parent', help='Parent cost to this current cost')
    cost_ids = fields.One2many('fleet.vehicle.cost', 'parent_id', 'Included Services', copy=True)
    odometer_id = fields.Many2one('fleet.vehicle.odometer', 'Odometer', help='Odometer measure of the vehicle at the moment of this log')
    odometer = fields.Float( string='Odometer Value',
        help='Odometer measure of the vehicle at the moment of this log')
    # odometer_unit = fields.Selection(related='vehicle_id.odometer_unit', string="Unit", readonly=True)
    date = fields.Date(help='Date when the cost has been executed')
    contract_id = fields.Many2one('fleet.vehicle.log.contract', 'Contract', help='Contract attached to this cost')
    auto_generated = fields.Boolean('Automatically Generated', readonly=True)
    description = fields.Char("Cost Description")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    def _get_odometer(self):
        self.odometer = 0.0
        for record in self:
            record.odometer = False
            if record.odometer_id:
                record.odometer = record.odometer_id.value

    def _set_odometer(self):
        for record in self:
            if not record.odometer:
                raise UserError(_('Emptying the odometer value of a vehicle is not allowed.'))
            odometer = self.env['fleet.vehicle.odometer'].create({
                'value': record.odometer,
                'date': record.date or fields.Date.context_today(record),
                'vehicle_id': record.vehicle_id.id
            })
            self.odometer_id = odometer

    @api.model_create_multi
    def create(self, vals_list):
        for data in vals_list:
            # make sure that the data are consistent with values of parent and contract records given
            if 'parent_id' in data and data['parent_id']:
                parent = self.browse(data['parent_id'])
                data['vehicle_id'] = parent.vehicle_id.id
                data['date'] = parent.date
                data['cost_type'] = parent.cost_type
            if 'contract_id' in data and data['contract_id']:
                contract = self.env['fleet.vehicle.log.contract'].browse(data['contract_id'])
                data['vehicle_id'] = contract.vehicle_id.id
                data['cost_subtype_id'] = contract.cost_subtype_id.id
                data['cost_type'] = contract.cost_type
            if 'odometer' in data and not data['odometer']:
                # if received value for odometer is 0, then remove it from the
                # data as it would result to the creation of a
                # odometer log with 0, which is to be avoided
                del data['odometer']
        return super(EquipementCost, self).create(vals_list)


class EquipmentLogContract(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'equipment.cost': 'cost_id'}
    _name = 'equipment.log.contract'
    _description = 'Contract information on a equipment'
    _order = 'state desc,expiration_date'




    def compute_next_year_date(self, strdate):
        oneyear = relativedelta(years=1)
        start_date = fields.Date.from_string(strdate)
        return fields.Date.to_string(start_date + oneyear)

    @api.model
    def default_get(self, default_fields):
        res = super(EquipmentLogContract, self).default_get(default_fields)
        contract = self.env.ref('fleet.type_contract_leasing', raise_if_not_found=False)
        res.update({
            'date': fields.Date.context_today(self),
            'cost_subtype_id': contract and contract.id or False,
            'cost_type': 'contract'
        })
        return res

    name = fields.Text(compute='_compute_contract_name', store=True)
    active = fields.Boolean(default=True)
    cost_subtype_id_tools = fields.Many2one('tools.service.type', 'Type', help='Cost type purchased with this cost')
    contract_owner = fields.Many2one('res.partner', string="Titulaire du contrat")
    user_id = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user, index=True)
    type_work_ids = fields.One2many('type.services.equipment.contract', 'contract_id', string="Type de travaux")
    start_date = fields.Date('Contract Start Date', default=fields.Date.context_today,
        help='Date when the coverage of the contract begins')
    equipment_id = fields.Many2one('equipement.bike.tools', "Equipement")
    expiration_date = fields.Date('Contract Expiration Date', default=lambda self:
        self.compute_next_year_date(fields.Date.context_today(self)),
        help='Date when the coverage of the contract expirates (by default, one year after begin date)')
    days_left = fields.Integer(compute='_compute_days_left', string='Warning Date')
    insurer_id = fields.Many2one('res.partner', 'Vendor')
    purchaser_id = fields.Many2one('res.partner', 'Driver', default=lambda self: self.env.user.partner_id.id,
        help='Person to which the contract is signed for')
    ins_ref = fields.Char('Contract Reference', size=64, copy=False)
    state = fields.Selection([
        ('futur', 'Incoming'),
        ('open', 'In Progress'),
        ('diesoon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('closed', 'Closed')
        ], 'Status', default='open', readonly=True,
        help='Choose whether the contract is still valid or not',
        tracking=True,
        copy=False)
    notes = fields.Text('Terms and Conditions', help='Write here all supplementary information relative to this contract', copy=False)
    cost_generated = fields.Float('Recurring Cost Amount', tracking=True,
        help="Costs paid at regular intervals, depending on the cost frequency. "
        "If the cost frequency is set to unique, the cost will be logged at the start date")
    cost_frequency = fields.Selection([
        ('no', 'No'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
        ], 'Recurring Cost Frequency', default='no', help='Frequency of the recuring cost', required=True)
    generated_cost_ids = fields.One2many('fleet.vehicle.cost', 'contract_id', 'Generated Costs')
    sum_cost = fields.Float(compute='_compute_sum_cost', string='Indicative Costs Total')
    cost_id = fields.Many2one('fleet.vehicle.cost', 'Cost', required=True, ondelete='cascade')
    # we need to keep this field as a related with store=True because the graph view doesn't support
    # (1) to address fields from inherited table
    # (2) fields that aren't stored in database
    cost_amount = fields.Float(related='cost_id.amount', string='Amount', store=True, readonly=False)
    odometer = fields.Float(string='Creation Contract Odometer',
        help='Odometer measure of the vehicle at the moment of the contract creation')

    @api.depends('equipment_id.name', 'cost_subtype_id', 'date')
    def _compute_contract_name(self):
        for record in self:
            name = record.equipment_id.name
            if record.cost_subtype_id.name:
                name += ' / ' + record.cost_subtype_id.name
            if record.date:
                name += ' / ' + str(record.date)
            record.name = name

    @api.depends('expiration_date', 'state')
    def _compute_days_left(self):
        """return a dict with as value for each contract an integer
        if contract is in an open state and is overdue, return 0
        if contract is in a closed state, return -1
        otherwise return the number of days before the contract expires
        """
        for record in self:
            if record.expiration_date and record.state in ['open', 'diesoon', 'expired']:
                today = fields.Date.from_string(fields.Date.today())
                renew_date = fields.Date.from_string(record.expiration_date)
                diff_time = (renew_date - today).days
                record.days_left = diff_time > 0 and diff_time or 0
            else:
                record.days_left = -1

    @api.depends('cost_ids.amount')
    def _compute_sum_cost(self):
        for contract in self:
            contract.sum_cost = sum(contract.cost_ids.mapped('amount'))

    # @api.onchange('equipment_id')
    # def _onchange_vehicle(self):
    #     if self.equipment_id:
    #         self.odometer_unit = self.equipment_id.odometer_unit

    def write(self, vals):
        res = super(EquipmentLogContract, self).write(vals)
        if vals.get('expiration_date') or vals.get('user_id'):
            self.activity_reschedule(['fleet.mail_act_fleet_contract_to_renew'], date_deadline=vals.get('expiration_date'), new_user_id=vals.get('user_id'))
        return res

    def contract_close(self):
        for record in self:
            record.state = 'closed'

    def contract_open(self):
        for record in self:
            record.state = 'open'

    def act_renew_contract(self):
        assert len(self.ids) == 1, "This operation should only be done for 1 single contract at a time, as it it suppose to open a window as result"
        for element in self:
            # compute end date
            startdate = fields.Date.from_string(element.start_date)
            enddate = fields.Date.from_string(element.expiration_date)
            diffdate = (enddate - startdate)
            default = {
                'date': fields.Date.context_today(self),
                'start_date': fields.Date.to_string(fields.Date.from_string(element.expiration_date) + relativedelta(days=1)),
                'expiration_date': fields.Date.to_string(enddate + diffdate),
            }
            newid = element.copy(default).id
        return {
            'name': _("Renew Contract"),
            'view_mode': 'form',
            'view_id': self.env.ref('fleet.fleet_vehicle_log_contract_view_form').id,
            'res_model': 'fleet.vehicle.log.contract',
            'type': 'ir.actions.act_window',
            'domain': '[]',
            'res_id': newid,
            'context': {'active_id': newid},
        }

    @api.model
    def scheduler_manage_auto_costs(self):
        # This method is called by a cron task
        # It creates costs for contracts having the "recurring cost" field setted, depending on their frequency
        # For example, if a contract has a reccuring cost of 200 with a weekly frequency, this method creates a cost of 200 on the
        # first day of each week, from the date of the last recurring costs in the database to today
        # If the contract has not yet any recurring costs in the database, the method generates the recurring costs from the start_date to today
        # The created costs are associated to a contract thanks to the many2one field contract_id
        # If the contract has no start_date, no cost will be created, even if the contract has recurring costs
        VehicleCost = self.env['fleet.vehicle.cost']
        deltas = {
            'yearly': relativedelta(years=+1),
            'monthly': relativedelta(months=+1),
            'weekly': relativedelta(weeks=+1),
            'daily': relativedelta(days=+1)
        }
        contracts = self.env['equipment.log.contract'].search([('state', '!=', 'closed')], offset=0, limit=None, order=None)
        for contract in contracts:
            if not contract.start_date or contract.cost_frequency == 'no':
                continue
            found = False
            startdate = contract.start_date
            if contract.generated_cost_ids:
                last_autogenerated_cost = VehicleCost.search([
                    ('contract_id', '=', contract.id),
                    ('auto_generated', '=', True)
                ], offset=0, limit=1, order='date desc')
                if last_autogenerated_cost:
                    found = True
                    startdate = last_autogenerated_cost.date
            if found:
                startdate += deltas.get(contract.cost_frequency)
            today = fields.Date.context_today(self)
            while (startdate <= today) & (startdate <= contract.expiration_date):
                data = {
                    'amount': contract.cost_generated,
                    'date': fields.Date.context_today(self),
                    'equipment_id': contract.equipment_id.id,
                    'cost_subtype_id': contract.cost_subtype_id.id,
                    'contract_id': contract.id,
                    'auto_generated': True
                }
                self.env['fleet.vehicle.cost'].create(data)
                startdate += deltas.get(contract.cost_frequency)
        return True

    @api.model
    def scheduler_manage_contract_expiration(self):
        # This method is called by a cron task
        # It manages the state of a contract, possibly by posting a message on the vehicle concerned and updating its status
        params = self.env['ir.config_parameter'].sudo()
        delay_alert_contract = int(params.get_param('hr_fleet.delay_alert_contract', default=30))
        date_today = fields.Date.from_string(fields.Date.today())
        outdated_days = fields.Date.to_string(date_today + relativedelta(days=+delay_alert_contract))
        nearly_expired_contracts = self.search([('state', '=', 'open'), ('expiration_date', '<', outdated_days)])

        nearly_expired_contracts.write({'state': 'diesoon'})
        for contract in nearly_expired_contracts.filtered(lambda contract: contract.user_id):
            contract.activity_schedule(
                'fleet.mail_act_fleet_contract_to_renew', contract.expiration_date,
                user_id=contract.user_id.id)

        expired_contracts = self.search([('state', 'not in', ['expired', 'closed']), ('expiration_date', '<',fields.Date.today() )])
        expired_contracts.write({'state': 'expired'})

        futur_contracts = self.search([('state', 'not in', ['futur', 'closed']), ('start_date', '>', fields.Date.today())])
        futur_contracts.write({'state': 'futur'})

        now_running_contracts = self.search([('state', '=', 'futur'), ('start_date', '<=', fields.Date.today())])
        now_running_contracts.write({'state': 'open'})

    def run_scheduler(self):
        self.scheduler_manage_auto_costs()
        self.scheduler_manage_contract_expiration()


class Tools_service_type(models.Model):
    _name = 'tools.service.type'

    name= fields.Char('Type de contrat')
odoo.define('web_gantt_project_task_app.gantt_controller', function (require) {
"use strict";


var AbstractController = require('web.AbstractController');
var core = require('web.core');
var dialogs = require('web.view_dialogs');
var confirmDialog = require('web.Dialog').confirm;

var QWeb = core.qweb;
var _t = core._t;


var gantt_controller = AbstractController.extend({

	init: function (parent, model, renderer, params) {
		this._super.apply(this, arguments);
	},
});

return gantt_controller;
});

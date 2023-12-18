odoo.define('web_gantt_project_task_app.GanttView', function (require) {
"use strict";

var AbstractView = require('web.AbstractView');
var core = require('web.core');
var GanttModel = require('web_gantt_project_task_app.gantt_model');
var GanttRenderer = require('web_gantt_project_task_app.gantt_renderer');
var GanttController = require('web_gantt_project_task_app.gantt_controller');
var view_registry = require('web.view_registry');
var QWeb = core.qweb;


var _t = core._t;
var _lt = core._lt;


var GantttView = AbstractView.extend({
	display_name: _lt('Ganttt'),
	template: "GantttView",
	jsLibs: [
			"/web_gantt_project_task_app/static/lib/anychart-core.min.js",
			"/web_gantt_project_task_app/static/lib/anychart-gantt.min.js"
		],
	icon: 'fa-tasks',
	config: _.extend({},AbstractView.prototype.config, {
        Model: GanttModel,
        Controller: GanttController,
        Renderer: GanttRenderer,
    }),
    view_type: "ganttt",

	/**
     * @override
     */
	init: function (viewInfo, params) {
		var self = this;
		self.parent_actions = parent.actions
		this._super.apply(this, arguments);
		this.$view = $(QWeb.render('GantttView'));
		this.$loading = this.$view.find('#container');
	},

});
view_registry.add('ganttt', GantttView);

return GantttView;

});

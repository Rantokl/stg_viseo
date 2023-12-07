odoo.define('web_gantt_project_task_app.gantt_renderer', function (require) {
"use strict";

var AbstractRenderer = require('web.AbstractRenderer');
var rpc = require('web.rpc');
var core = require('web.core');

return AbstractRenderer.extend({
className: "o_ganttt_view",

init: function () {
	this._super.apply(this, arguments);
},

_render: function () { 
	this.$el.empty();
	this.show_ganttt();
	return $.when();
},

open_project_item_form_page: function(id) {
	var self = this;
	self.do_action({
		type: 'ir.actions.act_window',
		res_model: 'viseo.project.project',
		// view_id: 'inherited_edit_project2',
		views: [
			[false, 'form']
		],
		target: 'current',
		context: {
			'form_view_ref': 'web_gantt_project_task_app.inherited_edit_project2',
			'form_view_initial_mode': 'edit',
		},
		res_id: id
	}, {
		on_reverse_breadcrumb: this.on_reverse_breadcrumb,
	});
},


open_task_item_form_page: function(id) {
	var self = this;
	self.do_action({
		type: 'ir.actions.act_window',
		res_model: 'viseo.project.task',
		// view_id: 'inherited_edit_project2',
		views: [
			[false, 'form']
		],
		target: 'current',
		context: {
			'form_view_ref': 'web_gantt_project_task_app.inherited_view_task_form2',
			'form_view_initial_mode': 'edit',
		},
		res_id: id
	}, {
		on_reverse_breadcrumb: this.on_reverse_breadcrumb,
	});
},


show_ganttt: function () {
	var self = this
	anychart.onDocumentReady(function () {

		core.bus.on('DOM_updated', this, function () {
			console.log(this)
			var url = window.location.href
			var match = url.match(/active_id=(\d+)|\/web#id=(\d+)/);
			var record_id = match ? match[1] : null;
			
			rpc.query({
				model: 'viseo.project.project',
				method: 'get_ganttt_data',
				args: [record_id],
			}).then(function(output) {
				if ($('.o_ganttt_view #container')) {
					$('.o_ganttt_view #container').remove()
				}
				$('.o_ganttt_view').css("height", "98%");

				$('.o_ganttt_view').append(`
					<div id='container'>
						<div style="display:flex; justify-content: space-between;">
							<div style="display:flex;">
								<button id="disableButton">Hide Grid</button>
								<button id="enableButton">Show Grid</button>
								<button id="collapseAll">Collaps all</button>
								<button id="expandAll">Expand all</button>
							</div>

							<div style="display:flex; margin-right: 10px">
								<button id="fitAllProject">fit all</button>
								<button id="zoomInButton">+</button>
								<button id="zoomOutButton">-</button>
								<button id="zoomToUnitsButton">Zoom To Units</button>
								<select id="unitSelect" style="width:40px;">
									<option value="hour">hour</option>
									<option value="day">day</option>
									<option value="week" selected>week</option>
									<option value="month">month</option>
									<option value="year">year</option>
								</select>

								<label>count: <input id="countInput" value="2" style="width:30px;"></label>
							</div>
						</div>
						<style>
							button, select, label {
								margin: 5px 0 5px 10px;
							}
	
							#container {
								width: 100%;
								height: calc(100% - 20px);
								padding: 0;
							}
	
						</style>
					</div>
				`);

				// create a chart
				var chart = anychart.ganttProject();

				// set the container id
				chart.container('container');

				// chart style
				var date_tooltip = "<span style='font-weight:600;font-size:12pt'> {%start}{dateTimeFormat:dd MMM} – {%end}{dateTimeFormat:dd MMM} </span>"
				chart.rowHoverFill("#ffd54f 0.3");
				chart.rowSelectedFill("#ffd54f 0.3");
				chart.defaultRowHeight(40);
				chart.dataGrid().tooltip().useHtml(true); 
				chart.dataGrid().tooltip().format(date_tooltip);

				// splitter position
				chart.splitterPosition("395px");

				// Grid style
				var dataGrid = chart.dataGrid();
				dataGrid.rowEvenFill("gray 0.2");
				dataGrid.rowOddFill("gray 0.01");
				dataGrid.rowHoverFill("#ffd54f 0.3");
				dataGrid.rowSelectedFill("#ffd54f 0.3");
				chart.getTimeline().tooltip().useHtml(true);
				chart.getTimeline().tooltip().format(date_tooltip);

				// Timeline style
				var timeline = chart.getTimeline();
				timeline.rowEvenFill("gray 0.2");
				timeline.rowOddFill("gray 0.01");
				timeline.rowHoverFill("#ffd54f 0.3");
				timeline.rowSelectedFill("#ffd54f 0.3");

				// Button expand style
				var buttons = chart.dataGrid().buttons();
				buttons.fontWeight(600);
				buttons.fontSize(13);
				buttons.width(30);
				buttons.fontFamily("Courier");
				buttons.background().fill(null);
				buttons.background().stroke(null);
				buttons.normal().content("[+]");
				buttons.normal().fontColor("#ef6c00");
				buttons.hovered().fontColor(anychart.color.lighten("#ef6c00"));
				buttons.selected().content("[-]");
				buttons.selected().fontColor("#64b5f6");

				/******************************  COLUMN CONFIG  *********************************/
				// FUNCTION STYLING for dataGrid data

				function formatParent(data , children){
					if (children) {
						return "<span style='font-weight:bold;color:#00234f;font-size:11px'>" + String(data).toUpperCase() + "</span>";
					} else {
						return "<span style='color:#00234f';font-size:14px>" + data + "</span>";
					}
				}

				function formatDate(date, children){
					if ( isNaN(date) ) return '...'
					let newDate = new Date(date);
					let formatted_date = newDate.getDate() + "/" + (newDate.getMonth() + 1) + "/" + newDate.getFullYear();
					return formatParent(formatted_date, children);
				}

				// Column 1 style
				var column1 = chart.dataGrid().column(0).width(50);
				column1.title().enabled(true);
				column1.title().text('#');
				column1.title().fontSize(12).fontWeight('bold').fontColor('#00234f');
				column1.labels().useHtml(true);
				column1.labels().format(function(){
					return formatParent(this.id, this.item.numChildren())
				});

				// Column 2 style
				var column2 = chart.dataGrid().column(1).width(150);
				column2.title().enabled(true);
				column2.title().text('Name');
				column2.title().fontSize(12).fontWeight('bold').fontColor('#00234f');
				column2.labels().useHtml(true);
				column2.labels().format(function(){
					return formatParent(this.name, this.item.numChildren())
				});

				// Column 3: start date style
				var startColumn = chart.dataGrid().column(2);
				startColumn.width(80);
				startColumn.title().enabled(true);
				startColumn.title().text('Start');
				startColumn.title().fontSize(12).fontWeight('bold').fontColor('#00234f');
				startColumn.labels().useHtml(true);
				startColumn.labels().format(function(){
					return formatDate(this.actualStart, this.item.numChildren())
				});

				// Column 4: end date style
				var endColumn = chart.dataGrid().column(3);
				endColumn.width(80);
				endColumn.title().enabled(true);
				endColumn.title().text('End');
				endColumn.title().fontSize(12).fontWeight('bold').fontColor('#00234f');
				endColumn.labels().useHtml(true);
				endColumn.labels().format(function(){
					return formatDate(this.actualEnd, this.item.numChildren())
				});

				// Column 5: durrée
				var deltadate = chart.dataGrid().column(4);
				deltadate.width(30);
				deltadate.title().enabled(true);
				deltadate.title().text('Δ');
				deltadate.title().fontSize(12).fontWeight('bold').fontColor('#00234f');
				deltadate.labels().useHtml(true);
				deltadate.labels().format(function(){
					if (isNaN(this.actualStart) || isNaN(this.actualEnd)) return '...'

					const date1 = new Date(this.actualStart);
					const date2 = new Date(this.actualEnd);
					const diffTime = date2 - date1;
					const diffDays = diffTime / (1000 * 60 * 60 * 24);

					return formatParent( diffDays , this.item.numChildren());
				});

				/******************************  EVENT LISTENER  *********************************/
				// Attach event listeners to the buttons
				$('#enableButton').click(() => {
					chart.splitterPosition("395px");
				});
				$('#disableButton').click(() => {
					chart.splitterPosition("0%");
				});
				$('#fitAllProject').click(() => {
					chart.fitAll();
				});
				$('#collapseAll').click(() => {
					chart.collapseAll();
				});
				$('#expandAll').click(() => {
					chart.expandAll();
				});
				$('#zoomInButton').click(() => {
					chart.zoomIn(1.5);
				});
				$('#zoomOutButton').click(() => {
					chart.zoomOut(1.5);
				});
				$('#zoomToUnitsButton').click(() => {
					var unit = document.getElementById("unitSelect").value;
					var count = document.getElementById("countInput").value;
					chart.zoomTo(unit, count, 'first-date');
				});

				/******************************  ROW EVENTS  *********************************/

				// redirection vers formulaires
				chart.listen("rowClick", function (row) {
					var id = row.item.get("redirection_Id");
					var hierarchical_id = row.item.get("id")
					if (hierarchical_id.length > 1) { hierarchical_id = hierarchical_id.slice(-1) }

					if (parseInt(hierarchical_id)) { self.open_project_item_form_page(id); }
					else { self.open_task_item_form_page(id); }

				});



				chart.fitAll();
				// create a data tree
				var treeData = anychart.data.tree(output, "as-tree");

				// set the data
				chart.data(treeData);

				// draw chart
				chart.draw();
			})
		})
	})
}})});




function showModal(content) {
        document.getElementById('modalContent').innerText = content;
        var myModal = new Modal(document.getElementById('dataModal'));
        myModal.show();
    }

function showWizard(){
//console.log('TEst')
    var action = {
                        type: 'ir.actions.act_window',
                        res_model: 'analytic.addchild',
                        view_mode: 'form',
                        view_type: 'form',
                        target: 'new',
                        context: {}  // Vous pouvez ajouter des valeurs contextuelles si nécessaire
                    };
}

//function loadTableData() {
//        var table = document.querySelector("#tableanalytique");
//        var tableHead = table.querySelector("thead");
//        var tableBody = table.querySelector("tbody");
//        // Supposons que vous avez une route définie pour obtenir les données du tableau.
//        odoo.define('module_name.dynamic_table', function(require) {
//            "use strict";
//            var ajax = require('web.ajax');
//
//            ajax.jsonRpc('/get_dynamic_table_data', 'call', {})
//                .then(function (data) {
//                    // Clear existing rows
//                    tableBody.innerHTML = '';
//                    data.forEach(function(row, index) {
//                        var tr = document.createElement('tr');
//                        var tdHeader = document.createElement('td');
//                        tdHeader.textContent = 'Row ' + (index + 1);
//                        tr.appendChild(tdHeader);
//
//                        row['rows'].forEach(function(cell) {
//                            var td = document.createElement('td');
//                            td.textContent = cell;
//                            tr.appendChild(td);
//                        });
//
//                        tableBody.appendChild(tr);
//                    });
//                });
//        });
//    }
//
//    document.addEventListener('DOMContentLoaded', function() {
//        loadTableData();
//    });

//document.addEventListener('DOMContentLoaded', function () {
//                const addButton = document.querySelector("#ajouterEnfantButton");
//                addButton.addEventListener("click", function () {
//                    // Ouvrir le wizard pour ajouter des enfants
//                    console.log('Add')
//                    var action = {
//                        type: 'ir.actions.act_window',
//                        res_model: 'analytic.addchild',
//                        view_mode: 'form',
//                        view_type: 'form',
//                        target: 'new',
//                        context: {}  // Vous pouvez ajouter des valeurs contextuelles si nécessaire
//                    };
//                    framework.blockUI();
//                    this.do_action(action, {
//                        on_close: function() { framework.unblockUI(); }
//                    });
//                });
//            });
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
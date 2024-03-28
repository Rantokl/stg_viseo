function showModal(content) {
        document.getElementById('modalContent').innerText = content;
        var myModal = new Modal(document.getElementById('dataModal'));
        myModal.show();
    }
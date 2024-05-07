document.addEventListener("DOMContentLoaded", function() {
    const openAddModalButton = document.getElementById("open-add-modal");
    const closeAddModalButton = document.getElementById("close-add-modal");
    const addModal = document.getElementById("add-modal");

    openAddModalButton.addEventListener("click", function() {
        addModal.style.display = "flex"; // Show modal
        addModal.style.alignItems = "center";
        addModal.style.justifyContent = "center";
    });

    closeAddModalButton.addEventListener("click", function() {
        addModal.style.display = "none"; // Close modal
    });

    window.addEventListener("click", function(event) {
        if (event.target == addModal) {
            addModal.style.display = "none"; // Close modal if clicked outside of it
        }
    });
});

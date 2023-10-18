// Add cafe

document.getElementById("cancel-button-add").addEventListener("click", AddConfirmationClose)

function AddConfirmationClose() {
  const dialog_add_cafe = document.getElementById("add-confirmation")
  const deleteConfirmation = dialog_add_cafe.close();
}

// Delete cafe/comment

document.getElementById("cancel-button-2").addEventListener("click", DeleteConfirmationClose)

function DeleteConfirmationClose() {
  const dialog_delete_cafe  = document.getElementById("delete-confirmation")
  const deleteConfirmation = dialog_delete_cafe.close();
}
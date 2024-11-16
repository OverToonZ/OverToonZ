sessionStorage.setItem("lastopened", "");

function operation(id) {
  var lastOpened = sessionStorage.getItem("lastopened");
  var modified = document.getElementsByClassName("Modifyfield");

  for (var i = 0; i < modified.length; i++) {
    modified[i].disabled = true;
  }

  if (!lastOpened) {
    sessionStorage.setItem("lastopened", id);
  } else if (id !== lastOpened) {
    var lastForm = document.getElementById(lastOpened + "form");
    if (lastForm) {
      lastForm.classList.add("d-none");
    }
    sessionStorage.setItem("lastopened", id);
  }

  var formid = id + "form";
  var content = document.getElementById(formid);

  if (content) {
    if (content.classList.contains("d-none")) {
      content.classList.remove("d-none");
    } else {
      content.classList.add("d-none");
    }
  } else {
    console.error("Element with ID " + formid + " not found.");
  }
}

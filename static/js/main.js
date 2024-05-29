function SQLBuilder(n) {
    let input = document.querySelector("#SQLInput")

    switch (n) {
        case 1:
            input.value += "SELECT * FROM maindb_presentation "
            break;

        case 2:
            input.value += " WHERE "
            break;
        case 3:
            input.value += " title = "
            break;
        case 4:
            input.value += " author =  "
            break;
        case 5:
            input.value += " [group] = "
            break;
        case 6:
            input.value += " time = "
            break;

        case 7:
            input.value += " AND "
            break;

        case 8:
            input.value += " OR "
            break;
        case 9:
            input.value += " NOT "
            break;
        case 10:
            input.value += " rating = "
            break;
        case 11:
            input.value += " notes = "
            break;
    }
}

const dropContainer = document.getElementById("dropcontainer");
const fileInput = document.getElementById("images");

dropContainer.addEventListener("dragover", e => {
    // prevent default to allow drop
    e.preventDefault();
}, false);

dropContainer.addEventListener("dragenter", () => {
    dropContainer.classList.add("drag-active");
});

dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-active");
});

dropContainer.addEventListener("drop", e => {
    e.preventDefault();
    dropContainer.classList.remove("drag-active");
    fileInput.files = e.dataTransfer.files;
});

function resetInput(name) {
    if (name === "group") {
        if (document.getElementById("is_auto")) {
            if (!document.getElementById("is_auto").checked) {
                document.getElementById(name).value = '';
            }
        }else {
            document.getElementById(name).value = '';
        }
    } else {
        document.getElementById(name).value = '';
    }

}


document.getElementById("is_auto").addEventListener("click", function () {
    document.getElementById('group').readOnly = !!document.getElementById("is_auto").checked;
    let isAutoChecked = document.getElementById("is_auto").checked;

    if (isAutoChecked && document.getElementById('group').value == '') {
        document.getElementById('group').value = "Вміст";
    } else if (document.getElementById('group').value == "Вміст") {
        document.getElementById('group').value = "";
    }

})


function loadingWindow() {
    if (checkInputs()) {
        document.getElementById("loading-overlay").style.display = "block";
    }

}

function checkInputs() {
    var inputs = document.querySelectorAll('input');
    var isValid = true;
    inputs.forEach(function (input) {
        if (input.value.trim() === '') {
            isValid = false;
        }
    });
    return isValid;
}


// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close1")[0];

// When the user clicks the button, open the modal
btn.onclick = function () {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
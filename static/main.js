window.addEventListener('load', function() {
    // Clear session
    fetch('/clear_session', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch((error) => console.error('Error:', error));

    // Clear form fields
    const clearBtn = document.getElementById("clearBtn");
    if (clearBtn) {
        clearBtn.addEventListener("click", function() {
            document.getElementById("search_term").value = "";
            document.getElementById("location").value = "";
            document.getElementById("distance").value = "";
            document.getElementById("job_type").value = "";
            document.getElementById("results_wanted").value = "";
        });
    }
});

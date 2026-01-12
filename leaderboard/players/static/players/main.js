document.addEventListener("DOMContentLoaded", function() {
    const addForm = document.getElementById("addForm");
    const csrftoken = getCookie('csrftoken');
    addForm.addEventListener("submit", async e => {
        e.preventDefault();
        const formData = new FormData(addForm);
        await fetch("/add/", { method: "POST", body: formData });
        location.reload();
    });

    document.querySelectorAll(".update-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
            const row = btn.closest("tr");
            const playerId = row.dataset.id;
            const score = row.querySelector(".score").value;
            await fetch("/update/", {
                method: "POST",
                headers:{
                    "X-CSRFToken" : csrftoken
                },
                body: new URLSearchParams({id: playerId, score: score})
            });
            location.reload();
        });
    });

    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
            const row = btn.closest("tr");
            const playerId = row.dataset.id;
            await fetch("/delete/", {
                method: "POST",
                headers:{
                    "X-CSRFToken" : csrftoken
                },
                body: new URLSearchParams({id: playerId})
            });
           location.reload();
        });
    });
});

function getCookie(name){
    let cookieValue = null;
    if (document.cookie){
        const cookies = document.cookie.split(';');
        for (let c of cookies){
            c = c.trim();
            if (c.startsWith(name + '=')){
                cookieValue = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
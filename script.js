function loadPage(page, btn) {
    fetch("pages/" + page)
        .then(res => {
            if (!res.ok) {
                throw new Error("Errore nel caricamento: " + page);
            }
            return res.text();
        })
        .then(html => {
            document.getElementById("content").innerHTML = html;
        })
        .catch(err => {
            document.getElementById("content").innerHTML =
                "<p style='color:red'>Errore caricamento pagina</p>";
            console.error(err);
        });

    document.querySelectorAll(".nav-btn").forEach(b => {
        b.classList.remove("active");
    });

    btn.classList.add("active");
}
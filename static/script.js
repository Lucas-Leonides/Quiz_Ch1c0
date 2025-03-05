let options = [];
let selectedIndex = 0;
let timer;

function fetchQuestion() {
    fetch("/question")
        .then(response => response.json())
        .then(data => {
            document.getElementById("question").innerText = data.pergunta;
            let optionsDiv = document.getElementById("options");
            optionsDiv.innerHTML = "";
            options = [data.opcao1, data.opcao2, data.opcao3];
            options.forEach((opt, index) => {
                let div = document.createElement("div");
                div.classList.add("option");
                div.innerText = opt;
                if (index === 0) div.classList.add("selected");
                optionsDiv.appendChild(div);
            });
            selectedIndex = 0;
            startTimer();
        });
}

function updateSelection() {
    document.querySelectorAll(".option").forEach((el, index) => {
        el.classList.toggle("selected", index === selectedIndex);
    });
}

function startTimer() {
    clearTimeout(timer);
    timer = setTimeout(() => fetchQuestion(), 15000);
}

document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowUp" || e.key === "ArrowDown") {
        selectedIndex = (selectedIndex + (e.key === "ArrowDown" ? 1 : -1) + options.length) % options.length;
        updateSelection();
    } else if (e.key === " ") {
        alert("Você escolheu: " + options[selectedIndex]);
        fetchQuestion();
    }
});

fetchQuestion();

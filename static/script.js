async function fetchEvents() {
    const res = await fetch('/events');
    const data = await res.json();

    const ul = document.getElementById("events");
    ul.innerHTML = "";

    data.forEach(e => {
        let msg = "";
        const time = new Date(e.timestamp).toUTCString();

        if (e.action === "PUSH") {
            msg = `${e.author} pushed to ${e.to_branch} on ${time}`;
        }

        if (e.action === "PULL_REQUEST") {
            msg = `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${time}`;
        }

        const li = document.createElement("li");
        li.innerText = msg;
        ul.appendChild(li);
    });
}

fetchEvents();
setInterval(fetchEvents, 15000);
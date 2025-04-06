document.getElementById("deadlockForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const processes = document.getElementById("processes").value;
    const resources = document.getElementById("resources").value;
    const allocationInput = document.getElementById("allocation").value.trim();
    const requestInput = document.getElementById("request").value.trim();

    const allocation = allocationInput.split(",").map(Number);
    const request = requestInput.split(",").map(Number);

    if (allocation.length !== processes * resources || request.length !== processes * resources) {
        document.getElementById("error-message").textContent = "Matrix dimensions do not match!";
        return;
    }

    document.getElementById("error-message").textContent = "";

    const response = await fetch("/detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ processes, resources, allocation, request })
    });

    const result = await response.json();
    
    document.getElementById("result").textContent = result.message || "Error occurred!";
});

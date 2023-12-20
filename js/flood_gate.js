import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
	name: "Comfy.FloodGate",
	async setup() {
		const floodButton = document.createElement("button");
		floodButton.textContent = "Floodgate: Close";
		floodButton.style.margin = '-4px 0px 6px 0px';

		floodButton.addEventListener("click", async () => {
			const resp = await api.fetchApi('/floodgate');
			const stat = await resp.json();

			if (stat['status'])
				floodButton.textContent = "Floodgate: Open";
			else
				floodButton.textContent = "Floodgate: Close";
		});

		const queueButton = document.getElementById("queue-button");
		queueButton.after(floodButton);
	}
});

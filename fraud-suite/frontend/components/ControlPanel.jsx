export default function ControlPanel() {
	const startSniffing = () => {
		axios.post("/start_sniffing").then(() => alert("Sniffing started."));
	};

	const startReplay = () => {
		axios.post("/start_replay").then(() => alert("Replay started."));
	};

	return (
		<div>
			<h2>Control Panel</h2>
			<button onClick={startSniffing}>Start Sniffing</button>
			<button onClick={startReplay}>Start Replay</button>
		</div>
	);
}

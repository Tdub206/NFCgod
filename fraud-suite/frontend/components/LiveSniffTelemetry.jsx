import React, { useEffect, useState } from "react";
import axios from "axios";

export default function LiveSniffTelemetry() {
	const [sniffedData, setSniffedData] = useState([]);

	useEffect(() => {
		const interval = setInterval(() => {
			axios.get("/live_sniffed_data").then((response) => {
				setSniffedData(response.data);
			});
		}, 1000); // Poll every second
		return () => clearInterval(interval);
	}, []);

	return (
		<div>
			<h2>Live Sniffed Data</h2>
			<ul>
				{sniffedData.map((entry, index) => (
					<li key={index}>
						<b>UID:</b> {entry.uid}, <b>AID:</b> {entry.aid}, <b>APDU:</b> {entry.apdu_request}, <b>Response:</b> {entry.apdu_response}
					</li>
				))}
			</ul>
		</div>
	);
}

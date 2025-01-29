import React from "react";
import FraudDashboard from "./components/FraudDashboard";
import ControlPanel from "./components/ControlPanel";

function App() {
	return (
		<div>
			<h1>Fraud Suite Dashboard</h1>
			<FraudDashboard />
			<ControlPanel />
		</div>
	);
}

export default App;

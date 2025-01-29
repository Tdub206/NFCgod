import React, { useState, useEffect } from "react";
import axios from "axios";

export default function FraudDashboard() {
	const [totalStolen, setTotalStolen] = useState(0);
	const [transactions, setTransactions] = useState([]);

	useEffect(() => {
		const interval = setInterval(() => {
			axios.get("/fraud_summary").then((response) => {
				setTotalStolen(response.data.totalStolen);
				setTransactions(response.data.transactions);
			});
		}, 1000);
		return () => clearInterval(interval);
	}, []);

	return (
		<div>
			<h1>Fraud Dashboard</h1>
			<h2>Total Stolen: ${totalStolen.toFixed(2)}</h2>
			<h2>Recent Transactions</h2>
			<ul>
				{transactions.map((tx, index) => (
					<li key={index}>
						<b>Card UID:</b> {tx.uid}, <b>Amount:</b> ${tx.amount / 100}
					</li>
				))}
			</ul>
		</div>
	);
}

import React, { useState } from "react";
import axios from "axios";

export default function TransactionConfig() {
	const [amount, setAmount] = useState("10.00");
	const [currency, setCurrency] = useState("840");
	const [merchant, setMerchant] = useState("FAKE1234");

	const updateParams = () => {
		axios.post("/update_params", {
			amount,
			currency_code: currency,
			merchant_id: merchant,
		}).then(() => {
			alert("Transaction parameters updated.");
		});
	};

	return (
		<div>
			<h2>Transaction Configuration</h2>
			<label>Amount: </label>
			<input value={amount} onChange={(e) => setAmount(e.target.value)} />
			<br />
			<label>Currency Code: </label>
			<input value={currency} onChange={(e) => setCurrency(e.target.value)} />
			<br />
			<label>Merchant ID: </label>
			<input value={merchant} onChange={(e) => setMerchant(e.target.value)} />
			<br />
			<button onClick={updateParams}>Update Parameters</button>
		</div>
	);
}

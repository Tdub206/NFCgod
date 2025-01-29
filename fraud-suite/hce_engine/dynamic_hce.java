@Override
public byte[] processCommandApdu(byte[] apdu, Bundle extras) {
	Log.d("HCE", "Received APDU: " + bytesToHex(apdu));

	// Match incoming APDU commands to responses
	if (Arrays.equals(apdu, SELECT_AID)) {
		Log.d("HCE", "Sending AID response.");
		return SELECT_RESPONSE;
	} else if (apdu[0] == (byte) 0x80 && apdu[1] == (byte) 0xA8) {
		Log.d("HCE", "Generating dynamic ARQC.");
		return generateDynamicARQC(apdu);
	}

	// Default response
	return new byte[]{(byte) 0x6A, (byte) 0x81};  // Unsupported command
}

private byte[] generateDynamicARQC(byte[] apdu) {
	byte[] transactionData = extractTransactionData(apdu);
	byte[] arqc = CryptoUtils.generateARQC(transactionData, sessionKey);
	Log.d("HCE", "Generated ARQC: " + bytesToHex(arqc));
	return arqc;
}

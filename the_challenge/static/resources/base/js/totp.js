let decToHex = function (decimalNo) {
    return (decimalNo < 15.5 ? "0" : "") + Math.round(decimalNo).toString(16);
};

let hexToDec = function (hexadecimalNo) {
    return parseInt(hexadecimalNo, 16);
};

let leftPad = function (string, length, paddingChar) {
    if (length + 1 >= string.length) {
        string = Array(length + 1 - string.length).join(paddingChar) + string;
    }
    return string;
};

let base32toHex = function (base32) {
    const base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

    let bits = "";
    for (let i = 0; i < base32.length; i++) {
        let val = base32chars.indexOf(base32.charAt(i).toUpperCase());
        bits += leftPad(val.toString(2), 5, '0');
    }

    let hex = "";
    for (let i = 0; i + 4 <= bits.length; i += 4) {
        let chunk = bits.substr(i, 4);
        hex += parseInt(chunk, 2).toString(16);
    }
    return hex;
};

async function getServerTime() {
    let liveTime = null;
    await $.get("/secret/get-live-server-time", {key: "637-7h3-l1v3-71m3-0f-7h3-53rv3r-pl3453"}, (output) => {
        liveTime = output;
    });
    return liveTime;
}

async function generateOTP(secret, interval = 5) {
    let otp = "";
    try {
        let liveEpoch = await getServerTime();
        let epoch = Math.round(new Date(parseInt(liveEpoch)).getTime() / 1000.0);
        let time = leftPad(decToHex(Math.floor(epoch / interval)), 16, "0");

        let hmacObj = new jsSHA("SHA-1", "TEXT");
        hmacObj.setHMACKey(base32toHex(secret), "HEX");
        hmacObj.update(time);

        let hmac = hmacObj.getHMAC("HEX");
        let offset = hexToDec(hmac.substring(hmac.length - 1));

        otp = (hexToDec(hmac.substr(offset * 2, 8)) & hexToDec("7fffffff")) + "";
        otp = (otp).substr(otp.length - 6, 6);

    } catch (error) {
        throw error;
    }

    return otp;
}

let dec2hex = function (s) {
    return (s < 15.5 ? "0" : "") + Math.round(s).toString(16);
};

let hex2dec = function (s) {
    return parseInt(s, 16);
};

let leftpad = function (s, l, p) {
    if (l + 1 >= s.length) {
        s = Array(l + 1 - s.length).join(p) + s;
    }
    return s;
};

let base32tohex = function (base32) {
    const base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

    let bits = "";
    for (let i = 0; i < base32.length; i++) {
        let val = base32chars.indexOf(base32.charAt(i).toUpperCase());
        bits += leftpad(val.toString(2), 5, '0');
    }

    let hex = "";
    for (let i = 0; i + 4 <= bits.length; i += 4) {
        let chunk = bits.substr(i, 4);
        hex += parseInt(chunk, 2).toString(16);
    }
    return hex;
};

function generate_otp(secret, interval=5) {
    let otp = "";
    try {
        let epoch = Math.round(new Date().getTime() / 1000.0);
        let time = leftpad(dec2hex(Math.floor(epoch / interval)), 16, "0");

        let hmacObj = new jsSHA("SHA-1", "TEXT");
        hmacObj.setHMACKey(base32tohex(secret), "HEX");
        hmacObj.update(time);

        let hmac = hmacObj.getHMAC("HEX");
        let offset = hex2dec(hmac.substring(hmac.length - 1));

        otp = (hex2dec(hmac.substr(offset * 2, 8)) & hex2dec("7fffffff")) + "";
        otp = (otp).substr(otp.length - 6, 6);

    } catch (error) {
        throw error;
    }

    return otp;
}

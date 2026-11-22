import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.List;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

// Verifies an Agilis webhook signature. Usage: AGILIS_WEBHOOK_SECRET=whsec_... AGILIS_SIGNATURE='t=...,v1=...' java Verify.java body.json
public class Verify {
    // rawBody: the request body exactly as received, read as a UTF-8 string before any JSON parsing.
    // Returns the verified body; parse it with your JSON library.
    static String verifyAgilisWebhook(String rawBody, String header, String secret) throws Exception {
        return verifyAgilisWebhook(rawBody, header, secret, 300);
    }

    static String verifyAgilisWebhook(String rawBody, String header, String secret, long toleranceSeconds) throws Exception {
        String t = null;
        List<String> signatures = new ArrayList<>();
        for (String part : (header == null ? "" : header).split(",")) {
            String[] kv = part.trim().split("=", 2);
            if (kv.length != 2) continue;
            if (kv[0].equals("t")) t = kv[1];
            if (kv[0].equals("v1")) signatures.add(kv[1]);
        }
        if (t == null || !t.matches("\\d+") || signatures.isEmpty()) throw new SecurityException("Invalid signature header");
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
        byte[] expected = HexFormat.of().formatHex(mac.doFinal((t + "." + rawBody).getBytes(StandardCharsets.UTF_8)))
            .getBytes(StandardCharsets.UTF_8);
        boolean ok = false;
        for (String s : signatures) ok |= MessageDigest.isEqual(expected, s.getBytes(StandardCharsets.UTF_8));
        if (!ok) throw new SecurityException("Signature does not match");
        if (Math.abs(System.currentTimeMillis() / 1000 - Long.parseLong(t)) > toleranceSeconds)
            throw new SecurityException("Timestamp outside the tolerance");
        return rawBody;
    }

    public static void main(String[] args) throws Exception {
        String body = new String(java.nio.file.Files.readAllBytes(java.nio.file.Path.of(args[0])), StandardCharsets.UTF_8);
        try {
            verifyAgilisWebhook(body, System.getenv("AGILIS_SIGNATURE"), System.getenv("AGILIS_WEBHOOK_SECRET"));
            System.out.println("verified");
        } catch (SecurityException e) {
            System.err.println("rejected: " + e.getMessage());
            System.exit(1);
        }
    }
}

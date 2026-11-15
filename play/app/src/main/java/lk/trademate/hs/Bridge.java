package lk.trademate.hs;

import android.net.Uri;
import android.webkit.JavascriptInterface;

/** window.Android in the app content — same two functions as the sideloaded APK. */
public class Bridge {
    private final MainActivity act;

    Bridge(MainActivity act) { this.act = act; }

    /** Close the app (Back pressed on the home screen). */
    @JavascriptInterface
    public void exit() {
        act.runOnUiThread(act::finish);
    }

    /** Open a web link, email or phone number outside the app. */
    @JavascriptInterface
    public void open(String url) {
        try {
            Uri u = Uri.parse(url);
            String scheme = u.getScheme() == null ? "" : u.getScheme().toLowerCase();
            if (scheme.equals("http") || scheme.equals("https") || scheme.equals("mailto") || scheme.equals("tel")) {
                act.runOnUiThread(() -> act.openOutside(u));
            }
        } catch (Exception ignored) { }
    }
}

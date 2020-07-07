rpc.exports = {
    copyfromclipboard: function() {
        Java.perform(function () {
            var ActivityThread = Java.use("android.app.ActivityThread");
            var ClipboardManager = Java.use("android.content.ClipboardManager");

            var context = ActivityThread.currentApplication().getApplicationContext();

            try {
                var clipboardManager = Java.cast(context.getSystemService("clipboard"), ClipboardManager);
            } catch (exception) {
                send("Please open target app first.");
                return;
            }

            var clipData = clipboardManager.getPrimaryClip();
            var itemCount = clipData.getItemCount();
            if(itemCount < 1) {
                send("Pasteboard is empty.");
                return;
            }
            for(var i = 0; i < itemCount; i++) {
                var item = clipData.getItemAt(i);
                send("Pasteboard item " + i + ": " + item.getText());
            }
        });
    },
    pastetoclipboard: function (data) {
        Java.perform(function () {
            var ActivityThread = Java.use("android.app.ActivityThread");
            var ClipboardManager = Java.use("android.content.ClipboardManager");
            var ClipData = Java.use("android.content.ClipData");
            var String = Java.use("java.lang.String");

            var context = ActivityThread.currentApplication().getApplicationContext();

            try {
                var clipboardManager = Java.cast(context.getSystemService("clipboard"), ClipboardManager);
            } catch (exception) {
                send("Please open target app first.");
                return;
            }

            var str = String.$new(data);
            var clipData = ClipData.newPlainText(str, str);
            send("Pasting '" + data + "' to clipboard...");
            clipboardManager.setPrimaryClip(clipData);
        });
    }
};
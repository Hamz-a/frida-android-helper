rpc.exports = {
    disablesecureflag: function(activity_name) {
        Java.perform(function() {
            // https://developer.android.com/reference/android/view/WindowManager.LayoutParams.html#FLAG_SECURE
            var FLAG_SECURE = 0x2000;

            var Runnable = Java.use("java.lang.Runnable");
            var DisableSecureRunnable = Java.registerClass({
                name: "me.bhamza.DisableSecureRunnable",
                implements: [Runnable],
                fields: {
                    activity: "android.app.Activity",
                },
                methods: {
                    $init: [{
                        returnType: "void",
                        argumentTypes: ["android.app.Activity"],
                        implementation: function (activity) {
                            this.activity.value = activity;
                        }
                    }],
                    run: function() {
                        this.activity.value.getWindow().setFlags(0, FLAG_SECURE); // disable it!
                        send("Done disabling SECURE flag...")
                    }
                }
            });

            Java.choose(activity_name, {
                "onMatch": function (instance) {
                    var runnable = DisableSecureRunnable.$new(instance);
                    instance.runOnUiThread(runnable);
                },
                "onComplete": function () {}
            });
        });
    }
};

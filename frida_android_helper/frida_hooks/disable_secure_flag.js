Java.perform(function() {
    // https://developer.android.com/reference/android/view/WindowManager.LayoutParams.html#FLAG_SECURE
    var FLAG_SECURE = 0x2000;

    var activity_name;

    // recv(function (data) { // Wait and receive values from Python agent
    //     pkg_name = data.pkg_name;
    //     activity_name = data.activity_name;
    // }).wait();
    activity_name = "se.tink.android.MainActivity";
    Java.choose(activity_name, {
       "onMatch": function (instance) {
            instance.getWindow().setFlags(0, FLAG_SECURE); // disable it!
            send("Done disabling SECURE flag...")
       },
        "onComplete": function () {}
    });
});
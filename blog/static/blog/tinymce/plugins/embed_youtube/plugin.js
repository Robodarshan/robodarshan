tinymce.PluginManager.add('embed_youtube', function(editor, url) {
    function showDialog() {
        editor.windowManager.open({
            title: "Embed Youtube video",
            file: url + "/youtube.html",
            width: 500,
            height: 500,
            inline: 1,
            resizable: false,
            maximizable: false
        });
    }

    // Add a button that opens a window
    editor.addButton("embed_youtube", {
        icon: 'media',
        tooltip: "Add a video",
        onclick: showDialog()
    });
});

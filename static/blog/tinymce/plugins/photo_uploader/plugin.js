var progressUpdate = function(e, position, total, percentComplete) {
        console.log(e, position, total, percentComplete);
};

var success = function(response) {
        var editor = tinymce.activeEditor;
        var success_event = {message: 'no errors'};
        for(var photo in response) {            
            editor.selection.setContent("<img title=\"" + photo + "\" src=\"/"+ response[photo] +"\" />");            
        }
        setTimeout(function(){
            editor.execCommand('mceAutoResize');
            console.log('resized');
            }, 50);
};

var ajaxFormOptions = {
        dataType: 'json',
        uploadProgress: progressUpdate,
        success: success
};

var upload_photo = function() {
	$("#photo_uploader").ajaxSubmit(ajaxFormOptions);
}

$('#photos').change(upload_photo);

tinymce.PluginManager.add('photo_uploader', function(editor, url) {
    // Add a button that opens a window
    editor.addButton('photo_uploader', {
        title: 'Insert photo',
        icon: 'image',
        onclick: function() {
            // Open window
            $('#photos').click();
        }
    });
});

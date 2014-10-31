var enable_submit = function() {
        if($("#id_title").prop('value') != "" && tinymce.activeEditor.getContent() != "") {
                $("#submit_button").removeAttr('disabled');
                console.log('enabled');
        }
        else {
                $("#submit_button").attr('disabled', 'disabled');
                console.log('disabled');
        }
}

$(document).ready(function(){
        $("#photo_uploader").hide();
        $("#submit_button").attr('disabled', 'disabled');
        $("#photo_uploader").ajaxForm();
        $("#id_body").tinymce({
                script_url : '/static/blog/tinymce/tinymce.min.js',
                execcommand_callback: 'myCustomExecCommandHandler',
                plugins : 'autoresize, link, embed_youtube, photo_uploader',
                autoresize_min_height: '200',
                skin: 'custom',
                menubar : false,
                statusbar: false,
                file_picker_types: 'image',
                setup : function(ed){
                                ed.addButton('heading',
                                        {
                                                tooltip: 'Add a Heading',
                                                onPostRender: function() {
                                                        var self = this;
                                                        if (ed.formatter) {
                                                                ed.formatter.formatChanged('h2', function(state) {
                                                                        self.active(state);
                                                                });
                                                        } 
                                                        else {
                                                                ed.on('init', function() {
                                                                        ed.formatter.formatChanged('h2', function(state) {
                                                                                self.active(state);
                                                                        });
                                                                });
                                                        }
                                                },
                                                onclick: function() {
                                                        ed.execCommand('mceToggleFormat', false, 'h2');
                                                }
                                        }
                                );    
                                ed.on('keyup', enable_submit);
                        },
                toolbar: "heading bold italic strikethrough link unlink bullist numlist outdent indent blockquote subscript superscript photo_uploader embed_youtube",
        });
        
        $("#id_title").keyup(enable_submit);
});

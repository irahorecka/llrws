Dropzone.autoDiscover = false;
$(".dropzone").dropzone({
    addRemoveLinks: true,
    maxFiles: 2,
    removedfile: function(file) {
        var name = file.name;
        $.ajax({
            type: 'POST',
            url: '/upload',
        });
        var _ref;
        return (_ref = file.previewElement) != null ? _ref
            .parentNode.removeChild(file.previewElement) : void 0;
    },
    init: function() {
        // Get intance of Dropzone object
        function invoke_blue_border() {
            invoke_border_color('rgb(0, 135, 247)');
        }
        function invoke_red_border() {
            invoke_border_color('rgb(220, 53, 69)');
        }
        function invoke_border_color(color) {
            setTimeout(function(){
                $('.dropzone').css('border', '2px dashed ' + color);
            }, 200);
        }

        this.on("error", function(file, response) {
            invoke_red_border();
        });
        this.on("removedfile", function(file, response) {
            $(".dz-error-message span").each(function(){
                // Check if no error messages are present
                if (!$(this).text().trim().length) {
                    invoke_blue_border();
                } else {
                    invoke_red_border();
                }
            });
            var maveCSVDropzone = Dropzone.forElement(".dropzone");
            // No more files in Dropzone instance
            if (maveCSVDropzone.files.length == 0) {
                invoke_blue_border();
            }
        });
    }
});

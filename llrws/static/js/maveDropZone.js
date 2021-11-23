$(document).ready(function() {
    Dropzone.autoDiscover = false;
    $(".dropzone").dropzone({
        addRemoveLinks: true,
        maxFiles: 1,
        removedfile: function(file) {
            var name = file.name;
            $.ajax({
                type: 'POST',
                url: '/upload',
            });
            var _ref;
            return (_ref = file.previewElement) != null ? _ref
                .parentNode.removeChild(file.previewElement) : void 0;
        }
    });
});

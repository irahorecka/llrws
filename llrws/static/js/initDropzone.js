Dropzone.autoDiscover = false;

var dropzone = new Dropzone('#mave-csv-upload', {
    autoProcessQueue: false,
    previewTemplate: document.querySelector('#preview-template')
        .innerHTML,
    parallelUploads: 2,
    thumbnailHeight: 120,
    thumbnailWidth: 120,
    thumbnail: function(file, dataUrl) {
        if (file.previewElement) {
            file.previewElement.classList.remove("dz-file-preview");
            var images = file.previewElement.querySelectorAll(
                "[data-dz-thumbnail]");
            for (var i = 0; i < images.length; i++) {
                var thumbnailElement = images[i];
                thumbnailElement.alt = file.name;
                thumbnailElement.src = dataUrl;
            }
            setTimeout(function() {
                file.previewElement.classList.add(
                    "dz-image-preview");
            }, 1);
        }
    }

});

$('#mave-csv-upload').click(function(){
    dropzone.processQueue();
});

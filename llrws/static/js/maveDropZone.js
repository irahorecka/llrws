Dropzone.autoDiscover = false;
$("#mave-upload-csv").dropzone({
    addRemoveLinks: true,
    // We only need one benchmark and one score CSV file.
    maxFiles: 2,
    removedfile: function(file) {
        $.ajax({
            type: "POST",
            url: "/upload",
        });
        var _ref;
        return (_ref = file.previewElement) != null ? _ref
            .parentNode.removeChild(file.previewElement) : void 0;
    },
    init: function() {
        // Get intance of Dropzone object.
        var maveCSVDropzone = Dropzone.forElement("#mave-upload-csv");

        this.on("error", function(file, response) {
            invokeJobSuspension();
        });

        this.on("maxfilesexceeded", function(file, response) {
            this.removeFile(file);
        });

        this.on("removedfile", function(file, response) {
            if (anyErrorFilesPresent()) {
                invokeJobSuspension();
                return;
            }
            invokeJobOpen();
        });

        this.on("success", function(file, response) {
            // On successful upload, the number of uploads should equal the max size
            // and there should be no error files present.
            if (maveCSVDropzone.files.length == maveCSVDropzone.options.maxFiles) {
                if (anyErrorFilesPresent() || isDuplicateFile(maveCSVDropzone)) {
                    invokeJobSuspension();
                    return;
                }
                invokeJobReady();
                return;
            }
            // At this point, a 200 response was received from the server - therefore we
            // assume we have ONE valid file in the Dropzone instance.
            invokeJobOpen();
        });
    }
});

function invokeJobReady() {
    /**
     * Sets border color of #mave-upload-csv element to green and enables
     * submit button.
     */
    invokeBorderColor("rgb(52, 168, 83)");
    $('#mave-button-submit').prop('disabled', false);
}

function invokeJobSuspension() {
    /**
     * Sets border color of #mave-upload-csv element to red and disables
     * submit button.
     */
    invokeBorderColor("rgb(220, 53, 69)");
    $('#mave-button-submit').prop('disabled', true);
}

function invokeJobOpen() {
    /**
     * Sets border color of #mave-upload-csv element to blue and disables
     * submit button.
     */
    invokeBorderColor("rgb(0, 135, 247)");
    $('#mave-button-submit').prop('disabled', true);
}

function invokeBorderColor(color) {
    /**
     * Sets border color of #mave-upload-csv element
     * @param  {[string]} color Color to set border color.
     */
    setTimeout(function(){
        $("#mave-upload-csv").css("border", "2px dashed " + color);
    }, 200);
}

function anyErrorFilesPresent() {
    /**
     * Checks if any Dropzone-flagged error files are present on the DOM.
     * @return {[bool]} Indicates whether there are or are not error files.
     */
    var errorMessages = new Set();
    $(".dz-error-message span").each(function(){
        errorMessages.add($(this).text().trim().length);
    });
    if (errorMessages.size > 1 && errorMessages.values().next() != 0) {
        // 0 represents a valid file.
        return true;
    }
    return false;
}

function isDuplicateFile(DropzoneObj) {
    /**
     * Checks if duplicate files are present in a Dropzone object.
     * @param  {[object]} DropzoneObj An instance of the Dropzone object.
     * @return {[bool]} Indicates whether there are or are not duplicate files.
     */
    var fileNames = DropzoneObj.getAcceptedFiles().map(x => x.name);
    var uniqueFileNames = new Set(fileNames)
    if (uniqueFileNames.size != fileNames.length) {
        return true;
    }
    return false;
}

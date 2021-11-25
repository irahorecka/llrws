Dropzone.autoDiscover = false;
$("#mave-upload-csv").dropzone({
    addRemoveLinks: true,
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
        // Get intance of Dropzone object
        var maveCSVDropzone = Dropzone.forElement("#mave-upload-csv");
        var loadedFileTypes = new Object();
        this.on("error", function(file, response) {
            invokeJobSuspension();
        });

        this.on("maxfilesexceeded", function(file, response) {
            this.removeFile(file);
        });

        this.on("removedfile", function(file, response) {
            // Cleans up dictionary storing filetypes by removing disposed files.
            if (maveCSVDropzone.files.length == 1 && Object.keys(loadedFileTypes).length > 1) {
                delete loadedFileTypes[file.name];
            }
            if (anyErrorFilesPresent()) {
                invokeJobSuspension();
                return;
            }
            if (areBothBenchmarkAndScoreFilesLoaded(maveCSVDropzone, loadedFileTypes)) {
                invokeJobReady();
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
                } else {
                    invokeJobReady();
                }
                return;
            }
            // Check both correct filetypes are loaded
            loadedFileTypes[file.name] = response;
            if (areBothBenchmarkAndScoreFilesLoaded(maveCSVDropzone, loadedFileTypes)) {
                invokeJobReady();
            } else {
                invokeJobOpen();
            }
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
        // 0 represents a valid file
        return true;
    }
    return false;
}

function areBothBenchmarkAndScoreFilesLoaded(DropzoneObj, loadedFileTypes) {
    /**
     * Checks if both benchmark and score CSV files are loaded in the Dropzone portal.
     * @param  {[object]} DropzoneObj An instance of the Dropzone object.
     * @param  {[object]} loadedFileTypes A dictionary mapping filename to filetype (i.e. 'benchmark' or 'score').
     * @return {[bool]} Indicates whether both benchmark and score files are or are not present.
     */
    var filesInDropzone = DropzoneObj.getAcceptedFiles()
    var filenamesInDropzone = filesInDropzone.map(x => loadedFileTypes[x.name])
    if (filesInDropzone.length == 2) {
        if ("benchmark" in filenamesInDropzone && "score" in filenamesInDropzone) {
            return true;
        }
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

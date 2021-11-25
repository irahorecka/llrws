$(document).ready(function() {
	// Initialzie with empty data table.
	var table = $("#data").DataTable({
		// Disable initial sorting
		aaSorting: [],
		columns: [
			{data: "hgvs_pro", sortable: false},
			{data: "score", searchable: false},
			{data: "sd", searchable: false},
			{data: "se", searchable: false},
			{data: "llr",searchable: false},
			{data: "llrCIlower", searchable: false},
			{data: "llrCIupper", searchable: false},
		],
		language: {
			searchPlaceholder: "Search HGVS Pro",
		},
		lengthMenu: [
			[100, 250, 500, -1],
			[100, 250, 500, "All"],
		],
		pageLength: 100,
		scrollX: true,
		scrollY: "500px",
		scroller: true,
		scrollCollapse: true,
	});

	// Get table content on button click.
	$("#mave-button-submit").click(function() {
		maveCSVDropzone = Dropzone.forElement("#mave-upload-csv");
		// SYNCHRONOUSLY resubmit loaded documents in Dropzone instance to override persisted
		// temp files stored on server. The temp files are caused by the user uploading and
		// removing files from the Dropzone instance.
		for (let i = 0; i < maveCSVDropzone.options.maxFiles; i++) {
			var formData = new FormData();
			formData.append('file', maveCSVDropzone.files[i]);
			$.ajax({
				async: false,
				url : '/upload',
				type : 'POST',
				data : formData,
				processData: false,  // tell jQuery not to process the data
				contentType: false,  // tell jQuery not to set contentType
				success : function(data) {
					setLoadingButtonState();
				}
			});
		}
		// Then call an AJAX GET request to /data. Await request from /data before populating DataTable.
		$.ajax({
			url: "/data",
			success: function(data) {
				table.rows.add(data.data).draw();
				// Remove loaded Dropzone files on successful load.
				maveCSVDropzone.removeAllFiles(true);
				setDefaultButtonState();
				scrollToBottomOfPage();
			},
			error: function(jqXHR, textStatus, errorThrown) {
				switch(jqXHR.status)
				{
					case 400:
						alert("Error [400]: " + jqXHR.responseText);
						invokeJobSuspension();
						break;
					case 500:
						alert("Error [500]: " + jqXHR.responseText);
						invokeJobSuspension();
				}
				setDefaultButtonState();
			},
		});
	});
});

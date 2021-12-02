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
		setLoadingButtonState();
		scoreCSVDropzone = Dropzone.forElement("#score-upload-csv");
		benchmarkCSVDropzone = Dropzone.forElement("#benchmark-upload-csv");
		$.ajax({
			url: "/data",
			success: function(data) {
				// Clear existing content.
				table.clear();
				// Fill table content.
				table.rows.add(data.data).draw();
				// Remove loaded Dropzone files on successful load.
				scoreCSVDropzone.removeAllFiles(true);
				benchmarkCSVDropzone.removeAllFiles(true);
				setDefaultButtonState();
				scrollToBottomOfPage();
			},
			error: function(jqXHR, textStatus, errorThrown) {
				switch(jqXHR.status) {
					case 400:
						alert("Error [400]: " + jqXHR.responseText);
						invokeJobSuspension("#score-upload-csv", "#score-accordion span.file-invalid");
						invokeJobSuspension("#benchmark-upload-csv", "#benchmark-accordion span.file-invalid");
						break;
					case 500:
						alert("Error [500]: " + jqXHR.responseText);
						invokeJobSuspension("#score-upload-csv", "#score-accordion span.file-invalid");
						invokeJobSuspension("#benchmark-upload-csv", "#benchmark-accordion span.file-invalid");
				}
				setDefaultButtonState();
			},
		});
	});
});

$(document).ready(function() {
	// Declare common variables used in DataTables
	var datatableLang = {
		searchPlaceholder: "Search HGVS Pro"
	}
	var datatableLengthMenu = [
		[50, 100, 250, -1],
		[50, 100, 250, "All"]
	]
	// Initialzie with empty data table.
	$("#data").DataTable({
		language: datatableLang,
		lengthMenu: datatableLengthMenu,
	});

	// Get table content on button click.
	$("#mave-button-submit").click(function() {
		var table = $("#data").DataTable({
			ajax: "/data",
			columns: [{
					data: "hgvs_pro"
				},
				{
					data: "score",
					searchable: false
				},
				{
					data: "sd",
					searchable: false
				},
				{
					data: "se",
					searchable: false
				},
				{
					data: "llr",
					searchable: false
				},
				{
					data: "llrCIlower",
					searchable: false
				},
				{
					data: "llrCIupper",
					searchable: false
				},
			],
			// Destroy previous DataTable instance
			destroy: true,
			initComplete: function(settings, json) {
				$("html, body").animate({
					scrollTop: document.body.scrollHeight
				}, "slow");
			},
			language: datatableLang,
			lengthMenu: datatableLengthMenu,
			pageLength: 50,
			scrollX: true,
			scrollY: "500px",
			scroller: true,
			scrollCollapse: true,
			sorting: false,
		});
		table.columns.adjust();
	});
});

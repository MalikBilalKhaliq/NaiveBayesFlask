$(document).ready(function () {
	$('#start_classification_btn').click(function (event) {
		event.preventDefault();
		$("#imgMain").attr('src', "#");
		// $('#image').get(0).files.length === 0
		// document.getElementById("image").value != ""
		var select = document.getElementById('select-Method');
		var option = select.options[select.selectedIndex].value;
		$('#successAlert_converter').hide();
		var outputDiv = document.getElementById("ClassificationResult");
		outputDiv.innerHTML = "<img src='./static/Images/Loading.gif'>";
		dataMain = {
			"Main": option
		}
		console.log(dataMain);
		event.preventDefault();
		$.ajax({
			type: 'POST',
			url: '/apply-model',
			data: JSON.stringify(dataMain),
			contentType: 'application/json;charset=UTF-8',
			success: function (data, status, xhr) {
				// success callback function
				// alert("Testing before if");
				if (data.error) {
					// alert("Testing if"); 
					$('#errorAlert_converter').text(data.error).show();
					$('#successAlert_converter').hide();
				} else {
					let str = ""
					const loadTd = function (preVal, realVal) {
						for (const ele in preVal) {
							str += "<tr><td>" + realVal[ele] + "</td><td>" + preVal[ele] + "</td></tr>";
						}
						return str;
					}
					$('#successAlert_converter').text("Prediction Done Successfully").show();
					obj = JSON.parse(data);
					$("#imgMain").attr('src', 'data:image/png;base64,' + obj.Output[0]["Base64Img"]);
					var OutputDiv = document.getElementById("ClassificationResult");
					OutputDiv.innerHTML = "<table class=\"table table-bordered table-striped\">\n" +
						"  <thead>\n" +
						"      <tr>\n" +
						"        <th colspan=\"2\"><center><h2>" + option + " Distribution Results</h2></center></th>\n" +
						"      </tr>\n" +
						"      <tr>\n" +
						"        <th colspan=\"2\"><center><h2>Model Accuracy:" + obj.Output[2]["ModelAccuracy"] + "</h2></center></th>\n" +
						"      </tr>\n" +
						"    </thead>\n" +
						"    <thead>\n" +
						"      <tr>\n" +
						"        <th>Real Values</th>\n" +
						"        <th>Predicted Values</th>\n" +
						"      </tr>\n" +
						"    </thead>\n" +
						"    <tbody>\n" +
						"        " + loadTd(obj.Output[1]["Predictions"]["PredictedValues"], obj.Output[1]["Predictions"]["RealValues"]) + "</td>  \n" +
						"    </tbody>\n" +
						"  </table>";

					// $('#downloadBtn').css("display","inline");
					// alert("/DownloadImage");
					delete obj;
					$('#errorAlert_converter').hide();
				}
			}
		});

	});
});
function getRoomValue(){
    var uiRoom = document.getElementsByName("uiRoom");
    for (var i in uiRoom) {
        if(uiRoom[i].checked) {
            return parseInt(i)+1;
        }
    }
}

function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    var area = document.getElementById("uiArea");
    var location = document.getElementById("uiLocations");
    var heating = document.getElementById("uiHeat");
    var general_condition = document.getElementById("uiGeneral_condition");
    var room = getRoomValue();
    var estPrice = document.getElementById("uiEstimatedPrice");

    var url = "http://127.0.0.1:5000/predict_price";

    $.post(url, {
        area_m2: parseFloat(area.value),
        neighborhood: location.value,
        heating: heating.value,
        general_condition: general_condition.value,
        rooms: room
    },function(data, status) {
        console.log(data.estimated_price);
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " EUR</h2>";
        console.log(status);
    });

}



function OnPageLoad() {
    console.log("Welcome to the Belgrade Renting Price Prediction App");
    
    var url_loc = "http://127.0.0.1:5000/get_location_names";

    var url_heat = "http://127.0.0.1:5000/get_heating";

    var url_general_condition = "http://127.0.0.1:5000/get_general_condition";

    $.get(url_loc, function(data, status) {
        console.log("got response for get_location_names request");
        if (data) {
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            for (var i in locations) {
                var opt = new Option(locations[i]);
                $('#uiLocations').append(opt);
            }
        }
    });

    $.get(url_heat, function(data, status) {
        console.log("got response for get_heating request");
        if (data) {
            var heat = data.heating;
            var uiHeat = document.getElementById("uiHeat");
            $('#uiHeat').empty();
            for (var i in heat) {
                var opt = new Option(heat[i]);
                $('#uiHeat').append(opt);
            }
        }
    });

    $.get(url_general_condition, function(data, status) {
        console.log("got response for get_general_condition request");
        if (data) {
            var general_condition = data.general_condition;
            var uiGeneral_condition = document.getElementById("uiGeneral_condition");
            $('#uiGeneral_condition').empty();
            for (var i in general_condition) {
                var opt = new Option(general_condition[i]);
                $('#uiGeneral_condition').append(opt);
            }
        }
    });
}

window.onload = OnPageLoad;
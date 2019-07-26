$(document).ready(function() {
    $('.popover-dismiss').popover({
        trigger: 'focus'
    })
    let carquery = new CarQuery();
    carquery.init(year, make_id, model, trim_id);
    let space = " ";
    let final_string = carquery.settings.year + space;
    $.getJSON(carquery.base_url+"?callback=?", {cmd: "getMakes", year: carquery.settings.year}, function(data) {

        let makes = data.Makes;
        for (let i = 0; i < makes.length; i++) {
            if (makes[i].make_id == carquery.settings.make) {
                final_string += makes[i].make_display + space + carquery.settings.model + space;
            }
        }
        $.getJSON(carquery.base_url+"?callback=?", {cmd: "getTrims", year: carquery.settings.year, make: carquery.settings.make, model: carquery.settings.model, full_results: false}, function(data) {
            let trims = data.Trims;
            for (let j = 0; j < trims.length; j++) {
                if (trims[j].model_id == carquery.settings.trim) {
                    final_string += trims[j].model_trim;
                    console.log(final_string);
                    $('#car_summary').html(final_string);
                }
            }
        })
    });
    
});
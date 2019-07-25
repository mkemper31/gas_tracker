$(document).ready(function() {
    let today = new Date();
    let yyyy = today.getFullYear();
    let carquery = new CarQuery();
    carquery.init();
    carquery.setFilters( {sold_in_us:true} );
    carquery.initYearMakeModelTrim('car-years', 'car-makes', 'car-models', 'car-model-trims');
    //$('#cq-show-data').click( function() { carquery.populateCarData('car-model-data'); } );
    carquery.year_select_min=1900;
    carquery.year_select_max=yyyy+1;
});
$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=manufacturer]', function() {
        var countrySelectElement = $(this);
        var regionSelectElement = $('#' + $(this).attr('id').replace('manufacturer', 'wec_typ'));
        var regionWidgetElement = regionSelectElement.parents('.autocomplete-light-widget');

        // When the manufacturer select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            wec_typWidgetElement.yourlabsWidget().autocomplete.data = {
                'manufacturer_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            wec_typWidgetElement.yourlabsWidget().autocomplete.data = {}
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        // console.log($(this), 'changed to', value);
        // console.log(regionWidgetElement, 'data is', regionWidgetElement.yourlabsWidget().autocomplete.data)
    })
});
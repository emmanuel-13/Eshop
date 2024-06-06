// admin_custom.js

(function($) {
    $(document).ready(function() {
        $('#id_category').change(function() {
            var categoryId = $(this).val();
            $.ajax({
                url: '/get_subcategories/',
                data: {
                    'category_id': categoryId
                },
                dataType: 'json',
                success: function(data) {
                    var subcategorySelect = $('#id_subcategory');
                    subcategorySelect.empty();
                    $.each(data, function(key, value) {
                        subcategorySelect.append($('<option></option>').attr('value', value.id).text(value.name));
                    });
                    // Trigger the change event on the subcategory select to update the brands
                    subcategorySelect.trigger('change');
                }
            });
        });

        $('#id_subcategory').change(function() {
            var subcategoryId = $(this).val();
            $.ajax({
                url: '/get_brands/',
                data: {
                    'subcategory_id': subcategoryId
                },
                dataType: 'json',
                success: function(data) {
                    var brandSelect = $('#id_brand');
                    brandSelect.empty();
                    $.each(data, function(key, value) {
                        brandSelect.append($('<option></option>').attr('value', value.id).text(value.name));
                    });
                }
            });
        });
    });
})(django.jQuery);
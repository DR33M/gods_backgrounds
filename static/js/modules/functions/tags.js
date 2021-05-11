(function ($, element_id = '#id_tags', url = '/api/tags/') {
    $(element_id).select2({
        tags: true,
        tokenSeparators: [','],
        minimumInputLength: 2,
        ajax: {
            url: url,
            delay: 250,
            dataType: 'json',
            data: function (params) {
                return {
                    name: params.term,
                    page: params.page || 1
                };
            },
            processResults: function (data) {
                $.each(data.results, function (index, value) {
                    value.id = value.name;
                    value.text = value.name;
                });
                return {
                    results: data.results,
                    pagination: {
                        more: data.next
                    }
                };
            },
        }
    });
})($);

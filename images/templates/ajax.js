var page = 1;
    var empty_page = false
    var block_request = false


    $(window).scoll(function() {
        var margin = $(document).height() - $(window).height() - 200;
        if (($.window).scrollTop() > margin && empty_page == false && block_request == false){
            block_request = true;
            page += 1;
            $.get('?page=' + page, function(data) {
                empty_page = true;
            })
        }
    })
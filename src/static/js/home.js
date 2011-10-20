(function ($) {

    var translate = function (event) {
        var button = $(event.currentTarget);
        var tweet = $(".text", button.parent("p"));
        button.hide();
        $.ajax({
            url: "/translate",
            type: "POST",
            dataType: "json",
            data: {
                text: tweet.html(),
                lang: $(".lang", button.parent("p")).text()
            },
            success: function (response) {
                tweet.html(response.translatedText);
            },
            error: function () {
                button.show();
            }
        });
    };

    $(".translate").click(translate);
    
})(jQuery);
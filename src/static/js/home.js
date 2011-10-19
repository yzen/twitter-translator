(function ($) {

    var translate = function (event) {
        var button = $(event.currentTarget);
        var tweet = $(".text", button.parent("p"));
        $.ajax({
            url: "/translate",
            type: "POST",
            dataType: "json",
            data: {
                text: tweet.text(),
                lang: $(".lang", button.parent("p")).text()
            },
            success: function (response) {
                tweet.text(response.translatedText);
            }
        });
    };

    $(".translate").click(translate);
    
})(jQuery);
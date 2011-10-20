(function ($) {

    var translate = function (event) {
        // Define the necessary selectors.
        var button = $(event.currentTarget),
            paragraph = button.parent("p"),
            tweet = $(".text", paragraph),
            lang = $(".lang", paragraph);

        // Hide Translate button after the user requested translation.
        button.hide();

        // Make an ajax request to the server to translate the tweet.
        $.ajax({
            url: "/translate?" + $.param({
                text: tweet.html(),
                lang: lang.text()
            }),
            type: "GET",
            dataType: "json",
            success: function (response) {
                // Replace tweet's original text with translation.
                tweet.html(response.translatedText);
            },
            // If there was an error during the ajax request show the 
            // translate button again.
            error: button.show
        });
    };

    $(document).ready(function () {
        // Bind the translate button click event once the page has been loaded.
        $(".translate").click(translate);
    });
    
})(jQuery);
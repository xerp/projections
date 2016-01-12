(function ($) {
    $.fn.textfill = function (tag, maxFontSize) {
        maxFontSize = parseInt(maxFontSize, 10);
        return this.each(function () {
            var ourText = $(tag, this),
                parent = ourText.parent(),
                maxHeight = parent.height(),
                maxWidth = parent.width(),
                fontSize = parseInt(ourText.css("fontSize"), 10),
                multiplier = maxWidth / ourText.width(),
                newSize = (fontSize * (multiplier - 0.1));
            ourText.css(
                "fontSize",
                (maxFontSize > 0 && newSize > maxFontSize) ?
                    maxFontSize :
                    newSize
            );
        });
    };
})(jQuery);
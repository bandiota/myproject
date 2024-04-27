window.onload = function () {
    var button = document.getElementById("myButton");
    {% if no != 0 %}
    button.click();
    {% endif %}
};




const taiwan = document.getElementById('taiwan');
const colors = ["", "#FFEEB5", "#F2CA74", "#DBA14B", "#E88223", "#A83E00"];

taiwan.addEventListener("load", function() {
    const content = taiwan.contentDocument;

    var paths = content.querySelectorAll("path");
    for (var i = 0, length = paths.length; i < length; i++) {
        paths[i].style.stroke = "#77909E";
        paths[i].style.transition = "fill 0.8s";
    }

    var attributes = content.querySelectorAll("a");
    for (var i = 0, length = attributes.length; i < length; i++) {
        attributes[i].addEventListener("mouseenter", function() {
            var area = (this.id).replaceAll('-', ' ');
            var patients = records[area];

            var info = '<h2>' + area + '</h2><h3 class="special">' + patients + '</h3>';
            document.getElementById("info").innerHTML = info;

            for (var key of Object.keys(ranges)) {
                if (ranges[key]['from'] <= patients && patients <= ranges[key]['to']) {
                    // content.getElementById(this.id).classList.add("level" + key);
                    this.style.fill = colors[key];
                    break;
                }
                if (key == 5 && ranges[key]["to"] < patients) {
                    // content.getElementById(this.id).classList.add("level" + key);
                    this.style.fill = colors[key];
                    break;
                }
            }
        });

        attributes[i].addEventListener("mouseout", function() {
            this.style.fill = "";
        });
    }
});
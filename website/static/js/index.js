$('a').mouseenter(function() {
    var area = (this.id).replaceAll('-', ' ')
    var patients = records[area]
    var info = '<h2>' + area + '</h2><h3 class="special">' + patients + '</h3>'
    document.getElementById("info").innerHTML = info;

    for (var key of Object.keys(ranges)) {
        if (ranges[key]['from'] <= patients && patients <= ranges[key]['to']) {
            document.getElementById(this.id).classList.add("level" + key);
            break;
        }
        if (key == 5 && ranges[key]["to"] < patients) {
            document.getElementById(this.id).classList.add("level" + key);
            break;
        }
    }
});

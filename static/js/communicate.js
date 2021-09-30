$("document").ready(function(){
    $("#submit").click(function(){
        var level = $("#level").val();
        var leap = $("#leap").val();
        var h = $("#h").val();
        var arrow_size = $("#arrow_size").val();
        $.ajax({
            url: "http://localhost:5000/api/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"level": level, "leap": leap, "h": h, "arrow_size": arrow_size}),
            dataType: "json"
        }).done(function(data) {
            print(data)
        });
    });
});

/**
 * TODO
 */

$("#post-request").bind("click", function(){
    $.ajax({
        url: 'test/greeting?name=jay', //http://10.141.212.21:12300/demo
        datatype: 'json',
        type: 'get',
        success: function (data) {
            console.log("get_ss");
        },
        error: function () {
            alert("Get - wrong");
        }
    });

    $.ajax({
        url: 'test/greeting?name=jay', //http://10.141.212.21:12300/demo
        datatype: 'json',
        type: 'post',
        async: false,
        data: JSON.stringify({
            username: "name",
            password: "pass"
        }),
        success: function (data) {
        	console.log("post_ss");
        },
        error: function () {
            alert("Post - wrong");
        }
    });
});


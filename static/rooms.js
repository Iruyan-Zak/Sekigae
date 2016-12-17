/**
 * Created by yuri on 16/12/15.
 */

$(document).ready(function(){
    var switchCommandStr = {
        "change": function(){
            $('input[name="pos1"]:text').show();
            $("#s1").text("と");
            $("#s2").text("の席を入れ替える。");
        },
        "request": function(){
            $('input[name="pos1"]:text').show();
            $("#s1").text("が");
            $("#s2").text("に席の交換をお願いする。");
        },
        "decline": function(){
            $('input[name="pos1"]:text').hide();
            $("#s1").text("ID");
            $("#s2").text("のお願いを断る。");
        }
    };
    $('input[name="command"]:radio').change(
        function(){
            var val = $('input[name="command"]:checked').val();
            switchCommandStr[val]();
        }
    );
});

$(window).scroll(function() {
    if($(window).scrollTop()  > 10) {
        $(".navbar").css("box-shadow", "0 0 5px 0 #555");
    }
    else {    	
        $(".navbar").css("box-shadow", "none");
    }
});
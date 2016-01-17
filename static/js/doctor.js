jQuery(document).ready(function($){
// JavaScript Document
//slider
$('.carousel').carousel({
  interval: 4000
})
//fine slider
		<!--Codice Popover-->
		$(function(){
			$('[rel=popover]').popover({ 
				html : true, 
				content: function() {
      				return $('#popover_verifica').html();
    			}
			});
		});	
		<!--Fine Codice Popover-->
		
		<!--Codice Scroll blocco cassa-->
		$(function() {
    		var offset = $(".carrello-box").offset();
    		var topPadding = 50;
    		$(window).scroll(function() {
        		if ($(window).scrollTop() > offset.top) {
            		$(".carrello-box").stop().animate({
               	 		marginTop: $(window).scrollTop() - offset.top + topPadding
            		});
        		} else {
            		$(".carrello-box").stop().animate({
                		marginTop: 0
            		});
        		}
    		});
		});
		<!--Fine Codice Scroll blocco cassa-->

		<!--Codice Scroll blocco carrello-->
		$(function() {
    		var offset = $(".carrello-box").offset();
    		var topPadding = 50;
    		$(window).scroll(function() {
        		if ($(window).scrollTop() > offset.top) {
            		$(".carrello-box").stop().animate({
               	 		marginTop: $(window).scrollTop() - offset.top + topPadding
            		});
        		} else {
            		$(".carrello-box").stop().animate({
                		marginTop: 0
            		});
        		}
    		});
		});
		<!--Fine Codice Scroll blocco cassa-->

		<!--Codice ScrollToTop-->
		$(window).scroll(function(){
			if ($(this).scrollTop() > 100) {
				$('.scrollToTop').fadeIn();
			} else {
				$('.scrollToTop').fadeOut();
			}
		});
	
		//Click event to scroll to top
		$('.scrollToTop').click(function(){
			$('html, body').animate({scrollTop : 0},800);
			return false;
		});	
		<!--Fine Codice ScrollToTop-->
		<!--Codice Logo Top-->
		$(window).scroll(function(){
			if ($(this).scrollTop() > 100) {
				$('.logo-top').fadeIn();
			} else {
				$('.logo-top').fadeOut();
			}
		});
		<!--Codice Logo Top-->
		
		<!--animazione form-->
		
		//funzione campi per tipo cliente
		
		function change_select () {
					$('h5#intestazione-sezione-fatturazione').hide();
					$('div.a, div.b, div.c, div.d').hide();
					var valore = $('select#tipo_cliente').val();

					if (valore == "Associazione") {
						$('div.d').toggle(function () {
							$('div.d, h5#intestazione-sezione-fatturazione').show("fast",
							function (){
								$('div.a, div.b, div.c').hide("fast");
								})
						});
			
					} else if (valore == "Ditta") {
						$('div.c').toggle(function () {
							$('div.c, h5#intestazione-sezione-fatturazione').show("fast",
							function (){
								$('div.a, div.b, div.d').hide("fast");
								})
						});
			
					} else if (valore == "Privato") {
						$('div.b').toggle(function () {
							$('div.b, h5#intestazione-sezione-fatturazione').show("fast",
							function (){
								$('div.a, div.c, div.d').hide("fast");
								})
						});
			
					} else if (valore == "Societa") {
						$('div.a').toggle(function () {
							$('div.a, h5#intestazione-sezione-fatturazione').show("fast",
							function (){
								$('div.b, div.c, div.d').hide("fast");
								})
						});
			
					} else if (valore == "---") {
						$('div.a,div.b, div.c, div.d, h5#intestazione-sezione-fatturazione').hide("fast");
			
					};
		
		}
		
		$('h5#intestazione-sezione-fatturazione').hide();
		$('div.a, div.b, div.c, div.d').hide();
		var valore = $(this).val();

		if (valore == "Associazione") {
			$('div.d').toggle(function () {
				$('div.d, h5#intestazione-sezione-fatturazione').show("fast",
				function (){
					$('div.a, div.b, div.c').hide("fast");
				})
			});
			
		} else if (valore == "Ditta") {
			$('div.c').toggle(function () {$('div.c, h5#intestazione-sezione-fatturazione').show("fast",
				function (){
					$('div.a, div.b, div.d').hide("fast");
				})
		});
			
		} else if (valore == "Privato") {
			$('div.b').toggle(function () {$('div.b, h5#intestazione-sezione-fatturazione').show("fast",
				function (){
					$('div.a, div.c, div.d').hide("fast");
				})
		});
			
		} else if (valore == "Societa") {
			$('div.a').toggle(function () {$('div.a, h5#intestazione-sezione-fatturazione').show("fast",
				function (){
					$('div.b, div.c, div.d').hide("fast");
				});
		});
			
		} else if (valore == "---") {
			$('div.a,div.b, div.c, div.d, h5#intestazione-sezione-fatturazione').hide("fast");
		};
		
		$('select#tipo_cliente').change(function(){
			change_select ();
		});
		//fine funzione campi per tipo cliente
		
		//codice jquery tab
		$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    		var target = this.href.split('#');
    		$('.nav a').filter('a[href="#'+target[1]+'"]').tab('show');
		})
		
		//barre di avanzamento

});



/*function get_continente_paese() {
    new Ajax.Request('/registrazione/', {
        method: 'get',
        parameters: $H({'continente': $('continente').getValue()}),
        onSuccess: function (transport) {
            var e = $('paese')
            var t = $('tipo_cliente')
            var f =$('fatturazione')
            if (transport.responseText) {
                e.update(transport.responseText)
                onreset(t)
                f.update('')
            }

        }
    });
}// end new Ajax.Request

//function get_tipo_societa() {
function get_tipo(){
    new Ajax.Request('/registrazione/', {
        method: 'get',
        parameters: $H({'tipo_cliente':$('tipo_cliente').getValue(),'paese':$('paese').getValue()}),
        onSuccess: function (transport) {
            var t = $('fatturazione')
            if (transport.responseText){
                t.update(transport.responseText)
                }
        }
    });*/
    //new Ajax.Request('/registrazione/tipo_societa/', {
        //method: 'get',
        //parameters: $H({'p': $('paese').getValue()}),
        //onSuccess: function (transport) {
            //var t = $('tipo')
            //if (transport.responseText){
                //t.update(transport.responseText)
                //}
        //}
    //});
    //new Ajax.Request('/registrazione/provincie/', {
        //method: 'get',
        //parameters: $H({'p': $('paese').getValue()}),
        //onSuccess: function (transport) {
            //var p=$('provincia')
            //if (transport.responseText){
                //p.update(transport.responseText)}
        //}
    //});

//}// end new Ajax.Request
//function get_tipo() {

// end new Ajax.Request


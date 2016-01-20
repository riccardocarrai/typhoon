/**
 * Created by riccardocarrai on 11/06/15.
 */

$(document).ready(function() {
    var campi= $.merge($(".form-control"),$(".campo"))
    var componente=$("#componente").text();
    var accessorioClass=$(".Accessori")
    var campiSpecifiche=$("[specifica]")
    var btnCarrello=$.merge($("#carrello1"),$("#carrello2"))
    //var campiLavo=$("[lav]")
    var campiLavo=campi.not("[specifica]")
    var accessori_num
    var campiFigli=$("[padre]")
    var campiLav={}
    var campiMisure=[]
    var accessori={};
    var accessorio;
    var prezzoAcc;
    var varAcc;
    var campiPadre=$("[figli]");
   var csrftoken = getCookie('csrftoken');
   var formati=$("[sclass='formati']")
   var consegne=$(".consegne")
   var giorni=$(".giorno");
   var mesi=$(".mese");
   var campiAccessori=[]
   var datiAcc={}
   var prezzo;
   var formatoSel=$(formati[0]).val();
    var check=$(consegne[0]).attr('id');
    var defa=$("[default='true']")

    $(btnCarrello).attr('disabled','disabled')
    var x=0
    for(var i=0;i<campi.length;i++){
        if($(campi[i]).attr('oggetto')!=componente && $(campi[i]).attr('oggetto')!=undefined){
            if(x==0){
                accessori[x]=$(campi[i]).attr('oggetto')
                x++;
            }
            else{
                for(var z= 0;z<accessori.length;z++){
                if(accessori[z]!=$ (campi[i]).attr('oggetto')){
                     accessori[x]=$(campi[i]).attr('oggetto')
                    x++;
                }
            }
            }


        }
    }
    accessori_num=x
    $(defa).prop("checked",true)
    accessorio=$('#nessuno').val()

    $("#dataPreventivo").text($(giorni[0]).text()+"/"+$(mesi[0]).attr("name"));
    $(consegne[0]).attr('checked',true)

    $(formati).change(function(){
        formatoSel=$(this).val();
        if(formatoSel!="Formato Personalizzato") {
            for(var i=0;i< campiSpecifiche.length;i++){
                if($(this).attr($(campiSpecifiche[i]).attr('specifica'))){
                    var spec=$(campiSpecifiche[i]).attr('specifica')
                    campiMisure[i]=campiSpecifiche[i]
                    $(campiSpecifiche[i]).val($(this).attr(spec));
                }
            }

        }
        else{
             for(i in campiMisure){
                $(campiSpecifiche[i]).val('');
            }

        }

    });
  $(campiSpecifiche).change(function(){
      var spec=$(this).attr('specifica')
      for(var i=0; i<defa.length;i++){
          if(!($(defa[i]).attr('specifica'))&& $(defa[i]).attr(spec)){
             $(defa[i]).prop("checked",true)
          }

      }

   })

$(campiPadre).change(function(){
    if(!($(this).attr('padre'))) {
        var dati = {'padre': $(this).attr('id'), 'valore': $(this).val(),'figli':$(this).attr('figli'),'componente':$(this).attr('oggetto')}
        getAjax(dati,false, function (output) {
            $.each(output, function (index, element) {
                if($('#' + element.id).is('select')) {
                    $('#' + element.id).find('option').remove();
                    var valori = element.valori
                    for (var i = 0; i < valori.length; i++) {
                        $('#' + element.id).append('<option value="' + valori[i] + '">' + valori[i] + '</option>')
                    }
                }
                else{
                    $('#' + element.id).val(element.valori[0]);
                    if(element.non_editabile=='True'){
                        $('#' + element.id).attr('disabled', true);

                    }
                    else{
                        $('#' + element.id).attr('disabled', false);

                    }
                }

            });
        });
    }
})
   $(consegne).change(function(){
       check=$(this).attr('id');
       aggiornapreventivo(check,consegne);

    });

$(campi).change(function(){

        //if(!($(this).attr('padre'))){
            var dati={}
            var control=true;
            var aControl;
            var idx;
            var idc;
            var val;
            var quantita=0;
            var data={}
            for(var i=0;i<campiSpecifiche.length ; i++) {
                idc = $(campiSpecifiche[i]).attr('oggetto')
                if(data[idc]){
                    dati=data[idc]
                }
                else{
                  dati={}
                }

                if ($(campiSpecifiche[i]).attr('type') == 'radio') {
                    if ($(campiSpecifiche[i]).is(':checked')) {
                        idx = $(campiSpecifiche[i]).attr('id')
                        dati[idx]=$(campiSpecifiche[i]).val()

                    }
                    if ( idc == componente) {aControl = true;}
                }
                else {
                    if ($(campiSpecifiche[i]).val()) {
                        idx = $(campiSpecifiche[i]).attr('id')
                        dati[idx]=$(campiSpecifiche[i]).val()
                        if ( idc == componente) {aControl = true;}
                    }
                    else {
                        if ( idc == componente) {aControl = false;}
                    }
                }
                if($(campiSpecifiche[i]).attr('specifica')=='3'&& $(campiSpecifiche[i]).attr('oggetto')==componente){
                    quantita=$(campiSpecifiche[i]).val()
                }
                control = control && aControl;
                data[idc]=dati
            }
            //control=false//debug
            if(control){
                //data['componente']=componente
                for(var i=0;i<campiLavo.length;i++){
                    idc = $(campiLavo[i]).attr('oggetto')
                    if(data[idc]){
                        dati=data[idc]
                    }
                    else{
                    dati={}
                    }
                    //if($(campiLavo[i]).attr('oggetto')==componente) {
                        idx = $(campiLavo[i]).attr('id')
                        dati[idx] = $(campiLavo[i]).val()
                    //}
                    data[idc]=dati
                }
                data['componente']=componente
                data['accessori']=accessori
                data['accessori_nr']=accessori_num
                getAjax(data,true,function(output) {
                     prezzo=output['prezzo']
                     prezzo=parseFloat(prezzo)//+parseFloat(prezzoAcc);
                     aggiornaConsegne(consegne,prezzo,check,quantita);
                });
            }
            dati={}
    })

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getAjax(data,sync,handleData){
    $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
         $.ajax({
            url: "/preventivo/",
            type:"POST",
            data:data,
            dataType:'json',
            async:sync,
            success: function (data) {
                 handleData(data);
            }
        });

}



function aggiornaConsegne(consegne,prezzo,check,quantita){
    var prezziConsegna=[];
    var consegneP=$(".dat_cons");
    var l=consegne.length;
    for (var i = 0; i < l; i++) {
        var a = parseFloat($(consegne[i]).val());
        var sc = parseFloat($(consegne[i]).attr('sc'));
        var pr = parseFloat(prezzo);
        prezziConsegna[i] = ((pr + ((pr * a) / 100.00)) - ((pr * sc) / 100.00)).toFixed(2);
        if($(consegne[i]).attr('nr')){
            prezziConsegna[i]=(prezziConsegna[i]*parseInt($(consegne[i]).attr('nr'))).toFixed(2);
        }
        $(consegneP[i]).text(' € ' + prezziConsegna[i]);
        $(consegne[i]).attr('prezzo',prezziConsegna[i]);
        }

    if($(".quantita").attr('agg')=='true'){
            $(".quantita").text(quantita)
        }
    aggiornapreventivo(check,consegne);
}
function aggiornapreventivo(check,consegne){
    $("#dataPreventivo").text($(giorni[check]).text()+"/"+$(mesi[check]).attr("name"));
    $("#nettoPreventivo").text($(consegne[check]).attr('prezzo'));
    $("#prezzoFinale").text((($(consegne[check]).attr('prezzo')*22)/100).toFixed(2));
    $("#totalePreventivo").text((parseFloat($("#prezzoFinale").text())+parseFloat($("#nettoPreventivo").text())).toFixed(2));
}


});
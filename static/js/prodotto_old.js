/**
 * Created by riccardocarrai on 11/06/15.
 */

$(document).ready(function() {
    var campi= $.merge($(".form-control"),$(".campo"))
    var componente=$("#componente").text();
    var accessorioClass=$(".accessorio")
    var campiSpecifiche=$("[specifica]")
    //var campiLavo=$("[lav]")
    var campiLavo=campi.not("[specifica]")

    var campiFigli=$("[padre]")
    var campiLav={}
    var campiMisure=[]
    var accessori=[];
    var accessorio;
    var prezzoAcc;
    var varAcc;
    var campiPadre;
   var csrftoken = getCookie('csrftoken');
   var formati=$("[sclass='formati']")
   var consegne=$(".consegne")
   var giorni=$(".giorno");
   var mesi=$(".mese");
   var campiAccessori=[]
   var datiAcc={}
    var dati={}
   var prezzo;
   var formatoSel=$(formati[0]).val();
    var check=$(consegne[0]).attr('id');
    var defa=$("[default='true']")

    for(var i= 0, x=0;i<accessorioClass.length;i++){
        if(!accessori[$(accessorioClass[i]).attr('acc_id')]) {
            accessori[$(accessorioClass[i]).attr('acc_id')] = {'campiSpec': {}, 'campiLav': {}}
        }
    }
    for(var i=0;i<campiFigli.length;i++){
        var id=$(campiFigli[i]).attr('padre')
        var figlio=$(campiFigli[i]).attr('id')
        campiPadre=$("#"+id)
        $('#'+id).attr('figli',figlio)

    }

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
         //if($(defa).attr($(this).attr('specifica'))){
           //$(defa).prop("checked",true)

       //}
   })
   $(accessorioClass).change(function(){
           varAcc=$(this).val()
            if($(this).attr('id')=='nessuno') {
                for (i in accessori[$(this).attr('value')]['campiSpec']) {
                    $("#" + accessori[$(this).attr('value')]['campiSpec'][i]).prop('disabled', true).val('')
                    $('#nessuno').val('nessuno')
                        accessorio=$('#nessuno').val()
                    }
                }

            else{
                    for (i in accessori[$(this).attr('acc_id')]['campiSpec']) {
                        var idA='#'+accessori[$(this).attr('acc_id')]['campiSpec'][i]
                        //$('#1').prop('disabled', false)
                        $(idA).removeAttr('disabled')
                        $('#nessuno').val($(this).attr('acc_id'))
                        accessorio=$('#nessuno').val()
                    }

                }
        controlloCampi(componente,campiSecifiche,campiLav,formatoSel,function(output){
            prezzo=output['prezzo']
             if(accessorio && accessorio!='nessuno'){
                 controlloCampi(accessorio,varAcc,accessori[accessorio]['campiSpec'],accessori[accessorio]['campiLav'],'',function(output){
                    prezzoAcc=output['prezzo']
                     prezzo=parseFloat(prezzo)+parseFloat(prezzoAcc);
                     aggiornaConsegne(consegne,prezzo,check);
                 });
              }
            else{
                 aggiornaConsegne(consegne,prezzo,check);
             }

        });


   });

   $(consegne).change(function(){
       check=$(this).attr('id');
       aggiornapreventivo(check,consegne);

    });

$(campi).change(function(){

        //if(!($(this).attr('padre'))){
            var control=true;
            var aControl;
            var idx;
            var idc;
            var val;
            var vals={};
            for(var i=0;i<campiSpecifiche.length ; i++){
               if($(campiSpecifiche[i]).attr('type')=='radio'){
                   if($(campiSpecifiche[i]).is(':checked')){
                       idx = $(campiSpecifiche[i]).attr('specifica')
                       val=$(campiSpecifiche[i]).val()
                       //dati[idx] = $(campiSpecifiche[i]).val()
                   }
                    aControl=true;
               }
               else {
                   if ($(campiSpecifiche[i]).val()) {
                       idx = $(campiSpecifiche[i]).attr('specifica')
                       val=$(campiSpecifiche[i]).val()
                       //dati[idx] = $(campiSpecifiche[i]).val()
                       aControl = true;
                   }
                   else {
                       aControl = false;
                   }
               }
               if(dati[idx] && $(campiSpecifiche[i]).attr('type')!='radio'){
                       vals=dati[idx]
                       idc=idc+1;
                       vals[idc]=val
                       dati[idx]=vals
                       vals={}
                   }

               else{
                   idc=0
                   vals={}
                   vals[idc]=val
                   dati[idx] = vals
               }

               control=control&&aControl;
            }
            if(control){
                dati['componente']=componente
                for(var i=0;i<campiLavo.length;i++){
                    //if(!$(campiLavo[i]).attr('padre')){
                    idx=$(campiLavo[i]).attr('name')
                    dati[idx]=$(campiLavo[i]).val()


                }
                getAjax(dati,function(output) {
                     prezzo=output['prezzo']
                     prezzo=parseFloat(prezzo)//+parseFloat(prezzoAcc);
                     aggiornaConsegne(consegne,prezzo,check);
                });
            }
            dati={}

        //}
    })
$(campiPadre).change(function(){
    if(!($(this).attr('padre'))) {
        var dati = {'padre': $(this).attr('id'), 'valore': $(this).val(),'figli':$(this).attr('figli'),'componente':componente}
        getAjax(dati, function (output) {
            $.each(output, function (index, element) {
                $('#' + element.id).find('option').remove();
                var valori = element.valori
                for (var i = 0; i < valori.length; i++) {
                    $('#' + element.id).append('<option value="' + valori[i] + '">' + valori[i] + '</option>')
                }
            });
        });
    }
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

function getAjax(data,handleData){
    $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
         $.ajax({
            url: "/preventivo/",
            type:"POST",
            data:data,
            dataType:'json',
            success: function (data) {
                 handleData(data);
            }
        });

}

function controlloCampi(componente,specifiche,lavorazioni,formato,handleData){
    var control=true;
    var Acontrol;
    var valoriCampi=[];
    var dati={formato:formato};
    for(i in specifiche){
      var idl="#"+specifiche[i];
      valoriCampi[i]= $(idl).val()
      if(valoriCampi[i]){
            Acontrol=true;
        }
        else{
            Acontrol=false
        }
        control=control&&Acontrol;
    }
    if(control){
        for(i in valoriCampi){
            dati[i]=valoriCampi[i]
        }
        for(i in lavorazioni){
            dati[i]=$("#"+lavorazioni[i]['id']).val()
        }
        getAjax(dati,function(output) {
           handleData(output);

        });
    }
    else{
        handleData({'prezzo':0})
    }
}

function aggiornaConsegne(consegne,prezzo,check){
    var prezziConsegna=[];
    var consegneP=$(".dat_cons");
    var l=consegne.length;
    for (var i = 0; i < l; i++) {
        var a = parseFloat($(consegne[i]).val());
        var pr = parseFloat(prezzo);
        prezziConsegna[i] = (pr + ((pr * a) / 100.00)).toFixed(2);
        $(consegneP[i]).text(' € ' + prezziConsegna[i]);
        $(consegne[i]).attr('prezzo',prezziConsegna[i]);
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
/**
 * Created by riccardocarrai on 09/04/15.
 */

$(document).ready(function() {
    var paese;
    var PF=false;
    var Soc=false;
    $('select[name=continente]').change(function(){
        continente = $(this).val();
        $('#tipo_cliente').val('');
        $('#fatturazione').html('');
        request_url = '/registrazione/' + '?'+'continente='+continente ;
        $.ajax({
            url: request_url,
            success: function(data){
                $('#paese').find('option').remove().end();
                $.each(data, function(key, value){
                    $('select[name=paese]').append('<option value="' + key + '">' + value +'</option>');
                });
            }

        })
    })
    $('select[name=tipo_cliente]').change(function(){
        tipoCliente = $(this).val();
        if(tipoCliente=='Privato'){
            PF=true;
            Soc=false;
        }
        else{
            PF=false;
            Soc=true;
        }
        paese=$('#paese').val();
        request_url = '/registrazione/' + '?'+'tipo_cliente='+tipoCliente+'&'+'paese='+paese ;
        $.ajax({
            url: request_url,
            success: function(data){
                    $('#fatturazione').html(data);
            }

        })
    })
    $('select[name=paese]').change(function() {
        continente = $(this).val();
        $('#tipo_cliente').val('');
        $('#fatturazione').html('');
    })

    $("#ripeti_email").focusout(function(){
        if($("#email").valid() && $(this).valid()) {
            var user=$("#email").val();
            $("#username").val(user)
        }
        else{
            $("#username").val('')
        }

    })



    $("#registrazione").validate(
        {
            errorLabelContainer: $("#error"),

            rules:{

                persona_riferimento:
                {
                    required: true
                },
                telefono:
                {
                    required:true,
                    telefono:true

                },
                cellulare:
                {
                    telefono:true
                },
                fax:
                {
                    telefono:true
                },
                email:
                {
                    required: true,
                    email:true,
                    EmailAvailability:true
                },
                ripeti_email:
                {
                    equalTo:'#email'
                },
                username:
                {
                    required:true,
                    UserAvailability:true
                },
                password:
                {
                    required:true,
                    password:true
                },
                ripeti_password:
                {
                    equalTo:'#password'
                },
                privacy:
                {
                    required:true
                },
                denominazione:
                {
                    required:true
                },
                partita_iva:
                {
                    required:true,
                    partitaIva:true,
                    PIvaAvailability:true
                },
                codice_fiscale:
                {
                    required:true,
                    codiceFiscale:true,
                    codFisAvailability:true
                },
                localita:
                {
                    required:true
                },
                indirizzo:
                {
                    required:true
                },
                cap:
                {
                    required:true,
                    CAP:true
                },
                nome:
                {
                    required:true
                },
                cognome:
                {
                    required:true
                }



            },
            messages: {
                'username': {
                    remote: "L'username è già utilizzato da un altro utente!"
                }

            }
        }

        )

});

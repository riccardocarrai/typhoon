/**
 * Created by riccardocarrai on 13/04/15.
 */

 $.validator.addMethod("telefono", function(value, element) {
    return this.optional(element) || /^[0-9]+\/[0-9]+$/i.test(value);
    }, "Inserisci un numero di telefono valido.");

$.validator.addMethod("partitaIva", function(value, element) {
    return this.optional(element) || /^[0-9]{11}$/i.test(value);
    }, "Inserisci un numero di Partita Iva Valido.");

$.validator.addMethod("codiceFiscale", function(value, element) {
    if(($('#tipo_cliente').val())=="Privato") {
        return this.optional(element) || /^[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1}$/.test(value);
    }
    else
    {
        return this.optional(element) || /^[0-9]{11}$/i.test(value);
    }
    }, "Codice Fiscale non corretto.");

$.validator.addMethod("CAP", function(value, element) {
    return this.optional(element) || /^[0-9]{5}$/i.test(value);
    }, "Cap non Valido.");
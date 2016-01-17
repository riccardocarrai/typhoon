/**
 * Created by riccardocarrai on 15/04/15.
 */

$.validator.addMethod("UserAvailability", function (value, element) {
        return this.optional(element) || (myValidator(element.id,value));
    }, "Username not available");

$.validator.addMethod("EmailAvailability", function (value, element) {
       return this.optional(element) || (myValidator(element.id,value));
    }, "Email not available");

$.validator.addMethod("PIvaAvailability", function (value, element) {
       return this.optional(element) || (myValidator(element.id,value));
    }, "Partita Iva  not available");

$.validator.addMethod("codFisAvailability", function (value, element) {
       return this.optional(element) || (myValidator(element.id,value));
    }, "Cod Fiscale not available");

function myValidator(type,value) {
   var isSuccess = false;

   $.ajax({ url: "",
            data: type +"=" + value,
            async: false,
            success:
                function(msg) { isSuccess = msg === "true" ? false : true }
          });
    return isSuccess;
}
/**
 * Created by riccardocarrai on 14/04/15.
 */
$.validator.addMethod("password", function(value, element) {
    return this.optional(element) || (/^[a-zA-Z0-9]{8,16}$/.test(value) &&
        /[A-Z]/.test(value) && /[a-z]/.test(value) && /[0-9]/.test(value));
    }, "Deve contenere minimo 8 caratteri di cui almeno una maiuscola ed una cifra");
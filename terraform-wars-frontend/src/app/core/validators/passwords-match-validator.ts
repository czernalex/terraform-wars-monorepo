import { AbstractControl, ValidatorFn } from "@angular/forms";

export const passwordsMatchValidator: ValidatorFn = (control: AbstractControl) => {
    const password1 = control.get('password1');
    const password2 = control.get('password2');

    if (!control.pristine && password1?.value && password2?.value && (password1?.value !== password2?.value)) {
        password2?.setErrors({ passwordsMismatch: true });
        return { passwordsMismatch: true };
    } else {
        password2?.setErrors(null);
        return null;
    }
};

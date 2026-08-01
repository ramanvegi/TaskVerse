import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
@Component({
  selector: 'app-register',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly form = this.fb.nonNullable.group({
    first_name: ['', Validators.required],
    last_name: ['', Validators.required],
    username: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    phone_number: [''],
    password: ['', Validators.required],
    password_confirm: ['', Validators.required],
  });
  submit(): void {
    if (this.form.invalid) return;
    this.loading.set(true);
    this.error.set(null);
    this.auth.register(this.form.getRawValue()).subscribe({
      next: () => void this.router.navigate(['/dashboard']),
      error: (error: HttpErrorResponse) => {
        this.error.set(this.buildErrorMessage(error));
        this.loading.set(false);
      },
    });
  }
  private buildErrorMessage(error: HttpErrorResponse): string {
    const errors = error.error?.errors;
    if (!errors) {
      return 'Registration failed. Please check that the backend server is running.';
    }
    if (typeof errors === 'string') return errors;
    if (Array.isArray(errors)) return errors.join(' ');
    return Object.entries(errors)
      .map(([field, messages]) => `${this.toLabel(field)}: ${this.flattenMessages(messages).join(' ')}`)
      .join(' ');
  }
  private flattenMessages(messages: unknown): string[] {
    if (Array.isArray(messages)) return messages.flatMap((message) => this.flattenMessages(message));
    if (messages && typeof messages === 'object') {
      return Object.values(messages).flatMap((message) => this.flattenMessages(message));
    }
    return [String(messages)];
  }
  private toLabel(field: string): string {
    return field.replaceAll('_', ' ').replace(/^./, (char) => char.toUpperCase());
  }
}

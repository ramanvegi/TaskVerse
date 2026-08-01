import { Component, input, output } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-page-header',
  imports: [ReactiveFormsModule],
  templateUrl: './page-header.component.html',
  styleUrl: './page-header.component.scss',
})
export class PageHeaderComponent {
  readonly eyebrow = input('');
  readonly title = input.required<string>();
  readonly placeholder = input('Search');
  readonly buttonText = input('Search');
  readonly searchControl = input.required<FormControl<string>>();
  readonly submitted = output<void>();
}

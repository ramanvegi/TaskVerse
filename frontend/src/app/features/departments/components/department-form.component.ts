import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
@Component({
  selector: 'app-department-form',
  imports: [ReactiveFormsModule],
  templateUrl: './department-form.component.html',
  styleUrl: './department-form.component.scss',
})
export class DepartmentFormComponent {
  @Input({ required: true }) form!: FormGroup;
  @Input() editingId: number | null = null;
  @Input() saving = false;
  @Input() error: string | null = null;
  @Output() save = new EventEmitter<void>();
  @Output() cancel = new EventEmitter<void>();
}

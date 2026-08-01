import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Department } from '../../../core/models/department.model';
@Component({
  selector: 'app-employee-form',
  imports: [ReactiveFormsModule],
  templateUrl: './employee-form.component.html',
  styleUrl: './employee-form.component.scss',
})
export class EmployeeFormComponent {
  @Input({ required: true }) form!: FormGroup;
  @Input() departments: Department[] = [];
  @Input() editingId: number | null = null;
  @Input() saving = false;
  @Input() error: string | null = null;
  @Output() save = new EventEmitter<void>();
  @Output() cancel = new EventEmitter<void>();
}

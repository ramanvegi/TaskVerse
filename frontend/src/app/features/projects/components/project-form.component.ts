import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Employee } from '../../../core/models/employee.model';
import { ProjectStatus } from '../../../core/models/project.model';
@Component({
  selector: 'app-project-form',
  imports: [ReactiveFormsModule],
  templateUrl: './project-form.component.html',
  styleUrl: './project-form.component.scss',
})
export class ProjectFormComponent {
  @Input({ required: true }) form!: FormGroup;
  @Input() employees: Employee[] = [];
  @Input() statuses: ProjectStatus[] = [];
  @Input() editingId: number | null = null;
  @Input() saving = false;
  @Input() error: string | null = null;
  @Output() save = new EventEmitter<void>();
  @Output() cancel = new EventEmitter<void>();

  employeeSearch = '';

  filteredEmployees(): Employee[] {
    const search = this.employeeSearch.trim().toLowerCase();
    if (!search) return this.employees;
    return this.employees.filter((employee) =>
      [employee.full_name, employee.employee_code, employee.email]
        .some((value) => value.toLowerCase().includes(search)),
    );
  }

  selectedEmployeeIds(): number[] {
    return ((this.form.get('employees')?.value ?? []) as number[]).map(Number);
  }

  selectedEmployees(): Employee[] {
    const selectedIds = new Set(this.selectedEmployeeIds());
    return this.employees.filter((employee) => selectedIds.has(employee.id));
  }

  isEmployeeSelected(employeeId: number): boolean {
    return this.selectedEmployeeIds().includes(employeeId);
  }

  toggleEmployee(employeeId: number, checked: boolean): void {
    const selectedIds = new Set(this.selectedEmployeeIds());
    checked ? selectedIds.add(employeeId) : selectedIds.delete(employeeId);
    this.form.get('employees')?.setValue([...selectedIds]);
    this.form.get('employees')?.markAsDirty();
  }

  removeEmployee(employeeId: number): void {
    this.toggleEmployee(employeeId, false);
  }
}

import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { debounceTime, distinctUntilChanged, merge } from 'rxjs';
import { Department } from '../../core/models/department.model';
import { Employee, EmployeePayload, EmployeeStatus } from '../../core/models/employee.model';
import { DepartmentService } from '../../core/services/department.service';
import { EmployeeService } from '../../core/services/employee.service';
import { AuthService } from '../../core/services/auth.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';
import { EmployeeFormComponent } from './components/employee-form.component';
import { EmployeeTableComponent } from './components/employee-table.component';
@Component({
  selector: 'app-employees',
  imports: [ReactiveFormsModule, PageHeaderComponent, EmployeeFormComponent, EmployeeTableComponent],
  templateUrl: './employees.component.html',
  styleUrl: './employees.component.scss',
})
export class EmployeesComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly employeeService = inject(EmployeeService);
  private readonly departmentService = inject(DepartmentService);
  readonly auth = inject(AuthService);
  private readonly destroyRef = inject(DestroyRef);
  readonly employees = signal<Employee[]>([]);
  readonly departments = signal<Department[]>([]);
  readonly loading = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);
  readonly editingId = signal<number | null>(null);
  readonly searchControl = this.fb.nonNullable.control('');
  readonly departmentFilter = this.fb.nonNullable.control('');
  readonly statusFilter = this.fb.nonNullable.control('');
  readonly form = this.fb.nonNullable.group({
    department: [0, [Validators.required, Validators.min(1)]],
    employee_code: ['', Validators.required],
    first_name: ['', Validators.required],
    last_name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    phone_number: [''],
    job_title: ['', Validators.required],
    hire_date: [new Date().toISOString().slice(0, 10), Validators.required],
    status: ['ACTIVE' as EmployeeStatus, Validators.required],
    address: [''],
  });
  ngOnInit(): void {
    this.bindFilters();
    this.loadDepartments();
    this.loadEmployees();
  }

  private bindFilters(): void {
    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.loadEmployees());

    merge(
      this.departmentFilter.valueChanges.pipe(distinctUntilChanged()),
      this.statusFilter.valueChanges.pipe(distinctUntilChanged()),
    )
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.loadEmployees());
  }

  activeDepartments(): Department[] {
    return this.departments().filter((department) => department.is_active);
  }
  loadDepartments(): void {
    this.departmentService.list().subscribe({
      next: (response) => this.departments.set(response.results),
      error: () => this.error.set('Unable to load departments.'),
    });
  }
  loadEmployees(): void {
    this.loading.set(true);
    this.error.set(null);
    this.employeeService.list(this.searchControl.value, this.departmentFilter.value, this.statusFilter.value).subscribe({
      next: (response) => {
        this.employees.set(response.results);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Unable to load employees.');
        this.loading.set(false);
      },
    });
  }
  save(): void {
    if (this.form.invalid) return;
    const payload: EmployeePayload = this.form.getRawValue();
    const id = this.editingId();
    this.saving.set(true);
    const request = id ? this.employeeService.update(id, payload) : this.employeeService.create(payload);
    request.subscribe({
      next: () => {
        this.resetForm();
        this.saving.set(false);
        this.loadEmployees();
      },
      error: () => {
        this.error.set('Unable to save employee. Please check duplicate email/code and required fields.');
        this.saving.set(false);
      },
    });
  }
  edit(employee: Employee): void {
    this.editingId.set(employee.id);
    this.form.setValue({
      department: employee.department,
      employee_code: employee.employee_code,
      first_name: employee.first_name,
      last_name: employee.last_name,
      email: employee.email,
      phone_number: employee.phone_number || '',
      job_title: employee.job_title,
      hire_date: employee.hire_date,
      status: employee.status,
      address: employee.address || '',
    });
  }
  cancelEdit(): void {
    this.resetForm();
  }
  remove(employee: Employee): void {
    if (!confirm(`Delete employee "${employee.full_name}"?`)) return;
    this.employeeService.delete(employee.id).subscribe({
      next: () => this.loadEmployees(),
      error: () => this.error.set('Unable to delete employee.'),
    });
  }
  private resetForm(): void {
    this.editingId.set(null);
    this.form.reset({
      department: 0,
      employee_code: '',
      first_name: '',
      last_name: '',
      email: '',
      phone_number: '',
      job_title: '',
      hire_date: new Date().toISOString().slice(0, 10),
      status: 'ACTIVE',
      address: '',
    });
  }
}

import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { debounceTime, distinctUntilChanged } from 'rxjs';
import { Department, DepartmentPayload } from '../../core/models/department.model';
import { DepartmentService } from '../../core/services/department.service';
import { AuthService } from '../../core/services/auth.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';
import { DepartmentFormComponent } from './components/department-form.component';
import { DepartmentTableComponent } from './components/department-table.component';
@Component({
  selector: 'app-departments',
  imports: [PageHeaderComponent, DepartmentFormComponent, DepartmentTableComponent],
  templateUrl: './departments.component.html',
  styleUrl: './departments.component.scss',
})
export class DepartmentsComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly departmentService = inject(DepartmentService);
  readonly auth = inject(AuthService);
  private readonly destroyRef = inject(DestroyRef);
  readonly departments = signal<Department[]>([]);
  readonly loading = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);
  readonly editingId = signal<number | null>(null);
  readonly searchControl = this.fb.nonNullable.control('');
  readonly form = this.fb.nonNullable.group({
    name: ['', Validators.required],
    code: [''],
    description: [''],
    is_active: [true],
  });
  ngOnInit(): void {
    this.bindFilters();
    this.loadDepartments();
  }

  private bindFilters(): void {
    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.loadDepartments());
  }

  loadDepartments(): void {
    this.loading.set(true);
    this.error.set(null);
    this.departmentService.list(this.searchControl.value).subscribe({
      next: (response) => {
        this.departments.set(response.results);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Unable to load departments.');
        this.loading.set(false);
      },
    });
  }
  save(): void {
    if (this.form.invalid) return;
    const payload: DepartmentPayload = this.form.getRawValue();
    const id = this.editingId();
    this.saving.set(true);
    const request = id ? this.departmentService.update(id, payload) : this.departmentService.create(payload);
    request.subscribe({
      next: () => {
        this.form.reset({ name: '', code: '', description: '', is_active: true });
        this.editingId.set(null);
        this.saving.set(false);
        this.loadDepartments();
      },
      error: () => {
        this.error.set('Unable to save department. Please check duplicate name/code.');
        this.saving.set(false);
      },
    });
  }
  edit(department: Department): void {
    this.editingId.set(department.id);
    this.form.setValue({
      name: department.name,
      code: department.code || '',
      description: department.description || '',
      is_active: department.is_active,
    });
  }
  cancelEdit(): void {
    this.editingId.set(null);
    this.form.reset({ name: '', code: '', description: '', is_active: true });
  }
  remove(department: Department): void {
    if (!confirm(`Delete department "${department.name}"?`)) return;
    this.departmentService.delete(department.id).subscribe({
      next: () => this.loadDepartments(),
      error: () => this.error.set('Unable to delete department. It may be linked to employees.'),
    });
  }
}

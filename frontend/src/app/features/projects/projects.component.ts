import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { debounceTime, distinctUntilChanged } from 'rxjs';
import { Employee } from '../../core/models/employee.model';
import { Project, ProjectPayload, ProjectStatus } from '../../core/models/project.model';
import { EmployeeService } from '../../core/services/employee.service';
import { ProjectService } from '../../core/services/project.service';
import { AuthService } from '../../core/services/auth.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';
import { ProjectFormComponent } from './components/project-form.component';
import { ProjectTableComponent } from './components/project-table.component';
@Component({
  selector: 'app-projects',
  imports: [ReactiveFormsModule, PageHeaderComponent, ProjectFormComponent, ProjectTableComponent],
  templateUrl: './projects.component.html',
  styleUrl: './projects.component.scss',
})
export class ProjectsComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly projectService = inject(ProjectService);
  private readonly employeeService = inject(EmployeeService);
  readonly auth = inject(AuthService);
  private readonly destroyRef = inject(DestroyRef);
  readonly statuses: ProjectStatus[] = ['PLANNED', 'IN_PROGRESS', 'ON_HOLD', 'COMPLETED', 'CANCELLED'];
  readonly projects = signal<Project[]>([]);
  readonly employees = signal<Employee[]>([]);
  readonly loading = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);
  readonly editingId = signal<number | null>(null);
  readonly searchControl = this.fb.nonNullable.control('');
  readonly statusFilter = this.fb.nonNullable.control('');
  readonly form = this.fb.nonNullable.group({
    name: ['', Validators.required],
    project_code: ['', Validators.required],
    description: [''],
    employees: [[] as number[]],
    start_date: [new Date().toISOString().slice(0, 10), Validators.required],
    end_date: [''],
    status: ['PLANNED' as ProjectStatus, Validators.required],
    is_active: [true],
  });
  ngOnInit(): void {
    this.bindFilters();
    this.loadEmployees();
    this.loadProjects();
  }

  private bindFilters(): void {
    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.loadProjects());

    this.statusFilter.valueChanges
      .pipe(distinctUntilChanged(), takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.loadProjects());
  }

  activeEmployees(): Employee[] {
    return this.employees().filter((employee) => employee.status === 'ACTIVE');
  }
  loadEmployees(): void {
    this.employeeService.list('', '', 'ACTIVE').subscribe({
      next: (response) => this.employees.set(response.results),
      error: () => this.error.set('Unable to load employees.'),
    });
  }
  loadProjects(): void {
    this.loading.set(true);
    this.error.set(null);
    this.projectService.list(this.searchControl.value, this.statusFilter.value).subscribe({
      next: (response) => {
        this.projects.set(response.results);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Unable to load projects.');
        this.loading.set(false);
      },
    });
  }
  save(): void {
    if (this.form.invalid) return;
    const raw = this.form.getRawValue();
    const payload: ProjectPayload = { ...raw, employees: raw.employees.map(Number), end_date: raw.end_date || null };
    const id = this.editingId();
    this.saving.set(true);
    const request = id ? this.projectService.update(id, payload) : this.projectService.create(payload);
    request.subscribe({
      next: () => {
        this.resetForm();
        this.saving.set(false);
        this.loadProjects();
      },
      error: () => {
        this.error.set('Unable to save project. Please check duplicate name/code and dates.');
        this.saving.set(false);
      },
    });
  }
  edit(project: Project): void {
    this.editingId.set(project.id);
    this.form.setValue({
      name: project.name,
      project_code: project.project_code,
      description: project.description || '',
      employees: project.employee_details.map((employee) => employee.id),
      start_date: project.start_date,
      end_date: project.end_date || '',
      status: project.status,
      is_active: project.is_active,
    });
  }
  cancelEdit(): void {
    this.resetForm();
  }
  remove(project: Project): void {
    if (!confirm(`Delete project "${project.name}"?`)) return;
    this.projectService.delete(project.id).subscribe({
      next: () => this.loadProjects(),
      error: () => this.error.set('Unable to delete project.'),
    });
  }
  private resetForm(): void {
    this.editingId.set(null);
    this.form.reset({
      name: '',
      project_code: '',
      description: '',
      employees: [],
      start_date: new Date().toISOString().slice(0, 10),
      end_date: '',
      status: 'PLANNED',
      is_active: true,
    });
  }
}

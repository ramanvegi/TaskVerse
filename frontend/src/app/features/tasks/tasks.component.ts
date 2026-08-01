import { Component, DestroyRef, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { debounceTime, distinctUntilChanged, merge } from 'rxjs';
import { Employee } from '../../core/models/employee.model';
import { Project } from '../../core/models/project.model';
import { Task, TaskComment, TaskPayload, TaskPriority, TaskStatus } from '../../core/models/task.model';
import { EmployeeService } from '../../core/services/employee.service';
import { ProjectService } from '../../core/services/project.service';
import { TaskService } from '../../core/services/task.service';
import { AuthService } from '../../core/services/auth.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';
import { TaskCommentsComponent } from './components/task-comments.component';
import { TaskFormComponent } from './components/task-form.component';
import { TaskTableComponent } from './components/task-table.component';
@Component({
  selector: 'app-tasks',
  imports: [ReactiveFormsModule, PageHeaderComponent, TaskFormComponent, TaskTableComponent, TaskCommentsComponent],
  templateUrl: './tasks.component.html',
  styleUrl: './tasks.component.scss',
})
export class TasksComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly taskService = inject(TaskService);
  private readonly projectService = inject(ProjectService);
  private readonly employeeService = inject(EmployeeService);
  readonly auth = inject(AuthService);
  private readonly destroyRef = inject(DestroyRef);
  readonly statuses: TaskStatus[] = ['TODO', 'IN_PROGRESS', 'COMPLETED'];
  readonly priorities: TaskPriority[] = ['LOW', 'MEDIUM', 'HIGH'];
  readonly tasks = signal<Task[]>([]);
  readonly projects = signal<Project[]>([]);
  readonly employees = signal<Employee[]>([]);
  readonly comments = signal<TaskComment[]>([]);
  readonly selectedTask = signal<Task | null>(null);
  readonly loading = signal(false);
  readonly saving = signal(false);
  readonly commentsLoading = signal(false);
  readonly commentsSaving = signal(false);
  readonly commentsError = signal<string | null>(null);
  readonly error = signal<string | null>(null);
  readonly editingId = signal<number | null>(null);
  readonly searchControl = this.fb.nonNullable.control('');
  readonly projectFilter = this.fb.nonNullable.control('');
  readonly employeeFilter = this.fb.nonNullable.control('');
  readonly statusFilter = this.fb.nonNullable.control('');
  readonly priorityFilter = this.fb.nonNullable.control('');
  readonly commentControl = this.fb.nonNullable.control('');
  readonly form = this.fb.nonNullable.group({
    project: [0, [Validators.required, Validators.min(1)]],
    assigned_to: [null as number | null],
    title: ['', Validators.required],
    description: [''],
    due_date: [new Date().toISOString().slice(0, 10), Validators.required],
    priority: ['MEDIUM' as TaskPriority, Validators.required],
    status: ['TODO' as TaskStatus, Validators.required],
  });
  ngOnInit(): void {
    this.bindFilters();
    this.loadProjects();
    this.loadEmployees();
    this.loadTasks();
  }

  private bindFilters(): void {
    this.searchControl.valueChanges
      .pipe(debounceTime(300), distinctUntilChanged(), takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.loadTasks());

    merge(
      this.projectFilter.valueChanges.pipe(distinctUntilChanged()),
      this.employeeFilter.valueChanges.pipe(distinctUntilChanged()),
      this.statusFilter.valueChanges.pipe(distinctUntilChanged()),
      this.priorityFilter.valueChanges.pipe(distinctUntilChanged()),
    )
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.loadTasks());
  }

  loadProjects(): void {
    this.projectService.list().subscribe({
      next: (response) => this.projects.set(response.results),
      error: () => this.error.set('Unable to load projects.'),
    });
  }
  loadEmployees(): void {
    this.employeeService.list('', '', 'ACTIVE').subscribe({
      next: (response) => this.employees.set(response.results),
      error: () => this.error.set('Unable to load employees.'),
    });
  }
  loadTasks(): void {
    this.loading.set(true);
    this.error.set(null);
    this.taskService
      .list(
        this.searchControl.value,
        this.projectFilter.value,
        this.employeeFilter.value,
        this.statusFilter.value,
        this.priorityFilter.value,
      )
      .subscribe({
        next: (response) => {
          this.tasks.set(response.results);
          this.loading.set(false);
        },
        error: () => {
          this.error.set('Unable to load tasks.');
          this.loading.set(false);
        },
      });
  }
  save(): void {
    if (this.form.invalid) return;
    const payload: TaskPayload = this.form.getRawValue();
    const id = this.editingId();
    this.saving.set(true);
    const request = id ? this.taskService.update(id, payload) : this.taskService.create(payload);
    request.subscribe({
      next: () => {
        this.resetForm();
        this.saving.set(false);
        this.loadTasks();
      },
      error: () => {
        this.error.set('Unable to save task. Please check required fields and due date.');
        this.saving.set(false);
      },
    });
  }
  edit(task: Task): void {
    this.editingId.set(task.id);
    this.form.setValue({
      project: task.project,
      assigned_to: task.assigned_to,
      title: task.title,
      description: task.description || '',
      due_date: task.due_date,
      priority: task.priority,
      status: task.status,
    });
  }
  cancelEdit(): void {
    this.resetForm();
  }
  remove(task: Task): void {
    if (!confirm(`Delete task "${task.title}"?`)) return;
    this.taskService.delete(task.id).subscribe({
      next: () => this.loadTasks(),
      error: () => this.error.set('Unable to delete task.'),
    });
  }
  openComments(task: Task): void {
    this.selectedTask.set(task);
    this.comments.set([]);
    this.commentsError.set(null);
    this.commentsLoading.set(true);
    this.commentControl.setValue('');
    setTimeout(() => document.getElementById('task-comments-viewer')?.scrollIntoView({ behavior: 'smooth', block: 'start' }));
    this.taskService.comments(task.id).subscribe({
      next: (comments) => {
        this.comments.set(comments);
        this.commentsLoading.set(false);
      },
      error: () => {
        this.commentsError.set('Unable to load comments. Please try again.');
        this.commentsLoading.set(false);
      },
    });
  }
  addComment(message: string): void {
    const task = this.selectedTask();
    if (!task || !message.trim()) return;
    this.commentsSaving.set(true);
    this.commentsError.set(null);
    this.taskService.addComment(task.id, message.trim()).subscribe({
      next: (comment) => {
        this.comments.update((comments) => [...comments, comment]);
        this.commentControl.setValue('');
        this.commentsSaving.set(false);
        this.loadTasks();
      },
      error: () => {
        this.commentsError.set('Unable to add comment. Enter at least 2 characters and try again.');
        this.commentsSaving.set(false);
      },
    });
  }
  closeComments(): void {
    this.selectedTask.set(null);
    this.comments.set([]);
    this.commentsError.set(null);
    this.commentsLoading.set(false);
    this.commentsSaving.set(false);
    this.commentControl.setValue('');
  }
  private resetForm(): void {
    this.editingId.set(null);
    this.form.reset({
      project: 0,
      assigned_to: null,
      title: '',
      description: '',
      due_date: new Date().toISOString().slice(0, 10),
      priority: 'MEDIUM',
      status: 'TODO',
    });
  }
}

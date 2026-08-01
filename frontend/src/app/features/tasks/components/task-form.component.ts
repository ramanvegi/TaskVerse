import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Employee } from '../../../core/models/employee.model';
import { Project } from '../../../core/models/project.model';
import { TaskPriority, TaskStatus } from '../../../core/models/task.model';
@Component({
  selector: 'app-task-form',
  imports: [ReactiveFormsModule],
  templateUrl: './task-form.component.html',
  styleUrl: './task-form.component.scss',
})
export class TaskFormComponent {
  @Input({ required: true }) form!: FormGroup;
  @Input() projects: Project[] = [];
  @Input() employees: Employee[] = [];
  @Input() statuses: TaskStatus[] = [];
  @Input() priorities: TaskPriority[] = [];
  @Input() editingId: number | null = null;
  @Input() saving = false;
  @Input() error: string | null = null;
  @Output() save = new EventEmitter<void>();
  @Output() cancel = new EventEmitter<void>();
}

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Task, TaskComment } from '../../../core/models/task.model';
@Component({
  selector: 'app-task-comments',
  imports: [DatePipe, ReactiveFormsModule],
  templateUrl: './task-comments.component.html',
  styleUrl: './task-comments.component.scss',
})
export class TaskCommentsComponent {
  @Input() task: Task | null = null;
  @Input() comments: TaskComment[] = [];
  @Input() loading = false;
  @Input() saving = false;
  @Input() error: string | null = null;
  @Input({ required: true }) messageControl!: FormControl<string>;
  @Output() add = new EventEmitter<string>();
  @Output() close = new EventEmitter<void>();
}

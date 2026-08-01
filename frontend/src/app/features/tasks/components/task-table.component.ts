import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Task } from '../../../core/models/task.model';
@Component({
  selector: 'app-task-table',
  templateUrl: './task-table.component.html',
  styleUrl: './task-table.component.scss',
})
export class TaskTableComponent {
  @Input() tasks: Task[] = [];
  @Input() loading = false;
  @Input() canManage = false;
  @Output() edit = new EventEmitter<Task>();
  @Output() remove = new EventEmitter<Task>();
  @Output() comments = new EventEmitter<Task>();
}

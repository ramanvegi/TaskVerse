import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Department } from '../../../core/models/department.model';
@Component({
  selector: 'app-department-table',
  templateUrl: './department-table.component.html',
  styleUrl: './department-table.component.scss',
})
export class DepartmentTableComponent {
  @Input() departments: Department[] = [];
  @Input() loading = false;
  @Input() canManage = false;
  @Output() edit = new EventEmitter<Department>();
  @Output() remove = new EventEmitter<Department>();
}

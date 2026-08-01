import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Employee } from '../../../core/models/employee.model';
@Component({
  selector: 'app-employee-table',
  templateUrl: './employee-table.component.html',
  styleUrl: './employee-table.component.scss',
})
export class EmployeeTableComponent {
  @Input() employees: Employee[] = [];
  @Input() loading = false;
  @Input() canManage = false;
  @Output() edit = new EventEmitter<Employee>();
  @Output() remove = new EventEmitter<Employee>();
}

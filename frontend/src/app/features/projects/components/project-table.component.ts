import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Project } from '../../../core/models/project.model';
@Component({
  selector: 'app-project-table',
  templateUrl: './project-table.component.html',
  styleUrl: './project-table.component.scss',
})
export class ProjectTableComponent {
  @Input() projects: Project[] = [];
  @Input() loading = false;
  @Input() canManage = false;
  @Output() edit = new EventEmitter<Project>();
  @Output() remove = new EventEmitter<Project>();

  employeeNames(project: Project): string {
    return project.employee_details.map((employee) => employee.full_name).join(', ') || 'No employees assigned';
  }
}

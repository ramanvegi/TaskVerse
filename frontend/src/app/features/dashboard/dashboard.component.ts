import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { DashboardSummary } from '../../core/models/dashboard.model';
import { DashboardService } from '../../core/services/dashboard.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements OnInit {
  private readonly dashboardService = inject(DashboardService);
  readonly auth = inject(AuthService);

  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly summary = signal<DashboardSummary | null>(null);

  isAdmin(): boolean {
    return this.auth.currentUser()?.role === 'ADMIN';
  }

  ngOnInit(): void {
    this.dashboardService.getSummary().subscribe({
      next: (summary) => {
        this.summary.set(summary);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Unable to load dashboard summary. Please confirm the backend server is running.');
        this.loading.set(false);
      },
    });
  }

  cards(): { label: string; value: number }[] {
    const summary = this.summary();
    if (!summary) return [];
    return [
      { label: 'Employees', value: summary.total_employees },
      { label: 'Departments', value: summary.total_departments },
      { label: 'Projects', value: summary.total_projects },
      { label: 'Tasks', value: summary.total_tasks },
      { label: 'Completed Tasks', value: summary.completed_tasks },
      { label: 'Pending Tasks', value: summary.pending_tasks },
      { label: 'Overdue Tasks', value: summary.overdue_tasks },
    ];
  }
}
